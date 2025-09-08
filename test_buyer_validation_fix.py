#!/usr/bin/env python3
"""
Test buyer validation fix - ensure no more fit_score errors
"""

def test_buyer_validation():
    """Test that buyer validation works with new field names"""
    print("🧪 Testing buyer validation with new field names...")
    
    try:
        # Import the validation function
        import sys
        sys.path.append('.')
        from app import validate_buyer_profiles_slide
        
        # Create test data with the new field structure
        test_slide = {
            "template": "buyer_profiles",
            "content_ir_key": "strategic_buyers",
            "data": {
                "title": "Strategic Buyer Profiles",
                "table_headers": ["Buyer Name", "Description", "Strategic Rationale", "Key Synergies", "Fit"]
            }
        }
        
        test_content_ir = {
            "strategic_buyers": [
                {
                    "buyer_name": "Test Buyer 1",
                    "description": "Test description",
                    "strategic_rationale": "Expand market reach globally",  # 5 words
                    "key_synergies": "Technology integration, market expansion",
                    "fit": "High (9/10)"  # Using 'fit' not 'fit_score'
                },
                {
                    "buyer_name": "Test Buyer 2", 
                    "description": "Another test description",
                    "strategic_rationale": "Enhance operational efficiency and scale",  # 6 words
                    "key_synergies": "Cost reduction, operational optimization",
                    "fit": "Medium-High (7/10)"  # Using 'fit' not 'fit_score'
                }
            ]
        }
        
        # Run validation
        validation = validate_buyer_profiles_slide(test_slide, test_content_ir)
        
        print(f"✅ Validation results:")
        print(f"   Issues: {validation.get('issues', [])}")
        print(f"   Warnings: {validation.get('warnings', [])}")
        print(f"   Missing fields: {validation.get('missing_fields', [])}")
        print(f"   Empty fields: {validation.get('empty_fields', [])}")
        
        # Check if fit_score error is gone
        has_fit_score_errors = any('fit_score' in str(error) for error in validation.get('empty_fields', []))
        
        if has_fit_score_errors:
            print("❌ Still has fit_score validation errors!")
            return False
        else:
            print("✅ No more fit_score validation errors!")
            return True
            
    except Exception as e:
        print(f"❌ Error testing buyer validation: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_buyer_validation()
    if success:
        print("\n🎉 Buyer validation fix successful! The fit_score errors should be resolved.")
    else:
        print("\n❌ Buyer validation fix needs more work.")