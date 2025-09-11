#!/usr/bin/env python3
"""
Debug why JSON is STILL empty despite all fixes
"""

import json
import os

def analyze_empty_json_pattern():
    """Analyze the specific empty JSON pattern you're seeing"""
    
    print("🚨 DEBUGGING PERSISTENT EMPTY JSON ISSUE")
    print("=" * 60)
    
    # The exact JSON you showed
    your_empty_json = {
        "entities": {"company": {"name": "Netflix"}},
        "facts": {
            "years": ["2024", "2025", "2026", "2027", "2028", "2029"],
            "revenue_usd_m": [39001.0, 42901.0, 47191.0, 51910.0, 57101.0, 62811.0],
            "ebitda_usd_m": [9750.0, 10725.0, 11798.0, 12978.0, 14275.0, 15703.0],
            "ebitda_margins": []
        },
        "management_team": {"left_column_profiles": [], "right_column_profiles": []},
        "strategic_buyers": [],
        "financial_buyers": [],
        "competitive_analysis": {"competitors": [{"name": "Netflix", "revenue": 62811.0}], "assessment": [], "barriers": [], "advantages": []},
        "precedent_transactions": ["WarnerMedia (AT&T) / Discovery, Inc. ($96B, 2021, all-stock merger)", "MGM Studios / Amazon ($8.45B, 2021, all-cash)", "Hulu (33% stake) / Walt Disney Co. ($8.61B for 33%, 2024, cash buyout)", "DAZN / Access Industries ($4.3B recap, 2022)"],
        "valuation_data": [],
        "product_service_data": {"services": [], "coverage_table": [], "metrics": {}},
        "business_overview_data": {"description": "", "timeline": {"start_year": None, "end_year": 2025}, "highlights": [], "services": [], "positioning_desc": ""},
        "growth_strategy_data": {"growth_strategy": {"strategies": []}, "financial_projections": {}},
        "investor_process_data": {"diligence_topics": [], "synergy_opportunities": [], "risk_factors": [], "mitigants": [], "timeline": []},
        "margin_cost_data": {"chart_data": {"categories": ["2024", "2025", "2026", "2027", "2028", "2029"], "values": []}, "cost_management": {}, "risk_mitigation": {}},
        "sea_conglomerates": [],
        "investor_considerations": {"considerations": [], "mitigants": []}
    }
    
    print("🔍 ANALYSIS OF YOUR EMPTY JSON:")
    
    # What's populated
    populated_sections = []
    empty_sections = []
    
    def analyze_section(name, data):
        if isinstance(data, list):
            return len(data) > 0
        elif isinstance(data, dict):
            if name == "facts":
                # Special handling for facts section
                return any(len(v) > 0 for k, v in data.items() if isinstance(v, list))
            else:
                return any(analyze_section(k, v) for k, v in data.items())
        elif isinstance(data, str):
            return len(data.strip()) > 0
        else:
            return data is not None
    
    for section, data in your_empty_json.items():
        if analyze_section(section, data):
            populated_sections.append(section)
        else:
            empty_sections.append(section)
    
    print(f"✅ POPULATED SECTIONS ({len(populated_sections)}):")
    for section in populated_sections:
        print(f"   • {section}")
    
    print(f"\n❌ EMPTY SECTIONS ({len(empty_sections)}):")
    for section in empty_sections:
        print(f"   • {section}")
    
    # Key observations
    print(f"\n🔍 KEY OBSERVATIONS:")
    print(f"   • Company name: Netflix (basic)")
    print(f"   • Financial data: Present (revenue/EBITDA projections)")
    print(f"   • Precedent transactions: Present (4 deals)")
    print(f"   • Strategic buyers: EMPTY ❌")
    print(f"   • Financial buyers: EMPTY ❌")
    print(f"   • Management team: EMPTY ❌")
    print(f"   • Valuation data: EMPTY ❌")
    print(f"   • Business description: EMPTY ❌")
    
    print(f"\n🚨 CRITICAL ISSUE IDENTIFIED:")
    print(f"   This looks like FALLBACK DATA, not real research!")
    print(f"   - Basic financials present = Generic fallback")  
    print(f"   - All strategic sections empty = API calls failed")
    print(f"   - Netflix name = Generic company fallback")

def trace_api_call_path():
    """Trace where API calls might be failing"""
    
    print(f"\n🔍 TRACING API CALL FAILURE PATH")
    print("=" * 50)
    
    possible_failure_points = [
        {
            "step": "1. Sidebar API Key Not Reaching bulletproof_llm_call",
            "symptom": "API key debug logs show 'None'",
            "test": "Check console for '[API_KEY_DEBUG] Session state api_key: None'"
        },
        {
            "step": "2. Conversation Extraction Failing",
            "symptom": "No conversation data extracted",
            "test": "Check for '[CLEAN] Starting INDEPENDENT conversation data extraction' followed by failure"
        },
        {
            "step": "3. LLM Gap-Filling Failing",
            "symptom": "Gap-filling returns empty or errors",
            "test": "Check for '[CLEAN] Making LLM call for comprehensive gap-filling' followed by error"
        },
        {
            "step": "4. JSON Structure Mapping Issue", 
            "symptom": "Data extracted but not mapped to final JSON",
            "test": "Conversation extraction succeeds but final JSON still empty"
        },
        {
            "step": "5. Perplexity API Rate Limits/Errors",
            "symptom": "API calls timeout or return errors",
            "test": "Check for API error messages or timeout responses"
        }
    ]
    
    print("🎯 FAILURE POINT CHECKLIST:")
    for point in possible_failure_points:
        print(f"\n{point['step']}:")
        print(f"   Symptom: {point['symptom']}")
        print(f"   Test: {point['test']}")

