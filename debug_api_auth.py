#!/usr/bin/env python3
"""
Debug API Authentication - Check why Perplexity API returns 401 errors
"""

import requests
import json

def test_perplexity_api_auth():
    """Test Perplexity API authentication with different scenarios"""
    print("🔍 Testing Perplexity API Authentication...")
    
    # Test cases with different API key formats
    test_cases = [
        {
            "name": "Invalid API Key Format", 
            "api_key": "test-api-key-configured",
            "expected": "401 - Invalid key format"
        },
        {
            "name": "Empty API Key", 
            "api_key": "",
            "expected": "401 - No key provided"
        },
        {
            "name": "Typical Perplexity Key Format", 
            "api_key": "pplx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", 
            "expected": "401 - Invalid key (but correct format)"
        }
    ]
    
    for test_case in test_cases:
        print(f"\n📋 Testing: {test_case['name']}")
        print(f"🔍 API Key: {test_case['api_key'][:10]}..." if test_case['api_key'] else "🔍 API Key: (empty)")
        
        # Test with minimal request
        headers = {
            'Authorization': f'Bearer {test_case["api_key"]}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'sonar-pro',
            'messages': [{"role": "user", "content": "Hello"}],
            'max_tokens': 50
        }
        
        try:
            response = requests.post(
                'https://api.perplexity.ai/chat/completions',
                headers=headers,
                json=data,
                timeout=10
            )
            
            print(f"🔍 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                print(f"✅ SUCCESS: API key valid")
                result = response.json()
                content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
                print(f"✅ Response: {content[:100]}...")
            elif response.status_code == 401:
                print(f"❌ 401 UNAUTHORIZED: {test_case['expected']}")
                print(f"🔍 Response: {response.text[:200]}...")
            else:
                print(f"⚠️ Other Error: {response.status_code}")
                print(f"🔍 Response: {response.text[:200]}...")
                
        except Exception as e:
            print(f"❌ Request Failed: {e}")

def check_api_key_requirements():
    """Check Perplexity API key requirements and format"""
    print(f"\n📋 Perplexity API Key Requirements:")
    print(f"✅ Format: Should start with 'pplx-'")
    print(f"✅ Length: Typically 40+ characters after 'pplx-'")
    print(f"✅ Source: Get from https://perplexity.ai/settings/api")
    print(f"✅ Billing: Requires valid payment method on account")
    print(f"✅ Credits: Account must have available API credits")

def diagnose_current_issue():
    """Diagnose the current authentication issue"""
    print(f"\n🎯 DIAGNOSIS: Why You're Getting Empty Arrays")
    print(f"=" * 50)
    
    print(f"❌ **Root Cause**: API Authentication Failure (401 Unauthorized)")
    print(f"")
    print(f"📊 **What's Happening**:")
    print(f"   1. You configure an API key in the app")
    print(f"   2. App tries to call Perplexity API for gap-filling")
    print(f"   3. Perplexity returns 401 Unauthorized error")
    print(f"   4. System falls back to conversation extraction only")
    print(f"   5. No comprehensive gap-filling = empty strategic/financial buyers")
    print(f"")
    print(f"🔧 **Solutions**:")
    print(f"   ✅ **Check API Key Format**: Must start with 'pplx-'")
    print(f"   ✅ **Verify API Key**: Copy fresh from https://perplexity.ai/settings/api")
    print(f"   ✅ **Check Billing**: Ensure payment method added to Perplexity account")
    print(f"   ✅ **Verify Credits**: Confirm API credits available")
    print(f"   ✅ **Test Key**: Use the debug script to validate authentication")
    
def main():
    """Run API authentication debugging"""
    print("🚀 Debugging Perplexity API Authentication...")
    print("=" * 60)
    
    test_perplexity_api_auth()
    check_api_key_requirements()
    diagnose_current_issue()
    
    print(f"\n" + "=" * 60)
    print(f"💡 **Next Steps**:")
    print(f"1. Get a valid Perplexity API key from: https://perplexity.ai/settings/api")
    print(f"2. Ensure it starts with 'pplx-' and is 40+ characters")
    print(f"3. Add payment method to your Perplexity account")
    print(f"4. Test the key with this debug script")
    print(f"5. Use the working key in your Investment Banking app")

if __name__ == "__main__":
    main()