#!/usr/bin/env python3

"""
Debug the current issue where the system is stuck asking for financial data
after providing comprehensive research
"""

import sys
sys.path.append('/home/user/webapp')
from app import analyze_conversation_progress

def simulate_current_conversation():
    """Simulate the conversation flow that's causing the current issue"""
    
    messages = [
        # Topic 1: Business Overview
        {
            "role": "assistant",
            "content": "What is your company name and give me a brief overview of what your business does?"
        },
        {
            "role": "user", 
            "content": "Nvidia"
        },
        
        # Topic 2: Product/Service Footprint (correctly advanced to)
        {
            "role": "assistant",
            "content": "Now let's discuss your product/service footprint. What are your main offerings? Please provide the title and description for each product/service. Also, where do you operate geographically and what's your market coverage?"
        },
        {
            "role": "user",
            "content": "research this for me"
        },
        
        # AI provided comprehensive research (over 200 chars)
        {
            "role": "assistant",
            "content": "Nvidia is the global leader in AI semiconductors, commanding unmatched market share and growth metrics due to soaring demand for its data center and AI products... [comprehensive research content of 1000+ chars]"
        },
        {
            "role": "user",
            "content": "next topic"
        },
        
        # Topic 3: Historical Financial Performance (should advance here)
        {
            "role": "assistant",
            "content": "Let's analyze your historical financial performance. Can you provide your revenue, EBITDA, margins, and key financial metrics for the last 3-5 years? I need specific numbers: annual revenue in USD millions, EBITDA figures, margin percentages, growth rates, and key performance drivers. What are the main revenue streams and how have they evolved?"
        },
        {
            "role": "user",
            "content": "research this for me"
        },
        
        # AI should provide research, but then is asking again instead of moving forward
        {
            "role": "assistant",
            "content": "Thanks for that information! To complete the financial analysis, I additionally need revenue figures and EBITDA margins and growth rates. Do you have this data, or should I research it?"
        }
    ]
    
    return messages

def main():
    """Analyze the current conversation issue"""
    print("🔍 DEBUGGING CURRENT CONVERSATION ISSUE")
    print("=" * 50)
    
    messages = simulate_current_conversation()
    
    print("📝 Current conversation flow:")
    for i, msg in enumerate(messages[-6:], start=len(messages)-5):  # Show last 6 messages
        role_icon = "🤖" if msg["role"] == "assistant" else "👤"
        content_preview = msg["content"][:80] + "..." if len(msg["content"]) > 80 else msg["content"]
        print(f"  {i}. {role_icon} {msg['role']}: {content_preview}")
    
    print(f"\n🔍 Analyzing conversation progress...")
    result = analyze_conversation_progress(messages)
    
    print(f"\n📊 ANALYSIS RESULTS:")
    print(f"   Topics completed: {result['topics_completed']}")
    print(f"   Current topic: {result['current_topic']}")
    print(f"   Current position: {result['current_position']}")
    print(f"   Is complete: {result['is_complete']}")
    
    # Analyze what should happen next
    print(f"\n🤔 ISSUE ANALYSIS:")
    
    if result['topics_completed'] == 2 and result['current_topic'] == 'historical_financial_performance':
        print("✅ TOPIC PROGRESSION: Correctly at topic 3 (financial performance)")
        print("❌ CONVERSATION FLOW: But system is asking for the same data again")
        print("🔍 ROOT CAUSE: Research completion detection may be broken")
    elif result['topics_completed'] == 3:
        print("✅ TOPIC PROGRESSION: Topic 3 should be completed")  
        print(f"📍 SHOULD BE: Asking about topic 4 ({result.get('next_question', 'unknown')})")
    else:
        print(f"⚠️  UNEXPECTED STATE: {result['topics_completed']} topics completed")
    
    return result

if __name__ == "__main__":
    main()