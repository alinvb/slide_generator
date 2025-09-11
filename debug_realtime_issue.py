#!/usr/bin/env python3
"""
Create a simple test to diagnose the exact issue in real-time
"""

def create_minimal_test():
    """Create a minimal test that can be run in the Streamlit app"""
    
    print("🔧 MINIMAL DIAGNOSTIC TEST FOR STREAMLIT")
    print("=" * 50)
    
    test_code = '''
# Add this to your Streamlit app to debug the issue:

import streamlit as st
import json

st.write("🔍 **DEBUG: API Key and Conversation Extraction Test**")

# Test 1: Check API Key
st.write("### Test 1: API Key Status")
api_key = st.session_state.get('api_key', '')
if api_key:
    st.success(f"✅ API Key Found: {len(api_key)} characters")
    st.write(f"Key preview: {api_key[:8]}...{api_key[-4:]}")
else:
    st.error("❌ No API Key in Session State")

# Test 2: Test Actual Conversation Extraction
st.write("### Test 2: Conversation Extraction Test")
if st.button("Test Conversation Extraction"):
    try:
        from bulletproof_json_generator_clean import CleanBulletproofJSONGenerator
        
        # Mock LLM call that uses session state API key
        def test_llm_call(messages):
            working_api_key = st.session_state.get('api_key', '')
            if working_api_key:
                st.write(f"✅ Using API key: {len(working_api_key)} chars")
                # Return realistic JSON for strategic buyers
                return """{
                    "company_name": "TestCorp",
                    "strategic_buyers_mentioned": ["Microsoft", "Salesforce"],
                    "financial_buyers_mentioned": ["Vista Equity", "Thoma Bravo"],
                    "valuation_estimates_mentioned": ["15-20x revenue"]
                }"""
            else:
                st.write("❌ No API key available")
                return "{}"
        
        # Test conversation
        messages = [{"role": "user", "content": "Analyze TestCorp. Strategic buyers are Microsoft and Salesforce. Financial buyers are Vista Equity and Thoma Bravo."}]
        
        generator = CleanBulletproofJSONGenerator()
        result = generator.extract_conversation_data(messages, test_llm_call)
        
        st.write("**Extraction Result:**")
        st.json(result)
        
        if result and result.get('strategic_buyers_mentioned'):
            st.success("✅ Conversation extraction working!")
        else:
            st.error("❌ Conversation extraction failed!")
            
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Test 3: Test Gap-Filling
st.write("### Test 3: Gap-Filling Test")  
if st.button("Test Gap-Filling"):
    try:
        from bulletproof_json_generator_clean import CleanBulletproofJSONGenerator
        
        # Simulate extracted data with buyers
        extracted_data = {
            "company_name": "TestCorp",
            "strategic_buyers_mentioned": ["Microsoft", "Salesforce"],
            "financial_buyers_mentioned": ["Vista Equity", "Thoma Bravo"]
        }
        
        def test_gap_fill_llm(messages):
            working_api_key = st.session_state.get('api_key', '')
            if working_api_key:
                return """{
                    "strategic_buyers": [
                        {"buyer_name": "Microsoft", "strategic_rationale": "From conversation"},
                        {"buyer_name": "Salesforce", "strategic_rationale": "From conversation"}
                    ],
                    "financial_buyers": [
                        {"buyer_name": "Vista Equity", "strategic_rationale": "From conversation"},
                        {"buyer_name": "Thoma Bravo", "strategic_rationale": "From conversation"}  
                    ]
                }"""
            else:
                return "{}"
        
        generator = CleanBulletproofJSONGenerator()
        result = generator.comprehensive_llm_gap_filling(extracted_data, test_gap_fill_llm)
        
        st.write("**Gap-Filling Result:**")
        st.json(result)
        
        if result.get('strategic_buyers'):
            st.success("✅ Gap-filling working!")
        else:
            st.error("❌ Gap-filling failed!")
            
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Test 4: Check Slide Count
st.write("### Test 4: Slide Configuration")
expected_slides = [
    "business_overview", "product_service_footprint", 
    "historical_financial_performance", "management_team",
    "growth_strategy_projections", "competitive_positioning",
    "precedent_transactions", "valuation_overview",
    "strategic_buyers", "financial_buyers", "global_conglomerates",
    "margin_cost_resilience", "investor_considerations", "investor_process_overview"
]
st.write(f"Expected slides: {len(expected_slides)}")
for i, slide in enumerate(expected_slides, 1):
    st.write(f"{i}. {slide}")

'''

    print("📋 STREAMLIT DIAGNOSTIC CODE:")
    print(test_code)
    
    return test_code

