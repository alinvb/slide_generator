#!/usr/bin/env python3
"""
Debug buyer profiles slide data processing
"""

import sys
import os
sys.path.append('/home/user/webapp')

from slide_templates import render_buyer_profiles_slide
import json

def test_buyer_profiles_debug():
    """Debug buyer profiles data processing"""
    
    print("Testing buyer profiles data processing...")
    
    # Load the fixed content IR to get the buyer data
    try:
        with open('/home/user/webapp/fixed_content_ir.json', 'r') as f:
            content_ir = json.load(f)
        print("✅ Loaded content IR successfully")
    except Exception as e:
        print(f"❌ Failed to load content IR: {e}")
        return False
    
    # Get the strategic buyers
    strategic_buyers = content_ir.get('strategic_buyers', [])
    
    print(f"\n📊 Found {len(strategic_buyers)} strategic buyers")
    
    if strategic_buyers:
        print(f"\n🔍 First strategic buyer raw data:")
        first_buyer = strategic_buyers[0]
        for key, value in first_buyer.items():
            print(f"  - {key}: {value}")
    
    # Test data structure that should be passed to the slide
    test_slide_data = {
        "title": "Financial Buyer Profiles",
        "table_headers": ["Buyer Name", "Description", "Strategic Rationale", "Key Synergies", "Fit"],
        "table_rows": strategic_buyers  # Pass the actual buyer data
    }
    
    print(f"\n📋 Test slide data structure:")
    print(f"  - Title: {test_slide_data['title']}")
    print(f"  - Headers: {test_slide_data['table_headers']}")
    print(f"  - Rows: {len(test_slide_data['table_rows'])}")
    
    print(f"\n🔍 First row detailed check:")
    if test_slide_data['table_rows']:
        row = test_slide_data['table_rows'][0]
        print(f"  - Row type: {type(row)}")
        print(f"  - Is dict: {isinstance(row, dict)}")
        
        if isinstance(row, dict):
            # Test the extraction logic from the slide renderer
            cell_data = [
                row.get('buyer_name', row.get('name', '')),
                row.get('description', ''),
                row.get('strategic_rationale', row.get('rationale', '')),
                row.get('key_synergies', row.get('synergies', '')),
                row.get('fit', row.get('concerns', ''))
            ]
            
            print(f"  - Extracted cell data:")
            for i, cell in enumerate(cell_data):
                header = test_slide_data['table_headers'][i] if i < len(test_slide_data['table_headers']) else f"Col {i+1}"
                print(f"    {header}: '{cell}' (type: {type(cell).__name__})")
    
    print(f"\n🧪 Testing slide generation...")
    
    try:
        prs = render_buyer_profiles_slide(data=test_slide_data, company_name="Test Company")
        if prs and len(prs.slides) > 0:
            print("✅ SUCCESS: Buyer profiles slide created successfully")
            prs.save('/home/user/webapp/test_buyer_debug_output.pptx')
            print("📊 Saved test file: test_buyer_debug_output.pptx")
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
    print("=== Buyer Profiles Debug Test ===\n")
    
    success = test_buyer_profiles_debug()
    
    if success:
        print("\n🎉 Buyer profiles debug test completed!")
    else:
        print("\n💥 Buyer profiles debug test failed!")