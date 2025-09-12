#!/usr/bin/env python3
"""
Quick check of slide data in content_ir
"""

import json

def check_slides():
    print("🔍 Quick Slide Data Check")
    print("=" * 40)
    
    # Load test data
    with open('/home/user/webapp/working_content_ir_example.json', 'r') as f:
        content_ir = json.load(f)
    
    print(f"Content IR keys: {list(content_ir.keys())}")
    
    # Check 1: Product Service Data
    print(f"\n📊 Product Service Data:")
    product_data = content_ir.get('product_service_data', {})
    if product_data:
        print(f"  Keys: {list(product_data.keys())}")
        
        offerings = product_data.get('offerings', [])
        print(f"  Offerings: {len(offerings)} items")
        if offerings:
            print(f"  First offering: {offerings[0]}")
            print(f"  First offering type: {type(offerings[0])}")
        
        services = product_data.get('services', [])
        print(f"  Services: {len(services)} items")
        if services:
            print(f"  First service: {services[0]}")
    else:
        print(f"  ❌ No product_service_data found")
    
    # Check 2: Investor Process Data
    print(f"\n📊 Investor Process Data:")
    investor_data = content_ir.get('investor_process_data', {})
    if investor_data:
        print(f"  Keys: {list(investor_data.keys())}")
        
        risk_factors = investor_data.get('risk_factors', [])
        print(f"  Risk factors: {len(risk_factors)} items")
        if risk_factors:
            print(f"  First risk: {risk_factors[0]}")
        
        mitigants = investor_data.get('mitigants', [])
        print(f"  Mitigants: {len(mitigants)} items")
        if mitigants:
            print(f"  First mitigant: {mitigants[0]}")
    else:
        print(f"  ❌ No investor_process_data found")

if __name__ == "__main__":
    check_slides()