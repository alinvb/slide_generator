#!/usr/bin/env python3
"""
Debug the entire pipeline step by step to find where it's failing
"""

import json
import os
import sys

def test_step_1_conversation_extraction():
    """Test Step 1: Conversation Extraction"""
    
    print("🔍 STEP 1: TESTING CONVERSATION EXTRACTION")
    print("=" * 50)
    
    try:
        from bulletproof_json_generator_clean import CleanBulletproofJSONGenerator
        
        # Netflix conversation messages
        netflix_messages = [
            {"role": "user", "content": "Strategic buyers could include Apple (has $200B+ cash, needs content for Apple TV+), Amazon (content for Prime Video, cloud synergies), Microsoft (gaming + content convergence, Azure integration)"},
            {"role": "user", "content": "Financial buyers include Berkshire Hathaway (Warren Buffett likes media/content businesses), Apollo Global Management (large media deals), KKR (has media expertise)"}
        ]
        
        # Mock API call that should return proper JSON
        def mock_extraction_api(messages):
            print(f"   🤖 Mock API called with {len(messages)} messages")
            return '''
            {
                "company_name": "Netflix, Inc.",
                "strategic_buyers_mentioned": ["Apple (has $200B+ cash, needs content for Apple TV+)", "Amazon (content for Prime Video, cloud synergies)", "Microsoft (gaming + content convergence, Azure integration)"],
                "financial_buyers_mentioned": ["Berkshire Hathaway (Warren Buffett likes media/content businesses)", "Apollo Global Management (large media deals)", "KKR (has media expertise)"],
                "valuation_estimates_mentioned": ["10-15x revenue multiple"]
            }
            '''
        
        generator = CleanBulletproofJSONGenerator()
        result = generator.extract_conversation_data(netflix_messages, mock_extraction_api)
        
        print(f"✅ STEP 1 RESULT:")
        print(f"   • Extracted fields: {len(result) if result else 0}")
        if result:
            for key, value in result.items():
                print(f"   • {key}: {value}")
        
        return result
        
    except Exception as e:
        print(f"❌ STEP 1 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_step_2_gap_filling():
    """Test Step 2: Gap Filling"""
    
    print(f"\n🔍 STEP 2: TESTING GAP FILLING")
    print("=" * 50)
    
    try:
        from bulletproof_json_generator_clean import CleanBulletproofJSONGenerator
        
        # Simulated extracted data from Step 1
        extracted_data = {
            "company_name": "Netflix, Inc.",
            "strategic_buyers_mentioned": ["Apple", "Amazon", "Microsoft"],
            "financial_buyers_mentioned": ["Berkshire Hathaway", "Apollo", "KKR"],
            "management_team_detailed": ["Ted Sarandos (Co-CEO)", "Greg Peters (Co-CEO)"]
        }
        
        # Mock gap-filling API that returns comprehensive JSON
        def mock_gap_filling_api(messages):
            print(f"   🤖 Gap-filling API called with {len(messages)} messages")
            return '''
            {
                "company_name": "Netflix, Inc.",
                "strategic_buyers": [
                    {"buyer_name": "Apple Inc.", "strategic_rationale": "Apple TV+ content needs"},
                    {"buyer_name": "Amazon.com Inc.", "strategic_rationale": "Prime Video integration"},
                    {"buyer_name": "Microsoft Corporation", "strategic_rationale": "Gaming convergence"}
                ],
                "financial_buyers": [
                    {"buyer_name": "Berkshire Hathaway", "strategic_rationale": "Media business preference"},
                    {"buyer_name": "Apollo Global Management", "strategic_rationale": "Large media deals"},
                    {"buyer_name": "KKR & Co", "strategic_rationale": "Media expertise"}
                ],
                "management_team_profiles": [
                    {"name": "Ted Sarandos", "role_title": "Co-CEO", "experience_bullets": ["Content expertise", "Hollywood relationships"]},
                    {"name": "Greg Peters", "role_title": "Co-CEO", "experience_bullets": ["Product focus", "Technology background"]}
                ]
            }
            '''
        
        generator = CleanBulletproofJSONGenerator()
        result = generator.comprehensive_llm_gap_filling(extracted_data, mock_gap_filling_api)
        
        print(f"✅ STEP 2 RESULT:")
        print(f"   • Gap-filled fields: {len(result) if result else 0}")
        if result:
            for key, value in result.items():
                if isinstance(value, list) and len(value) > 0:
                    print(f"   ✅ {key}: {len(value)} items")
                elif isinstance(value, str) and len(value) > 0:
                    print(f"   ✅ {key}: {value[:50]}...")
        
        return result
        
    except Exception as e:
        print(f"❌ STEP 2 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_step_3_content_ir_building():
    """Test Step 3: Content IR Building"""
    
    print(f"\n🔍 STEP 3: TESTING CONTENT IR BUILDING")
    print("=" * 50)
    
    try:
        from bulletproof_json_generator_clean import CleanBulletproofJSONGenerator
        
        # Simulated gap-filled data from Step 2
        enhanced_data = {
            "company_name": "Netflix, Inc.",
            "strategic_buyers": [
                {"buyer_name": "Apple Inc.", "strategic_rationale": "Apple TV+ content needs"},
                {"buyer_name": "Amazon.com Inc.", "strategic_rationale": "Prime Video integration"}
            ],
            "financial_buyers": [
                {"buyer_name": "Berkshire Hathaway", "strategic_rationale": "Media business preference"},
                {"buyer_name": "Apollo Global Management", "strategic_rationale": "Large media deals"}
            ]
        }
        
        # Mock API for content IR
        def mock_content_ir_api(messages):
            return '{"status": "content_ir_complete"}'
        
        # Required slides list
        required_slides = [
            "business_overview", "management_team", "strategic_buyers", 
            "financial_buyers", "valuation_overview"
        ]
        
        generator = CleanBulletproofJSONGenerator()
        result = generator.build_content_ir(enhanced_data, required_slides, mock_content_ir_api)
        
        print(f"✅ STEP 3 RESULT:")
        print(f"   • Content IR sections: {len(result) if result else 0}")
        if result:
            for key, value in result.items():
                if isinstance(value, dict) or isinstance(value, list):
                    print(f"   ✅ {key}: {type(value).__name__}")
                else:
                    print(f"   ✅ {key}: {str(value)[:30]}...")
        
        return result
        
    except Exception as e:
        print(f"❌ STEP 3 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_step_4_json_structure_mapping():
    """Test Step 4: JSON Structure Mapping"""
    
    print(f"\n🔍 STEP 4: TESTING JSON STRUCTURE MAPPING")
    print("=" * 50)
    
    # Simulate what should be in content_ir
    content_ir = {
        "strategic_buyers": [
            {"buyer_name": "Apple Inc.", "strategic_rationale": "Apple TV+ content needs"},
            {"buyer_name": "Amazon.com Inc.", "strategic_rationale": "Prime Video integration"}
        ],
        "financial_buyers": [
            {"buyer_name": "Berkshire Hathaway", "strategic_rationale": "Media business preference"}
        ],
        "management_team_profiles": [
            {"name": "Ted Sarandos", "role_title": "Co-CEO"}
        ]
    }
    
    # Check how this maps to the final JSON structure
    final_json_structure = {
        "strategic_buyers": content_ir.get("strategic_buyers", []),
        "financial_buyers": content_ir.get("financial_buyers", []),
        "management_team": {
            "left_column_profiles": content_ir.get("management_team_profiles", []),
            "right_column_profiles": []
        }
    }
    
    print(f"✅ STEP 4 RESULT:")
    for section, data in final_json_structure.items():
        if isinstance(data, list):
            print(f"   • {section}: {len(data)} items")
        elif isinstance(data, dict):
            total_items = sum(len(v) if isinstance(v, list) else 1 for v in data.values())
            print(f"   • {section}: {total_items} total items")
    
    return final_json_structure

def test_step_5_api_key_and_real_calls():
    """Test Step 5: API Key and Real Calls"""
    
    print(f"\n🔍 STEP 5: TESTING API KEY AND REAL CALLS")
    print("=" * 50)
    
    # Check API key availability
    import streamlit as st
    session_api_key = st.session_state.get('api_key', '') if 'st' in sys.modules else ''
    env_api_key = os.getenv('PERPLEXITY_API_KEY', '')
    
    print(f"📋 API KEY STATUS:")
    print(f"   • Session state: {'Found' if session_api_key else 'Missing'} ({len(session_api_key)} chars)")
    print(f"   • Environment: {'Found' if env_api_key else 'Missing'} ({len(env_api_key)} chars)")
    
    working_key = session_api_key or env_api_key
    
    if working_key:
        print(f"   ✅ API key available for real calls")
        
        # Test a simple API call if shared_functions is available
        try:
            from shared_functions import call_llm_api
            
            test_messages = [{"role": "user", "content": "Return just the word 'SUCCESS' if you receive this"}]
            response = call_llm_api(test_messages, "sonar-pro", working_key, "perplexity", 0, 30)
            
            print(f"   ✅ Test API call result: {len(response) if response else 0} characters")
            if response and len(response) > 0:
                print(f"   ✅ API calls working: {response[:50]}...")
            else:
                print(f"   ❌ API call returned empty response")
            
        except Exception as e:
            print(f"   ❌ API call failed: {e}")
    else:
        print(f"   ❌ No API key available - this is likely the root cause")
    
    return working_key is not None

def run_full_pipeline_diagnostic():
    """Run the complete diagnostic"""
    
    print("🚨 COMPLETE PIPELINE DIAGNOSTIC")
    print("=" * 60)
    
    results = {}
    
    # Test each step
    results['step_1'] = test_step_1_conversation_extraction()
    results['step_2'] = test_step_2_gap_filling()
    results['step_3'] = test_step_3_content_ir_building()
    results['step_4'] = test_step_4_json_structure_mapping()
    results['step_5'] = test_step_5_api_key_and_real_calls()
    
    # Summary
    print(f"\n🎯 DIAGNOSTIC SUMMARY:")
    print("=" * 30)
    
    step_names = [
        "Conversation Extraction",
        "Gap Filling", 
        "Content IR Building",
        "JSON Structure Mapping",
        "API Key & Real Calls"
    ]
    
    for i, (step_key, step_name) in enumerate(zip(results.keys(), step_names), 1):
        result = results[step_key]
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   Step {i}: {step_name} - {status}")
    
    # Identify likely root cause
    print(f"\n🔍 ROOT CAUSE ANALYSIS:")
    
    if not results['step_5']:
        print(f"   🚨 PRIMARY ISSUE: No API key - all LLM calls will fail")
        print(f"   💡 SOLUTION: Add valid Perplexity API key in sidebar")
    elif not results['step_1']:
        print(f"   🚨 PRIMARY ISSUE: Conversation extraction failing")
        print(f"   💡 SOLUTION: Debug CleanBulletproofJSONGenerator.extract_conversation_data()")
    elif not results['step_2']:
        print(f"   🚨 PRIMARY ISSUE: Gap filling failing")
        print(f"   💡 SOLUTION: Debug comprehensive_llm_gap_filling()")
    elif not results['step_3']:
        print(f"   🚨 PRIMARY ISSUE: Content IR building failing")
        print(f"   💡 SOLUTION: Debug build_content_ir()")
    else:
        print(f"   ✅ All steps working - issue might be in final JSON assembly")
    
    return results

if __name__ == "__main__":
    results = run_full_pipeline_diagnostic()
    
    print(f"\n🎯 NEXT ACTIONS:")
    if not results['step_5']:
        print(f"   1. 🔴 CRITICAL: Add Perplexity API key in sidebar")
        print(f"   2. Check console for 'CRITICAL: No API Key Found!' messages") 
        print(f"   3. Verify key is being saved to session state")
    else:
        print(f"   1. Focus debugging on the first failing step above")
        print(f"   2. Add detailed logging to that specific component")
        print(f"   3. Test with minimal inputs to isolate the issue")