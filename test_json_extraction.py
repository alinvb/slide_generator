#!/usr/bin/env python3
"""
Test JSON extraction with the exact conversation content that failed to auto-populate
"""

import json
import sys
import os

# Add the webapp directory to the path to import modules
sys.path.append('/home/user/webapp')

from app import extract_jsons_from_response, extract_and_validate_jsons

def test_json_extraction():
    """Test JSON extraction with the user's failing conversation"""
    
    # This is the exact AI response that failed to auto-populate
    test_response = """Perfect! I now have all the information needed to create your comprehensive pitch deck. Here are your complete, downloadable pitch deck files:

CONTENT IR JSON:
{
  "entities": {
    "company": {
      "name": "Qi Card"
    }
  },
  "facts": {
    "years": ["2020", "2021", "2022", "2023", "2024E"],
    "revenue_usd_m": [120, 145, 180, 210, 240],
    "ebitda_usd_m": [18, 24, 31, 40, 47],
    "ebitda_margins": [15.0, 16.6, 17.2, 19.0, 19.6]
  },
  "strategic_buyers": [
    {
      "buyer_name": "NymCard",
      "description": "UAE-based MENA payments infrastructure leader",
      "strategic_rationale": "Expand embedded finance, leverage Qi Card's user base for pan-regional growth",
      "key_synergies": "Technology integration, scale, cross-border payments",
      "fit": "High (9/10) - Strong regional strategic alignment",
      "financial_capacity": "High"
    }
  ]
}

RENDER PLAN JSON:
{
  "slides": [
    {"template": "business_overview", "data": {
      "title": "Business Overview",
      "description": "Qi Card, operated by International Smart Card (ISC), is Iraq's largest fintech company"
    }}
  ]
}

These files are now ready for download and can be used directly with your pitch deck generation system!"""

    print("🔍 Testing JSON extraction with user's failing conversation...")
    print(f"Response length: {len(test_response)} characters")
    
    # Test the basic extraction function
    print("\n" + "="*60)
    print("TESTING: extract_jsons_from_response()")
    print("="*60)
    
    content_ir, render_plan = extract_jsons_from_response(test_response)
    
    print(f"\nExtraction Results:")
    print(f"Content IR extracted: {'✅ YES' if content_ir else '❌ NO'}")
    print(f"Render Plan extracted: {'✅ YES' if render_plan else '❌ NO'}")
    
    if content_ir:
        print(f"Content IR type: {type(content_ir)}")
        print(f"Content IR keys: {list(content_ir.keys()) if isinstance(content_ir, dict) else 'Not a dict'}")
        print(f"Company name: {content_ir.get('entities', {}).get('company', {}).get('name', 'Not found')}")
        
    if render_plan:
        print(f"Render Plan type: {type(render_plan)}")
        print(f"Slides count: {len(render_plan.get('slides', []))}")
    
    # Test the full validation function
    print("\n" + "="*60) 
    print("TESTING: extract_and_validate_jsons()")
    print("="*60)
    
    content_ir_val, render_plan_val, validation_results = extract_and_validate_jsons(test_response)
    
    print(f"\nValidation Results:")
    print(f"Content IR validated: {'✅ YES' if content_ir_val else '❌ NO'}")
    print(f"Render Plan validated: {'✅ YES' if render_plan_val else '❌ NO'}")
    print(f"Overall valid: {validation_results.get('overall_valid', False)}")
    print(f"Extraction failed: {validation_results.get('extraction_failed', False)}")
    
    if validation_results.get('critical_issues'):
        print(f"Critical issues: {validation_results['critical_issues']}")
        
    # Test if the JSONs are actually valid
    print("\n" + "="*60)
    print("MANUAL JSON VALIDATION")
    print("="*60)
    
    # Find JSON manually
    content_start = test_response.find("CONTENT IR JSON:")
    render_start = test_response.find("RENDER PLAN JSON:")
    
    if content_start != -1:
        json_start = test_response.find('{', content_start)
        render_json_start = test_response.find("RENDER PLAN JSON:", json_start)
        
        if render_json_start != -1:
            content_json_text = test_response[json_start:render_json_start].strip()
        else:
            content_json_text = test_response[json_start:].strip()
            
        print(f"Found Content IR JSON at position {json_start}")
        print(f"Content IR JSON length: {len(content_json_text)} characters")
        
        try:
            manual_content_ir = json.loads(content_json_text)
            print("✅ Manual Content IR parsing: SUCCESS")
            print(f"Company: {manual_content_ir.get('entities', {}).get('company', {}).get('name', 'Not found')}")
        except json.JSONDecodeError as e:
            print(f"❌ Manual Content IR parsing failed: {e}")
            print(f"JSON excerpt: {content_json_text[:200]}...")
    
    if render_start != -1:
        render_json_start = test_response.find('{', render_start)
        if render_json_start != -1:
            render_json_text = test_response[render_json_start:].strip()
            # Clean up trailing text
            brace_count = 0
            end_pos = render_json_start
            for i, char in enumerate(test_response[render_json_start:]):
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end_pos = render_json_start + i + 1
                        break
            
            render_json_text = test_response[render_json_start:end_pos]
            
            print(f"Found Render Plan JSON at position {render_json_start}")
            print(f"Render Plan JSON length: {len(render_json_text)} characters")
            
            try:
                manual_render_plan = json.loads(render_json_text)
                print("✅ Manual Render Plan parsing: SUCCESS")
                print(f"Slides: {len(manual_render_plan.get('slides', []))}")
            except json.JSONDecodeError as e:
                print(f"❌ Manual Render Plan parsing failed: {e}")
                print(f"JSON excerpt: {render_json_text[:200]}...")

if __name__ == "__main__":
    test_json_extraction()