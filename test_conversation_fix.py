#!/usr/bin/env python3

"""
Test the fixed conversation analysis logic
"""

import sys
sys.path.append('/home/user/webapp')
from app import analyze_conversation_progress

def test_conversation_fix():
    """Test the conversation that was causing issues"""
    
    print("🧪 TESTING FIXED CONVERSATION ANALYSIS")
    print("=" * 50)
    
    # Actual conversation from user's report
    messages = [
        {
            "role": "assistant",
            "content": "What is your company name and give me a brief overview of what your business does?"
        },
        {
            "role": "user", 
            "content": "Nvidia"
        },
        {
            "role": "assistant",
            "content": "Now let's discuss your product/service footprint. What are your main offerings? Please provide the title and description for each product/service. Also, where do you operate geographically and what's your market coverage?"
        },
        {
            "role": "user",
            "content": "research this for me"
        },
        {
            "role": "assistant",
            "content": "Nvidia is the global leader in AI semiconductors, commanding unmatched market share and growth metrics due to soaring demand for its data center and AI products. Its strategic positioning and technological leadership have propelled its market capitalization past $4 trillion in 2025, underscoring its dominance and relevance in the semiconductor industry. Very long research content here with detailed analysis, financial metrics, competitive positioning, and comprehensive market data that exceeds 200 characters easily."
        },
        {
            "role": "user",
            "content": "next topic"
        },
        {
            "role": "assistant",
            "content": "Let's analyze your historical financial performance. Can you provide your revenue, EBITDA, margins, and key financial metrics for the last 3-5 years? I need specific numbers: annual revenue in USD millions, EBITDA figures, margin percentages, growth rates, and key performance drivers. What are the main revenue streams and how have they evolved?"
        },
        {
            "role": "user",
            "content": "research this for me"
        }
    ]
    
    print("📝 Testing conversation with 8 messages...")
    result = analyze_conversation_progress(messages)
    
    print(f"\n📊 RESULTS:")
    print(f"   Topics completed: {result['topics_completed']}")
    print(f"   Current topic: {result['current_topic']}")
    print(f"   Current position: {result['current_position']}")
    
    # Expected: 2 topics completed (business_overview + product_service_footprint)
    # Should be asking for topic 3 (historical_financial_performance)
    if result['topics_completed'] == 2 and result['current_topic'] == 'historical_financial_performance':
        print("\n✅ SUCCESS: Fixed conversation analysis!")
        print("   ✓ Topic 1 (business_overview): Completed with 'Nvidia' → auto-advancement")
        print("   ✓ Topic 2 (product_service_footprint): Completed with research → 'next topic'")
        print("   ✓ Topic 3 (historical_financial_performance): Correctly identified as current")
        return True
    else:
        print(f"\n❌ FAILURE: Expected 2 completed topics and 'historical_financial_performance'")
        print(f"   Got {result['topics_completed']} topics and '{result['current_topic']}'")
        return False

def test_simple_progression():
    """Test simple topic progression without research"""
    
    print("\n🧪 TESTING SIMPLE TOPIC PROGRESSION")
    print("=" * 50)
    
    messages = [
        {
            "role": "assistant",
            "content": "What is your company name and give me a brief overview of what your business does?"
        },
        {
            "role": "user", 
            "content": "Tesla - electric vehicle manufacturer"
        },
        {
            "role": "assistant",
            "content": "Now let's discuss your product/service footprint. What are your main offerings?"
        },
        {
            "role": "user",
            "content": "Model S, Model 3, Model X, Model Y vehicles plus energy storage"
        },
        {
            "role": "assistant",
            "content": "Let's analyze your historical financial performance. Can you provide your revenue?"
        }
    ]
    
    result = analyze_conversation_progress(messages)
    
    print(f"📊 RESULTS:")
    print(f"   Topics completed: {result['topics_completed']}")
    print(f"   Current topic: {result['current_topic']}")
    
    # Should have 2 completed topics, asking for topic 3
    if result['topics_completed'] == 2 and result['current_topic'] == 'historical_financial_performance':
        print("✅ SUCCESS: Simple progression working!")
        return True
    else:
        print("❌ FAILURE: Simple progression broken")
        return False

def main():
    """Run all tests"""
    
    test1 = test_conversation_fix()
    test2 = test_simple_progression()
    
    print(f"\n🎯 OVERALL RESULT:")
    if test1 and test2:
        print("✅ ALL TESTS PASSED! Conversation analysis is fixed!")
    else:
        print("❌ Some tests failed. Need more investigation.")
    
    return test1 and test2

if __name__ == "__main__":
    main()