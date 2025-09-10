#!/usr/bin/env python3

def test_conversation_loop_fix():
    """Test that the conversation loop is fixed and topics advance properly"""
    
    print("🧪 TESTING CONVERSATION LOOP FIX")
    print("=" * 50)
    
    # Test the exact scenario that was causing the loop
    messages = [
        {"role": "assistant", "content": "What is your company name and give me a brief overview of what your business does?"},
        {"role": "user", "content": "prypco"},  # Topic 1 response
        {"role": "assistant", "content": "PRYPCO, founded in 2022 by Amira Sajwani..."},  # Research response
        {"role": "user", "content": "next topic"}  # This should advance to topic 2, not loop back!
    ]
    
    from app import analyze_conversation_progress
    
    result = analyze_conversation_progress(messages)
    
    print("=== CONVERSATION ANALYSIS ===")
    print(f"✅ Messages processed: {len(messages)}")
    print(f"✅ Topics completed: {result.get('topics_completed', 'ERROR')}")
    print(f"✅ Current position: {result.get('current_position', 'ERROR')}")
    print(f"✅ Current topic: {result.get('current_topic', 'ERROR')}")
    
    # Check the next question - it should be about product/service footprint (topic 2)
    next_question = result.get('next_question', '')
    print(f"✅ Next question preview: {next_question[:100]}...")
    
    # CRITICAL TESTS
    print("\n=== CRITICAL VALIDATIONS ===")
    
    # Test 1: Should be at position 2 (product footprint)
    if result.get('current_position') == 2:
        print("✅ PASS: Correctly at position 2")
        test1_pass = True
    else:
        print(f"❌ FAIL: At position {result.get('current_position')}, should be 2")
        test1_pass = False
    
    # Test 2: Should be asking about product/service footprint 
    if 'product' in result.get('current_topic', '') and 'service' in result.get('current_topic', ''):
        print("✅ PASS: Correctly asking about product/service footprint")
        test2_pass = True
    else:
        print(f"❌ FAIL: Asking about '{result.get('current_topic')}', should be 'product_service_footprint'")
        test2_pass = False
        
    # Test 3: Next question should NOT be the first question
    if "company name" not in next_question.lower():
        print("✅ PASS: Not looping back to first question")
        test3_pass = True
    else:
        print("❌ FAIL: Still showing company name question - loop not fixed!")
        test3_pass = False
        
    # Test 4: Next question should be about products/services
    if "product" in next_question.lower() or "service" in next_question.lower():
        print("✅ PASS: Next question is about products/services")
        test4_pass = True
    else:
        print(f"❌ FAIL: Next question is not about products/services")
        test4_pass = False
    
    # Overall result
    all_pass = test1_pass and test2_pass and test3_pass and test4_pass
    
    print("\n" + "=" * 50)
    if all_pass:
        print("🎉 ALL TESTS PASSED - CONVERSATION LOOP FIXED!")
        print("\n📋 VERIFIED FIXES:")
        print("✅ Topic progression works correctly (1 → 2)")
        print("✅ 'next topic' advances instead of looping")  
        print("✅ Research responses count as topic completion")
        print("✅ Next question is appropriate for current topic")
        return True
    else:
        print("❌ SOME TESTS FAILED - Issues remain")
        failed_tests = []
        if not test1_pass: failed_tests.append("Position tracking")
        if not test2_pass: failed_tests.append("Topic identification") 
        if not test3_pass: failed_tests.append("Loop prevention")
        if not test4_pass: failed_tests.append("Question appropriateness")
        print(f"   Failed areas: {', '.join(failed_tests)}")
        return False

if __name__ == "__main__":
    success = test_conversation_loop_fix()
    
    print(f"\n🔗 FIXED SERVICE URL: https://8501-i1igkppq2hiu9o5h7uppm-6532622b.e2b.dev")
    if success:
        print("🚀 Ready to test! The conversation loop should now be fixed.")
        print("\n📋 TEST STEPS:")
        print("1. Go to the service URL above")
        print("2. Start with: 'prypco' (or any company)")
        print("3. Wait for research response")
        print("4. Say: 'next topic'")
        print("5. ✅ Should ask about product/service footprint, NOT loop back!")
    else:
        print("⚠️  Issues detected - may need further investigation")
        
    print(f"\n🔗 PULL REQUEST: https://github.com/alinvb/slide_generator/pull/6")
    print("   ↳ Latest fixes committed and deployed")