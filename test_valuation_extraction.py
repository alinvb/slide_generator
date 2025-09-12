#!/usr/bin/env python3
"""
Test valuation data extraction
"""

import json
from bulletproof_json_generator_clean import CleanBulletproofJSONGenerator

def test_valuation_extraction():
    print("🔍 Testing Valuation Data Extraction")
    print("=" * 50)
    
    # Load test data
    with open('/home/user/webapp/working_content_ir_example.json', 'r') as f:
        content_ir = json.load(f)
    
    print(f"Content_ir keys: {list(content_ir.keys())}")
    
    # Check if valuation_data exists
    if 'valuation_data' in content_ir:
        print(f"✅ Found valuation_data with {len(content_ir['valuation_data'])} items")
        
        # Show the data
        for i, item in enumerate(content_ir['valuation_data']):
            print(f"\nItem {i+1}:")
            for key, value in item.items():
                print(f"  {key}: {value}")
    else:
        print("❌ No valuation_data found")
        return
    
    # Test extraction
    generator = CleanBulletproofJSONGenerator()
    
    # Test extraction using the extract_slide_data method
    print(f"\n🧪 Testing slide extraction...")
    
    # Build the required slides list (this may be needed)
    required_slides = ['valuation_overview']
    
    # Build content_ir structure
    print(f"Building content_ir...")
    full_content_ir = generator.build_content_ir(content_ir, required_slides)
    
    if full_content_ir:
        print(f"✅ Built content_ir successfully")
        print(f"Full content_ir keys: {list(full_content_ir.keys())}")
        
        # Check if valuation is in the full content_ir
        if 'valuation_data' in full_content_ir:
            print(f"✅ valuation_data in full_content_ir: {len(full_content_ir['valuation_data'])} items")
        if 'valuation_overview' in full_content_ir:
            print(f"✅ valuation_overview in full_content_ir: {len(full_content_ir['valuation_overview'])} items")
        
    else:
        print(f"❌ Failed to build content_ir")

if __name__ == "__main__":
    test_valuation_extraction()