#!/usr/bin/env python3
"""
Debug investor process overview slide data processing
"""

import sys
import os
sys.path.append('/home/user/webapp')

from slide_templates import render_investor_process_overview_slide
import json

def test_investor_process_debug():
    """Debug investor process overview data processing"""
    
    print("Testing investor process overview data processing...")
    
    # Load the fixed content IR to get the investor data
    try:
        with open('/home/user/webapp/fixed_content_ir.json', 'r') as f:
            content_ir = json.load(f)
        print("✅ Loaded content IR successfully")
    except Exception as e:
        print(f"❌ Failed to load content IR: {e}")
        return False
    
    # Get the investor process data
    investor_data = content_ir.get('investor_process_data', {})
    
    print(f"\n📊 Investor process data found: {bool(investor_data)}")
    
    if investor_data:
        print(f"\n🔍 Investor process data structure:")
        for key, value in investor_data.items():
            if isinstance(value, list):
                print(f"  - {key}: {len(value)} items")
                if value:  # Show first item as sample
                    print(f"    Sample: {value[0]}")
            else:
                print(f"  - {key}: {value}")
    
    # Test data structure that should be passed to the slide
    test_slide_data = {
        "title": "Investor Process Overview",
        "diligence_topics": investor_data.get('diligence_topics', []),
        "synergy_opportunities": investor_data.get('synergy_opportunities', []),
        "risk_factors": investor_data.get('risk_factors', []),
        "mitigants": investor_data.get('mitigants', []),
        "timeline": investor_data.get('timeline', [])
    }
    
    print(f"\n📋 Test slide data structure:")
    for key, value in test_slide_data.items():
        if isinstance(value, list):
            print(f"  - {key}: {len(value)} items")
        else:
            print(f"  - {key}: {value}")
    
    print(f"\n🔍 Timeline detailed check:")
    timeline_data = test_slide_data.get('timeline', [])
    print(f"  - Timeline type: {type(timeline_data)}")
    print(f"  - Timeline length: {len(timeline_data)}")
    
    if timeline_data:
        print(f"  - Timeline items:")
        for i, item in enumerate(timeline_data):
            print(f"    {i+1}. {item}")
    else:
        print(f"  - ❌ Timeline is empty!")
    
    print(f"\n🧪 Testing slide generation...")
    
    try:
        prs = render_investor_process_overview_slide(data=test_slide_data, company_name="Test Company")
        if prs and len(prs.slides) > 0:
            print("✅ SUCCESS: Investor process overview slide created successfully")
            prs.save('/home/user/webapp/test_investor_debug_output.pptx')
            print("📊 Saved test file: test_investor_debug_output.pptx")
            return True
        else:
            print("❌ FAILED: No slides generated")
            return False
    except Exception as e:
        print(f"❌ ERROR during slide generation: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== Investor Process Overview Debug Test ===\n")
    
    success = test_investor_process_debug()
    
    if success:
        print("\n🎉 Investor process overview debug test completed!")
    else:
        print("\n💥 Investor process overview debug test failed!")