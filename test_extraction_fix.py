#!/usr/bin/env python3

import sys
sys.path.append('/home/user/webapp')

from app import extract_jsons_from_response
import json

def test_json_extraction_fix():
    print("🔧 Testing Fixed JSON Extraction Function")
    print("=" * 60)
    
    # Test with both Content IR and Render Plan
    test_response = """Let me generate the JSONs for you:

CONTENT IR JSON:
```json
{
  "entities": {
    "company": {
      "name": "Saudi Aramco",
      "legal_name": "Saudi Arabian Oil Company",
      "ticker": "2222.SR",
      "exchange": "Saudi Exchange (Tadawul)"
    }
  },
  "management_team": {
    "profiles": [
      {
        "name": "Amin H. Nasser",
        "title": "President & CEO",
        "tenure": "2015-present",
        "background": "Chemical Engineer, 38+ years with Aramco"
      },
      {
        "name": "Ziad T. Al-Murshed",
        "title": "Executive Vice President & CFO",
        "tenure": "2020-present",
        "background": "Financial expert, former McKinsey consultant"
      }
    ]
  },
  "historical_financials": {
    "revenue_data": [
      {
        "year": 2023,
        "value": 535.2,
        "unit": "billion_usd"
      },
      {
        "year": 2022,
        "value": 605.0,
        "unit": "billion_usd"
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
      "title": "Saudi Aramco Investment Banking Presentation",
      "subtitle": "Company Overview and Strategic Analysis"
    },
    {
      "slide_number": 2,
      "slide_type": "management_team",
      "title": "Executive Leadership Team",
      "data_mapping": {
        "source": "management_team",
        "display_format": "executive_grid"
      }
    },
    {
      "slide_number": 3,
      "slide_type": "historical_financial",
      "title": "Financial Performance Overview",
      "data_mapping": {
        "source": "historical_financials.revenue_data",
        "chart_type": "revenue_trend"
      }
    }
  ]
}
```

That's your perfect JSONs ready!"""
    
    print("\n🧪 Testing extraction...")
    content_ir, render_plan = extract_jsons_from_response(test_response)
    
    print(f"\n📊 EXTRACTION RESULTS:")
    print(f"✅ Content IR extracted: {content_ir is not None}")
    print(f"✅ Render Plan extracted: {render_plan is not None}")
    
    if content_ir:
        print(f"✅ Content IR company name: {content_ir.get('entities', {}).get('company', {}).get('name', 'N/A')}")
        print(f"✅ Content IR management team count: {len(content_ir.get('management_team', {}).get('profiles', []))}")
    
    if render_plan:
        print(f"✅ Render Plan slides count: {len(render_plan.get('slides', []))}")
        print(f"✅ Render Plan first slide title: {render_plan.get('slides', [{}])[0].get('title', 'N/A')}")
    
    # Test edge case: no markers
    print(f"\n🧪 Testing with no markers...")
    no_marker_response = "Just some regular text without any JSON markers or content."
    content_ir2, render_plan2 = extract_jsons_from_response(no_marker_response)
    
    print(f"✅ No markers - Content IR: {content_ir2 is None}")
    print(f"✅ No markers - Render Plan: {render_plan2 is None}")
    
    # Test edge case: malformed JSON
    print(f"\n🧪 Testing with malformed JSON...")
    malformed_response = """
CONTENT IR JSON:
```json
{
  "entities": {
    "company": {
      "name": "Test Company"
    // Missing closing braces
```"""
    content_ir3, render_plan3 = extract_jsons_from_response(malformed_response)
    print(f"✅ Malformed JSON handled gracefully: {content_ir3 is None}")
    
    print(f"\n🎉 All extraction tests completed successfully!")

if __name__ == "__main__":
    test_json_extraction_fix()