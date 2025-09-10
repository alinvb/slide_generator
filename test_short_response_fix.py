#!/usr/bin/env python3

"""
Test the fix for topic completion detection with short responses.
This tests that short but valid company names like "prypco" are now accepted.
"""

import sys
import os
sys.path.append('/home/user/webapp')

from app import analyze_conversation_progress

def test_short_company_name():
    """Test that short company names now work for topic completion"""
    
    print("🧪 Testing short company name progression...")
    
    # Simulate conversation with short company name "prypco"
    messages = [
        {"role": "system", "content": "You are an investment banking copilot."},
        {"role": "assistant", "content": "What is your company name and give me a brief overview of what your business does?"},
        {"role": "user", "content": "prypco"},  # This is only 6 characters - should now work
        {"role": "user", "content": "next topic"}
    ]
    
    print(f"📋 Test conversation:")
    for i, msg in enumerate(messages[1:], 1):  # Skip system message
        print(f"  {i}. {msg['role']}: {msg['content']}")
    
    # Analyze progress
    progress = analyze_conversation_progress(messages)
    
    print(f"\n📊 Results:")
    print(f"  Current topic: {progress['current_topic']}")
    print(f"  Topics completed: {progress['topics_covered']}")
    print(f"  Completion percentage: {progress['completion_percentage']:.1%}")
    
    # Check if it progresses to topic 2
    if progress['topics_covered'] >= 1 and progress['current_topic'] == 'product_service_footprint':
        print("✅ SUCCESS: Short company name 'prypco' now allows topic progression!")
        print("✅ The conversation loop issue should be fixed!")
        return True
    else:
        print("❌ FAILURE: Short company name still blocking progression")
        print(f"❌ Expected: topics_covered >= 1 and current_topic == 'product_service_footprint'")
        print(f"❌ Got: topics_covered = {progress['topics_covered']}, current_topic = '{progress['current_topic']}'")
        return False

def test_various_short_names():
    """Test other short but valid company names"""
    
    print("\n🧪 Testing various short company names...")
    
    short_names = ["Apple", "Meta", "Nike", "Sony", "Dell", "IBM", "HP"]
    
    for name in short_names:
        messages = [
            {"role": "system", "content": "You are an investment banking copilot."},
            {"role": "assistant", "content": "What is your company name and give me a brief overview of what your business does?"},
            {"role": "user", "content": name},
            {"role": "user", "content": "next topic"}
        ]
        
        progress = analyze_conversation_progress(messages)
        
        status = "✅" if progress['topics_covered'] >= 1 else "❌"
        print(f"  {status} '{name}' (len={len(name)}): {progress['topics_covered']} topics completed")

if __name__ == "__main__":
    print("🔧 Testing Fix for Short Response Topic Completion")
    print("=" * 60)
    
    success = test_short_company_name()
    test_various_short_names()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 FIX CONFIRMED: Short company names now work!")
        print("🚀 The conversation loop issue should be resolved!")
    else:
        print("⚠️  Fix may need additional adjustments")