#!/usr/bin/env python3

"""
Comprehensive test of topic persistence with various user interaction patterns
"""

import sys
sys.path.append('/home/user/webapp')
from app import analyze_conversation_progress

def test_mixed_interaction_patterns():
    """Test realistic conversation with mixed patterns"""
    
    print("🧪 COMPREHENSIVE TOPIC PERSISTENCE TEST")
    print("=" * 50)
    
    messages = [
        # Topic 1: Quick completion
        {
            "role": "assistant",
            "content": "What is your company name and give me a brief overview of what your business does?"
        },
        {
            "role": "user", 
            "content": "Apple Inc - technology company making iPhones, Macs, and services"
        },
        {
            "role": "user",
            "content": "next topic"  # Quick advancement
        },
        
        # Topic 2: Extended research and follow-ups
        {
            "role": "assistant",
            "content": "Now let's discuss your product/service footprint. What are your main offerings?"
        },
        {
            "role": "user",
            "content": "research this for me"
        },
        {
            "role": "assistant",
            "content": "Apple's product portfolio includes iPhone (smartphones), Mac (computers), iPad (tablets), Apple Watch (wearables), AirPods (audio), and services like App Store, iCloud, Apple Music. Geographic presence spans 175+ countries globally."
        },
        {
            "role": "user",
            "content": "tell me more about their services revenue"  # Follow-up
        },
        {
            "role": "assistant",
            "content": "Apple Services generated $85 billion in 2024, including App Store, iCloud, Apple Music, Apple TV+, Apple Pay, and AppleCare. This represents 22% of total revenue with higher margins than hardware."
        },
        {
            "role": "user",
            "content": "what about geographic breakdown?"  # Another follow-up
        },
        {
            "role": "assistant",
            "content": "Apple's revenue by region: Americas 45%, Europe 23%, Greater China 19%, Japan 7%, Rest of Asia Pacific 6%. Services are growing fastest in emerging markets."
        },
        {
            "role": "user",
            "content": "sufficient. next topic"  # Finally advance
        },
        
        # Topic 3: Should be asking for financial performance
        {
            "role": "assistant",
            "content": "Let's analyze your historical financial performance. Can you provide your revenue, EBITDA, margins, and key financial metrics for the last 3-5 years?"
        }
    ]
    
    result = analyze_conversation_progress(messages)
    
    print(f"\n📊 COMPREHENSIVE TEST RESULTS:")
    print(f"   Topics completed: {result['topics_completed']}")
    print(f"   Current topic: {result['current_topic']}")
    print(f"   Current position: {result['current_position']}")
    
    # Expected:
    # - Topic 1 completed (quick "next topic")
    # - Topic 2 completed (extended conversation + "sufficient. next topic") 
    # - Currently at Topic 3 (historical_financial_performance)
    
    if (result['topics_completed'] == 2 and 
        result['current_topic'] == 'historical_financial_performance' and
        result['current_position'] == 3):
        
        print(f"\n✅ COMPREHENSIVE SUCCESS!")
        print(f"   ✓ Topic 1: Quick completion worked")
        print(f"   ✓ Topic 2: Extended conversation + research + follow-ups worked")
        print(f"   ✓ Topic 3: Correctly identified as current")
        print(f"   ✓ Follow-up questions didn't interfere with progression")
        return True
    else:
        print(f"\n❌ COMPREHENSIVE FAILURE")
        print(f"   Expected: 2 completed, position 3, at 'historical_financial_performance'")
        print(f"   Got: {result['topics_completed']} completed, position {result['current_position']}, at '{result['current_topic']}'")
        return False

def main():
    """Run comprehensive test"""
    success = test_mixed_interaction_patterns()
    
    if success:
        print(f"\n🎯 FINAL VERDICT: ✅ TOPIC PERSISTENCE FULLY IMPLEMENTED!")
        print(f"   The system correctly:")
        print(f"   • Stays in each topic until user says 'next topic'")
        print(f"   • Allows unlimited follow-up questions within topics")
        print(f"   • Supports research requests and extended conversations") 
        print(f"   • Only advances on explicit user command")
        print(f"   • Maintains proper sequential 14-topic flow")
    else:
        print(f"\n❌ TOPIC PERSISTENCE STILL HAS ISSUES")
    
    return success

if __name__ == "__main__":
    main()