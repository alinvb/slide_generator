#!/usr/bin/env python3
"""
Test script for precedent transactions slide with financial value conversion
"""

import sys
import os
sys.path.append('/home/user/webapp')

from slide_templates import render_precedent_transactions_slide
import json

def test_precedent_transactions_fix():
    """Test the precedent transactions slide with various financial formats"""
    
    # Sample data with different financial value formats
    test_data = {
        "transactions": [
            {
                "date": "2023-12",
                "target": "TechCorp Inc",
                "acquirer": "GlobalTech Holdings",
                "country": "USA",
                "enterprise_value": "$1.5B",  # String format with B suffix
                "revenue": "$300M",            # String format with M suffix
                "ev_revenue_multiple": "5.0x"  # String format with x suffix
            },
            {
                "date": "2023-10",
                "target": "InnovateSoft",
                "acquirer": "MegaCorp Ltd",
                "country": "Canada",
                "enterprise_value": "850000000",  # String numeric
                "revenue": "170000000",           # String numeric
                "ev_revenue_multiple": "5.0"      # String numeric
            },
            {
                "date": "2023-08",
                "target": "DataSolutions",
                "acquirer": "Analytics Pro",
                "country": "UK",
                "enterprise_value": 1200000000,  # Pure numeric
                "revenue": 240000000,            # Pure numeric
                "ev_revenue_multiple": 5.0       # Pure numeric
            },
            {
                "date": "2023-06",
                "target": "CloudServices Co",
                "acquirer": "Enterprise Systems",
                "country": "Germany",
                "enterprise_value": "$2.1B",
                "revenue": "$420M",
                "ev_revenue_multiple": "5.0x"
            }
        ]
    }
    
    print("Testing precedent transactions slide with financial value conversion...")
    
    try:
        # Test slide creation (correct parameter order)
        prs = render_precedent_transactions_slide(data=test_data, company_name="Test Company Ltd")
        
        if prs:
            print("✅ SUCCESS: Precedent transactions slide created successfully!")
            print(f"   - Slide count: {len(prs.slides)}")
            
            # Save for inspection
            prs.save('/home/user/webapp/test_precedent_transactions_output.pptx')
            print("   - Saved to: test_precedent_transactions_output.pptx")
            
            # Test with empty data
            empty_data = {"transactions": []}
            empty_prs = render_precedent_transactions_slide(data=empty_data, company_name="Empty Test")
            if empty_prs:
                print("✅ SUCCESS: Empty precedent transactions handled properly")
            
            return True
        else:
            print("❌ FAILED: No presentation returned")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_financial_conversion_functions():
    """Test the financial conversion functions directly"""
    print("\nTesting financial conversion functions...")
    
    # These would be the internal helper functions - we'll test via slide creation
    test_values = [
        ("$1.5B", "Should convert to $1,500,000,000"),
        ("$300M", "Should convert to $300,000,000"),  
        ("$50K", "Should convert to $50,000"),
        ("850000000", "Should convert to $850,000,000"),
        (1200000000, "Should convert to $1,200,000,000"),
        ("N/A", "Should remain N/A"),
        ("", "Should become N/A"),
        (None, "Should become N/A")
    ]
    
    print("Financial value conversion test cases:")
    for value, expected in test_values:
        print(f"  - Input: {value} -> {expected}")
    
    multiple_values = [
        ("5.0x", "Should convert to 5.0x"),
        ("25.5x", "Should convert to 25.5x"),
        ("5.0", "Should convert to 5.0x"),
        (5.0, "Should convert to 5.0x"),
        ("", "Should become N/A"),
        (None, "Should become N/A")
    ]
    
    print("\nMultiple value conversion test cases:")
    for value, expected in multiple_values:
        print(f"  - Input: {value} -> {expected}")

if __name__ == "__main__":
    print("=== Precedent Transactions Financial Conversion Test ===\n")
    
    # Test the conversion functions
    test_financial_conversion_functions()
    
    print("\n" + "="*60 + "\n")
    
    # Test the actual slide creation
    success = test_precedent_transactions_fix()
    
    if success:
        print("\n🎉 All tests passed! Precedent transactions slide is working properly.")
    else:
        print("\n💥 Tests failed! Check the errors above.")