#!/usr/bin/env python3
"""
Test script to debug bulletproof JSON generator
"""

import os
from bulletproof_json_generator_clean import generate_clean_bulletproof_json
from shared_functions import call_llm_api

def test_bulletproof_generator():
    """Test the bulletproof JSON generator directly"""
    
    print("🧪 Testing bulletproof JSON generator...")
    
    # Create test messages like a conversation about Sephora
    test_messages = [
        {
            "role": "user", 
            "content": "I want to analyze Sephora for investment banking purposes"
        },
        {
            "role": "assistant", 
            "content": "I'll help you analyze Sephora. What specific information do you need for the investment banking analysis?"
        },
        {
            "role": "user", 
            "content": "Sephora is the world's leading global prestige beauty retail brand, operating over 3,200 stores and iconic flagships in 35 markets. It offers a curated selection of more than 300 brands and its own Sephora Collection. Founded in 1969 in France, part of LVMH Group since 1997. Annual revenue around $17 billion, with strong digital innovation and omnichannel network."
        }
    ]
    
    # Required slides list
    required_slides = [
        "business_overview",
        "management_team", 
        "historical_financial_performance",
        "strategic_buyers",
        "financial_buyers",
        "competitive_positioning",
        "precedent_transactions",
        "valuation_overview"
    ]
    
    def test_llm_call(messages):
        """Test LLM call function"""
        print(f"🤖 [TEST] LLM call with {len(messages)} messages")
        
        # Check API key
        api_key = os.getenv('PERPLEXITY_API_KEY', '')
        if not api_key:
            print("⚠️ [TEST] No API key found in environment")
            print("⚠️ [TEST] This will trigger fallback data generation")
        else:
            print(f"✅ [TEST] API key found: {api_key[:10]}...")
        
        # Make actual API call
        try:
            response = call_llm_api(messages, timeout=180)  # Extended timeout
            print(f"✅ [TEST] LLM response received: {len(response)} characters")
            return response
        except Exception as e:
            print(f"❌ [TEST] LLM call failed: {e}")
            return f"Error: {e}"
    
    print("\n🚀 Starting bulletproof JSON generation test...")
    
    try:
        # Call the bulletproof generator
        response, content_ir, render_plan = generate_clean_bulletproof_json(
            test_messages,
            required_slides, 
            test_llm_call
        )
        
        print(f"\n✅ Generation completed!")
        print(f"📝 Response length: {len(response)}")
        print(f"📊 Content IR keys: {list(content_ir.keys()) if isinstance(content_ir, dict) else 'Not a dict'}")
        print(f"📋 Render plan keys: {list(render_plan.keys()) if isinstance(render_plan, dict) else 'Not a dict'}")
        
        # Check for empty data issue
        if isinstance(content_ir, dict):
            print("\n🔍 Checking for empty data issue...")
            
            # Check key sections for empty arrays
            empty_sections = []
            for key, value in content_ir.items():
                if isinstance(value, list) and len(value) == 0:
                    empty_sections.append(f"{key}: empty array")
                elif isinstance(value, dict):
                    empty_subsections = []
                    for subkey, subvalue in value.items():
                        if isinstance(subvalue, list) and len(subvalue) == 0:
                            empty_subsections.append(subkey)
                    if empty_subsections:
                        empty_sections.append(f"{key}: {empty_subsections}")
            
            if empty_sections:
                print(f"❌ Found empty sections: {empty_sections}")
            else:
                print("✅ No empty sections found")
            
            # Check specific problematic fields from user's example
            problematic_fields = [
                "management_team.left_column_profiles",
                "management_team.right_column_profiles", 
                "strategic_buyers",
                "financial_buyers",
                "competitive_analysis.assessment",
                "precedent_transactions",
                "valuation_data"
            ]
            
            print(f"\n🔍 Checking specific problematic fields...")
            for field_path in problematic_fields:
                parts = field_path.split('.')
                current = content_ir
                try:
                    for part in parts:
                        current = current[part]
                    if isinstance(current, list):
                        print(f"  {field_path}: {len(current)} items")
                        if len(current) > 0:
                            print(f"    Sample: {str(current[0])[:100]}...")
                    else:
                        print(f"  {field_path}: {current}")
                except (KeyError, TypeError):
                    print(f"  {field_path}: NOT FOUND")
        
        return response, content_ir, render_plan
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}")
        return None, None, None

if __name__ == "__main__":
    test_bulletproof_generator()