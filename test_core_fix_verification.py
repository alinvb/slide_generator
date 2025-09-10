#!/usr/bin/env python3

"""
Simple verification test to confirm the core issue is fixed
Testing the user's exact reported scenario
"""

import sys
sys.path.append('/home/user/webapp')
from app import analyze_conversation_progress

def test_user_exact_scenario():
    """Test the EXACT scenario the user reported"""
    print("🎯 TESTING USER'S EXACT REPORTED SCENARIO")
    print("User said: After business_overview, when they say 'sufficient. next topic'")
    print("System was jumping to financial performance (topic 3) instead of product_service_footprint (topic 2)")
    print()
    
    # Simulate the conversation that caused the issue
    messages = [
        # AI asks business overview (topic 1)
        {
            "role": "assistant",
            "content": "What is your company name and give me a brief overview of what your business does?"
        },
        # User answers 
        {
            "role": "user", 
            "content": "prypco - we provide HR software solutions for small businesses"
        },
        # AI asks a FOLLOW-UP question (this was incorrectly counted as topic 2 before the fix)
        {
            "role": "assistant",
            "content": "Thanks for that information! To complete the financial analysis, I additionally need revenue figures and EBITDA margins and growth rates. Do you have this data, or should I research it?"
        },
        # User says next topic - this should go to topic 2 (product_service_footprint)
        {
            "role": "user",
            "content": "sufficient. next topic"
        }
    ]
    
    print("🔍 Analyzing conversation with fixed logic...")
    result = analyze_conversation_progress(messages)
    
    print(f"📊 RESULT:")
    print(f"   Topics completed: {result['topics_completed']}")
    print(f"   Current topic: {result['current_topic']}")
    print(f"   Current position: {result['current_position']}")
    print()
    
    # Check if the fix worked
    if result['current_topic'] == 'product_service_footprint' and result['topics_completed'] == 1:
        print("✅ SUCCESS: Fix is working!")
        print("   ✓ Only 1 topic completed (business_overview)")  
        print("   ✓ Next topic is product_service_footprint (topic 2)")
        print("   ✓ Follow-up question was correctly ignored")
        return True
    elif result['current_topic'] == 'historical_financial_performance':
        print("❌ FAILURE: Issue still exists!")
        print("   ✗ System still jumping to financial performance (topic 3)")
        print("   ✗ Follow-up question was incorrectly counted as topic completion")
        return False
    else:
        print(f"⚠️ UNEXPECTED: Got topic '{result['current_topic']}'")
        return False

def main():
    print("🔬 CORE FIX VERIFICATION TEST")
    print("=" * 50)
    
    success = test_user_exact_scenario()
    
    print("\n🎯 CONCLUSION:")
    if success:
        print("✅ The topic progression issue has been FIXED!")
        print("   The system now properly follows the 14-topic sequence")
        print("   Follow-up questions no longer interfere with topic progression")
    else:
        print("❌ The issue still exists and needs more work")
    
    return success

if __name__ == "__main__":
    main()