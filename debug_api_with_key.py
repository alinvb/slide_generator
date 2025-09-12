#!/usr/bin/env python3
"""
Debug API with Valid Key - Check why configured API still returns empty arrays
"""

import json
import streamlit as st
from shared_functions import call_llm_api
from bulletproof_json_generator_clean import CleanBulletproofJSONGenerator

def setup_mock_session_with_api_key():
    """Setup session state with a mock API key for testing"""
    # Simulate having an API key configured
    st.session_state['api_key'] = 'test-api-key-configured'
    st.session_state['model'] = 'sonar-pro'
    st.session_state['api_service'] = 'perplexity'
    print(f"✅ Mock API key configured: {st.session_state['api_key'][:10]}...")

def test_api_call_with_configured_key():
    """Test what happens when API key is configured but call might fail"""
    print("🔍 Testing API call with configured key...")
    
    # Simple test message
    test_messages = [{"role": "user", "content": "Generate strategic buyers for Netflix: Microsoft, Apple, Amazon"}]
    
    try:
        print(f"🔍 Session state api_key: {st.session_state.get('api_key', 'NOT_FOUND')}")
        response = call_llm_api(test_messages, timeout=30)
        
        print(f"✅ API Response received")
        print(f"🔍 Response length: {len(response)} characters")
        print(f"🔍 Response preview: {response[:200]}...")
        
        # Check if response looks like actual API data or fallback
        if "TechCorp Solutions" in response:
            print("⚠️ DETECTED: Response is fallback data, not real API response")
            return "fallback"
        elif len(response) > 100:
            print("✅ DETECTED: Response appears to be real API data")
            return "real"
        else:
            print("❌ DETECTED: Response too short, likely failed")
            return "failed"
            
    except Exception as e:
        print(f"❌ API call failed: {e}")
        return "error"

def test_gap_filling_with_configured_api():
    """Test the comprehensive gap-filling with configured API"""
    print("\n🔍 Testing comprehensive gap-filling with configured API...")
    
    generator = CleanBulletproofJSONGenerator()
    
    # Netflix conversation with specific details
    netflix_messages = [
        {"role": "user", "content": "I want to analyze Netflix as an investment opportunity"},
        {"role": "assistant", "content": "Netflix is a leading streaming company with Ted Sarandos and Greg Peters as Co-CEOs, Spencer Neumann as CFO. Revenue around $31.6B, EBITDA $9.4B. Competitors include Disney+, Apple TV+, Amazon Prime Video."},
    ]
    
    # Extract conversation data first
    extracted_data = generator.extract_conversation_data(netflix_messages, call_llm_api)
    print(f"✅ Extracted data: {len(extracted_data)} fields")
    
    # Check what we got from conversation extraction
    strategic_mentioned = extracted_data.get('strategic_buyers_mentioned', [])
    financial_mentioned = extracted_data.get('financial_buyers_mentioned', [])
    
    print(f"🔍 Strategic buyers mentioned: {len(strategic_mentioned)} - {strategic_mentioned}")
    print(f"🔍 Financial buyers mentioned: {len(financial_mentioned)} - {financial_mentioned}")
    
    # Now test gap-filling
    print("\n🔍 Testing comprehensive LLM gap-filling...")
    comprehensive_data = generator.comprehensive_llm_gap_filling(extracted_data, call_llm_api)
    
    print(f"✅ Gap-filling complete: {len(comprehensive_data)} fields")
    
    # Check the key fields
    strategic_buyers = comprehensive_data.get('strategic_buyers', [])
    financial_buyers = comprehensive_data.get('financial_buyers', [])
    
    print(f"\n📊 Final Results:")
    print(f"   Strategic buyers: {len(strategic_buyers)} items")
    print(f"   Financial buyers: {len(financial_buyers)} items")
    
    if len(strategic_buyers) > 0:
        print(f"   First strategic buyer: {strategic_buyers[0].get('buyer_name', 'Unknown')}")
    
    if len(strategic_buyers) == 0 and len(financial_buyers) == 0:
        print("❌ ISSUE CONFIRMED: Gap-filling still returns empty arrays even with API key")
        return False
    else:
        print("✅ Gap-filling working correctly with API key")
        return True

def debug_llm_response_parsing():
    """Test if the issue is in JSON parsing of LLM responses"""
    print("\n🔍 Testing LLM response parsing...")
    
    # Simulate what an LLM might return for gap-filling
    mock_llm_response = '''Based on the Netflix analysis, here's the comprehensive investment banking data:

{
  "strategic_buyers": [
    {"buyer_name": "Apple Inc", "description": "Technology giant with streaming ambitions", "strategic_rationale": "Content and platform synergies"},
    {"buyer_name": "Microsoft Corporation", "description": "Cloud and enterprise leader", "strategic_rationale": "Gaming and cloud content integration"}
  ],
  "financial_buyers": [
    {"buyer_name": "Apollo Global Management", "description": "Leading private equity firm", "strategic_rationale": "Media sector expertise"}
  ],
  "management_team_profiles": [
    {"name": "Ted Sarandos", "role_title": "Co-CEO", "experience_bullets": ["20+ years at Netflix", "Content strategy expert"]}
  ]
}

This analysis shows strong strategic interest from technology companies.'''
    
    # Test JSON extraction
    import re
    json_match = re.search(r'\{.*\}', mock_llm_response, re.DOTALL)
    if json_match:
        json_str = json_match.group()
        print(f"✅ JSON found in response")
        
        try:
            parsed_data = json.loads(json_str)
            print(f"✅ JSON parsed successfully: {len(parsed_data)} fields")
            
            strategic_buyers = parsed_data.get('strategic_buyers', [])
            print(f"✅ Strategic buyers parsed: {len(strategic_buyers)} items")
            
            return True
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing failed: {e}")
            return False
    else:
        print(f"❌ No JSON found in response")
        return False

def main():
    """Run comprehensive API debugging with configured key"""
    print("🚀 Debugging API with Configured Key...")
    print("=" * 60)
    
    # Setup mock API key
    setup_mock_session_with_api_key()
    
    # Test 1: Basic API call
    print("📋 TEST 1: Basic API Call")
    api_result = test_api_call_with_configured_key()
    print(f"Result: {api_result}")
    
    # Test 2: JSON Parsing
    print("\n📋 TEST 2: JSON Parsing")
    parsing_works = debug_llm_response_parsing()
    print(f"Result: {'✅ Working' if parsing_works else '❌ Failed'}")
    
    # Test 3: Gap-filling with API
    print("\n📋 TEST 3: Gap-filling with Configured API") 
    gap_filling_works = test_gap_filling_with_configured_api()
    print(f"Result: {'✅ Working' if gap_filling_works else '❌ Failed'}")
    
    print("\n" + "=" * 60)
    print("🎯 DIAGNOSIS:")
    
    if api_result == "fallback":
        print("❌ ISSUE: API key configured but calls are still using fallback data")
        print("💡 CAUSE: API authentication failing or API service unreachable")
    elif api_result == "real" and not gap_filling_works:
        print("❌ ISSUE: API working but gap-filling returns empty arrays") 
        print("💡 CAUSE: LLM response format issues or parsing problems")
    elif gap_filling_works:
        print("✅ SUCCESS: API and gap-filling working correctly")
    else:
        print("❌ ISSUE: Multiple problems detected")

if __name__ == "__main__":
    main()