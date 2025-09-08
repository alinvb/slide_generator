#!/usr/bin/env python3
"""
Test the enhanced validation and improve button functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import validate_historical_financial_performance_slide

def test_historical_financial_validation():
    """Test the enhanced historical financial performance validation"""
    
    print("🧪 Testing Enhanced Historical Financial Performance Validation")
    
    # Test case 1: Valid slide data
    valid_slide = {
        'data': {
            'title': 'Historical Financial Performance',
            'chart': {
                'categories': ['2020', '2021', '2022', '2023', '2024E'],
                'revenue': [100, 150, 200, 250, 300],
                'ebitda': [10, 20, 30, 40, 50]
            },
            'key_metrics': {
                'metrics': [
                    'Revenue Growth: 25% CAGR',
                    'EBITDA Margin: 15%'
                ]
            }
        }
    }
    
    # Test case 2: Invalid slide data (missing chart fields)
    invalid_slide = {
        'data': {
            'title': 'Historical Financial Performance',
            'chart': {
                'categories': ['2020', '2021', '2022'],
                'revenue': [],  # Empty array
                # Missing 'ebitda' field
            },
            'key_metrics': {
                'metrics': []  # Empty metrics
            }
        }
    }
    
    # Test case 3: Missing chart entirely
    missing_chart_slide = {
        'data': {
            'title': 'Historical Financial Performance',
            'key_metrics': {
                'metrics': ['Some metric']
            }
            # Missing 'chart' field
        }
    }
    
    # Run tests
    print("\n✅ Test 1: Valid Slide")
    result1 = validate_historical_financial_performance_slide(valid_slide, {})
    print(f"Issues: {len(result1['issues'])}, Missing: {len(result1['missing_fields'])}, Empty: {len(result1['empty_fields'])}")
    
    print("\n❌ Test 2: Invalid Slide (empty revenue, missing ebitda)")
    result2 = validate_historical_financial_performance_slide(invalid_slide, {})
    print(f"Issues: {len(result2['issues'])}, Missing: {len(result2['missing_fields'])}, Empty: {len(result2['empty_fields'])}")
    if result2['missing_fields']:
        print(f"Missing fields: {result2['missing_fields']}")
    if result2['empty_fields']:
        print(f"Empty fields: {result2['empty_fields']}")
    
    print("\n❌ Test 3: Missing Chart Slide")
    result3 = validate_historical_financial_performance_slide(missing_chart_slide, {})
    print(f"Issues: {len(result3['issues'])}, Missing: {len(result3['missing_fields'])}, Empty: {len(result3['empty_fields'])}")
    if result3['missing_fields']:
        print(f"Missing fields: {result3['missing_fields']}")
    
    # Verify the validation is working correctly
    is_valid_1 = len(result1['issues']) == 0 and len(result1['missing_fields']) == 0
    is_valid_2 = len(result2['issues']) == 0 and len(result2['missing_fields']) == 0 and len(result2['empty_fields']) == 0
    is_valid_3 = len(result3['issues']) == 0 and len(result3['missing_fields']) == 0
    
    print(f"\n🎯 Results: Valid should pass: {is_valid_1}, Invalid should fail: {not is_valid_2}, Missing chart should fail: {not is_valid_3}")
    
    success = is_valid_1 and not is_valid_2 and not is_valid_3
    
    if success:
        print("✅ All validation tests passed!")
        return True
    else:
        print("❌ Validation tests failed!")
        return False

if __name__ == "__main__":
    test_historical_financial_validation()