#!/usr/bin/env python3
"""
Test slide data mapping for investor process overview and buyer profiles
"""

import sys
import os
sys.path.append('/home/user/webapp')

import json

def test_data_mapping():
    """Test how data is mapped to slides"""
    
    print("Testing slide data mapping...")
    
    # Load the fixed content IR
    try:
        with open('/home/user/webapp/fixed_content_ir.json', 'r') as f:
            content_ir = json.load(f)
        print("✅ Loaded content IR successfully")
    except Exception as e:
        print(f"❌ Failed to load content IR: {e}")
        return False
    
    # Load the fixed render plan
    try:
        with open('/home/user/webapp/fixed_render_plan.json', 'r') as f:
            render_plan = json.load(f)
        print("✅ Loaded render plan successfully")
    except Exception as e:
        print(f"❌ Failed to load render plan: {e}")
        return False
    
    print("\n" + "="*60)
    print("TESTING INVESTOR PROCESS OVERVIEW SLIDE DATA")
    print("="*60)
    
    # Check if investor_process_data exists in Content IR
    investor_data = content_ir.get('investor_process_data', {})
    print(f"📊 Investor process data found: {bool(investor_data)}")
    
    if investor_data:
        print(f"  - Diligence topics: {len(investor_data.get('diligence_topics', []))}")
        print(f"  - Synergy opportunities: {len(investor_data.get('synergy_opportunities', []))}")
        print(f"  - Risk factors: {len(investor_data.get('risk_factors', []))}")
        print(f"  - Mitigants: {len(investor_data.get('mitigants', []))}")
        print(f"  - Timeline: {len(investor_data.get('timeline', []))}")
        
        print("\n📋 Timeline data:")
        for i, item in enumerate(investor_data.get('timeline', [])):
            print(f"  {i+1}. {item}")
    
    # Check how this maps to the render plan
    investor_slides = [s for s in render_plan.get('slides', []) if s.get('template') == 'investor_process_overview']
    print(f"\n🎯 Investor process overview slides in render plan: {len(investor_slides)}")
    
    for i, slide in enumerate(investor_slides):
        print(f"\nSlide {i+1}:")
        print(f"  - Template: {slide.get('template')}")
        print(f"  - Title: {slide.get('data', {}).get('title', 'No title')}")
        print(f"  - Timeline items: {len(slide.get('data', {}).get('timeline', []))}")
        
        timeline_data = slide.get('data', {}).get('timeline', [])
        if timeline_data:
            print("  - Timeline content:")
            for j, item in enumerate(timeline_data):
                print(f"    {j+1}. {item}")
        else:
            print("  - ❌ Timeline is empty!")
    
    print("\n" + "="*60)
    print("TESTING BUYER PROFILES SLIDE DATA")
    print("="*60)
    
    # Check buyer data in Content IR
    strategic_buyers = content_ir.get('strategic_buyers', [])
    financial_buyers = content_ir.get('financial_buyers', [])
    
    print(f"📊 Strategic buyers found: {len(strategic_buyers)}")
    print(f"📊 Financial buyers found: {len(financial_buyers)}")
    
    if strategic_buyers:
        print(f"\n📋 First strategic buyer:")
        buyer = strategic_buyers[0]
        print(f"  - Name: {buyer.get('buyer_name', 'No name')}")
        print(f"  - Description: {buyer.get('description', 'No description')}")
        print(f"  - Rationale: {buyer.get('strategic_rationale', 'No rationale')}")
        print(f"  - Synergies: {buyer.get('key_synergies', 'No synergies')}")
        print(f"  - Fit: {buyer.get('fit', 'No fit')}")
    
    # Check how this maps to render plan
    buyer_slides = [s for s in render_plan.get('slides', []) if s.get('template') == 'buyer_profiles']
    print(f"\n🎯 Buyer profiles slides in render plan: {len(buyer_slides)}")
    
    for i, slide in enumerate(buyer_slides):
        print(f"\nBuyer slide {i+1}:")
        print(f"  - Template: {slide.get('template')}")
        print(f"  - Content IR key: {slide.get('content_ir_key', 'No content_ir_key')}")
        print(f"  - Title: {slide.get('data', {}).get('title', 'No title')}")
        
        table_rows = slide.get('data', {}).get('table_rows', [])
        print(f"  - Table rows: {len(table_rows)}")
        
        if table_rows and len(table_rows) > 0:
            print(f"  - First row sample:")
            row = table_rows[0]
            if isinstance(row, dict):
                print(f"    - Name: {row.get('buyer_name', row.get('name', 'No name'))}")
                print(f"    - Description: {row.get('description', 'No description')}")
            else:
                print(f"    - Row type: {type(row)}")
                print(f"    - Row data: {row}")
        else:
            print("  - ❌ Table rows is empty!")
    
    return True

if __name__ == "__main__":
    print("=== Slide Data Mapping Test ===\n")
    
    success = test_data_mapping()
    
    if success:
        print("\n🎉 Data mapping test completed!")
    else:
        print("\n💥 Data mapping test failed!")