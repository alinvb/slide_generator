"""
Test script to verify slide rendering fixes
This script tests the specific issues identified from the user's JSON data
"""
import sys
import os

# Add the current directory to the path
sys.path.append('/home/user/webapp')

from slide_templates import render_precedent_transactions_slide, render_competitive_positioning_slide
from pptx import Presentation
import json

def test_precedent_transactions_fix():
    """Test the precedent transactions renderer with null acquirer fix"""
    print("🔍 Testing precedent transactions renderer...")
    
    # Test data with null acquirer (problematic case)
    test_data = {
        "title": "Precedent Transactions",
        "transactions": [
            {
                "target": "Energy Future Holdings",
                "acquirer": None,  # This was causing the error
                "date": "2007",
                "country": "N/A", 
                "enterprise_value": "$45B",
                "revenue": "Data Issue",
                "ev_revenue_multiple": None
            }
        ]
    }
    
    try:
        prs = render_precedent_transactions_slide(data=test_data)
        print("✅ Precedent transactions renderer handled null acquirer successfully!")
        return True
    except Exception as e:
        print(f"❌ Error in precedent transactions renderer: {e}")
        return False

def test_competitive_positioning_fix():
    """Test the competitive positioning renderer with complete assessment data"""
    print("🔍 Testing competitive positioning renderer...")
    
    # Test data with complete assessment matrix
    test_data = {
        "title": "Competitive Positioning",
        "competitors": [
            {"name": "NVIDIA", "revenue": 130500},
            {"name": "AMD", "revenue": 50.0},
            {"name": "Intel", "revenue": 42.0}
        ],
        "assessment": [
            ["Company", "Market Focus", "Product Quality", "Enterprise Adoption", "Innovation"],
            ["NVIDIA", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"],
            ["AMD", "⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐"],
            ["Intel", "⭐⭐⭐", "⭐⭐⭐", "⭐⭐⭐", "⭐⭐⭐"]
        ],
        "barriers": [
            {"title": "Market Position", "desc": "Strong competitive positioning in market"}
        ],
        "advantages": [
            {"title": "Competitive Edge", "desc": "Key differentiators from conversation analysis"}
        ]
    }
    
    try:
        prs = render_competitive_positioning_slide(data=test_data)
        print("✅ Competitive positioning renderer handled complete assessment data successfully!")
        return True
    except Exception as e:
        print(f"❌ Error in competitive positioning renderer: {e}")
        return False

def test_incomplete_assessment_case():
    """Test competitive positioning with only headers (original problematic case)"""
    print("🔍 Testing competitive positioning with incomplete assessment...")
    
    # Test data with only headers (original problem)
    test_data = {
        "title": "Competitive Positioning", 
        "competitors": [
            {"name": "NVIDIA", "revenue": 130500},
            {"name": "AMD", "revenue": 50.0}
        ],
        "assessment": [
            ["Company", "Market Focus", "Product Quality", "Enterprise Adoption", "Innovation"]
            # Missing actual assessment rows - this should now show a helpful message
        ],
        "barriers": [],
        "advantages": []
    }
    
    try:
        prs = render_competitive_positioning_slide(data=test_data)
        print("✅ Competitive positioning handled incomplete assessment gracefully!")
        return True
    except Exception as e:
        print(f"❌ Error with incomplete assessment: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Running slide rendering fix tests...\n")
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: Precedent transactions with null acquirer
    if test_precedent_transactions_fix():
        tests_passed += 1
    
    print()
    
    # Test 2: Complete competitive assessment 
    if test_competitive_positioning_fix():
        tests_passed += 1
    
    print()
    
    # Test 3: Incomplete assessment handling
    if test_incomplete_assessment_case():
        tests_passed += 1
    
    print(f"\n🎯 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("✅ All slide rendering fixes are working correctly!")
        print("\n📋 Summary of fixes:")
        print("• Fixed NoneType error in precedent transactions renderer")
        print("• Enhanced competitive assessment data validation")
        print("• Added graceful handling of missing assessment data")
        print("• Improved null value handling in transaction processing")
    else:
        print("⚠️ Some tests failed - additional fixes may be needed")

if __name__ == "__main__":
    main()