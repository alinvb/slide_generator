#!/usr/bin/env python3
"""
Test script to debug the coverage table issue in product_service_footprint slide
"""
import json
from executor import execute_plan

# Load the fixed JSONs
with open('/home/user/webapp/fixed_content_ir.json', 'r') as f:
    content_ir = json.load(f)

with open('/home/user/webapp/fixed_render_plan.json', 'r') as f:
    render_plan = json.load(f)

print("🔍 DEBUGGING COVERAGE TABLE ISSUE")
print("="*60)

# Find the product_service_footprint slide
product_slide = None
for slide in render_plan.get('slides', []):
    if slide.get('template') == 'product_service_footprint':
        product_slide = slide
        break

if product_slide:
    print(f"📋 Found product_service_footprint slide:")
    print(f"   Data keys: {list(product_slide.get('data', {}).keys())}")
    
    slide_data = product_slide.get('data', {})
    coverage_table = slide_data.get('coverage_table', [])
    
    print(f"\n📊 Coverage table data:")
    print(f"   Type: {type(coverage_table)}")
    print(f"   Length: {len(coverage_table) if coverage_table else 0}")
    
    if coverage_table:
        print(f"   First item type: {type(coverage_table[0])}")
        print(f"   First 2 rows:")
        for i, row in enumerate(coverage_table[:2]):
            print(f"      Row {i}: {row}")
    
    # Test generating just this slide
    print(f"\n🧪 Testing slide generation...")
    
    # Create a mini render plan with just this slide
    test_plan = {
        "slides": [product_slide]
    }
    
    try:
        prs, path = execute_plan(
            plan=test_plan,
            content_ir=content_ir,
            output_path="test_coverage_table_debug.pptx",
            company_name="LlamaIndex"
        )
        print(f"✅ Successfully generated test slide: {path}")
        print(f"   Slides created: {len(prs.slides)}")
        
    except Exception as e:
        print(f"❌ Error generating slide: {str(e)}")
        import traceback
        traceback.print_exc()
else:
    print("❌ No product_service_footprint slide found!")

print("\n🔍 Debug complete")