#!/usr/bin/env python3
"""
Debug script to test JSON extraction with user's specific format
This will help identify exactly why auto-population isn't working
"""

import json
import re
from pathlib import Path

def clean_json_string(json_str):
    """EXACT COPY of the fixed clean function from app.py"""
    if not json_str:
        return ""
    
    # Remove common markdown/formatting including bold markers
    json_str = json_str.replace("```json", "").replace("```", "")
    json_str = json_str.replace("**", "")  # Remove markdown bold
    json_str = json_str.replace("*", "")   # Remove markdown italic
    
    # Remove any leading text before JSON
    lines = json_str.split('\n')
    json_lines = []
    found_start = False
    
    for line in lines:
        line = line.strip()
        if line.startswith('{') or found_start:
            found_start = True
            json_lines.append(line)
        elif '{' in line:
            # Line contains { but doesn't start with it
            start_pos = line.find('{')
            json_lines.append(line[start_pos:])
            found_start = True
    
    if json_lines:
        cleaned = '\n'.join(json_lines).strip()
        
        # Find first { and last }
        start = cleaned.find("{")
        end = cleaned.rfind("}") + 1
        
        if start >= 0 and end > start:
            return cleaned[start:end].strip()
    
    # Fallback to original method
    start = json_str.find("{")
    end = json_str.rfind("}") + 1
    
    if start >= 0 and end > start:
        return json_str[start:end].strip()
    
    return json_str.strip()

def extract_jsons_from_response(response_text):
    """EXACT COPY of the fixed extraction function from app.py"""
    content_ir = None
    render_plan = None
    
    print(f"[JSON EXTRACTION] Starting extraction from response of length: {len(response_text)}")
    
    try:
        # 🚨 PRIORITY 1 FIX: Enhanced extraction supporting user's exact format with markdown
        content_ir_markers = [
            "**CONTENT IR JSON:**", "**Content IR JSON:**", "**content ir json:**",
            "CONTENT IR JSON:", "Content IR JSON:", "content ir json:", "CONTENT_IR JSON:",
            "Content IR:", "content ir:", "CONTENT IR:"
        ]
        render_plan_markers = [
            "**RENDER PLAN JSON:**", "**Render Plan JSON:**", "**render plan json:**",
            "RENDER PLAN JSON:", "Render Plan JSON:", "render plan json:", "RENDER_PLAN JSON:",
            "Render Plan:", "render plan:", "RENDER PLAN:"
        ]
        
        # Find the correct markers (case-insensitive)
        content_ir_marker = None
        render_plan_marker = None
        
        for marker in content_ir_markers:
            if marker in response_text:
                content_ir_marker = marker
                print(f"[JSON EXTRACTION] 🎯 Found Content IR marker: '{marker}'")
                break
        
        for marker in render_plan_markers:
            if marker in response_text:
                render_plan_marker = marker
                print(f"[JSON EXTRACTION] 🎯 Found Render Plan marker: '{marker}'")
                break
        
        if content_ir_marker and render_plan_marker:
            print(f"[JSON EXTRACTION] ✅ Both markers found!")
            
            # Extract Content IR JSON
            content_ir_start = response_text.find(content_ir_marker) + len(content_ir_marker)
            content_ir_end = response_text.find(render_plan_marker)
            content_ir_json_str = response_text[content_ir_start:content_ir_end].strip()
            
            # Extract Render Plan JSON  
            render_plan_start = response_text.find(render_plan_marker) + len(render_plan_marker)
            render_plan_json_str = response_text[render_plan_start:].strip()
            
            # Clean JSON strings - enhanced for markdown format
            content_ir_json_str = clean_json_string(content_ir_json_str)
            render_plan_json_str = clean_json_string(render_plan_json_str)
            
            print(f"[JSON EXTRACTION] Content IR JSON length: {len(content_ir_json_str)}")
            print(f"[JSON EXTRACTION] Render Plan JSON length: {len(render_plan_json_str)}")
            
            # Debug: Show first 200 chars of each JSON
            print(f"[JSON EXTRACTION] Content IR preview: {content_ir_json_str[:200]}...")
            print(f"[JSON EXTRACTION] Render Plan preview: {render_plan_json_str[:200]}...")
            
            # Parse JSONs
            try:
                content_ir = json.loads(content_ir_json_str)
                print(f"[JSON EXTRACTION] ✅ Content IR parsed successfully")
                if 'entities' in content_ir and 'company' in content_ir['entities']:
                    company_name = content_ir['entities']['company'].get('name', 'Unknown')
                    print(f"[JSON EXTRACTION] Company name: {company_name}")
            except json.JSONDecodeError as e:
                print(f"[JSON EXTRACTION] ❌ Content IR parse failed: {e}")
                print(f"[JSON EXTRACTION] Problematic JSON: {content_ir_json_str[:500]}...")
            
            try:
                render_plan = json.loads(render_plan_json_str)
                print(f"[JSON EXTRACTION] ✅ Render Plan parsed successfully")
                slides_count = len(render_plan.get('slides', []))
                print(f"[JSON EXTRACTION] Slides count: {slides_count}")
            except json.JSONDecodeError as e:
                print(f"[JSON EXTRACTION] ❌ Render Plan parse failed: {e}")
                print(f"[JSON EXTRACTION] Problematic JSON: {render_plan_json_str[:500]}...")
                
        else:
            print(f"[JSON EXTRACTION] 🚨 PRIORITY 1: Missing required markers")
            print(f"Content IR marker found: {content_ir_marker}")
            print(f"Render Plan marker found: {render_plan_marker}")
            
            # Enhanced debugging - check for partial matches
            response_lower = response_text.lower()
            if "content ir" in response_lower:
                print("[JSON EXTRACTION] Found 'content ir' in response")
            if "render plan" in response_lower:
                print("[JSON EXTRACTION] Found 'render plan' in response")
            if "json" in response_lower:
                print("[JSON EXTRACTION] Found 'json' in response")
                
            # Show what markers were actually found in the response
            print(f"[JSON EXTRACTION] Response preview: {response_text[:500]}...")
            return None, None
    
    except Exception as e:
        print(f"[JSON EXTRACTION] Extraction failed: {e}")
    
    return content_ir, render_plan


