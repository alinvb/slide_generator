#!/usr/bin/env python3
"""
Simple test to verify API key configuration works with a basic API call
"""

import json
import os

def test_simple_api_call():
    """Test a simple API call using configured API key"""
    print("🔍 Testing Simple API Call...")
    print("=" * 40)
    
    try:
        # Import config system
        from config import get_working_api_key, get_default_settings
        
        # Get configured API key
        settings = get_default_settings()
        api_key = settings['api_key']
        model = settings['model']
        service = settings['service']
        
        print(f"✅ API Key: {'*' * len(api_key) if api_key else 'None'}")
        print(f"✅ Model: {model}")
        print(f"✅ Service: {service}")
        
        if not api_key:
            print("🚨 FAILED: No API key found!")
            return False
        
        # Test simple API call
        from shared_functions import call_llm_api as shared_call_llm_api
        
        test_messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Reply with exactly: 'API_TEST_SUCCESS'"}
        ]
        
        print("\n🚀 Making test API call...")
        response = shared_call_llm_api(test_messages, model, api_key, service)
        
        print(f"📝 Response: {response}")
        
        if response and "API_TEST_SUCCESS" in response:
            print("✅ SUCCESS: API call worked perfectly!")
            return True
        elif response and len(response) > 0:
            print("✅ PARTIAL SUCCESS: Got response from API (key is working)")
            return True
        else:
            print("🚨 FAILED: No response from API")
            return False
            
    except Exception as e:
        print(f"🚨 ERROR: {str(e)}")
        return False

def test_strategic_buyers_extraction():
    """Test extraction of strategic buyers from Netflix conversation"""
    print("\n🔍 Testing Strategic Buyers Extraction...")
    print("=" * 45)
    
    try:
        # Get API settings
        from config import get_working_api_key, get_default_settings
        settings = get_default_settings()
        api_key = settings['api_key']
        
        if not api_key:
            print("🚨 Skipping: No API key configured")
            return False
        
        # Simple extraction prompt for strategic buyers from Netflix conversation
        from shared_functions import call_llm_api as shared_call_llm_api
        
        netflix_text = """
        User mentioned: "Strategic buyers could include Apple (has $200B+ cash, needs content for Apple TV+), 
        Amazon (content for Prime Video, cloud synergies), Microsoft (gaming + content convergence, Azure integration), 
        Disney (streaming consolidation, content library combination), and potentially Google/Alphabet 
        (YouTube synergies, cloud infrastructure)."
        """
        
        extraction_messages = [
            {"role": "system", "content": "Extract strategic buyers mentioned in the conversation. Return JSON format."},
            {"role": "user", "content": f"""Extract strategic buyers from this text and return JSON:

{netflix_text}

Format:
{{"strategic_buyers": [{{"buyer_name": "CompanyName", "strategic_rationale": "reason"}}]}}"""}
        ]
        
        print("🚀 Extracting strategic buyers...")
        response = shared_call_llm_api(extraction_messages, settings['model'], api_key, settings['service'])
        
        print(f"📝 Raw Response: {response[:200]}...")
        
        # Try to parse JSON
        try:
            # Clean response to extract JSON
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                parsed = json.loads(json_str)
                
                strategic_buyers = parsed.get('strategic_buyers', [])
                print(f"\n✅ Found {len(strategic_buyers)} strategic buyers:")
                for i, buyer in enumerate(strategic_buyers[:3]):
                    name = buyer.get('buyer_name', 'Unknown')
                    rationale = buyer.get('strategic_rationale', 'No rationale')
                    print(f"  {i+1}. {name}: {rationale[:80]}...")
                
                return len(strategic_buyers) > 0
            else:
                print("🚨 Could not find valid JSON in response")
                return False
                
        except json.JSONDecodeError as e:
            print(f"🚨 JSON Parse Error: {e}")
            return False
        
    except Exception as e:
        print(f"🚨 ERROR: {str(e)}")
        return False

def main():
    """Run tests"""
    print("🧪 Simple API Key Configuration Test")
    print("=" * 50)
    
    # Test 1: Basic API call
    api_success = test_simple_api_call()
    
    if not api_success:
        print("\n❌ OVERALL: API key configuration failed")
        return
    
    # Test 2: Strategic buyers extraction
    extraction_success = test_strategic_buyers_extraction()
    
    if api_success and extraction_success:
        print("\n✅ OVERALL SUCCESS: API key fix works! Strategic buyers can be extracted.")
        print("🎉 The empty JSON issue should now be resolved in the main app!")
    elif api_success:
        print("\n✅ PARTIAL SUCCESS: API key works, but extraction needs refinement.")
        print("💡 At minimum, you should no longer see empty JSONs in the app.")
    else:
        print("\n⚠️ MIXED RESULTS: Check logs for details")

if __name__ == "__main__":
    main()