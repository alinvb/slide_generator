#!/usr/bin/env python3
"""
Test the fixed valuation overview slide with Saudi Aramco data
"""

import json
from slide_templates import render_valuation_overview_slide
from pptx import Presentation

# Saudi Aramco valuation data from user
valuation_data = [
    {
        "methodology": "Public Trading Comparables",
        "enterprise_value": "US$1.57T",
        "metric": "EV/Revenue",
        "22a_multiple": "3.3x",
        "23e_multiple": "3.3x",
        "commentary": "Reflects scale, margin, and stability premium.",
        "methodology_type": "trading_comps"
    },
    {
        "methodology": "Public Trading Comparables",
        "enterprise_value": "US$1.57T",
        "metric": "EV/EBITDA",
        "22a_multiple": "6.6x",
        "23e_multiple": "6.5x",
        "commentary": "In line with peers, but premium for cash flow stability.",
        "methodology_type": "trading_comps"
    },
    {
        "methodology": "Public Trading Comparables",
        "enterprise_value": "US$1.53T",
        "metric": "P/E",
        "22a_multiple": "15.3x",
        "23e_multiple": "15.3x",
        "commentary": "Top decile among global majors.",
        "methodology_type": "trading_comps"
    },
    {
        "methodology": "DCF",
        "enterprise_value": "US$1.45–1.60T",
        "metric": "FCF-based",
        "22a_multiple": "",
        "23e_multiple": "",
        "commentary": "Assumes modest growth, high CapEx, resilient FCF.",
        "methodology_type": "dcf"
    },
    {
        "methodology": "DDM",
        "enterprise_value": "US$1.50T+",
        "metric": "Dividend",
        "22a_multiple": "",
        "23e_multiple": "",
        "commentary": "Very high payout ratio, stable base dividend."
    }
]

slide_data = {
    "title": "Valuation Overview",
    "valuation_data": valuation_data
}

print("=== Testing Fixed Valuation Overview Slide ===")
print(f"Testing with {len(valuation_data)} valuation rows")

try:
    # Test the slide generation
    prs = render_valuation_overview_slide(
        data=slide_data,
        company_name="Saudi Aramco"
    )
    
    print(f"[SUCCESS] Generated valuation slide with {len(prs.slides)} slides")
    
    # Save test file
    output_file = "test_valuation_fix.pptx"
    prs.save(output_file)
    print(f"[SUCCESS] Saved test valuation slide as: {output_file}")
    
    # Print data structure for verification
    print("\n=== Data Structure Verification ===")
    for i, row in enumerate(valuation_data):
        print(f"Row {i+1}: {row['methodology']} - {row['enterprise_value']}")
        
    print("\n=== Test Complete ===")
    print("Check the generated PowerPoint file to see if the table displays correctly!")
    
except Exception as e:
    print(f"[ERROR] Test failed with error: {e}")
    import traceback
    traceback.print_exc()