def test_with_user_example():
    """Test with the user's exact response format they reported"""
    
    print("🧪 TESTING WITH USER'S EXACT JSON FORMAT")
    print("=" * 80)
    
    # User's exact format that should have been detected
    test_response = '''
Looking at Qi Card (International Smart Card), here's the comprehensive analysis:

**CONTENT IR JSON:**
{
  "entities": {
    "company": {
      "name": "Qi Card (International Smart Card)",
      "industry": "Financial Technology / Digital Payments",
      "founded": "2019",
      "headquarters": "Singapore",
      "website": "https://qicard.com"
    }
  },
  "facts": {
    "company_overview": "Leading fintech company specializing in smart card solutions and digital payment infrastructure across Southeast Asia",
    "revenue_usd_m": [15, 28, 45, 72, 95],
    "years": ["2020", "2021", "2022", "2023", "2024E"]
  }
}

**RENDER PLAN JSON:**
{
  "slides": [
    {
      "template": "management_team",
      "data": {
        "title": "Leadership Team",
        "team_members": [
          {
            "name": "John Chen",
            "title": "Chief Executive Officer",
            "background": "Former VP at Visa Asia Pacific"
          }
        ]
      }
    },
    {
      "template": "historical_financial_performance", 
      "data": {
        "title": "Financial Performance",
        "revenue_chart": {
          "categories": ["2020", "2021", "2022", "2023", "2024E"],
          "revenue": [15, 28, 45, 72, 95]
        }
      }
    }
  ]
}
'''
    
    # Test extraction
    content_ir, render_plan = extract_jsons_from_response(test_response)
    
    # Report results
    print("\n" + "=" * 80)
    print("🎯 TEST RESULTS:")
    print("=" * 80)
    
    if content_ir and render_plan:
        print("🎊 SUCCESS: Both JSONs extracted successfully!")
        print(f"✅ Company: {content_ir['entities']['company']['name']}")  
        print(f"✅ Slides: {len(render_plan['slides'])}")
        print("🚀 Auto-population should work with this format!")
        return True
    else:
        print("❌ FAILURE: JSON extraction failed")
        print(f"   Content IR: {'✅' if content_ir else '❌'}")
        print(f"   Render Plan: {'✅' if render_plan else '❌'}")
        print("🚨 This explains why auto-population isn't working!")
        return False


if __name__ == "__main__":
    success = test_with_user_example()
    
    if success:
        print("\n✅ JSON extraction is working correctly!")
        print("🔍 If auto-population still fails, the issue is elsewhere in the workflow")
    else:
        print("\n❌ JSON extraction is broken!")
        print("🔧 Need to fix the extraction patterns")