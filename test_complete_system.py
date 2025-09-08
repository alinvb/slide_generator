#!/usr/bin/env python3
"""
Test complete slide generation system with all recent fixes
"""

import sys
import os
sys.path.append('/home/user/webapp')

from app import generate_presentation
import json

def test_complete_system():
    """Test complete slide generation system"""
    
    print("Testing complete slide generation system...")
    
    # Load the fixed render plan with all corrections
    try:
        with open('/home/user/webapp/fixed_render_plan.json', 'r') as f:
            render_plan = json.load(f)
        print("✅ Loaded fixed render plan successfully")
    except Exception as e:
        print(f"❌ Failed to load render plan: {e}")
        return False
    
    # Load the fixed content IR
    try:
        with open('/home/user/webapp/fixed_content_ir.json', 'r') as f:
            content_ir = json.load(f)
        print("✅ Loaded fixed content IR successfully")
    except Exception as e:
        print(f"❌ Failed to load content IR: {e}")
        return False
    
    # Test key components
    print("\nTesting key components:")
    
    # Test management team data
    management_team = content_ir.get('management_team', [])
    print(f"  - Management team profiles: {len(management_team)}")
    for i, profile in enumerate(management_team[:3]):  # Show first 3
        name = profile.get('name', 'No name')
        position = profile.get('position', 'No position')
        print(f"    {i+1}. {name} - {position}")
    
    # Test precedent transactions data
    precedent_transactions = content_ir.get('precedent_transactions', [])
    print(f"  - Precedent transactions: {len(precedent_transactions)}")
    if precedent_transactions:
        tx = precedent_transactions[0]
        print(f"    Sample: {tx.get('target', 'N/A')} by {tx.get('acquirer', 'N/A')}")
    
    # Test key metrics data
    key_metrics = render_plan.get('slides', [{}])[0].get('key_metrics', [])
    print(f"  - Key metrics: {len(key_metrics)}")
    if key_metrics and isinstance(key_metrics[0], dict):
        print(f"    Sample: {key_metrics[0].get('title', 'No title')}")
    
    print("\n" + "="*60)
    
    # Test slide generation
    try:
        print("Generating presentation slides...")
        
        result = generate_presentation(
            content_ir=content_ir,
            render_plan=render_plan,
            output_filename="test_complete_system_output.pptx"
        )
        
        if result.get('success'):
            print("✅ SUCCESS: Complete slide generation worked!")
            print(f"   - Output file: {result.get('filename', 'N/A')}")
            print(f"   - Slide count: {result.get('slide_count', 'N/A')}")
            return True
        else:
            print(f"❌ FAILED: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== Complete System Test ===\n")
    
    success = test_complete_system()
    
    if success:
        print("\n🎉 Complete system test passed! All fixes are working together.")
    else:
        print("\n💥 Complete system test failed! Check the errors above.")