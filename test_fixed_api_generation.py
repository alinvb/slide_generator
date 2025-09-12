"""
Test precedent transactions with CORRECT Perplexity API model
"""

import json
import os
from dotenv import load_dotenv
import requests
from bulletproof_json_generator_clean import CleanBulletproofJSONGenerator

load_dotenv()

def test_precedent_transactions_with_correct_model():
    """Test precedent transactions with the correct Perplexity model"""
    
    api_key = os.getenv('PERPLEXITY_API_KEY')
    if not api_key:
        print("❌ No PERPLEXITY_API_KEY found")
        return
    
    print(f"✅ Using API key: {api_key[:10]}...")
    
    def llm_api_call(messages):
        """Make API call with CORRECT model name"""
        try:
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            # FIXED: Use the correct model name that app uses
            payload = {
                'model': 'sonar-pro',  # Changed from 'llama-3.1-sonar-small-128k-chat'
                'messages': messages,
                'max_tokens': 2000,
                'temperature': 0.2,
                'top_p': 0.9,
                'return_citations': True,
                'return_images': False,
                'return_related_questions': False
            }
            
            print(f"🔍 Making API call with model: {payload['model']}")
            response = requests.post('https://api.perplexity.ai/chat/completions', 
                                   headers=headers, json=payload, timeout=60)
            
            print(f"📡 API Response Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
                print(f"✅ API call successful, content length: {len(content)}")
                print(f"🔍 Content preview: {content[:200]}...")
                return content
            else:
                print(f"❌ API call failed: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"❌ API call error: {e}")
            return None
    
    # Test the competitive/valuation chunk generation with working API
    generator = CleanBulletproofJSONGenerator()
    
    extracted_data = {
        'competitors_mentioned': [],
        'company_name': 'Netflix'
    }
    
    print("=== TESTING WITH CORRECT SONAR-PRO MODEL ===")
    
    try:
        result = generator._generate_competitive_valuation_chunk(
            company_name="Netflix",
            industry="Streaming Entertainment",
            extracted_data=extracted_data,
            llm_api_call=llm_api_call
        )
        
        print(f"📊 Result type: {type(result)}")
        print(f"📊 Result keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
        
        if isinstance(result, dict) and 'precedent_transactions' in result:
            transactions = result['precedent_transactions']
            print(f"🎯 SUCCESS! Found {len(transactions)} precedent transactions")
            
            for i, txn in enumerate(transactions[:2]):  # Show first 2
                print(f"  Transaction {i+1}: {json.dumps(txn, indent=2)}")
                
            if len(transactions) > 2:
                print(f"  ... and {len(transactions) - 2} more transactions")
                
            print("✅ This data WILL render properly in slides!")
            return True
        else:
            print("❌ Still no precedent_transactions in result")
            print(f"🔍 Full result: {json.dumps(result, indent=2) if result else 'Empty result'}")
            return False
    
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_current_bulletproof_generator_api():
    """Test if the bulletproof generator has the same API issue"""
    print("\n=== TESTING CURRENT BULLETPROOF GENERATOR API ===")
    
    # Check what the current app.py uses for API calls
    try:
        from shared_functions import make_perplexity_api_call
        
        print("✅ Found shared_functions.make_perplexity_api_call")
        
        # Test with a simple message
        test_messages = [{"role": "user", "content": "Generate a test JSON with precedent_transactions field containing one sample transaction."}]
        
        result = make_perplexity_api_call(test_messages)
        
        if result:
            print(f"✅ Shared function API call worked: {len(result)} chars")
            print(f"🔍 Result preview: {result[:200]}...")
        else:
            print("❌ Shared function API call failed or returned None")
            
    except Exception as e:
        print(f"❌ Could not test shared function: {e}")

if __name__ == "__main__":
    success = test_precedent_transactions_with_correct_model()
    test_current_bulletproof_generator_api()
    
    if success:
        print("\n🎉 SOLUTION FOUND!")
        print("The API works with 'sonar-pro' model")
        print("Need to fix the model name in bulletproof_json_generator_clean.py")
    else:
        print("\n⚠️ Still investigating API issues...")
