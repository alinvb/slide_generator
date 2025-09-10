#!/usr/bin/env python3

"""
Test script to verify the topic progression fix
The fix should prevent follow-up questions from being counted as official topic questions
"""

# Import the fixed function from app.py
import sys
sys.path.append('/home/user/webapp')
from app import analyze_conversation_progress

def test_user_reported_scenario():
    """Test the exact scenario the user reported: business_overview + follow-up + 'sufficient. next topic'"""
    print("🧪 TEST: User's reported scenario with follow-up question")
    
    messages = [
        {
            "role": "assistant",
            "content": "What is your company name and give me a brief overview of what your business does?"
        },
        {
            "role": "user", 
            "content": "prypco - we provide HR software solutions for small businesses"
        },
        {
            "role": "assistant",
            "content": "Thanks for that information! To complete the financial analysis, I additionally need revenue figures and EBITDA margins and growth rates. Do you have this data, or should I research it?"
        },
        {
            "role": "user",
            "content": "sufficient. next topic"
        }
    ]
    
    result = analyze_conversation_progress(messages)
    
    print(f"📊 Result: Current topic = '{result['current_topic']}'")
    
    if result['current_topic'] == 'product_service_footprint':
        print("✅ SUCCESS: System correctly advances to product_service_footprint (topic 2)")
        return True
    elif result['current_topic'] == 'historical_financial_performance':
        print("❌ FAILURE: System still incorrectly jumps to financial performance (topic 3)")
        return False
    else:
        print(f"⚠️  UNEXPECTED: System returned topic '{result['current_topic']}'")
        return False

def test_normal_progression():
    """Test normal progression through first few topics"""
    print("\n🧪 TEST: Normal progression through first 3 topics")
    
    messages = [
        # Topic 1: Business Overview
        {
            "role": "assistant",
            "content": "What is your company name and give me a brief overview of what your business does?"
        },
        {
            "role": "user", 
            "content": "prypco - we provide HR software solutions for small businesses"
        },
        
        # Topic 2: Product/Service Footprint  
        {
            "role": "assistant",
            "content": "Now let's discuss your product/service footprint. What are your main offerings? Please provide the title and description for each product/service. Also, where do you operate geographically and what's your market coverage?"
        },
        {
            "role": "user", 
            "content": "We have 3 main products: payroll management, employee tracking, and performance reviews. We operate in North America."
        },
        
        # Topic 3: Historical Financial Performance
        {
            "role": "assistant",
            "content": "Let's analyze your historical financial performance. Can you provide your revenue, EBITDA, margins, and key financial metrics for the last 3-5 years?"
        },
        {
            "role": "user", 
            "content": "Revenue has grown from $1M to $5M over 3 years, with 25% EBITDA margins"
        },
        {
            "role": "user",
            "content": "sufficient. next topic"
        }
    ]
    
    result = analyze_conversation_progress(messages)
    
    print(f"📊 Result: Current topic = '{result['current_topic']}', Topics completed = {result['topics_completed']}")
    
    if result['topics_completed'] == 3 and result['current_topic'] == 'management_team':
        print("✅ SUCCESS: Correctly completed 3 topics, asking for management_team (topic 4)")
        return True
    else:
        print(f"❌ FAILURE: Expected 3 completed topics and 'management_team', got {result['topics_completed']} and '{result['current_topic']}'")
        return False

def test_follow_up_resistance():
    """Test that follow-up questions don't advance the topic counter"""
    print("\n🧪 TEST: Follow-up questions should not advance topic counter")
    
    messages = [
        # Topic 1: Business Overview
        {
            "role": "assistant",
            "content": "What is your company name and give me a brief overview of what your business does?"
        },
        {
            "role": "user", 
            "content": "prypco - we provide HR software solutions"
        },
        
        # Follow-up question (should NOT count as new topic)
        {
            "role": "assistant",
            "content": "Can you tell me more about your target customers?"
        },
        {
            "role": "user", 
            "content": "We target small businesses with 10-100 employees"
        },
        
        # Another follow-up question (should NOT count as new topic)
        {
            "role": "assistant",
            "content": "What industries do you primarily serve?"
        },
        {
            "role": "user",
            "content": "sufficient. next topic"
        }
    ]
    
    result = analyze_conversation_progress(messages)
    
    print(f"📊 Result: Current topic = '{result['current_topic']}', Topics completed = {result['topics_completed']}")
    
    if result['topics_completed'] == 1 and result['current_topic'] == 'product_service_footprint':
        print("✅ SUCCESS: Follow-up questions ignored, correctly at topic 2 (product_service_footprint)")
        return True
    else:
        print(f"❌ FAILURE: Expected 1 completed topic and 'product_service_footprint', got {result['topics_completed']} and '{result['current_topic']}'")
        return False

def main():
    """Run all tests"""
    print("🔬 TESTING TOPIC PROGRESSION FIX")
    print("=" * 50)
    
    test1_result = test_user_reported_scenario()
    test2_result = test_normal_progression()  
    test3_result = test_follow_up_resistance()
    
    print(f"\n📋 RESULTS SUMMARY:")
    print(f"   User scenario fix: {'✅ PASS' if test1_result else '❌ FAIL'}")
    print(f"   Normal progression: {'✅ PASS' if test2_result else '❌ FAIL'}")
    print(f"   Follow-up resistance: {'✅ PASS' if test3_result else '❌ FAIL'}")
    
    if all([test1_result, test2_result, test3_result]):
        print("\n🎉 ALL TESTS PASSED! Topic progression fix is working correctly.")
        return True
    else:
        print(f"\n🚨 SOME TESTS FAILED! Need further investigation.")
        return False

if __name__ == "__main__":
    main()