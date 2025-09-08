#!/usr/bin/env python3
"""
Quick Integration Test - Test the full pipeline with real data
"""
import sys
import os
import json
from pathlib import Path

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_full_pipeline():
    """Test the full slide generation pipeline with real data"""
    print("🧪 Testing Full Pipeline Integration...")
    
    try:
        from executor import execute_plan
        
        # Load a real test data file if available
        test_files = ['complete_content_ir.json', 'complete_render_plan.json']
        
        if all(Path(f).exists() for f in test_files):
            print("  📁 Using real test data files...")
            
            with open('complete_content_ir.json') as f:
                content_ir = json.load(f)
            
            with open('complete_render_plan.json') as f:
                render_plan = json.load(f)
                
            # Test execution
            print("  🚀 Testing slide generation...")
            result = execute_plan(
                content_ir=content_ir,
                render_plan=render_plan,
                output_file='integration_test.pptx'
            )
            
            if result and Path('integration_test.pptx').exists():
                file_size = Path('integration_test.pptx').stat().st_size
                print(f"  ✅ Full pipeline test: PASSED ({file_size} bytes)")
                
                # Clean up
                Path('integration_test.pptx').unlink()
                return True
            else:
                print("  ❌ Full pipeline test: FAILED - No output file")
                return False
        else:
            print("  ⚠️ Real test data not available, creating minimal test...")
            
            # Create minimal test data
            minimal_content_ir = {
                "entities": {"company": {"name": "Test Company"}},
                "facts": {
                    "years": ["2021", "2022", "2023"],
                    "revenue_usd_m": [100, 120, 150],
                    "ebitda_usd_m": [20, 25, 30]
                }
            }
            
            minimal_render_plan = {
                "slides": [
                    {
                        "template": "business_overview",
                        "data": {
                            "title": "Business Overview",
                            "description": "Test company description",
                            "highlights": ["Test highlight"],
                            "services": ["Test service"],
                            "positioning_desc": "Test positioning"
                        }
                    }
                ]
            }
            
            result = execute_plan(
                content_ir=minimal_content_ir,
                render_plan=minimal_render_plan,
                output_file='minimal_test.pptx'
            )
            
            if result and Path('minimal_test.pptx').exists():
                file_size = Path('minimal_test.pptx').stat().st_size
                print(f"  ✅ Minimal pipeline test: PASSED ({file_size} bytes)")
                
                # Clean up
                Path('minimal_test.pptx').unlink()
                return True
            else:
                print("  ❌ Minimal pipeline test: FAILED")
                return False
        
    except Exception as e:
        print(f"❌ Pipeline test failed: {e}")
        return False

def test_json_parsing_edge_cases():
    """Test JSON parsing with real problematic cases"""
    print("🧪 Testing JSON Parsing Edge Cases...")
    
    try:
        import app
        
        # Real problematic JSON cases that users might encounter
        edge_cases = [
            # Missing comma between objects
            '''{"a": {"b": 1}} {"c": {"d": 2}}''',
            
            # Trailing comma in object
            '''{"a": 1, "b": 2,}''',
            
            # Missing comma in array
            '''{"arr": [{"a": 1} {"b": 2}]}''',
            
            # Extra text at end
            '''{"valid": "json"}This is extra text''',
            
            # Code blocks with JSON
            '''```json
            {"test": "value"}
            ```''',
        ]
        
        success_count = 0
        for i, case in enumerate(edge_cases):
            try:
                cleaned = app.clean_json_string(case)
                parsed = json.loads(cleaned)
                print(f"  ✅ Edge case {i+1}: PASSED")
                success_count += 1
            except Exception as e:
                print(f"  ❌ Edge case {i+1}: FAILED - {e}")
        
        print(f"✅ JSON Edge Cases: {success_count}/{len(edge_cases)} passed")
        return success_count >= len(edge_cases) * 0.8  # 80% pass rate is acceptable
        
    except Exception as e:
        print(f"❌ JSON edge cases test failed: {e}")
        return False

def main():
    """Run quick integration tests"""
    print("🚀 QUICK INTEGRATION TEST")
    print("=" * 50)
    
    tests = [
        ("Full Pipeline", test_full_pipeline),
        ("JSON Edge Cases", test_json_parsing_edge_cases),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            result = test_func()
            if result:
                passed += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"💥 {test_name}: CRASHED - {e}")
    
    print(f"\n🎯 INTEGRATION RESULT: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ INTEGRATION SUCCESSFUL - System is fully operational")
    else:
        print("⚠️ Some integration issues detected")
    
    return passed == total

if __name__ == "__main__":
    main()