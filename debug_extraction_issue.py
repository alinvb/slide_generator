#!/usr/bin/env python3

import sys
sys.path.append('/home/user/webapp')

from app import extract_jsons_from_response
import json

def test_current_extraction_issue():
    print("🚨 DEBUGGING THE CURRENT JSON EXTRACTION ISSUE")
    print("=" * 60)
    
    # This is the type of response that's currently failing based on the logs
    test_response = """All 14 required interview topics are now complete. Ready to generate the JSON files with the latest research-backed content.

CONTENT IR JSON:
```json
{
  "entities": {
    "company": {
      "name": "Saudi Aramco",
      "legal_name": "Saudi Arabian Oil Company"
    }
  },
  "management_team": {
    "left_column_profiles": [
      {
        "name": "Amin H. Nasser",
        "title": "President & CEO"
      }
    ],
    "right_column_profiles": [
      {
        "name": "Ziad T. Al-Murshed", 
        "title": "Executive Vice President & CFO"
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
```

Ready to proceed with pitch deck generation!"""
    
    print(f"📏 Test response length: {len(test_response)}")
    print(f"📝 Contains 'CONTENT IR JSON:': {'CONTENT IR JSON:' in test_response}")
    print(f"📝 Contains 'RENDER PLAN JSON:': {'RENDER PLAN JSON:' in test_response}")
    print(f"📝 Contains opening braces: {'{' in test_response}")
    
    print(f"\n🧪 Running extraction...")
    content_ir, render_plan = extract_jsons_from_response(test_response)
    
    print(f"\n📊 RESULTS:")
    print(f"✅ Content IR extracted: {content_ir is not None}")
    print(f"✅ Render Plan extracted: {render_plan is not None}")
    
    if content_ir:
        print(f"✅ Content IR company name: {content_ir.get('entities', {}).get('company', {}).get('name', 'N/A')}")
    
    if render_plan:
        print(f"✅ Render Plan slides: {len(render_plan.get('slides', []))}")
    
    print(f"\n🔍 Manual marker search...")
    content_ir_pos = test_response.find("CONTENT IR JSON:")
    render_plan_pos = test_response.find("RENDER PLAN JSON:")
    first_brace_pos = test_response.find("{")
    
    print(f"📍 'CONTENT IR JSON:' found at position: {content_ir_pos}")
    print(f"📍 'RENDER PLAN JSON:' found at position: {render_plan_pos}")
    print(f"📍 First opening brace found at position: {first_brace_pos}")
    
    if content_ir_pos != -1:
        # Manual extraction test
        start_search = content_ir_pos + len("CONTENT IR JSON:")
        json_start = test_response.find("{", start_search)
        print(f"📍 First brace after Content IR marker: {json_start}")
        
        if json_start != -1:
            # Count braces manually
            brace_count = 0
            json_end = json_start
            
            for i in range(json_start, len(test_response)):
                char = test_response[i]
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        json_end = i + 1
                        break
            
            print(f"📍 Manual extraction range: {json_start} to {json_end}")
            print(f"📏 Manual extraction length: {json_end - json_start}")
            
            if json_end > json_start:
                manual_json = test_response[json_start:json_end]
                print(f"📝 Manually extracted length: {len(manual_json)}")
                print(f"📝 First 100 chars: {manual_json[:100]}")
                
                try:
                    parsed = json.loads(manual_json)
                    print(f"✅ Manual extraction JSON is valid!")
                except Exception as e:
                    print(f"❌ Manual extraction JSON invalid: {e}")

if __name__ == "__main__":
    test_current_extraction_issue()