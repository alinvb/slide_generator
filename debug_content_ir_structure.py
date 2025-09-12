#!/usr/bin/env python3
"""
Debug Content IR Structure - Check why management team is missing
"""

import json
from bulletproof_json_generator_clean import generate_clean_bulletproof_json

def debug_content_ir_structure():
    """Debug the Content IR structure to see why management team is empty"""
    print("🔍 Debugging Content IR structure...")
    
    netflix_messages = [
        {"role": "user", "content": "Analyze Netflix as investment opportunity"},
        {"role": "assistant", "content": "Netflix is a leading streaming company with Ted Sarandos and Greg Peters as Co-CEOs"}
    ]
    
    required_slides = ["business_overview", "management_team", "strategic_buyers"]
    
    def mock_api_call_with_fallback(messages):
        from shared_functions import generate_fallback_response
        return generate_fallback_response(messages)
    
    try:
        response, content_ir, render_plan = generate_clean_bulletproof_json(
            netflix_messages, 
            required_slides,
            mock_api_call_with_fallback
        )
        
        print(f"✅ Generation completed")
        
        if content_ir:
            print(f"\n📊 FULL CONTENT IR STRUCTURE:")
            for key, value in content_ir.items():
                if isinstance(value, list):
                    print(f"   {key}: {len(value)} items (list)")
                elif isinstance(value, dict):
                    print(f"   {key}: {len(value)} keys (dict)")
                else:
                    print(f"   {key}: {value}")
            
            # Check management team structure specifically
            print(f"\n🔍 MANAGEMENT TEAM ANALYSIS:")
            
            # Check different possible keys
            management_keys = [
                'management_team',
                'management_team_profiles', 
                'management_profiles',
                'leadership_team'
            ]
            
            for key in management_keys:
                if key in content_ir:
                    value = content_ir[key]
                    print(f"   {key}: {value}")
                    if isinstance(value, dict):
                        for subkey, subvalue in value.items():
                            if isinstance(subvalue, list):
                                print(f"     {subkey}: {len(subvalue)} items")
                            else:
                                print(f"     {subkey}: {subvalue}")
                    break
            else:
                print(f"   ❌ No management team found under any expected key")
                
            # Check for strategic buyers
            print(f"\n🔍 STRATEGIC BUYERS:")
            strategic_buyers = content_ir.get('strategic_buyers', [])
            if strategic_buyers:
                for i, buyer in enumerate(strategic_buyers[:2]):
                    print(f"   {i+1}. {buyer.get('buyer_name', 'Unknown')}")
            
            return content_ir
            
    except Exception as e:
        print(f"❌ Debug failed: {e}")
        return None

if __name__ == "__main__":
    debug_content_ir_structure()