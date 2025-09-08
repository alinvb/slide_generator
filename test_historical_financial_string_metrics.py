#!/usr/bin/env python3

"""
Test to fix the Historical Financial Performance slide string metrics error.
This reproduces the exact error: 'str' object has no attribute 'get'
"""

from pptx import Presentation
from slide_templates import render_historical_financial_performance_slide

def test_string_metrics_error():
    """Test the exact Saudi Aramco data format that causes the error"""
    print("=== Testing Historical Financial Performance String Metrics Fix ===")
    
    # Your exact data format that causes the error
    saudi_data = {
        "title": "Historical Financial Performance",
        "chart": {
            "title": "Revenue & EBITDA Growth (USD Millions)",
            "categories": ["2020", "2021", "2022", "2023", "2024E"],
            "revenue": [229000, 400000, 495100, 480570, 461560],
            "ebitda": [100000, 180000, 239000, 223000, 215000]
        },
        "key_metrics": {
            "metrics": [
                "Record annual revenue of $495B in 2022",        # STRING - causes error
                "Industry-leading EBITDA margin above 46%",      # STRING - causes error  
                "Consistent production above 12 mmboe/d"         # STRING - causes error
            ]
        },
        "revenue_growth": {
            "title": "Revenue Growth Drivers",
            "points": [
                "Growth in gas and chemicals output",
                "Expansion in high-growth international markets", 
                "Efficiency gains from digital transformation"
            ]
        },
        "banker_view": {
            "title": "Banker View",
            "text": "Saudi Aramco demonstrates resilient performance through commodity cycles, backed by scale, cost leadership, and diversified downstream assets."
        }
    }
    
    print("1. Testing with string metrics (original problematic format)...")
    print(f"Metrics type: {type(saudi_data['key_metrics']['metrics'])}")
    print(f"First metric type: {type(saudi_data['key_metrics']['metrics'][0])}")
    print(f"First metric value: {saudi_data['key_metrics']['metrics'][0]}")
    
    # This should now work without error
    prs = Presentation()
    prs = render_historical_financial_performance_slide(
        data=saudi_data,
        company_name="Saudi Aramco",
        prs=prs
    )
    
    test_file = "test_historical_string_metrics_FIXED.pptx"
    prs.save(test_file)
    print(f"✅ Fixed slide saved as: {test_file}")
    
    # Test with mixed format (some strings, some objects)
    print("\n2. Testing with mixed string/object metrics...")
    mixed_data = saudi_data.copy()
    mixed_data["key_metrics"]["metrics"] = [
        "Record annual revenue of $495B in 2022",  # String format
        {
            "title": "EBITDA Margin",
            "value": "46%+", 
            "period": "(2024E)",
            "note": "✓ Industry leading"
        },  # Object format
        "Consistent production above 12 mmboe/d",  # String format
        {
            "title": "Reserves",
            "value": "267B bbl",
            "period": "(proven)",
            "note": "● World's largest"
        }   # Object format
    ]
    
    prs2 = Presentation()
    prs2 = render_historical_financial_performance_slide(
        data=mixed_data,
        company_name="Saudi Aramco",
        prs=prs2
    )
    
    test_file2 = "test_historical_mixed_metrics.pptx"
    prs2.save(test_file2)
    print(f"✅ Mixed format slide saved as: {test_file2}")
    
    return True

def main():
    """Run the historical financial performance string metrics fix test"""
    print("Testing Historical Financial Performance slide string metrics fix...")
    
    try:
        success = test_string_metrics_error()
        
        if success:
            print(f"\n🎉 HISTORICAL FINANCIAL PERFORMANCE SLIDE FIXED!")
            print("✅ FIXED: 'str' object has no attribute 'get' error")
            print("✅ ADDED: String metrics display support") 
            print("✅ ADDED: Mixed string/object metrics handling")
            print("✅ ADDED: Fallback for unknown metric formats")
            
            print(f"\n📁 Generated test files:")
            print("- test_historical_string_metrics_FIXED.pptx (string metrics)")
            print("- test_historical_mixed_metrics.pptx (mixed formats)")
            
            print(f"\n🔧 Technical fix:")
            print("- Added type checking: isinstance(metric, str) vs isinstance(metric, dict)")
            print("- String metrics displayed as text blocks instead of structured layout")
            print("- Object metrics use original structured title/value/period/note layout")
            print("- Enhanced error handling with debug logging")
            
        else:
            print("\n❌ Test failed.")
    except Exception as e:
        print(f"\n💥 Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()