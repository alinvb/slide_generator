#!/usr/bin/env python3
"""
Validate the fixed slides: Product Service Footprint and Investor Process Overview
"""

import json

def validate_fixed_slides():
    print("🔧 VALIDATING FIXED SLIDES")
    print("=" * 50)
    
    # Load test data
    with open('/home/user/webapp/working_content_ir_example.json', 'r') as f:
        content_ir = json.load(f)
    
    print("🧪 Testing Product Service Footprint Data Structure")
    print("-" * 50)
    
    product_data = content_ir.get('product_service_data', {})
    services = product_data.get('services', [])
    
    print(f"Services count: {len(services)}")
    
    all_services_valid = True
    for i, service in enumerate(services):
        if isinstance(service, dict):
            if 'title' in service and 'desc' in service:
                print(f"  ✅ Service {i+1}: {service['title']} (dict format)")
            else:
                print(f"  ❌ Service {i+1}: Missing title or desc keys")
                all_services_valid = False
        else:
            print(f"  ⚠️  Service {i+1}: {type(service)} format - will be converted")
    
    if all_services_valid:
        print(f"✅ Product Service Footprint: All services in correct dict format")
    else:
        print(f"⚠️  Product Service Footprint: Some services need conversion (handled by extraction)")
    
    print(f"\n🧪 Testing Investor Process Overview Data")
    print("-" * 50)
    
    investor_data = content_ir.get('investor_process_data', {})
    
    risk_factors = investor_data.get('risk_factors', [])
    mitigants = investor_data.get('mitigants', [])
    diligence_topics = investor_data.get('diligence_topics', [])
    synergy_opportunities = investor_data.get('synergy_opportunities', [])
    timeline = investor_data.get('timeline', [])
    
    print(f"✅ Risk factors: {len(risk_factors)} items")
    if risk_factors:
        print(f"   • {risk_factors[0]}")
    
    print(f"✅ Mitigants: {len(mitigants)} items") 
    if mitigants:
        print(f"   • {mitigants[0]}")
        
    print(f"✅ Diligence topics: {len(diligence_topics)} items")
    print(f"✅ Synergy opportunities: {len(synergy_opportunities)} items")
    print(f"✅ Timeline: {len(timeline)} items")
    
    # Summary
    print(f"\n🏆 VALIDATION SUMMARY")
    print("=" * 50)
    
    if len(services) > 0:
        print(f"✅ Product Service Footprint: {len(services)} services available")
    else:
        print(f"❌ Product Service Footprint: No services found")
        
    if len(risk_factors) > 0 and len(mitigants) > 0:
        print(f"✅ Investor Process Overview: Risk factors and mitigants populated")
    else:
        print(f"❌ Investor Process Overview: Missing risk factors or mitigants")
    
    # Overall status
    product_ok = len(services) > 0
    investor_ok = len(risk_factors) > 0 and len(mitigants) > 0
    
    if product_ok and investor_ok:
        print(f"\n🎉 Both slides fixed and ready for rendering!")
        return True
    else:
        print(f"\n⚠️  Some issues remain to be addressed")
        return False

if __name__ == "__main__":
    validate_fixed_slides()