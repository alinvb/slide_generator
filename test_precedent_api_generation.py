"""
Test the precedent transactions API generation and data flow
"""

import json
import os
from dotenv import load_dotenv
import requests
from bulletproof_json_generator_clean import CleanBulletproofJSONGenerator

load_dotenv()

def test_precedent_transactions_api_call():
    """Test the actual API call for precedent transactions generation"""
    
    # Get API key
    api_key = os.getenv('PERPLEXITY_API_KEY')
    if not api_key:
        print("❌ No PERPLEXITY_API_KEY found in environment")
        return
    
    print(f"✅ Using API key: {api_key[:10]}...")
    
    def llm_api_call(messages):
        """Make actual API call to Perplexity"""
        try:
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'model': 'llama-3.1-sonar-small-128k-chat',
                'messages': messages,
                'max_tokens': 2000,
                'temperature': 0.2,
                'top_p': 0.9,
                'search_domain_filter': ["perplexity.ai"],
                'return_citations': True,
                'return_images': False,
                'return_related_questions': False
            }
            
            print(f"🔍 Making API call with {len(messages)} messages...")
            response = requests.post('https://api.perplexity.ai/chat/completions', 
                                   headers=headers, json=payload, timeout=60)
            
            print(f"📡 API Response Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
                print(f"✅ API call successful, content length: {len(content)}")
                return content
            else:
                print(f"❌ API call failed: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"❌ API call error: {e}")
            return None
    
    # Test the specific competitive/valuation chunk generation
    generator = CleanBulletproofJSONGenerator()
    
    # Sample extracted data (minimal)
    extracted_data = {
        'competitors_mentioned': [],
        'company_name': 'Netflix'
    }
    
    print("=== TESTING PRECEDENT TRANSACTIONS API GENERATION ===")
    
    # Test the chunk generation method
    try:
        result = generator._generate_competitive_valuation_chunk(
            company_name="Netflix",
            industry="Streaming Entertainment", 
            extracted_data=extracted_data,
            llm_api_call=llm_api_call
        )
        
        print(f"📊 Chunk generation result type: {type(result)}")
        print(f"📊 Chunk generation keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
        
        if isinstance(result, dict) and 'precedent_transactions' in result:
            transactions = result['precedent_transactions']
            print(f"🎯 Precedent transactions found: {len(transactions)} transactions")
            
            for i, txn in enumerate(transactions):
                print(f"  Transaction {i+1}: {txn}")
                
            # Test if this would work in slide rendering
            if transactions and len(transactions) > 0:
                print("✅ Precedent transactions data should render properly in slides")
            else:
                print("❌ No precedent transactions data - slides will show placeholder")
        else:
            print("❌ No precedent_transactions field in result")
            print(f"🔍 Full result: {json.dumps(result, indent=2)}")
    
    except Exception as e:
        print(f"❌ Chunk generation failed: {e}")
        import traceback
        traceback.print_exc()

def test_with_fallback_data():
    """Test what happens when API fails and we use fallback data"""
    print("\n=== TESTING FALLBACK PRECEDENT TRANSACTIONS ===")
    
    # Simulate failed API call
    def failed_api_call(messages):
        return None
    
    generator = CleanBulletproofJSONGenerator()
    extracted_data = {'competitors_mentioned': [], 'company_name': 'Netflix'}
    
    result = generator._generate_competitive_valuation_chunk(
        company_name="Netflix",
        industry="Streaming Entertainment",
        extracted_data=extracted_data, 
        llm_api_call=failed_api_call
    )
    
    print(f"📊 Fallback result: {result}")
    
    if not result or 'precedent_transactions' not in result:
        print("❌ Fallback does not provide precedent_transactions data")
        print("🔍 This explains why slides show placeholder content when API fails")
    else:
        print("✅ Fallback provides precedent_transactions data")

if __name__ == "__main__":
    test_precedent_transactions_api_call()
    test_with_fallback_data()
