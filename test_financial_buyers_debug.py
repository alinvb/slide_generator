#!/usr/bin/env python3
"""
Debug script specifically for financial buyers rationale issue
"""

import json
from pptx import Presentation
from slide_templates import render_buyer_profiles_slide

def test_financial_buyers():
    """Test financial buyers rationale mapping specifically"""
    
    # Load fixed content IR data
    with open('fixed_content_ir.json', 'r') as f:
        content_ir = json.load(f)
    
    # Extract financial buyers specifically
    financial_buyers = content_ir.get('financial_buyers', [])
    
    print(f"\n💰 Financial Buyers Debug:")
    print(f"Count: {len(financial_buyers)}")
    
    if financial_buyers:
        print(f"\n🔍 First financial buyer detailed analysis:")
        first_buyer = financial_buyers[0]
        
        for key, value in first_buyer.items():
            print(f"  {key}: '{value}'")
        
        # Check the specific field mapping
        strategic_rationale = first_buyer.get('strategic_rationale', 'MISSING')
        print(f"\n✅ strategic_rationale field: '{strategic_rationale}'")
        
        if not strategic_rationale or strategic_rationale == 'MISSING':
            print("❌ strategic_rationale is missing or empty!")
        else:
            print("✅ strategic_rationale has content")
    
    # Test slide generation with financial buyers
    slide_data = {
        'title': 'Financial Buyer Profiles',
        'table_headers': ['Buyer Name', 'Description', 'Investment Rationale', 'Key Synergies', 'Fit'],
        'table_rows': financial_buyers
    }
    
    print(f"\n🎯 Testing financial buyers slide generation...")
    
    try:
        prs = render_buyer_profiles_slide(data=slide_data)
        prs.save('test_financial_buyers_debug.pptx')
        
        # Check the slide content
        slide = prs.slides[0]
        for shape in slide.shapes:
            if hasattr(shape, 'table'):
                table = shape.table
                if len(table.rows) > 1 and len(table.columns) >= 3:
                    # Check rationale column (index 2)
                    rationale_cell = table.rows[1].cells[2]
                    cell_text = rationale_cell.text.strip()
                    print(f"📋 Rationale cell content: '{cell_text}'")
                    
                    if not cell_text or cell_text == 'N/A' or cell_text == '':
                        print("❌ PROBLEM: Rationale cell is empty!")
                        
                        # Debug the template mapping
                        print(f"\n🔍 Template mapping debug:")
                        print(f"Input data: {first_buyer.get('strategic_rationale', 'NOT FOUND')}")
                        
                        # Test direct mapping
                        mapped_values = [
                            first_buyer.get('buyer_name', first_buyer.get('name', '')),
                            first_buyer.get('description', ''),
                            first_buyer.get('strategic_rationale', first_buyer.get('rationale', '')),
                            first_buyer.get('key_synergies', first_buyer.get('synergies', '')),
                            first_buyer.get('fit', first_buyer.get('concerns', ''))
                        ]
                        print(f"Mapped values: {mapped_values}")
                        
                    else:
                        print("✅ Rationale cell has proper content!")
                        
        print(f"✅ Financial buyers slide saved: test_financial_buyers_debug.pptx")
        
    except Exception as e:
        print(f"❌ Financial buyers slide generation failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_financial_buyers()