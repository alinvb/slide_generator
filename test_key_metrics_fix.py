#!/usr/bin/env python3
"""
Test script to verify key metrics labels fix
"""
import json
from executor import execute_plan

# Load the fixed JSONs
with open('/home/user/webapp/fixed_content_ir.json', 'r') as f:
    content_ir = json.load(f)

with open('/home/user/webapp/fixed_render_plan.json', 'r') as f:
    render_plan = json.load(f)

print("🔍 TESTING KEY METRICS FIX")
print("="*50)

# Find the historical financial performance slide
historical_slide = None
for slide in render_plan.get('slides', []):
    if slide.get('template') == 'historical_financial_performance':
        historical_slide = slide
        break

if historical_slide:
    print(f"📋 Found historical_financial_performance slide")
    
    slide_data = historical_slide.get('data', {})
    key_metrics = slide_data.get('key_metrics', {})
    metrics = key_metrics.get('metrics', [])
    
    print(f"\n📊 Key metrics structure:")
    print(f"   Title: {key_metrics.get('title', 'N/A')}")
    print(f"   Metrics count: {len(metrics) if metrics else 0}")
    
    if metrics:
        print(f"   First metric type: {type(metrics[0])}")
        print(f"\n🏷️  Metric labels:")
        for i, metric in enumerate(metrics, 1):
            if isinstance(metric, dict):
                title = metric.get('title', 'No title')
                value = metric.get('value', 'No value')
                print(f"      Metric {i}: {title} = {value}")
            else:
                print(f"      Metric {i}: {metric} (string format)")
    
    # Test generating just this slide
    print(f"\n🧪 Testing slide generation...")
    
    # Create a mini render plan with just this slide
    test_plan = {
        "slides": [historical_slide]
    }
    
    try:
        prs, path = execute_plan(
            plan=test_plan,
            content_ir=content_ir,
            output_path="test_key_metrics_fix.pptx",
            company_name="LlamaIndex"
        )
        print(f"✅ Successfully generated test slide: {path}")
        print(f"   Slides created: {len(prs.slides)}")
        
    except Exception as e:
        print(f"❌ Error generating slide: {str(e)}")
        import traceback
        traceback.print_exc()
else:
    print("❌ No historical_financial_performance slide found!")

print("\n🔍 Test complete")