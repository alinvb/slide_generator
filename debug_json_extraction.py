#!/usr/bin/env python3

import json
import re

def clean_json_string(json_str):
    """Clean JSON string for parsing"""
    print(f"[JSON CLEAN] Input length: {len(json_str)}")
    
    if not json_str or not json_str.strip():
        return "{}"
    
    json_str = json_str.strip()
    
    # Quick validation check - if it can parse, return as-is
    try:
        json.loads(json_str)
        print(f"[JSON CLEAN] JSON is valid as-is")
        return json_str
    except:
        pass
    
    # Remove markdown formatting
    json_str = re.sub(r'^```json\s*', '', json_str, flags=re.MULTILINE)
    json_str = re.sub(r'\s*```$', '', json_str, flags=re.MULTILINE)
    
    # Remove any text before the first { and after the last }
    start_brace = json_str.find('{')
    end_brace = json_str.rfind('}')
    
    if start_brace != -1 and end_brace != -1 and start_brace < end_brace:
        json_str = json_str[start_brace:end_brace+1]
    
    return json_str

def debug_extract_jsons_from_response(response_text):
    """Debug version of JSON extraction function"""
    content_ir = None
    render_plan = None
    
    print(f"[DEBUG] Starting extraction from response of length: {len(response_text)}")
    
    # Method 1: Look for specific JSON markers in the response
    content_ir_markers = [
        "CONTENT IR JSON:",
        "Content IR:",
        "content_ir",
        "## CONTENT IR JSON:",
        "**CONTENT IR JSON:**"
    ]
    
    render_plan_markers = [
        "RENDER PLAN JSON:",
        "Render Plan:",
        "render_plan", 
        "## RENDER PLAN JSON:",
        "**RENDER PLAN JSON:**"
    ]
    
    # Find Content IR section
    content_ir_start = None
    
    for marker in content_ir_markers:
        pos = response_text.find(marker)
        if pos != -1:
            content_ir_start = pos + len(marker)
            print(f"[DEBUG] Found Content IR marker: '{marker}' at position {pos}")
            print(f"[DEBUG] Content after marker: {repr(response_text[pos:pos+100])}")
            break
    
    # Find Render Plan section
    render_plan_start = None
    
    for marker in render_plan_markers:
        pos = response_text.find(marker)
        if pos != -1:
            render_plan_start = pos + len(marker)
            print(f"[DEBUG] Found Render Plan marker: '{marker}' at position {pos}")
            print(f"[DEBUG] Content after marker: {repr(response_text[pos:pos+100])}")
            break
    
    # Extract Content IR JSON
    if content_ir_start is not None:
        print(f"[DEBUG] Looking for JSON starting from position {content_ir_start}")
        # Find the start of the JSON (first { after marker)
        json_start = response_text.find('{', content_ir_start)
        print(f"[DEBUG] Found opening brace at position {json_start}")
        
        if json_start != -1:
            # Find the matching closing brace
            brace_count = 0
            content_ir_end = json_start
            
            for i in range(json_start, len(response_text)):
                if response_text[i] == '{':
                    brace_count += 1
                elif response_text[i] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        content_ir_end = i + 1
                        break
            
            print(f"[DEBUG] JSON extraction range: {json_start} to {content_ir_end}")
            
            if content_ir_end > json_start:
                content_ir_json = response_text[json_start:content_ir_end]
                print(f"[DEBUG] Extracted Content IR JSON (first 200 chars): {repr(content_ir_json[:200])}")
                print(f"[DEBUG] Extracted Content IR JSON (last 200 chars): {repr(content_ir_json[-200:])}")
                
                try:
                    cleaned_json = clean_json_string(content_ir_json)
                    print(f"[DEBUG] Cleaned JSON length: {len(cleaned_json)}")
                    content_ir = json.loads(cleaned_json)
                    print(f"✅ Successfully parsed Content IR JSON")
                except json.JSONDecodeError as e:
                    print(f"❌ Failed to parse Content IR JSON: {e}")
                    print(f"[DEBUG] Problematic JSON (first 500 chars): {repr(cleaned_json[:500])}")
                except Exception as e:
                    print(f"❌ Unexpected error: {e}")
    
    return content_ir, render_plan

# Test with a sample response
test_response = """CONTENT IR JSON:
```json
{
  "entities": {
    "company": {
      "name": "Saudi Aramco"
    }
  },
  "management_team": {
    "profiles": [
      {
        "name": "Amin H. Nasser",
        "title": "President & CEO",
        "tenure": "2015-present",
        "background": "Chemical Engineer, 38+ years with Aramco"
      }
    ]
  }
}
```

RENDER PLAN JSON:
```json
{
  "slides": [
    {
      "slide_number": 1,
      "slide_type": "title",
      "title": "Saudi Aramco Investment Banking Presentation"
    }
  ]
}
```"""

if __name__ == "__main__":
    print("Testing JSON extraction...")
    content_ir, render_plan = debug_extract_jsons_from_response(test_response)
    print(f"\nResult - Content IR extracted: {content_ir is not None}")
    print(f"Result - Render Plan extracted: {render_plan is not None}")