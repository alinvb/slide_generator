#!/usr/bin/env python3
"""
Test the simple interview integration in main app
"""

import sys
sys.path.append('/home/user/webapp')

from app import analyze_conversation_progress

def test_simple_integration():
    print("🔍 Testing Simple Integration in Main App")
    print("=" * 60)
    
    # Netflix conversation that was causing issues
    messages = [
        {"role": "system", "content": "System prompt"},
        {"role": "assistant", "content": "What is your company name and give me a brief overview of what your business does?"},
        {"role": "user", "content": "Netflix - streaming service"},
        {"role": "assistant", "content": "Now let's discuss your product/service footprint..."},
        {"role": "user", "content": "research this yourself"},
        {"role": "assistant", "content": "Netflix's ability to deliver timely, culturally relevant content... Are you satisfied with this research, or would you like me to investigate any specific areas further?"},
        {"role": "user", "content": "ok"},
        {"role": "assistant", "content": "Let's analyze your historical financial performance..."},
        {"role": "user", "content": "research this yourself"},  
        {"role": "assistant", "content": "Netflix's historical financial performance from 2021 to 2025... Are you satisfied with this research, or would you like me to investigate any specific areas further?"},
        {"role": "user", "content": "ok"}
    ]
    
    print("📊 Analyzing Netflix conversation with simple logic...")
    result = analyze_conversation_progress(messages)
    
    print(f"\n🎯 Results:")
    print(f"  Current Topic: {result.get('current_topic')}")
    print(f"  Next Topic: {result.get('next_topic')}")  
    print(f"  Topics Completed: {result.get('topics_completed')}")
    print(f"  Current Position: {result.get('current_position')}")
    print(f"  Is Complete: {result.get('is_complete')}")
    print(f"  Next Question: {result.get('next_question', 'None')[:100]}...")
    
    # Expected: Should be asking management team (topic 4) after completing 3 topics
    expected_behaviors = [
        (result.get('topics_completed') == 3, "Should have 3 topics completed"),
        (result.get('current_topic') == 'management_team', "Current topic should be management_team"),
        (result.get('current_position') == 4, "Should be at position 4"),
        ("management team" in result.get('next_question', '').lower(), "Next question should be about management team")
    ]
    
    print(f"\n🧪 Test Results:")
    all_passed = True
    for condition, description in expected_behaviors:
        status = "✅ PASS" if condition else "❌ FAIL"
        print(f"  {status}: {description}")
        if not condition:
            all_passed = False
            
    if all_passed:
        print(f"\n🎉 SUCCESS: Simple integration works perfectly!")
        print(f"✅ Netflix will now correctly ask about management team instead of repeating financial performance")
    else:
        print(f"\n💔 FAILED: Integration needs adjustment")
        
    return result

if __name__ == "__main__":
    test_simple_integration()