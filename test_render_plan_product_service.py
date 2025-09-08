#!/usr/bin/env python3

"""
Test rendering the Product & Service slide using the actual render plan data
to determine why the metrics and table are showing as blank/placeholders
"""

from adapters import render_plan_to_pptx
from pptx import Presentation
import json

def test_render_plan_product_service():
    """Test using the actual render plan for product service slide"""
    print("=== Testing Product & Service Slide via Render Plan ===")
    
    # Load the actual render plan
    with open('complete_render_plan.json', 'r') as f:
        render_plan = json.load(f)
    
    print(f"Loaded render plan with {len(render_plan.get('slides', []))} slides")
    
    # Find the product_service_footprint slide
    product_service_slide = None
    for slide in render_plan.get('slides', []):
        if slide.get('template') == 'product_service_footprint':
            product_service_slide = slide
            break
    
    if not product_service_slide:
        print("❌ No product_service_footprint slide found in render plan")
        return False
    
    print("✓ Found product_service_footprint slide in render plan")
    print(f"✓ Slide data keys: {list(product_service_slide.get('data', {}).keys())}")
    
    # Check the data structure
    data = product_service_slide.get('data', {})
    services = data.get('services', [])
    coverage_table = data.get('coverage_table', [])
    metrics = data.get('metrics', {})
    
    print(f"\nData verification:")
    print(f"✓ Services count: {len(services)}")
    print(f"✓ Coverage table rows: {len(coverage_table)}")
    print(f"✓ Metrics count: {len(metrics)}")
    
    if services:
        print(f"✓ First service: {services[0].get('title', 'N/A')}")
    if coverage_table:
        print(f"✓ Table headers: {coverage_table[0] if coverage_table else 'None'}")
    if metrics:
        first_metric = list(metrics.keys())[0]
        print(f"✓ First metric: {first_metric} = {metrics[first_metric]}")
    
    # Test rendering just this slide
    single_slide_plan = {
        "slides": [product_service_slide]
    }
    
    print(f"\n1. Testing single slide rendering...")
    prs = render_plan_to_pptx(plan=single_slide_plan, company_name="SouthernCapital Healthcare")
    
    test_file = "test_single_product_service.pptx"
    prs.save(test_file)
    print(f"✓ Single slide saved as: {test_file}")
    
    # Test with content_ir as well
    print(f"\n2. Testing with content_ir...")
    
    # Load content_ir
    with open('complete_content_ir.json', 'r') as f:
        content_ir = json.load(f)
    
    print(f"✓ Loaded content_ir with sections: {list(content_ir.keys())}")
    
    # Check product_service_data
    if 'product_service_data' in content_ir:
        psd = content_ir['product_service_data']
        print(f"✓ product_service_data has: {list(psd.keys())}")
        print(f"✓ PSD services count: {len(psd.get('services', []))}")
        print(f"✓ PSD metrics count: {len(psd.get('metrics', {}))}")
    else:
        print("❌ No product_service_data found in content_ir")
    
    # Render with content_ir
    prs2 = render_plan_to_pptx(plan=single_slide_plan, content_ir=content_ir, company_name="SouthernCapital Healthcare")
    
    test_file2 = "test_product_service_with_ir.pptx"
    prs2.save(test_file2)
    print(f"✓ With content_ir saved as: {test_file2}")
    
    return True

def main():
    """Run render plan test"""
    print("Testing Product & Service slide rendering via actual render plan...")
    
    try:
        success = test_render_plan_product_service()
        
        if success:
            print("\n🎉 RENDER PLAN TEST COMPLETED!")
            print("Generated test files:")
            print("- test_single_product_service.pptx")
            print("- test_product_service_with_ir.pptx")
            print("\nCheck these files to see if metrics and table render correctly.")
        else:
            print("\n❌ Test failed.")
    except Exception as e:
        print(f"\n💥 Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()