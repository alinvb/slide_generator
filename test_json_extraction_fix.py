#!/usr/bin/env python3

import sys
sys.path.append('/home/user/webapp')

from app import extract_jsons_from_response, clean_json_string
import json

def test_json_extraction():
    print("🧪 Testing JSON Extraction Function Fixes")
    print("=" * 60)
    
    # Test 1: Basic working case
    print("\n1️⃣ TEST 1: Basic working case")
    basic_response = """
CONTENT IR JSON:
```json
{
  "entities": {
    "company": {
      "name": "Test Company"
    }
  },
  "management_team": {
    "profiles": [
      {
        "name": "John Doe",
        "title": "CEO"
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
      "title": "Test Presentation"
    }
  ]
}
```
"""
    
    content_ir, render_plan = extract_jsons_from_response(basic_response)
    print(f"✅ Content IR extracted: {content_ir is not None}")
    print(f"✅ Render Plan extracted: {render_plan is not None}")
    
    # Test 2: Case without proper markers (should fail gracefully)
    print("\n2️⃣ TEST 2: Case without markers")
    no_marker_response = """
Here's some regular text without JSON markers.
Just regular conversation content.
Nothing to extract here.
"""
    
    content_ir, render_plan = extract_jsons_from_response(no_marker_response)
    print(f"✅ Content IR extracted (should be None): {content_ir is None}")
    print(f"✅ Render Plan extracted (should be None): {render_plan is None}")
    
    # Test 3: Edge case with malformed JSON
    print("\n3️⃣ TEST 3: Malformed JSON")
    malformed_response = """
CONTENT IR JSON:
```json
{
  "entities": {
    "company": {
      "name": "Test Company"
    
  
}
```
"""
    
    content_ir, render_plan = extract_jsons_from_response(malformed_response)
    print(f"✅ Content IR extracted (should handle gracefully): {content_ir}")
    
    # Test 4: Test clean_json_string with 2-character input
    print("\n4️⃣ TEST 4: Short string handling")
    short_strings = ["{}", "{n", "  ", ""]
    
    for s in short_strings:
        result = clean_json_string(s)
        print(f"Input: {repr(s)} -> Output: {repr(result)}")
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    test_json_extraction()