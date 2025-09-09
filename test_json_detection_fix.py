#!/usr/bin/env python3
"""
Test JSON Detection Fix with User's Exact Response
Tests the enhanced JSON detection and extraction logic
"""

import sys
import os
sys.path.append('/home/user/webapp')

from app import extract_jsons_from_response

def test_json_detection_with_user_response():
    """Test with the exact response format that the user provided"""
    
    print("🧪 Testing JSON Detection Fix with User's Response")
    print("=" * 60)
    
    # User's exact response format (truncated for testing)
    user_response = """🚀 Adaptive JSON Generation Triggered

📊 Generated 10 slides based on conversation analysis: • Included: business_overview, management_team, historical_financial_performance, product_service_footprint, growth_strategy_projections, valuation_overview, precedent_transactions, margin_cost_resilience, sea_conglomerates, financial_buyers • Quality: {'high_quality_slides': 7, 'medium_quality_slides': 2, 'estimated_slides': 1, 'substantial_content_slides': 6}

CONTENT IR JSON:

{
  "entities": {
    "company": {
      "name": "Qi Card (International Smart Card)"
    }
  },
  "business_overview_data": {
    "description": "Qi Card (International Smart Card) is Iraq's leading electronic payments and digital banking platform, serving over 12 million Iraqis through a nationwide network. Founded in 2007 by Iraq's largest state banks, Qi Card pioneered offline smart card technology and rapidly scaled to provide salary disbursements, personal loans, biometric security, and digital wallets.",
    "timeline": [
      "2007: Qi Card launched as Iraq's first biometric smart card.",
      "2008–2015: Scaled to over 1.6 million users; expanded merchant network to 30,000."
    ],
    "highlights": [
      "Serves more than 12 million Iraqis, including public and private sector employees.",
      "Operates a network of 70,000+ POS terminals and 6,000 merchants."
    ],
    "services": [
      "Salary disbursement",
      "Personal loans",
      "Digital banking and wallet"
    ],
    "positioning_desc": "Qi Card is positioned as the foundational digital payments infrastructure in Iraq."
  }
}

RENDER PLAN JSON:

{
  "slides": [
    {
      "template": "business_overview",
      "data": {
        "title": "Business Overview"
      }
    },
    {
      "template": "management_team", 
      "data": {
        "title": "Management Team"
      }
    }
  ]
}"""

    print("\n📝 TEST CASE 1: Detection Logic")
    
    # Test detection logic
    ai_response_lower = user_response.lower()
    
    # Enhanced JSON keyword detection - supports multiple formats
    has_content_ir_markers = any(marker in ai_response_lower for marker in [
        "content ir json:", "content_ir json:", "content ir:", "content_ir:"
    ])
    has_render_plan_markers = any(marker in ai_response_lower for marker in [
        "render plan json:", "render_plan json:", "render plan:", "render_plan:"
    ])
    has_json_structure = "entities" in ai_response_lower and "slides" in ai_response_lower
    has_substantial_json = "{" in user_response and "}" in user_response and len(user_response) > 1000
    
    # Enhanced completion signals
    completion_signals = [
        "adaptive json generation triggered",  # This should match!
        "generated 10 slides based on",       # This should match!  
        "content ir json:",                   # This should match!
        "render plan json:"                   # This should match!
    ]
    has_completion_signal = any(signal in ai_response_lower for signal in completion_signals)
    
    print(f"✅ Content IR markers: {has_content_ir_markers}")
    print(f"✅ Render Plan markers: {has_render_plan_markers}")
    print(f"✅ JSON structure: {has_json_structure}")
    print(f"✅ Substantial JSON: {has_substantial_json}")
    print(f"✅ Completion signal: {has_completion_signal}")
    
    # Final detection
    has_complete_json_keywords = (has_content_ir_markers and has_render_plan_markers and has_json_structure)
    should_extract = (has_complete_json_keywords and has_substantial_json) or has_completion_signal or (has_content_ir_markers and has_render_plan_markers)
    
    print(f"✅ Should extract JSON: {should_extract}")
    
    print("\n📝 TEST CASE 2: JSON Extraction")
    
    # Test extraction
    if should_extract:
        try:
            content_ir, render_plan = extract_jsons_from_response(user_response)
            
            print(f"✅ Content IR extracted: {content_ir is not None}")
            if content_ir:
                print(f"   Company name: {content_ir.get('entities', {}).get('company', {}).get('name', 'Not found')}")
                print(f"   Sections: {list(content_ir.keys())}")
            
            print(f"✅ Render Plan extracted: {render_plan is not None}")
            if render_plan:
                print(f"   Slides count: {len(render_plan.get('slides', []))}")
                slide_types = [slide.get('template', 'unknown') for slide in render_plan.get('slides', [])]
                print(f"   Slide types: {slide_types}")
                
        except Exception as e:
            print(f"❌ Extraction failed: {str(e)}")
    else:
        print("❌ Detection failed - would not extract")
    
    print("\n📝 TEST CASE 3: Completion Signals Validation")
    
    # Check each completion signal
    for signal in completion_signals:
        found = signal in ai_response_lower
        print(f"   '{signal}': {'✅ FOUND' if found else '❌ NOT FOUND'}")
    
    print(f"\n🎯 SUMMARY:")
    print(f"Detection working: {'✅ YES' if should_extract else '❌ NO'}")
    print(f"Extraction working: {'✅ YES' if should_extract and content_ir and render_plan else '❌ NO'}")
    
    if should_extract and content_ir and render_plan:
        print("🎊 SUCCESS: JSON detection and extraction fix is working!")
        return True
    else:
        print("🚨 FAILURE: JSON detection and extraction needs more fixes")
        return False

if __name__ == "__main__":
    success = test_json_detection_with_user_response()
    exit(0 if success else 1)