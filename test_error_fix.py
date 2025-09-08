#!/usr/bin/env python3
"""
Test the AttributeError fix for None render_plan
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import validate_and_fix_json, extract_and_validate_jsons

def test_none_handling():
    """Test that the functions handle None values correctly"""
    
    print("🧪 Testing None Handling in JSON Functions")
    
    # Test 1: Both None
    print("\n1️⃣ Testing validate_and_fix_json with both None")
    result1 = validate_and_fix_json(None, None)
    print(f"Result: {result1}")
    assert result1 == (None, None), "Should return (None, None) for both None inputs"
    
    # Test 2: Only render_plan None
    print("\n2️⃣ Testing validate_and_fix_json with render_plan=None")
    result2 = validate_and_fix_json({"some": "data"}, None)
    print(f"Result: {result2}")
    assert result2 == (None, None), "Should return (None, None) when render_plan is None"
    
    # Test 3: Only content_ir None
    print("\n3️⃣ Testing validate_and_fix_json with content_ir=None")
    result3 = validate_and_fix_json(None, {"some": "data"})
    print(f"Result: {result3}")
    assert result3 == (None, None), "Should return (None, None) when content_ir is None"
    
    # Test 4: Invalid response text
    print("\n4️⃣ Testing extract_and_validate_jsons with invalid response")
    result4 = extract_and_validate_jsons("This is not a JSON response")
    content_ir, render_plan, validation_results = result4
    print(f"Content IR: {content_ir}")
    print(f"Render Plan: {render_plan}")
    print(f"Validation passed: {validation_results is not None}")
    
    print("\n✅ ALL TESTS PASSED - Error handling is working correctly!")
    return True

if __name__ == "__main__":
    try:
        test_none_handling()
    except Exception as e:
        print(f"❌ TEST FAILED: {e}")
        sys.exit(1)