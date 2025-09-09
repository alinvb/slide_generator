#!/usr/bin/env python3
"""
Test the topic completion fix for Netflix conversation
"""

import sys
sys.path.append('/home/user/webapp')

from app import analyze_conversation_progress

def test_completion_fix():
    print("🔍 Testing Topic Completion Fix for Netflix")
    print("=" * 60)
    
    # The EXACT conversation from user where topics weren't completing
    messages = [
        {"role": "system", "content": "Investment banking system prompt..."},
        {"role": "assistant", "content": "What is your company name and give me a brief overview of what your business does?"},
        {"role": "user", "content": "Netflix - leading streaming service"},
        {"role": "assistant", "content": "Now let's discuss your product/service footprint..."},
        {"role": "user", "content": "research this yourself"},
        {"role": "assistant", "content": "Netflix's ability to deliver timely, culturally relevant, and genre-spanning content has solidified its status as the leading streaming service globally, with a strong presence in both original production and content licensing[2][4][5]. Are you satisfied with this research, or would you like me to investigate any specific areas further?"},
        {"role": "user", "content": "ok"},
        {"role": "assistant", "content": "Let's analyze your historical financial performance..."},
        {"role": "user", "content": "research this yourself"},
        {"role": "assistant", "content": "Netflix's historical financial performance from 2021 to 2025 demonstrates robust growth, expanding margins, and evolving revenue streams. Annual Revenue (USD millions): 2021: ~$29,700, 2022: ~$31,600, 2023: $33,720, 2024: $39,000, 2025 (forecast): $44,800–$45,200. Revenue Growth Rate: 2023 to 2024: 15.6%, 2024 to 2025 (forecast): ~15–16%. Operating income $7,121.7 million for H1 2025. Operating Margin: 34% (up 7 percentage points YoY). Key Performance Drivers: Subscriber Growth, Ads Revenue expansion, Content Slate hits, Currency Effects. Main Revenue Streams: Subscription Revenue (dominant), Advertising Revenue (growing rapidly since 2023–2024). Are you satisfied with this research, or would you like me to investigate any specific areas further?"},
        {"role": "user", "content": "ok"}
    ]
    
    print("📊 Analyzing conversation progress after extensive financial research...")
    progress_info = analyze_conversation_progress(messages)
    
    print(f"🎯 Current Topic: {progress_info.get('current_topic', 'UNKNOWN')}")
    print(f"🎯 Next Topic: {progress_info.get('next_topic', 'UNKNOWN')}")
    
    print("\n📋 Topics Coverage Status:")
    topics_info = progress_info.get('topics', {})
    
    critical_topics = ['business_overview', 'product_service_footprint', 'historical_financial_performance', 'management_team']
    
    for topic_name in critical_topics:
        if topic_name in topics_info:
            covered = topics_info[topic_name].get('covered', False)
            position = topics_info[topic_name].get('position', 0)
            status = "✅ COVERED" if covered else "❌ NOT COVERED"
            print(f"  {position}. {topic_name:<35} {status}")
            
            if not covered and position <= 3:
                print(f"     🔍 DEBUG: Why not covered?")
                # Show topic keywords found for debugging
                
    # Check what should happen next
    expected_behaviors = [
        (topics_info.get('business_overview', {}).get('covered', False), "business_overview should be covered"),
        (topics_info.get('product_service_footprint', {}).get('covered', False), "product_service_footprint should be covered"), 
        (topics_info.get('historical_financial_performance', {}).get('covered', False), "historical_financial_performance should be covered"),
        (progress_info.get('next_topic') == 'management_team', "next topic should be management_team")
    ]
    
    print(f"\n🧪 Test Results:")
    all_passed = True
    for condition, description in expected_behaviors:
        status = "✅ PASS" if condition else "❌ FAIL"
        print(f"  {status}: {description}")
        if not condition:
            all_passed = False
            
    if all_passed:
        print(f"\n🎉 SUCCESS: All topics marked complete correctly!")
        print(f"📝 Next Question: {progress_info.get('next_question', 'NONE')[:100]}...")
    else:
        print(f"\n💔 STILL BROKEN: Topic completion detection needs more work")

if __name__ == "__main__":
    test_completion_fix()