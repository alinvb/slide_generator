#!/usr/bin/env python3
"""
Final Validation Test - Validate that everything is working properly
"""
import sys
import os
import json
from pathlib import Path

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_minimal_slide_generation():
    """Test with minimal but valid data"""
    print("🧪 Testing Minimal Slide Generation...")
    
    try:
        from executor import execute_plan
        
        # Create minimal valid test data
        minimal_content_ir = {
            "entities": {"company": {"name": "Test Company"}},
            "facts": {
                "years": ["2021", "2022", "2023"],
                "revenue_usd_m": [100, 120, 150],
                "ebitda_usd_m": [20, 25, 30],
                "ebitda_margins": [20.0, 20.8, 20.0]
            },
            "management_team": {
                "left_column_profiles": [{
                    "role_title": "CEO", 
                    "experience_bullets": ["Test experience"]
                }],
                "right_column_profiles": [{
                    "role_title": "CTO", 
                    "experience_bullets": ["Test experience"]
                }]
            }
        }
        
        minimal_render_plan = {
            "slides": [
                {
                    "template": "business_overview",
                    "data": {
                        "title": "Business Overview",
                        "description": "Test company description",
                        "highlights": ["Test highlight 1", "Test highlight 2", "Test highlight 3"],
                        "services": ["Test service 1", "Test service 2", "Test service 3"],
                        "positioning_desc": "Test positioning description"
                    }
                }
            ]
        }
        
        # Test execution - pass the render_plan directly as expected
        print("  🚀 Executing slide generation...")
        result = execute_plan(
            content_ir=minimal_content_ir,
            render_plan=minimal_render_plan,  # This should have 'slides' key
            output_file='final_test.pptx'
        )
        
        if result and Path('final_test.pptx').exists():
            file_size = Path('final_test.pptx').stat().st_size
            print(f"  ✅ Minimal slide generation: PASSED ({file_size} bytes)")
            
            # Clean up
            Path('final_test.pptx').unlink()
            return True
        else:
            print("  ❌ Minimal slide generation: FAILED - No output file")
            return False
        
    except Exception as e:
        print(f"  ❌ Minimal slide generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_json_repair_improvements():
    """Test improved JSON repair function"""
    print("🧪 Testing Improved JSON Repair...")
    
    try:
        import app
        
        # Test cases that should now work
        test_cases = [
            ('{"test": "value"}extra text', "Valid JSON with extra text"),
            ('{"a": 1,}', "Trailing comma"),
            ('```json\n{"valid": true}\n```', "Code blocks"),
        ]
        
        success_count = 0
        for test_json, description in test_cases:
            try:
                cleaned = app.clean_json_string(test_json)
                parsed = json.loads(cleaned)
                print(f"  ✅ {description}: PASSED")
                success_count += 1
            except Exception as e:
                print(f"  ❌ {description}: FAILED - {e}")
        
        print(f"✅ JSON Repair: {success_count}/{len(test_cases)} tests passed")
        return success_count >= len(test_cases) * 0.8  # 80% success rate acceptable
        
    except Exception as e:
        print(f"❌ JSON repair test failed: {e}")
        return False

def test_critical_slide_templates():
    """Test the most critical slide templates that users rely on"""
    print("🧪 Testing Critical Slide Templates...")
    
    try:
        from slide_templates import (
            render_business_overview_slide,
            render_competitive_positioning_slide,
            render_buyer_profiles_slide,
            render_investor_process_overview_slide
        )
        from pptx import Presentation
        
        prs = Presentation()
        
        # Test business overview (most critical)
        business_data = {
            'title': 'Business Overview',
            'description': 'Test company',
            'highlights': ['H1', 'H2', 'H3'],
            'services': ['S1', 'S2', 'S3'],
            'positioning_desc': 'Test positioning'
        }
        
        slide = render_business_overview_slide(data=business_data, prs=prs)
        if not slide:
            print("  ❌ Business overview: FAILED")
            return False
        print("  ✅ Business overview: PASSED")
        
        # Test competitive positioning (recently enhanced)
        comp_data = {
            'title': 'Competitive Positioning',
            'competitors': [{'name': 'A', 'revenue': 100}],
            'assessment': [
                ['Company', 'Market Share', 'Tech Platform', 'Coverage', 'Revenue (M)'],
                ['Us', '⭐⭐⭐⭐', '⭐⭐⭐⭐⭐', '⭐⭐⭐⭐', '$150M']
            ],
            'advantages': [{'title': 'Adv1', 'desc': 'Desc1'}],
            'barriers': [{'title': 'Bar1', 'desc': 'Desc1'}]
        }
        
        slide = render_competitive_positioning_slide(data=comp_data, prs=prs)
        if not slide:
            print("  ❌ Competitive positioning: FAILED")
            return False
        print("  ✅ Competitive positioning: PASSED")
        
        # Test buyer profiles (recently fixed)
        buyer_data = {
            'title': 'Buyers',
            'table_headers': ['Name', 'Desc', 'Rationale', 'Synergies', 'Fit'],
            'table_rows': [{
                'buyer_name': 'Test Buyer',
                'description': 'Test desc',
                'strategic_rationale': 'Test rationale',
                'key_synergies': 'Test synergies',
                'fit': 'High (9/10)'
            }]
        }
        
        slide = render_buyer_profiles_slide(data=buyer_data, prs=prs)
        if not slide:
            print("  ❌ Buyer profiles: FAILED")
            return False
        print("  ✅ Buyer profiles: PASSED")
        
        # Test investor process overview (recently enhanced)
        process_data = {
            'title': 'Investment Process',
            'diligence_topics': ['Topic1', 'Topic2'],
            'synergy_opportunities': ['Syn1', 'Syn2'],
            'risk_factors': ['Risk1', 'Risk2'],
            'mitigants': ['Mit1', 'Mit2'],
            'timeline': [
                {'date': 'Week 1-2', 'description': 'Initial outreach'},
                {'date': 'Week 3-4', 'description': 'Management presentations'}
            ]
        }
        
        slide = render_investor_process_overview_slide(data=process_data, prs=prs)
        if not slide:
            print("  ❌ Investment process: FAILED")
            return False
        print("  ✅ Investment process: PASSED")
        
        print("✅ Critical Slide Templates: All tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Critical slide templates test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run final validation"""
    print("🎯 FINAL SYSTEM VALIDATION")
    print("=" * 60)
    print("Testing core functionality that users depend on...")
    
    tests = [
        ("Minimal Slide Generation", test_minimal_slide_generation),
        ("JSON Repair Improvements", test_json_repair_improvements),
        ("Critical Slide Templates", test_critical_slide_templates),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            if result:
                passed += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"💥 {test_name}: CRASHED - {e}")
    
    print(f"\n{'='*60}")
    print("📊 FINAL VALIDATION RESULTS")
    print(f"{'='*60}")
    print(f"🎯 RESULT: {passed}/{total} critical tests passed")
    
    if passed == total:
        print("✅ SYSTEM IS FULLY OPERATIONAL")
        print("🚀 All critical functionality is working correctly")
        print("📈 Users can proceed with confidence")
        return True
    else:
        print("⚠️ SOME CRITICAL ISSUES DETECTED")
        print("🔧 Please review failed tests before proceeding")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)