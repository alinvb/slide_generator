#!/usr/bin/env python3

"""
Debug why the system gets stuck at Topic 3 (financial performance)
"""

import sys
sys.path.append('/home/user/webapp')
from app import analyze_conversation_progress

def simulate_stuck_scenario():
    """Reproduce the exact stuck scenario from user's report"""
    
    print("🔍 DEBUGGING TOPIC 3 STUCK ISSUE") 
    print("=" * 50)
    print("User reported getting stuck in this loop:")
    print("1. AI asks for financial performance")
    print("2. User says 'research for me'") 
    print("3. AI asks same question again instead of providing research")
    print("4. Infinite loop...")
    print()
    
    # Reproduce the exact conversation
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
        
        # Topic 2: Product/Service (completed) 
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
            "content": "Nvidia is the global leader in AI semiconductors... [comprehensive research with inventory write-downs data]"
        },
        {
            "role": "user",
            "content": "next topic"
        },
        
        # Topic 3: Financial Performance (GETTING STUCK HERE)
        {
            "role": "assistant",
            "content": "Let's analyze your historical financial performance. Can you provide your revenue, EBITDA, margins, and key financial metrics for the last 3-5 years? I need specific numbers: annual revenue in USD millions, EBITDA figures, margin percentages, growth rates, and key performance drivers. What are the main revenue streams and how have they evolved?"
        },
        {
            "role": "user",
            "content": "research for me"  # USER REQUESTS RESEARCH
        },
        {
            "role": "assistant", 
            "content": "Thanks for that information! To complete the financial analysis, I additionally need revenue figures and EBITDA margins and growth rates. Do you have this data, or should I research it?"  # AI IGNORES RESEARCH REQUEST
        },
        {
            "role": "user",
            "content": "research this for me"  # USER REQUESTS RESEARCH AGAIN
        },
        {
            "role": "assistant",
            "content": "Thanks for that information! To complete the financial analysis, I additionally need revenue figures and EBITDA margins and growth rates. Do you have this data, or should I research it?"  # AI IGNORES AGAIN
        }
    ]
    
    print("🔍 Analyzing conversation state...")
    result = analyze_conversation_progress(messages)
    
    print(f"\n📊 CONVERSATION STATE:")
    print(f"   Topics completed: {result['topics_completed']}")
    print(f"   Current topic: {result['current_topic']}")
    print(f"   Current position: {result['current_position']}")
    
    print(f"\n🚨 ISSUE ANALYSIS:")
    
    # The issue is that the AI is asking the same question repeatedly
    # instead of providing research when user says "research for me"
    
    if result['current_topic'] == 'historical_financial_performance':
        print("✅ TOPIC DETECTION: Correctly identifies we're at financial performance topic")
        
        # Check if the system should be providing research instead of asking again
        user_messages = [msg for msg in messages if msg["role"] == "user"]
        recent_user_messages = user_messages[-2:]  # Last 2 user messages
        
        research_requests = [msg for msg in recent_user_messages if "research" in msg["content"].lower()]
        
        if len(research_requests) >= 1:
            print("❌ RESEARCH LOOP DETECTED:")
            print(f"   • User requested research {len(research_requests)} times")
            print(f"   • AI should provide research, not ask same question")
            print(f"   • System is in infinite question loop")
            
            print(f"\n💡 ROOT CAUSE ANALYSIS:")
            print(f"   1. User says 'research for me'")
            print(f"   2. System should detect research request")
            print(f"   3. System should provide comprehensive research") 
            print(f"   4. System should then ask 'Are you satisfied?' or allow 'next topic'")
            print(f"   5. INSTEAD: System ignores research request and repeats question")
            
            return False
    
    return True

def analyze_research_handling():
    """Analyze how research requests should be handled"""
    
    print(f"\n🔬 RESEARCH HANDLING ANALYSIS")
    print("=" * 40)
    
    print("✅ CORRECT FLOW should be:")
    print("   1. AI asks: 'Can you provide financial metrics?'")
    print("   2. User: 'research for me'") 
    print("   3. AI: [PROVIDES COMPREHENSIVE RESEARCH]")
    print("   4. AI: 'Are you satisfied with this research?'")
    print("   5. User: 'sufficient. next topic' OR provides more info")
    print("   6. AI: [ADVANCES TO NEXT TOPIC]")
    
    print(f"\n❌ BROKEN FLOW currently:")
    print("   1. AI asks: 'Can you provide financial metrics?'")
    print("   2. User: 'research for me'")
    print("   3. AI: 'Thanks for that information! I need...' [IGNORES RESEARCH REQUEST]")
    print("   4. User: 'research this for me'") 
    print("   5. AI: 'Thanks for that information! I need...' [IGNORES AGAIN]")
    print("   6. [INFINITE LOOP]")

def main():
    """Debug the stuck issue"""
    
    success = simulate_stuck_scenario()
    analyze_research_handling()
    
    print(f"\n🎯 CONCLUSION:")
    if not success:
        print("❌ CONFIRMED: System is stuck in Topic 3 research loop")
        print("🔧 FIXES NEEDED:")
        print("   1. Research request detection is broken")
        print("   2. Research response generation is not triggered")
        print("   3. Topic completion after research is not working")
        print("   4. System falls back to repeating the same question")
    else:
        print("✅ System working correctly")
    
    return success

if __name__ == "__main__":
    main()