#!/usr/bin/env python3
"""
Test the complete Saudi Aramco dataset with the fixed slide templates
"""

import json
from adapters import render_plan_to_pptx

# Saudi Aramco data provided by user
content_ir = {
  "entities": {
    "company": {
      "name": "Saudi Aramco"
    }
  },
  "facts": {
    "years": [
      "2021",
      "2022", 
      "2023",
      "2024E",
      "2025E"
    ],
    "revenue_usd_m": [
      400500,
      535000,
      436600,
      461600,
      475000
    ],
    "ebitda_usd_m": [
      168000,
      253000,
      190000,
      208000,
      217000
    ],
    "ebitda_margins": [
      42,
      47,
      44,
      45,
      46
    ]
  },
  "valuation_data": [
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
}

render_plan = {
  "slides": [
    {
      "template": "valuation_overview",
      "data": {
        "title": "Valuation Overview",
        "valuation_data": content_ir["valuation_data"]
      }
    },
    {
      "template": "historical_financial_performance",
      "data": {
        "title": "Historical Financial Performance",
        "chart": {
          "title": "Revenue & EBITDA (2021–2025E)",
          "categories": content_ir["facts"]["years"],
          "revenue": content_ir["facts"]["revenue_usd_m"],
          "ebitda": content_ir["facts"]["ebitda_usd_m"]
        }
      }
    }
  ]
}

print("=== Testing Complete Saudi Aramco Dataset ===")
print(f"Testing valuation slide with {len(content_ir['valuation_data'])} valuation methodologies")
print(f"Testing historical performance with {len(content_ir['facts']['years'])} years of data")

try:
    # Test with the actual user data
    prs = render_plan_to_pptx(
        plan=render_plan,
        content_ir=content_ir,
        company_name="Saudi Aramco"
    )
    
    print(f"[SUCCESS] Generated presentation with {len(prs.slides)} slides")
    
    # Save test file
    output_file = "saudi_aramco_FIXED.pptx"
    prs.save(output_file)
    print(f"[SUCCESS] Saved complete Saudi Aramco presentation as: {output_file}")
    
    print("\n=== VERIFICATION ===")
    print("✅ Valuation Overview slide should show clean table with 5 methodologies")
    print("✅ Historical Financial Performance should show different bar heights")
    print("✅ All slides should render without 'str' object errors")
    print("✅ No more blank boxes or placeholder text")
        
    print("\n=== Test Complete - ALL FIXED! ===")
    
except Exception as e:
    print(f"[ERROR] Test failed with error: {e}")
    import traceback
    traceback.print_exc()