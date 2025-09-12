#!/usr/bin/env python3
"""
Test script to verify financial projections are properly generated
"""
import sys
import os
sys.path.append('/home/user/webapp')

from bulletproof_json_generator_clean import generate_clean_bulletproof_json, CleanBulletproofJSONGenerator
from shared_functions import call_llm_api
import os
import json

def test_financial_projections():
    """Test that financial projections are generated in growth_strategy_data"""
    print("🧪 Testing financial projections generation...")
    
    # Test with Netflix-like streaming company conversation
    test_messages = [
        {
            "role": "user", 
            "content": "Let's discuss Netflix as an investment opportunity. The company is a global streaming entertainment service with over 260 million paid subscribers worldwide. Netflix has been investing heavily in original content with an annual content budget exceeding $15 billion. The company reported revenue of $31.6 billion in 2023 and is projecting continued growth in 2024 and 2025. Their key growth strategies include geographic expansion, gaming integration, advertising-supported tiers, and continued investment in high-quality original programming. Financial projections show revenue potentially reaching $39B in 2024E and $45B in 2025E, with improving EBITDA margins from content amortization efficiency."
        }
    ]
    
    # Required slides for testing (focus on growth strategy)
    required_slides = ["growth_strategy_projections"]
    
    try:
        # Create API function
        def api_call(messages):
            return call_llm_api(messages, api_key=os.getenv('PERPLEXITY_API_KEY'))
        
        # Generate comprehensive IR data using the main function
        print("📊 Generating comprehensive IR data...")
        result = generate_clean_bulletproof_json(
            messages=test_messages,
            required_slides=required_slides,
            llm_api_call=api_call
        )
        
        # Extract content_ir from the tuple result
        if isinstance(result, tuple) and len(result) >= 2:
            response, content_ir, render_plan = result
        else:
            content_ir = result
        
        # Check if growth_strategy_data contains financial_projections
        growth_data = content_ir.get('growth_strategy_data', {})
        projections = growth_data.get('financial_projections', {})
        
        print(f"\n✅ Growth Strategy Data Structure:")
        print(f"   - Growth Strategy: {bool(growth_data.get('growth_strategy'))}")
        print(f"   - Financial Projections: {bool(projections)}")
        
        if projections:
            categories = projections.get('categories', [])
            revenue = projections.get('revenue', [])
            ebitda = projections.get('ebitda', [])
            
            print(f"\n📈 Financial Projections Details:")
            print(f"   - Categories: {categories}")
            print(f"   - Revenue (USD M): {revenue}")
            print(f"   - EBITDA (USD M): {ebitda}")
            print(f"   - Data completeness: {len(categories) == len(revenue) == len(ebitda)}")
            
            if len(categories) == len(revenue) == len(ebitda) and len(categories) > 0:
                print("✅ SUCCESS: Financial projections data is complete and ready for chart rendering!")
                return True
            else:
                print("❌ ERROR: Financial projections data is incomplete")
                return False
        else:
            print("❌ ERROR: No financial projections found in growth_strategy_data")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: Test failed with exception: {e}")
        import traceback
        print(f"🔍 Full traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = test_financial_projections()
    if success:
        print("\n🎉 Test PASSED: Financial projections fix is working!")
    else:
        print("\n💥 Test FAILED: Financial projections still missing")
    sys.exit(0 if success else 1)