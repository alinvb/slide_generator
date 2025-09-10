#!/usr/bin/env python3
"""
Test script to verify the fixed topic progression logic
"""

import sys
sys.path.append('/home/user/webapp')

from app import analyze_conversation_progress

def test_fixed_progression():
    print("🔍 Testing Fixed Topic Progression Logic")
    print("=" * 60)
    
    # Simulate the exact conversation from user where SWOT was incorrectly asked
    messages = [
        {"role": "system", "content": "System prompt here"},
        {"role": "assistant", "content": "What is your company name and give me a brief overview of what your business does?"},
        {"role": "user", "content": "Saudi Aramco is a major oil and gas company based in Saudi Arabia."},
        {"role": "assistant", "content": "Now let's discuss your product/service footprint. What are your main offerings?"},
        {"role": "user", "content": "We offer oil extraction, refining, and petrochemicals across multiple countries."},
        {"role": "assistant", "content": "Let's analyze your historical financial performance. Can you provide revenue, EBITDA, margins for the last 3-5 years?"},
        {"role": "user", "content": "Our revenue was $400B in 2023, $350B in 2022, with EBITDA margins around 45%."}
    ]
    
    print("📊 Analyzing conversation progress after completing first 3 topics...")
    progress_info = analyze_conversation_progress(messages)
    
    print(f"🎯 Expected Next Topic: {progress_info.get('next_topic', 'UNKNOWN')}")
    print(f"📝 Next Question: {progress_info.get('next_question', 'NONE')[:100]}...")
    
    # Check if it correctly identifies management_team as next
    if progress_info.get('next_topic') == 'management_team':
        print("✅ SUCCESS: System correctly identifies management_team as next topic")
        print("✅ This should fix the SWOT issue!")
    else:
        print("❌ STILL BROKEN: System does not identify management_team as next topic")
        
        # Show what topics are covered
        print("\n📋 Topic Coverage Analysis:")
        for topic_name, topic_info in progress_info.get('topics', {}).items():
            covered = topic_info.get('covered', False)
            position = topic_info.get('position', 0)
            status = "✅ COVERED" if covered else "❌ NOT COVERED"
            print(f"  {position:2d}. {topic_name:<30} {status}")

if __name__ == "__main__":
    test_fixed_progression()