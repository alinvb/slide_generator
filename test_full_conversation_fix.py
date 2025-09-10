#!/usr/bin/env python3

"""
Test the complete conversation flow after fixing the short response issue.
This simulates the exact scenario the user reported.
"""

import sys
import os
sys.path.append('/home/user/webapp')

from app import analyze_conversation_progress

def test_user_reported_scenario():
    """Test the exact scenario the user reported with 'prypco' and 'next topic'"""
    
    print("🧪 Testing User-Reported Scenario...")
    print("=" * 60)
    
    # Simulate the exact conversation flow the user reported
    messages = [
        {"role": "system", "content": "You are an investment banking copilot."},
        {"role": "assistant", "content": "What is your company name and give me a brief overview of what your business does?"},
        {"role": "user", "content": "prypco"},  # User's exact response
        {"role": "user", "content": "next topic"}  # User says next topic
    ]
    
    print("📋 Conversation Flow:")
    for i, msg in enumerate(messages[1:], 1):
        print(f"  {i}. {msg['role']}: '{msg['content']}'")
    
    # Analyze what happens
    progress = analyze_conversation_progress(messages)
    
    print(f"\n📊 Analysis Results:")
    print(f"  🎯 Current Topic: {progress['current_topic']}")
    print(f"  ✅ Topics Completed: {progress['topics_covered']} / {progress['applicable_topics']}")
    print(f"  📈 Progress: {progress['completion_percentage']:.1%}")
    
    # Check if the issue is fixed
    if progress['current_topic'] == 'product_service_footprint' and progress['topics_covered'] >= 1:
        print("\n🎉 SUCCESS: Conversation Loop FIXED!")
        print("✅ System correctly progresses from topic 1 → topic 2")
        print("✅ Short company names no longer cause loops")
        return True
    else:
        print(f"\n❌ ISSUE: Still stuck or incorrect progression")
        print(f"Expected: current_topic='product_service_footprint', topics_covered >= 1")
        print(f"Got: current_topic='{progress['current_topic']}', topics_covered={progress['topics_covered']}")
        return False

def test_full_progression():
    """Test progression through multiple topics"""
    
    print("\n🧪 Testing Multi-Topic Progression...")
    print("=" * 60)
    
    # Simulate progression through first few topics
    messages = [
        {"role": "system", "content": "You are an investment banking copilot."},
        
        # Topic 1: Business Overview
        {"role": "assistant", "content": "What is your company name and give me a brief overview of what your business does?"},
        {"role": "user", "content": "prypco"},
        {"role": "user", "content": "next topic"},
        
        # Topic 2: Product/Service Footprint  
        {"role": "assistant", "content": "Now let's discuss your product/service footprint. What are your main offerings?"},
        {"role": "user", "content": "SaaS platform"},
        {"role": "user", "content": "next topic"},
        
        # Topic 3: Historical Financial Performance
        {"role": "assistant", "content": "Let's analyze your historical financial performance. Can you provide your revenue, EBITDA, margins?"},
        {"role": "user", "content": "$5M revenue"},
        {"role": "user", "content": "next topic"}
    ]
    
    print("📋 Multi-Topic Conversation:")
    assistant_count = 0
    for i, msg in enumerate(messages[1:], 1):
        if msg['role'] == 'assistant':
            assistant_count += 1
            print(f"  {i}. AI Topic {assistant_count}: {msg['content'][:80]}...")
        else:
            print(f"  {i}. User: '{msg['content']}'")
    
    # Analyze final progress
    progress = analyze_conversation_progress(messages)
    
    print(f"\n📊 Multi-Topic Results:")
    print(f"  🎯 Current Topic: {progress['current_topic']}")
    print(f"  ✅ Topics Completed: {progress['topics_covered']} / {progress['applicable_topics']}")
    print(f"  📈 Progress: {progress['completion_percentage']:.1%}")
    
    # Should have completed 3 topics, be asking topic 4 (management_team)
    expected_completed = 3
    expected_current = "management_team"
    
    if progress['topics_covered'] >= expected_completed and progress['current_topic'] == expected_current:
        print("\n🎉 SUCCESS: Multi-topic progression works!")
        print("✅ System correctly handles sequential topic advancement")
        return True
    else:
        print(f"\n⚠️  PARTIAL: Progression may need adjustment")
        print(f"Expected: {expected_completed} topics completed, current='{expected_current}'")
        print(f"Got: {progress['topics_covered']} topics completed, current='{progress['current_topic']}'")
        return False

if __name__ == "__main__":
    print("🔧 Testing Complete Conversation Flow After Fix")
    print("=" * 80)
    
    # Test the user's exact scenario
    scenario_fixed = test_user_reported_scenario()
    
    # Test multi-topic progression
    progression_works = test_full_progression()
    
    print("\n" + "=" * 80)
    print("🎯 FINAL RESULTS:")
    
    if scenario_fixed and progression_works:
        print("🎉 ALL TESTS PASSED: Conversation loop issue is FIXED!")
        print("✅ Short company names work correctly")
        print("✅ Topic progression functions properly") 
        print("✅ The system should no longer get stuck asking the same question")
    elif scenario_fixed:
        print("✅ PRIMARY ISSUE FIXED: Short response loop resolved")
        print("⚠️  Multi-topic flow may need minor adjustments")
    else:
        print("❌ CRITICAL: Primary issue still exists")
        print("❌ Additional debugging may be required")