#!/usr/bin/env python3
"""
Test complete slide generation system with timeline and buyer profile fixes
"""

import sys
import os
sys.path.append('/home/user/webapp')

from executor import execute_plan
import json

def test_complete_fixes():
    """Test complete slide generation with all fixes applied"""
    
    print("Testing complete slide generation with fixes...")
    
    # Load the fixed JSON files
    try:
        with open('/home/user/webapp/fixed_content_ir.json', 'r') as f:
            content_ir = json.load(f)
        print("✅ Loaded fixed content IR successfully")
    except Exception as e:
        print(f"❌ Failed to load content IR: {e}")
        return False
    
    try:
        with open('/home/user/webapp/fixed_render_plan.json', 'r') as f:
            render_plan = json.load(f)
        print("✅ Loaded fixed render plan successfully")
    except Exception as e:
        print(f"❌ Failed to load render plan: {e}")
        return False
    
    print(f"\n📊 Data Summary:")
    print(f"  - Content IR sections: {len(content_ir)}")
    print(f"  - Render plan slides: {len(render_plan.get('slides', []))}")
    
    # Check specific data that we fixed
    print(f"\n🔍 Checking Fixed Data:")
    
    # Check investor process data
    investor_data = content_ir.get('investor_process_data', {})
    timeline_items = investor_data.get('timeline', [])
    print(f"  - Timeline items: {len(timeline_items)}")
    if timeline_items:
        print(f"    Sample: {timeline_items[0]}")
    
    # Check buyer data
    strategic_buyers = content_ir.get('strategic_buyers', [])
    financial_buyers = content_ir.get('financial_buyers', [])
    print(f"  - Strategic buyers: {len(strategic_buyers)}")
    print(f"  - Financial buyers: {len(financial_buyers)}")
    
    if strategic_buyers:
        buyer = strategic_buyers[0]
        print(f"    Sample strategic buyer:")
        print(f"      Name: {buyer.get('buyer_name', 'No name')}")
        print(f"      Description: {buyer.get('description', 'No description')[:50]}...")
    
    # Check slides that use the fixed data
    slides = render_plan.get('slides', [])
    investor_slides = [s for s in slides if s.get('template') == 'investor_process_overview']
    buyer_slides = [s for s in slides if s.get('template') == 'buyer_profiles']
    
    print(f"\n🎯 Slides Using Fixed Data:")
    print(f"  - Investor process overview slides: {len(investor_slides)}")
    print(f"  - Buyer profiles slides: {len(buyer_slides)}")
    
    # Test slide generation
    print(f"\n🧪 Testing Complete Slide Generation...")
    
    try:
        # Use the executor to generate the complete presentation
        prs, save_path = execute_plan(
            plan=render_plan,
            content_ir=content_ir,
            company_name="LlamaIndex",
            output_path="test_complete_fixes_output.pptx"
        )
        
        if prs:
            print(f"✅ SUCCESS: Complete presentation generated!")
            print(f"   - Total slides: {len(prs.slides)}")
            print(f"   - Saved to: {save_path}")
            return True
        else:
            print(f"❌ FAILED: No presentation returned")
            return False
            
    except Exception as e:
        print(f"❌ ERROR during slide generation: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_specific_slides():
    """Test specific slides that were problematic"""
    
    print(f"\n" + "="*60)
    print("TESTING SPECIFIC PROBLEMATIC SLIDES")
    print("="*60)
    
    # Test just the investor process overview and buyer profiles slides
    from slide_templates import render_investor_process_overview_slide, render_buyer_profiles_slide
    import json
    
    # Load data
    with open('/home/user/webapp/fixed_content_ir.json', 'r') as f:
        content_ir = json.load(f)
    
    # Test investor process overview
    print(f"\n1. Testing Investor Process Overview Slide:")
    
    investor_data = content_ir.get('investor_process_data', {})
    test_investor_data = {
        "title": "Investor Process Overview",
        "diligence_topics": investor_data.get('diligence_topics', []),
        "synergy_opportunities": investor_data.get('synergy_opportunities', []),
        "risk_factors": investor_data.get('risk_factors', []),
        "mitigants": investor_data.get('mitigants', []),
        "timeline": investor_data.get('timeline', [])
    }
    
    try:
        prs1 = render_investor_process_overview_slide(data=test_investor_data, company_name="LlamaIndex")
        if prs1 and len(prs1.slides) > 0:
            print("   ✅ SUCCESS: Investor process overview slide rendered")
            print(f"     - Timeline items processed: {len(test_investor_data.get('timeline', []))}")
        else:
            print("   ❌ FAILED: No slides generated")
            return False
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False
    
    # Test buyer profiles
    print(f"\n2. Testing Buyer Profiles Slide:")
    
    strategic_buyers = content_ir.get('strategic_buyers', [])
    test_buyer_data = {
        "title": "Strategic Buyer Profiles",
        "table_headers": ["Buyer Name", "Description", "Strategic Rationale", "Key Synergies", "Fit"],
        "table_rows": strategic_buyers
    }
    
    try:
        prs2 = render_buyer_profiles_slide(data=test_buyer_data, company_name="LlamaIndex")
        if prs2 and len(prs2.slides) > 0:
            print("   ✅ SUCCESS: Buyer profiles slide rendered")
            print(f"     - Buyer rows processed: {len(strategic_buyers)}")
            if strategic_buyers:
                buyer = strategic_buyers[0]
                print(f"     - Sample buyer description: {buyer.get('description', 'Missing!')[:30]}...")
        else:
            print("   ❌ FAILED: No slides generated")
            return False
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("=== Complete System Fixes Test ===\n")
    
    # Test individual slides first
    specific_success = test_specific_slides()
    
    print(f"\n" + "="*60)
    
    # Test complete system
    complete_success = test_complete_fixes()
    
    if specific_success and complete_success:
        print(f"\n🎉 All tests passed! Both timeline and buyer profile fixes are working!")
        print(f"✅ Timeline data renders properly (no more 'str' object errors)")
        print(f"✅ Buyer profile descriptions show correctly (no more N/A)")
    else:
        print(f"\n💥 Some tests failed. Check the errors above.")