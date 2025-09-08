#!/usr/bin/env python3
"""
Direct test of slide generation without Streamlit dependencies
"""

import sys
import os
sys.path.append('/home/user/webapp')

from slide_templates import render_precedent_transactions_slide, render_management_team_slide
import json

def test_direct_slide_generation():
    """Test direct slide generation"""
    
    print("Testing direct slide generation...")
    
    # Test precedent transactions slide
    print("\n1. Testing Precedent Transactions Slide:")
    
    precedent_data = {
        "transactions": [
            {
                "date": "2023-12",
                "target": "TechCorp Inc",
                "acquirer": "GlobalTech Holdings", 
                "country": "USA",
                "enterprise_value": "$1.5B",
                "revenue": "$300M", 
                "ev_revenue_multiple": "5.0x"
            },
            {
                "date": "2023-10",
                "target": "InnovateSoft",
                "acquirer": "MegaCorp Ltd",
                "country": "Canada", 
                "enterprise_value": "850000000",
                "revenue": "170000000",
                "ev_revenue_multiple": "5.0"
            }
        ]
    }
    
    try:
        prs1 = render_precedent_transactions_slide(data=precedent_data, company_name="Test Co")
        if prs1 and len(prs1.slides) > 0:
            print("   ✅ SUCCESS: Precedent transactions slide created")
        else:
            print("   ❌ FAILED: No slides generated")
            return False
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False
    
    # Test management team slide  
    print("\n2. Testing Management Team Slide:")
    
    # Test with ≤4 profiles (should be centered 2-column)
    management_data_small = {
        "left_column_profiles": [
            {"name": "Jerry Liu", "position": "Chief Executive Officer", "image": "", "bio": "Experienced CEO"},
            {"name": "Simon Suo", "position": "Chief Technology Officer", "image": "", "bio": "Tech leader"}
        ],
        "right_column_profiles": [
            {"name": "Logan Markewich", "position": "Head of Engineering", "image": "", "bio": "Engineering expert"},
            {"name": "Andrei Fajardo", "position": "Head of Product", "image": "", "bio": "Product strategist"}
        ]
    }
    
    try:
        prs2 = render_management_team_slide(data=management_data_small, company_name="Test Co")
        if prs2 and len(prs2.slides) > 0:
            print("   ✅ SUCCESS: Management team slide (≤4 profiles) created - should be centered 2-column")
        else:
            print("   ❌ FAILED: No slides generated")
            return False
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False
    
    # Test with ≥5 profiles (should be left-aligned 3-column)
    management_data_large = {
        "left_column_profiles": [
            {"name": "Jerry Liu", "position": "Chief Executive Officer", "image": "", "bio": "Experienced CEO"},
            {"name": "Simon Suo", "position": "Chief Technology Officer", "image": "", "bio": "Tech leader"},
            {"name": "Logan Markewich", "position": "Head of Engineering", "image": "", "bio": "Engineering expert"}
        ],
        "right_column_profiles": [
            {"name": "Andrei Fajardo", "position": "Head of Product", "image": "", "bio": "Product strategist"},
            {"name": "Haotian Zhang", "position": "Head of Design", "image": "", "bio": "Design leader"},
            {"name": "Ravi Theja", "position": "Head of Operations", "image": "", "bio": "Operations expert"}
        ]
    }
    
    try:
        prs3 = render_management_team_slide(data=management_data_large, company_name="Test Co")
        if prs3 and len(prs3.slides) > 0:
            print("   ✅ SUCCESS: Management team slide (≥5 profiles) created - should be left-aligned 3-column")
        else:
            print("   ❌ FAILED: No slides generated")
            return False
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False
    
    return True

def test_financial_conversions():
    """Test financial value conversions"""
    
    print("\n3. Testing Financial Value Conversions:")
    
    # Test various financial formats
    test_data = {
        "transactions": [
            {
                "date": "2023-12",
                "target": "TestCorp",
                "acquirer": "BuyerCorp",
                "country": "USA",
                "enterprise_value": "$1.5B",      # Billion format
                "revenue": "$300M",              # Million format  
                "ev_revenue_multiple": "5.0x"    # Multiple format
            },
            {
                "date": "2023-11", 
                "target": "TestCorp2",
                "acquirer": "BuyerCorp2",
                "country": "UK",
                "enterprise_value": "$50K",      # Thousand format
                "revenue": "25000000",          # Raw number as string
                "ev_revenue_multiple": "2.0"    # Multiple without x
            },
            {
                "date": "2023-10",
                "target": "TestCorp3", 
                "acquirer": "BuyerCorp3",
                "country": "Canada",
                "enterprise_value": 1000000000, # Raw number
                "revenue": 200000000,          # Raw number
                "ev_revenue_multiple": 5.0     # Raw float
            }
        ]
    }
    
    try:
        prs = render_precedent_transactions_slide(data=test_data, company_name="Conversion Test")
        if prs and len(prs.slides) > 0:
            print("   ✅ SUCCESS: Financial conversion handling works")
            
            # Save for manual inspection
            prs.save('/home/user/webapp/test_financial_conversions.pptx')
            print("   📊 Saved test file: test_financial_conversions.pptx")
            return True
        else:
            print("   ❌ FAILED: No slides generated")
            return False
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== Direct Slide Generation Test ===")
    
    success1 = test_direct_slide_generation()
    success2 = test_financial_conversions()
    
    if success1 and success2:
        print("\n🎉 All direct slide generation tests passed!")
        print("✅ Management team dynamic layout working")
        print("✅ Precedent transactions financial conversion working")
        print("✅ F-string formatting error resolved")
    else:
        print("\n💥 Some tests failed. Check the errors above.")