def create_debug_test():
    """Create a simple test to identify the exact failure point"""
    
    print(f"\n🧪 CREATING DIAGNOSTIC TEST")
    print("=" * 40)
    
    diagnostic_code = '''
import streamlit as st
import os

# Test 1: Check if API key is in session state
print("🔍 TEST 1: API Key Check")
api_key = st.session_state.get('api_key', '')
env_key = os.getenv('PERPLEXITY_API_KEY', '')
print(f"   Sidebar API key: {'Found' if api_key else 'Missing'}")
print(f"   Environment API key: {'Found' if env_key else 'Missing'}")

# Test 2: Test bulletproof_llm_call function
print("🔍 TEST 2: bulletproof_llm_call Test")
try:
    def test_llm_call(messages):
        working_api_key = st.session_state.get('api_key', '') or os.getenv('PERPLEXITY_API_KEY', '')
        print(f"   API Key Length: {len(working_api_key) if working_api_key else 0}")
        if working_api_key:
            print("   ✅ API key available for calls")
            return "TEST_SUCCESS"
        else:
            print("   ❌ No API key - using fallback")
            return "FALLBACK_DATA"
    
    result = test_llm_call([{"role": "user", "content": "test"}])
    print(f"   Result: {result}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Test conversation extraction
print("🔍 TEST 3: Conversation Extraction Test")
try:
    from bulletproof_json_generator_clean import CleanBulletproofJSONGenerator
    
    messages = [{"role": "user", "content": "Analyze Netflix. Strategic buyers include Disney and Apple."}]
    generator = CleanBulletproofJSONGenerator()
    
    def mock_api(msgs):
        return '{"company_name": "Netflix", "strategic_buyers_mentioned": ["Disney", "Apple"]}'
    
    result = generator.extract_conversation_data(messages, mock_api)
    print(f"   Extracted fields: {len(result) if result else 0}")
    if result:
        print(f"   Strategic buyers: {result.get('strategic_buyers_mentioned', [])}")
except Exception as e:
    print(f"   ❌ Error: {e}")
'''
    
    print("📋 ADD THIS TO YOUR STREAMLIT APP TO DIAGNOSE:")
    print("```python")
    print(diagnostic_code)
    print("```")

def analyze_5_slide_issue():
    """Analyze why only 5 slides are generated"""
    
    print(f"\n🎯 DEBUGGING 5-SLIDE LIMIT ISSUE")
    print("=" * 50)
    
    print("🔍 POSSIBLE CAUSES:")
    print("   1. Slide selection limited to 5 slides")
    print("   2. Empty JSON sections → slides skipped")
    print("   3. Slide template mapping issues")
    print("   4. Required slides not matching available slides")
    
    standard_ib_slides = [
        "executive_summary",
        "business_overview", 
        "management_team",
        "financial_performance",
        "competitive_analysis",
        "strategic_buyers",
        "financial_buyers",
        "precedent_transactions",
        "valuation_analysis",
        "investment_considerations",
        "growth_strategy",
        "risk_factors",
        "deal_structure",
        "appendix"
    ]
    
    print(f"\n📊 STANDARD IB PRESENTATION SLIDES ({len(standard_ib_slides)}):")
    for i, slide in enumerate(standard_ib_slides, 1):
        print(f"   {i:2d}. {slide}")
    
    print(f"\n🚨 IF ONLY 5 SLIDES GENERATED:")
    print(f"   Either: Slide list truncated to 5")
    print(f"   Or: 9+ slides skipped due to empty data")
    
    return standard_ib_slides

if __name__ == "__main__":
    analyze_empty_json_pattern()
    trace_api_call_path()
    standard_slides = analyze_5_slide_issue()
    create_debug_test()
    
    print(f"\n🎯 IMMEDIATE ACTION PLAN:")
    print(f"   1. Check Streamlit console logs for API key debug messages")
    print(f"   2. Look for conversation extraction success/failure logs")
    print(f"   3. Verify gap-filling LLM call completion")
    print(f"   4. Check slide count in slide selection")
    print(f"   5. Test with diagnostic code above")
    
    print(f"\n💡 HYPOTHESIS:")
    print(f"   Your JSON pattern suggests API calls are failing silently")
    print(f"   System is falling back to generic Netflix financial data")
    print(f"   Conversation extraction/gap-filling not executing properly")
    print(f"   Need to trace exact failure point in the pipeline")