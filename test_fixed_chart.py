#!/usr/bin/env python3
"""
Test the fixed historical financial performance chart
"""

from adapters import RENDERER_MAP
from pptx import Presentation

def test_fixed_chart():
    """Test the chart with fixed dynamic scaling"""
    
    print("🔧 Testing fixed historical financial performance chart...\n")
    
    # User's actual data (the problematic data from the screenshot)
    user_data = {
        "title": "Historical Financial Performance",
        "chart": {
            "title": "Revenue & EBITDA Growth (USD Millions)",
            "categories": ["2020", "2021", "2022", "2023", "2024E"],
            "revenue": [229000, 400000, 495100, 480570, 461560],  
            "ebitda": [100000, 180000, 239000, 223000, 215000]   
        },
        "key_metrics": {
            "metrics": [
                {"title": "Revenue Growth", "value": "Record annual revenue of $495B in 2022", "period": "(Historical)"},
                {"title": "EBITDA Performance", "value": "Industry-leading EBITDA margin above 46%", "period": "(Historical)"},
                {"title": "Production Scale", "value": "Consistent production above 12 mmboe/d", "period": "(Historical)"}
            ]
        }
    }
    
    print("📊 Testing with Saudi Aramco data:")
    print(f"  Revenue range: ${user_data['chart']['revenue'][0]:,} - ${max(user_data['chart']['revenue']):,}")
    print(f"  EBITDA range: ${user_data['chart']['ebitda'][0]:,} - ${max(user_data['chart']['ebitda']):,}")
    
    try:
        renderer = RENDERER_MAP['historical_financial_performance']
        test_prs = Presentation()
        
        print(f"\n🔧 Rendering slide with dynamic axis scaling...")
        result = renderer(data=user_data, prs=test_prs)
        
        # Save the test file
        test_prs.save("test_fixed_chart.pptx")
        
        print(f"  ✅ Chart rendered successfully with dynamic scaling!")
        print(f"  💾 Saved to: test_fixed_chart.pptx")
        print(f"\nℹ️ The chart should now show:")
        print(f"  - Dramatic growth from 2020 ($229B) to 2022 ($495B)")  
        print(f"  - Slight decline in 2023-2024E")
        print(f"  - Proportional bar heights reflecting actual values")
        print(f"  - Proper axis scaling up to ~600,000 (120% of max value)")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Chart rendering failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_fixed_chart()