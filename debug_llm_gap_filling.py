#!/usr/bin/env python3
"""
Debug LLM Gap-Filling - Check why bulletproof generator returns empty arrays
"""

import streamlit as st
import sys
from shared_functions import call_llm_api
from bulletproof_json_generator_clean import CleanBulletproofJSONGenerator
import json

def test_llm_api_connection():
    """Test basic LLM API connection"""
    print("🔍 Testing LLM API Connection...")
    
    # Setup session state like the app would
    if 'api_key' not in st.session_state:
        from config import PERPLEXITY_API_KEY
        st.session_state['api_key'] = PERPLEXITY_API_KEY
        st.session_state['model'] = 'sonar-pro'
        st.session_state['api_service'] = 'perplexity'
    
    # Simple test message
    test_messages = [{"role": "user", "content": "What is 2+2? Answer with just the number."}]
    
    try:
        response = call_llm_api(test_messages, timeout=30)
        print(f"✅ LLM API Response: {response[:200]}...")
        return True if response and len(response.strip()) > 0 else False
    except Exception as e:
        print(f"❌ LLM API Test Failed: {e}")
        return False

def test_conversation_extraction():
    """Test conversation extraction with Netflix example"""
    print("\n🔍 Testing Conversation Extraction...")
    
    generator = CleanBulletproofJSONGenerator()
    
    # Netflix conversation example
    netflix_messages = [
        {"role": "user", "content": "I want to analyze Netflix as an investment opportunity"},
        {"role": "assistant", "content": "I'll help you analyze Netflix. Netflix is a leading streaming entertainment company founded in 1997, headquartered in Los Gatos, California. The company operates in over 190 countries with approximately 260 million subscribers as of 2024."},
        {"role": "user", "content": "What about their financial performance and management team?"},
        {"role": "assistant", "content": "Netflix has strong financial performance with around $31.6B in annual revenue and $9.4B EBITDA in 2023. Key executives include Co-CEO Ted Sarandos (Chief Content Officer) and Co-CEO Greg Peters, along with CFO Spencer Neumann. They've invested heavily in original content, spending over $15B annually on content production."}
    ]
    
    try:
        extracted_data = generator.extract_conversation_data(netflix_messages, call_llm_api)
        print(f"✅ Conversation Extraction Complete")
        print(f"🔍 Company Name: {extracted_data.get('company_name', 'Not Found')}")
        print(f"🔍 Fields Extracted: {len(extracted_data)}")
        print(f"🔍 Strategic Buyers Mentioned: {len(extracted_data.get('strategic_buyers_mentioned', []))}")
        print(f"🔍 Financial Buyers Mentioned: {len(extracted_data.get('financial_buyers_mentioned', []))}")
        print(f"🔍 Management Team Detailed: {len(extracted_data.get('management_team_detailed', []))}")
        
        return extracted_data
    except Exception as e:
        print(f"❌ Conversation Extraction Failed: {e}")
        return None

def test_gap_filling(extracted_data):
    """Test comprehensive LLM gap-filling"""
    print("\n🔍 Testing Comprehensive LLM Gap-Filling...")
    
    if not extracted_data:
        print("❌ No extracted data to gap-fill")
        return None
    
    generator = CleanBulletproofJSONGenerator()
    
    try:
        comprehensive_data = generator.comprehensive_llm_gap_filling(extracted_data, call_llm_api)
        print(f"✅ Gap-Filling Complete")
        print(f"🔍 Total Fields: {len(comprehensive_data)}")
        
        # Check key investment banking fields
        key_fields = {
            'strategic_buyers': comprehensive_data.get('strategic_buyers', []),
            'financial_buyers': comprehensive_data.get('financial_buyers', []),
            'management_team_profiles': comprehensive_data.get('management_team_profiles', []),
            'precedent_transactions': comprehensive_data.get('precedent_transactions', []),
            'competitive_analysis': comprehensive_data.get('competitive_analysis', {}),
            'facts': comprehensive_data.get('facts', {}),
            'entities': comprehensive_data.get('entities', {}),
            'valuation_data': comprehensive_data.get('valuation_data', [])
        }
        
        print(f"\n📊 Key Fields Analysis:")
        for field_name, field_data in key_fields.items():
            if isinstance(field_data, list):
                count = len(field_data)
                status = "✅ POPULATED" if count > 0 else "❌ EMPTY"
                print(f"   {field_name}: {count} items - {status}")
            elif isinstance(field_data, dict):
                count = len(field_data)
                status = "✅ POPULATED" if count > 0 else "❌ EMPTY"
                print(f"   {field_name}: {count} keys - {status}")
            else:
                status = "✅ POPULATED" if field_data else "❌ EMPTY"
                print(f"   {field_name}: {field_data} - {status}")
        
        return comprehensive_data
        
    except Exception as e:
        print(f"❌ Gap-Filling Failed: {e}")
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}")
        return None

def main():
    """Run comprehensive LLM gap-filling debug tests"""
    print("🚀 Starting LLM Gap-Filling Debug Tests...")
    print("=" * 60)
    
    # Test 1: Basic LLM API Connection
    api_working = test_llm_api_connection()
    if not api_working:
        print("❌ CRITICAL: LLM API not working - cannot proceed")
        return
    
    # Test 2: Conversation Extraction
    extracted_data = test_conversation_extraction()
    if not extracted_data:
        print("❌ CRITICAL: Conversation extraction failed")
        return
    
    # Test 3: Gap-Filling
    comprehensive_data = test_gap_filling(extracted_data)
    if not comprehensive_data:
        print("❌ CRITICAL: Gap-filling failed")
        return
    
    print("\n" + "=" * 60)
    print("🎯 DIAGNOSIS COMPLETE")
    print("=" * 60)
    
    # Final analysis
    strategic_buyers = comprehensive_data.get('strategic_buyers', [])
    financial_buyers = comprehensive_data.get('financial_buyers', [])
    management_profiles = comprehensive_data.get('management_team_profiles', [])
    
    if len(strategic_buyers) == 0 and len(financial_buyers) == 0 and len(management_profiles) == 0:
        print("❌ ISSUE CONFIRMED: LLM gap-filling returns empty arrays")
        print("🔍 LIKELY CAUSES:")
        print("   1. LLM API calls succeeding but returning insufficient data")
        print("   2. JSON parsing issues in gap-filling response")
        print("   3. Template structure mismatch")
        print("   4. Prompt too complex or unclear")
    else:
        print("✅ LLM GAP-FILLING WORKING: Populated arrays found")
        print(f"   Strategic Buyers: {len(strategic_buyers)}")
        print(f"   Financial Buyers: {len(financial_buyers)}")
        print(f"   Management Profiles: {len(management_profiles)}")

if __name__ == "__main__":
    main()