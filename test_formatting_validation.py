#!/usr/bin/env python3
"""
Test script to validate formatting requirements for presentation consistency
"""

from bulletproof_json_generator_clean import CleanBulletproofJSONGenerator
import json

def test_formatting_validation():
    """Test the formatting validation function"""
    
    print("🧪 Testing formatting validation...")
    
    # Initialize generator
    generator = CleanBulletproofJSONGenerator()
    
    # Create test data with incorrect formatting
    test_data = {
        "business_overview_data": {
            "highlights": ["Only", "Two", "Highlights"]  # Should be 6
        },
        "product_service_data": {
            "services": [
                {"title": "Service 1", "desc": "Description 1"},
                {"title": "Service 2", "desc": "Description 2"}  # Should be 5
            ],
            "metrics": {
                "metric1": "value1"  # Should be 4 metrics
            }
        },
        "growth_strategy_data": {
            "growth_strategy": {
                "strategies": ["Strategy 1", "Strategy 2"]  # Should be 6
            }
        },
        "investor_considerations": {
            "considerations": ["Consideration 1"],  # Should be 5
            "mitigants": ["Mitigant 1", "Mitigant 2", "Mitigant 3"]  # Should be 5 and equal to considerations
        }
    }
    
    print(f"📊 BEFORE validation:")
    print(f"  - Business highlights: {len(test_data['business_overview_data']['highlights'])}")
    print(f"  - Product services: {len(test_data['product_service_data']['services'])}")  
    print(f"  - Product metrics: {len(test_data['product_service_data']['metrics'])}")
    print(f"  - Growth strategies: {len(test_data['growth_strategy_data']['growth_strategy']['strategies'])}")
    print(f"  - Considerations: {len(test_data['investor_considerations']['considerations'])}")
    print(f"  - Mitigants: {len(test_data['investor_considerations']['mitigants'])}")
    
    # Apply validation
    validated_data = generator._validate_and_fix_formatting(test_data)
    
    print(f"\n📊 AFTER validation:")
    print(f"  - Business highlights: {len(validated_data['business_overview_data']['highlights'])}")
    print(f"  - Product services: {len(validated_data['product_service_data']['services'])}")  
    print(f"  - Product metrics: {len(validated_data['product_service_data']['metrics'])}")
    print(f"  - Growth strategies: {len(validated_data['growth_strategy_data']['growth_strategy']['strategies'])}")
    print(f"  - Considerations: {len(validated_data['investor_considerations']['considerations'])}")
    print(f"  - Mitigants: {len(validated_data['investor_considerations']['mitigants'])}")
    
    # Validate results
    assert len(validated_data['business_overview_data']['highlights']) == 6, "Business highlights should be exactly 6"
    assert len(validated_data['product_service_data']['services']) == 5, "Product services should be exactly 5"
    assert len(validated_data['product_service_data']['metrics']) == 4, "Product metrics should be exactly 4"
    assert len(validated_data['growth_strategy_data']['growth_strategy']['strategies']) == 6, "Growth strategies should be exactly 6"
    assert len(validated_data['investor_considerations']['considerations']) == 5, "Considerations should be exactly 5"
    assert len(validated_data['investor_considerations']['mitigants']) == 5, "Mitigants should be exactly 5"
    assert len(validated_data['investor_considerations']['considerations']) == len(validated_data['investor_considerations']['mitigants']), "Considerations and mitigants must be equal"
    
    print(f"\n✅ All formatting validation tests PASSED!")
    print(f"🎯 The system will now ensure consistent formatting for ANY company/scenario")
    
    return True

if __name__ == "__main__":
    try:
        test_formatting_validation()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()