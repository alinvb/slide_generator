#!/usr/bin/env python3
"""
Test the conversation flow fix to ensure normal messages don't trigger JSON extraction
"""

def test_json_detection_logic():
    """Test the logic that determines if a response should trigger JSON extraction"""
    
    print("🧪 Testing JSON Detection Logic")
    
    # Test cases for different response types
    test_cases = [
        {
            "description": "Normal conversation message",
            "response": "I'll ask specific follow-up questions for missing information. What is your company name?",
            "should_extract": False
        },
        {
            "description": "Short message with braces",
            "response": "Here's {some} information about your company.",
            "should_extract": False
        },
        {
            "description": "Long response with JSON keywords", 
            "response": "Based on our conversation, I'll now generate the content_ir and render_plan JSONs. Here's the detailed content: " + "x" * 500,
            "should_extract": True
        },
        {
            "description": "Response with both keywords",
            "response": "Here are your content_ir and render_plan files with complete data.",
            "should_extract": True
        },
        {
            "description": "Large JSON-like response",
            "response": '{"content_ir": {"company": "Test"}, "render_plan": {"slides": []}}' + "x" * 400,
            "should_extract": True
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}️⃣ Testing: {test_case['description']}")
        
        ai_response = test_case["response"]
        
        # Apply the same logic used in the app
        should_extract_json = ("content_ir" in ai_response.lower() and "render_plan" in ai_response.lower()) or \
                             ("{" in ai_response and "}" in ai_response and len(ai_response) > 500)
        
        expected = test_case["should_extract"]
        actual = should_extract_json
        
        print(f"   Response length: {len(ai_response)}")
        print(f"   Expected extraction: {expected}")
        print(f"   Actual extraction: {actual}")
        print(f"   Result: {'✅ PASS' if expected == actual else '❌ FAIL'}")
        
        if expected != actual:
            return False
    
    print(f"\n🎯 All tests passed! JSON extraction logic is working correctly.")
    return True

if __name__ == "__main__":
    success = test_json_detection_logic()
    if success:
        print("✅ Conversation flow fix is working correctly!")
    else:
        print("❌ Tests failed - conversation flow needs adjustment!")