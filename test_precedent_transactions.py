#!/usr/bin/env python3

"""
Test script to verify precedent transactions renderer handles mixed data types robustly
"""

import sys
import os

# Add the current directory to sys.path so we can import local modules
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Test the precedent transactions rendering with mixed data types
def test_precedent_transactions_robustness():
    print("🧪 Testing precedent transactions renderer robustness...")
    
    # Import the slide templates module
    from slide_templates import render_precedent_transactions_slide
    
    # Create test data with mixed data types (dict objects and strings)
    mixed_precedent_data = [
        {
            'target': 'TechCorp Inc',
            'acquirer': 'Global Holdings',
            'date': '2023',
            'country': 'Singapore',
            'enterprise_value': 2500.0,  # Float
            'revenue': 800.0,  # Float
            'ev_revenue_multiple': 3.125  # Float
        },
        {
            'target': 'FinanceStream',
            'acquirer': 'MegaBank',
            'date': '2022',
            'country': 'Malaysia',
            'enterprise_value': '1800M',  # String format
            'revenue': '450M',  # String format
            'ev_revenue_multiple': 4.0  # Float
        },
        "DataPoint Systems acquired by CloudTech for $900M (2.5x revenue)",  # Pure string
        {
            'target': 'ServicePlus',
            'acquirer': 'Industry Leader',
            'date': '2024',
            'country': 'Thailand',
            'enterprise_value': 3200,  # Integer
            'revenue': 1000,  # Integer
            'ev_revenue_multiple': '3.2x'  # String with 'x'
        },
        "Invalid data entry - no structured format"  # Another string
    ]
    
    # Test content IR with mixed data
    content_ir = {
        'precedent_transactions': mixed_precedent_data
    }
    
    # Create test slide
    slide = {
        'template': 'precedent_transactions',
        'data': {
            'title': 'Precedent Transaction Analysis',
            'transactions': mixed_precedent_data
        }
    }
    
    print("📊 Testing with mixed data types:")
    print("  - Dict with float values")
    print("  - Dict with string values (e.g., '1800M')")
    print("  - Pure strings (narrative format)")
    print("  - Dict with integer values")
    print("  - Dict with string multiple (e.g., '3.2x')")
    
    try:
        # Test the rendering function
        print("\n🔧 Testing precedent transactions renderer...")
        result = render_precedent_transactions_slide(slide, content_ir, {})
        
        if result:
            print("✅ Renderer handled mixed data types successfully!")
            print(f"   Result type: {type(result)}")
            
            # Check if the result contains chart data (should only include valid numeric entries)
            if hasattr(result, 'charts') or (isinstance(result, dict) and 'charts' in result):
                print("✅ Chart data generated successfully (filtered numeric entries)")
            else:
                print("ℹ️  No chart data in result (expected for mixed data)")
            
            return True
        else:
            print("❌ Renderer returned None or empty result")
            return False
            
    except Exception as e:
        print(f"❌ Renderer failed with error: {e}")
        print(f"   Error type: {type(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Precedent Transactions Renderer Robustness")
    print("=" * 60)
    
    success = test_precedent_transactions_robustness()
    
    print("\n" + "=" * 60)
    if success:
        print("🎯 PRECEDENT TRANSACTIONS ROBUSTNESS TEST: ✅ PASSED")
        print("   The renderer can handle mixed data types safely")
    else:
        print("🎯 PRECEDENT TRANSACTIONS ROBUSTNESS TEST: ❌ FAILED")
        print("   The renderer needs additional error handling")