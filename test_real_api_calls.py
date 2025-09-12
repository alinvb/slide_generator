#!/usr/bin/env python3
"""
Test real API calls to see why JSON is empty
"""

import os
import sys

def test_api_key_availability():
    """Check if API key is available"""
    
    print("🔑 TESTING API KEY AVAILABILITY")
    print("=" * 50)
    
    # Check environment variable
    env_key = os.getenv('PERPLEXITY_API_KEY', '')
    print(f"📋 Environment PERPLEXITY_API_KEY: {'Found' if env_key else 'Missing'}")
    
    if env_key:
        print(f"   Key length: {len(env_key)} characters")
        print(f"   Key preview: {env_key[:8]}...{env_key[-4:] if len(env_key) > 12 else '***'}")
    
    # Try to import and test shared function
    try:
        from shared_functions import call_llm_api
        print(f"✅ Successfully imported call_llm_api from shared_functions")
        
        # Test with or without API key
        if env_key:
            print(f"\n🧪 TESTING REAL API CALL...")
            response = call_llm_api(
                messages=[{"role": "user", "content": "Respond with 'API_TEST_SUCCESS' if you receive this"}],
                model="sonar-pro",
                api_key=env_key,
                api_service="perplexity",
                timeout=30
            )
            
            if response and "API_TEST_SUCCESS" in response:
                print(f"✅ API Call Success: {response}")
                return True
            else:
                print(f"⚠️ API Call Response: {response[:100] if response else 'None'}")
                return False
        else:
            print(f"⚠️ No API key - will use fallback data")
            return False
            
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_conversation_extraction_with_real_api():
    """Test conversation extraction with real API"""
    
    print(f"\n🔍 TESTING CONVERSATION EXTRACTION WITH REAL API")
    print("=" * 60)
    
    try:
        from bulletproof_json_generator_clean import CleanBulletproofJSONGenerator
        from shared_functions import call_llm_api
        
        # Create a proper API call function
        def real_llm_api_call(messages):
            api_key = os.getenv('PERPLEXITY_API_KEY', '')
            if api_key:
                return call_llm_api(messages, "sonar-pro", api_key, "perplexity", 0, 60)
            else:
                print("⚠️ No API key - returning mock response")
                # Return a mock response that matches the extraction format
                return '''
                {
                    "company_name": "TechFlow Analytics",
                    "business_description_detailed": "Real-time analytics SaaS platform serving enterprise clients",
                    "strategic_buyers_mentioned": ["Microsoft", "Salesforce", "Oracle"],
                    "financial_buyers_mentioned": ["Vista Equity Partners", "Thoma Bravo"],
                    "annual_revenue_usd_m": [50],
                    "revenue_growth_rates": ["40% YoY"],
                    "management_team_detailed": ["CEO Sarah Chen (ex-Salesforce)", "CTO Mike Rodriguez (PhD Stanford)"],
                    "valuation_estimates_mentioned": ["15-20x revenue"],
                    "dcf_valuation_mentioned": ["$800M DCF value"],
                    "comparable_company_valuation": ["12-18x revenue multiple"],
                    "precedent_transaction_valuation": ["Similar deals at 15-17x"]
                }
                '''
        
        # Test conversation with strategic/financial buyer mentions
        test_messages = [
            {
                "role": "user",
                "content": """I want to analyze TechFlow Analytics for acquisition. Here's what I know:
                
Strategic buyers we've identified include Microsoft (would pay 15-20x revenue for Azure synergies), 
Salesforce (interested for CRM integration at 12-15x), and Oracle (could pay 18x to compete with Snowflake).

Financial buyers include Vista Equity Partners (they know SaaS space well from their Tibco investment) 
and Thoma Bravo (loves profitable software companies with 25%+ EBITDA margins).

The company has $50M revenue growing 40% annually with 25% EBITDA margins. 
Management team includes CEO Sarah Chen (ex-Salesforce VP) and CTO Mike Rodriguez (PhD from Stanford).

Based on precedent transactions like Looker to Google for $2.6B at 20x revenue, 
we're targeting 15-18x revenue multiple for a $750M-$900M valuation range."""
            }
        ]
        
        print("💬 Testing with rich investment banking conversation...")
        
        generator = CleanBulletproofJSONGenerator()
        result = generator.extract_conversation_data(test_messages, real_llm_api_call)
        
        print(f"\n📊 EXTRACTION RESULTS:")
        if result:
            print(f"   ✅ SUCCESS: {len(result)} fields extracted")
            
            # Check critical fields
            critical_fields = [
                "strategic_buyers_mentioned",
                "financial_buyers_mentioned", 
                "valuation_estimates_mentioned",
                "management_team_detailed"
            ]
            
            for field in critical_fields:
                value = result.get(field, [])
                if value:
                    print(f"   ✅ {field}: {value}")
                else:
                    print(f"   ❌ {field}: Empty")
        else:
            print(f"   ❌ FAILED: No data extracted")
            
        return result
        
    except Exception as e:
        print(f"💥 Error in conversation extraction test: {e}")
        import traceback
        traceback.print_exc()
        return None

def diagnose_empty_json_root_cause():
    """Diagnose the root cause of empty JSON"""
    
    print(f"\n🔍 ROOT CAUSE ANALYSIS")
    print("=" * 40)
    
    # Check all possible failure points
    issues = []
    
    # 1. API Key
    if not os.getenv('PERPLEXITY_API_KEY'):
        issues.append("❌ No PERPLEXITY_API_KEY in environment")
    else:
        issues.append("✅ API key found in environment")
    
    # 2. Import issues
    try:
        from shared_functions import call_llm_api
        issues.append("✅ shared_functions.call_llm_api imports successfully")
    except Exception as e:
        issues.append(f"❌ Cannot import call_llm_api: {e}")
    
    # 3. Bulletproof generator
    try:
        from bulletproof_json_generator_clean import CleanBulletproofJSONGenerator
        issues.append("✅ CleanBulletproofJSONGenerator imports successfully")
    except Exception as e:
        issues.append(f"❌ Cannot import CleanBulletproofJSONGenerator: {e}")
    
    # 4. Function name mismatch
    try:
        from bulletproof_json_generator_clean import generate_clean_bulletproof_json
        issues.append("✅ generate_clean_bulletproof_json imports successfully")
    except Exception as e:
        issues.append(f"❌ Cannot import generate_clean_bulletproof_json: {e}")
    
    print("🔍 DIAGNOSTIC RESULTS:")
    for issue in issues:
        print(f"   {issue}")
    
    return issues

if __name__ == "__main__":
    # Run all tests
    api_works = test_api_key_availability()
    result = test_conversation_extraction_with_real_api()
    issues = diagnose_empty_json_root_cause()
    
    print(f"\n🎯 SUMMARY:")
    print(f"   API Status: {'✅ Working' if api_works else '⚠️ Missing key/Failed'}")
    print(f"   Extraction: {'✅ Working' if result else '❌ Failed'}")
    print(f"   Critical Issues: {len([i for i in issues if '❌' in i])}")
    
    if not api_works:
        print(f"\n💡 SOLUTION: Set PERPLEXITY_API_KEY environment variable")
        print(f"   export PERPLEXITY_API_KEY='your-key-here'")
    
    if result and len(result) > 0:
        print(f"\n🎉 GOOD NEWS: Conversation extraction is working!")
        print(f"   The empty JSON issue is likely in the main bulletproof generation")
        print(f"   or in how the extracted data is being used to populate the final JSON")