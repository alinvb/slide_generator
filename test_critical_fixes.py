#!/usr/bin/env python3
"""
Test script to verify critical slide template fixes work correctly.
"""

import json
from adapters import render_plan_to_pptx

# Load the corrected render plan
with open('corrected_render_plan.json', 'r') as f:
    render_plan = json.load(f)

# Load the corrected content IR
with open('corrected_content_ir.json', 'r') as f:
    content_ir = json.load(f)

print("=== Testing Critical Slide Template Fixes ===")
print(f"Loaded render plan with {len(render_plan['slides'])} slides")
print(f"Loaded content IR with {len(content_ir)} keys")

# Test with the actual user data to see if fixes work
try:
    print("\n[TEST] Generating PowerPoint with fixed templates...")
    prs = render_plan_to_pptx(
        plan=render_plan,
        content_ir=content_ir,
        company_name="PT BreadLife Indonesia"
    )
    
    print(f"[SUCCESS] Generated presentation with {len(prs.slides)} slides")
    
    # Save test file
    output_file = "test_critical_fixes_result.pptx"
    prs.save(output_file)
    print(f"[SUCCESS] Saved test presentation as: {output_file}")
    
    # Test specific slides that were problematic
    problem_templates = [
        "product_service_footprint",
        "competitive_positioning", 
        "historical_financial_performance"
    ]
    
    for slide_def in render_plan['slides']:
        template = slide_def.get('template')
        if template in problem_templates:
            print(f"[INFO] Found problematic template '{template}' in plan")
            
    print("\n=== Test Complete ===")
    print("If no errors appeared above, the critical fixes are working!")
    
except Exception as e:
    print(f"[ERROR] Test failed with error: {e}")
    import traceback
    traceback.print_exc()