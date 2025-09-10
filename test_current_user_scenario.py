#!/usr/bin/env python3

"""
Test the exact scenario the user is currently experiencing
"""

import sys
sys.path.append('/home/user/webapp')
from app import analyze_conversation_progress

def test_user_current_scenario():
    """Test the EXACT current scenario where user is stuck"""
    
    print("🧪 TESTING USER'S CURRENT SCENARIO")
    print("=" * 50)
    print("User reported being stuck at this point:")
    print("1. AI asks for financial research")  
    print("2. User says 'research this for me'")
    print("3. AI provides research")
    print("4. AI asks: 'Thanks for that information! To complete the financial analysis...'")
    print("5. User should be able to say 'sufficient. next topic' to advance")
    print()
    
    # Full conversation leading to the current issue
    messages = [
        # Topic 1: Business Overview (completed)
        {
            "role": "assistant",
            "content": "What is your company name and give me a brief overview of what your business does?"
        },
        {
            "role": "user", 
            "content": "Nvidia"
        },
        
        # Topic 2: Product/Service Footprint (completed)
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
            "content": "Nvidia is the global leader in AI semiconductors, commanding unmatched market share and growth metrics due to soaring demand for its data center and AI products. Very long research content with comprehensive analysis exceeding 200 characters..."
        },
        {
            "role": "user",
            "content": "next topic"
        },
        
        # Topic 3: Historical Financial Performance (current issue)
        {
            "role": "assistant", 
            "content": "Let's analyze your historical financial performance. Can you provide your revenue, EBITDA, margins, and key financial metrics for the last 3-5 years? I need specific numbers: annual revenue in USD millions, EBITDA figures, margin percentages, growth rates, and key performance drivers. What are the main revenue streams and how have they evolved?"
        },
        {
            "role": "user",
            "content": "research this for me"
        },
        {
            "role": "assistant",
            "content": "Nvidia's financial performance shows exceptional growth... [COMPREHENSIVE RESEARCH WITH FINANCIAL DATA - over 200 chars]"
        },
        {
            "role": "user", 
            "content": "sufficient. next topic"  # User wants to advance but system is stuck
        },
        
        # This is where the system should advance to Topic 4, but instead asks follow-up
        {
            "role": "assistant",
            "content": "Thanks for that information! To complete the financial analysis, I additionally need revenue figures and EBITDA margins and growth rates. Do you have this data, or should I research it?"
        }
    ]
    
    result = analyze_conversation_progress(messages)
    
    print(f"📊 CURRENT STATE:")
    print(f"   Topics completed: {result['topics_completed']}")
    print(f"   Current topic: {result['current_topic']}")
    print(f"   Current position: {result['current_position']}")
    
    # The user expects to be advanced to Topic 4 (management_team) after saying "sufficient. next topic"
    if result['topics_completed'] == 3 and result['current_topic'] == 'management_team':
        print("\n✅ SUCCESS: System correctly completed Topic 3 and advanced to Topic 4")
        print("   ✓ Financial performance research was recognized as complete")
        print("   ✓ 'sufficient. next topic' correctly triggered advancement")
        return True
    elif result['topics_completed'] == 2 and result['current_topic'] == 'historical_financial_performance':
        print("\n❌ ISSUE CONFIRMED: System stuck at Topic 3")
        print("   ✗ Financial research + 'sufficient. next topic' not recognized as completion")
        print("   ✗ Topic 3 not marked complete despite user satisfaction")
        print("\n🔍 ROOT CAUSE: Research completion pattern not properly detected")
        return False
    else:
        print(f"\n⚠️ UNEXPECTED STATE: {result['topics_completed']} topics, current: {result['current_topic']}")
        return False

def main():
    """Test and analyze the issue"""
    success = test_user_current_scenario()
    
    print(f"\n🎯 CONCLUSION:")
    if success:
        print("✅ The issue is already fixed!")
    else:
        print("❌ The issue persists - need to investigate research completion logic")
        print("\n💡 POTENTIAL FIX NEEDED:")
        print("   The system needs to recognize that after providing research,")
        print("   when user says 'sufficient. next topic', the topic should be marked complete")
        print("   even if AI asks a follow-up question afterwards.")

if __name__ == "__main__":
    main()