#!/usr/bin/env python3
"""
Test script to verify chart data handling in historical financial performance slide
"""

import json
from adapters import RENDERER_MAP
from pptx import Presentation

def test_chart_data_extraction():
    """Test how chart data is extracted and processed"""
    
    print("🔍 Testing chart data extraction...\n")
    
    # User's actual data structure
    user_data = {
        "title": "Historical Financial Performance",
        "chart": {
            "title": "Revenue & EBITDA Growth (USD Millions)",
            "categories": ["2020", "2021", "2022", "2023", "2024E"],
            "revenue": [229000, 400000, 495100, 480570, 461560],  # These are HUGE values
            "ebitda": [100000, 180000, 239000, 223000, 215000]   # These are HUGE values
        },
        "key_metrics": {
            "metrics": [
                {"title": "Key Metric 1", "value": "Record annual revenue of $495B in 2022", "period": "(Historical)"},
                {"title": "Key Metric 2", "value": "Industry-leading EBITDA margin above 46%", "period": "(Historical)"},
                {"title": "Key Metric 3", "value": "Consistent production above 12 mmboe/d", "period": "(Historical)"}
            ]
        }
    }
    
    print("📊 User's actual data:")
    print(f"  Revenue values: {user_data['chart']['revenue']}")
    print(f"  EBITDA values: {user_data['chart']['ebitda']}")
    print(f"  Value range: {min(user_data['chart']['revenue'])} - {max(user_data['chart']['revenue'])}")
    
    # Test the renderer
    try:
        renderer = RENDERER_MAP['historical_financial_performance']
        test_prs = Presentation()
        
        print(f"\n🔧 Testing renderer with user data...")
        result = renderer(data=user_data, prs=test_prs)
        print(f"  ✅ Renderer executed successfully")
        
        # Try to inspect what data was actually used
        # This would require accessing the chart object, but let's see if we can debug
        
        return True
        
    except Exception as e:
        print(f"  ❌ Renderer failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_chart_axis_scaling():
    """Test appropriate axis scaling for large values"""
    
    print(f"\n🔍 Testing chart axis scaling...")
    
    revenue_values = [229000, 400000, 495100, 480570, 461560]
    ebitda_values = [100000, 180000, 239000, 223000, 215000]
    
    # Current hardcoded maximum
    current_max = 45
    
    # Recommended maximum (should be ~120% of highest value)
    data_max = max(max(revenue_values), max(ebitda_values))
    recommended_max = int(data_max * 1.2)
    
    print(f"📊 Chart scaling analysis:")
    print(f"  Current hardcoded maximum: {current_max:,}")
    print(f"  Actual data maximum: {data_max:,}")
    print(f"  Recommended maximum (120% of data): {recommended_max:,}")
    print(f"  Scale difference: {data_max / current_max:.1f}x too large!")
    
    # Show what happens with current scaling
    print(f"\n⚠️ With current scale (max={current_max}):")
    for i, (rev, ebitda) in enumerate(zip(revenue_values, ebitda_values)):
        rev_pct = min(100, (rev / current_max) * 100)
        ebitda_pct = min(100, (ebitda / current_max) * 100)
        print(f"  2020+{i}: Revenue {rev:,} → {rev_pct:.1f}% (truncated), EBITDA {ebitda:,} → {ebitda_pct:.1f}% (truncated)")
    
    print(f"\n✅ With recommended scale (max={recommended_max:,}):")
    for i, (rev, ebitda) in enumerate(zip(revenue_values, ebitda_values)):
        rev_pct = (rev / recommended_max) * 100
        ebitda_pct = (ebitda / recommended_max) * 100
        print(f"  2020+{i}: Revenue {rev:,} → {rev_pct:.1f}%, EBITDA {ebitda:,} → {ebitda_pct:.1f}%")

if __name__ == "__main__":
    print("🚀 Testing chart data handling...\n")
    
    test_chart_data_extraction()
    test_chart_axis_scaling()
    
    print(f"\n💡 CONCLUSION:")
    print(f"The chart bars appear the same height because:")
    print(f"1. Axis maximum is hardcoded to 45")
    print(f"2. User data values are 200,000+ (5000x larger)")
    print(f"3. All bars hit the maximum and get truncated")
    print(f"4. Need dynamic axis scaling based on actual data values")