def suggest_immediate_fixes():
    """Suggest immediate fixes based on the analysis"""
    
    print(f"\n🚨 IMMEDIATE FIXES NEEDED")
    print("=" * 40)
    
    fixes = [
        {
            "issue": "API calls failing silently",
            "fix": "Add error logging to bulletproof_llm_call function",
            "action": "Wrap API calls in try/catch with detailed error output"
        },
        {
            "issue": "Fallback data being used instead of real research", 
            "fix": "Force API calls or show clear error when they fail",
            "action": "Remove silent fallback behavior"
        },
        {
            "issue": "Only 5 slides instead of 14",
            "fix": "Check slide selection logic and empty data skipping",
            "action": "Ensure all 14 slides are attempted even with partial data"
        },
        {
            "issue": "Strategic/financial buyers empty despite conversation mentions",
            "fix": "Debug conversation extraction → gap-filling → JSON mapping",
            "action": "Add logging at each step to trace data flow"
        }
    ]
    
    print("🔧 CRITICAL FIXES:")
    for i, fix in enumerate(fixes, 1):
        print(f"\n{i}. {fix['issue']}")
        print(f"   Fix: {fix['fix']}")
        print(f"   Action: {fix['action']}")

def create_api_debug_patch():
    """Create a patch for the bulletproof_llm_call to add debugging"""
    
    print(f"\n🔧 API DEBUGGING PATCH")
    print("=" * 30)
    
    patch_code = '''
# PATCH: Add this debugging to bulletproof_llm_call function in app.py

def bulletproof_llm_call(messages):
    import os
    working_api_key = st.session_state.get('api_key', '') or os.getenv('PERPLEXITY_API_KEY', '')
    working_model = st.session_state.get('model', 'sonar-pro')  
    working_service = st.session_state.get('api_service', 'perplexity')
    
    # ENHANCED DEBUG LOGGING
    print(f"🔍 [API_DEBUG] Session state api_key length: {len(working_api_key) if working_api_key else 0}")
    print(f"🔍 [API_DEBUG] Using model: {working_model}")
    print(f"🔍 [API_DEBUG] Using service: {working_service}")
    
    if not working_api_key:
        print("🚨 [API_DEBUG] NO API KEY - THIS IS WHY JSON IS EMPTY!")
        st.error("🚨 **CRITICAL: No API Key Found!** This is why your JSON is empty.")
        return "FALLBACK_EMPTY_DATA"
    
    try:
        print(f"🔍 [API_DEBUG] Making real API call with {len(messages)} messages...")
        response = shared_call_llm_api(messages, working_model, working_api_key, working_service)
        print(f"🔍 [API_DEBUG] API response length: {len(response) if response else 0}")
        
        if not response or len(response) < 10:
            print("🚨 [API_DEBUG] API RESPONSE TOO SHORT - LIKELY FAILED!")
            st.error(f"🚨 **API Response Failed:** Got {len(response) if response else 0} chars")
        
        return response
        
    except Exception as e:
        print(f"🚨 [API_DEBUG] API CALL FAILED: {str(e)}")
        st.error(f"🚨 **API Call Failed:** {str(e)}")
        return "FALLBACK_ERROR_DATA"
'''

    print("📋 ENHANCED DEBUGGING PATCH:")
    print(patch_code)

if __name__ == "__main__":
    test_code = create_minimal_test()
    suggest_immediate_fixes()
    create_api_debug_patch()
    
    print(f"\n🎯 NEXT STEPS:")
    print(f"   1. Add the diagnostic code to your Streamlit app")
    print(f"   2. Run the tests to see exactly where it fails")
    print(f"   3. Apply the API debugging patch")
    print(f"   4. Check for specific error messages")
    
    print(f"\n💡 ROOT CAUSE HYPOTHESIS:")
    print(f"   Your sidebar API key is either:")
    print(f"   • Not being saved to session state properly")
    print(f"   • Being lost between function calls")  
    print(f"   • Invalid/expired causing silent failures")
    print(f"   • API rate limited or blocked")