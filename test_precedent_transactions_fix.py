#!/usr/bin/env python3
"""
Test script to verify precedent transactions string multiple fix
"""
import json
from executor import execute_plan

# Load the fixed JSONs
with open('/home/user/webapp/fixed_content_ir.json', 'r') as f:
    content_ir = json.load(f)

with open('/home/user/webapp/fixed_render_plan.json', 'r') as f:
    render_plan = json.load(f)

print("🔍 TESTING PRECEDENT TRANSACTIONS FIX")
print("="*50)

# Find the precedent transactions slide
precedent_slide = None
for slide in render_plan.get('slides', []):
    if slide.get('template') == 'precedent_transactions':
        precedent_slide = slide
        break

if precedent_slide:
    print(f"📋 Found precedent_transactions slide")
    
    slide_data = precedent_slide.get('data', {})
    transactions = slide_data.get('transactions', [])
    
    print(f"\n💰 Transaction data:")
    print(f"   Transactions count: {len(transactions)}")
    
    if transactions:
        print(f"\n🔢 EV/Revenue multiples:")
        for i, transaction in enumerate(transactions, 1):
            multiple_raw = transaction.get('ev_revenue_multiple', 'N/A')
            target = transaction.get('target', 'Unknown')
            print(f"      T{i}: {target} = {multiple_raw}")
    
    # Test generating just this slide
    print(f"\n🧪 Testing slide generation...")
    
    # Create a mini render plan with just this slide
    test_plan = {
        "slides": [precedent_slide]
    }
    
    try:
        prs, path = execute_plan(
            plan=test_plan,
            content_ir=content_ir,
            output_path="test_precedent_transactions_fix.pptx",
            company_name="LlamaIndex"
        )
        print(f"✅ Successfully generated test slide: {path}")
        print(f"   Slides created: {len(prs.slides)}")
        
    except Exception as e:
        print(f"❌ Error generating slide: {str(e)}")
        import traceback
        traceback.print_exc()
else:
    print("❌ No precedent_transactions slide found!")

print("\n🔍 Test complete")