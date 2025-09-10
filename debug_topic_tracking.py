#!/usr/bin/env python3

"""
Debug the topic tracking system to understand why the AI isn't using proper topic context
"""

import sys
import os
sys.path.append('/home/user/webapp')

from app import analyze_conversation_progress

def debug_topic_tracking():
    """Debug topic tracking with the user's example"""
    
    print("🔍 DEBUGGING TOPIC TRACKING ISSUE")
    print("=" * 70)
    
    # Simulate the conversation from the user's example
    messages = [
        {"role": "system", "content": "You are an investment banking copilot."},
        
        # Topic 1: Business Overview (Netflix content)
        {"role": "assistant", "content": "What is your company name and give me a brief overview of what your business does?"},
        {"role": "user", "content": "Netflix"},
        {"role": "assistant", "content": "These series are not only important for subscriber acquisition and retention but also demonstrate Netflix's ability to create globally resonant content across genres—drama, thriller, comedy, true crime, and reality. This diversity in high-profile originals is a key differentiator in the competitive streaming market."},
        {"role": "user", "content": "next topic"},
        
        # Topic 2: Product/Service Footprint
        {"role": "assistant", "content": "Now let's discuss your product/service footprint. What are your main offerings? Please provide the title and description for each product/service. Also, where do you operate geographically and what's your market coverage?"},
        {"role": "user", "content": "next topic"},
        
        # Topic 3: Historical Financial Performance
        {"role": "assistant", "content": "Let's analyze your historical financial performance. Can you provide your revenue, EBITDA, margins, and key financial metrics for the last 3-5 years? I need specific numbers: annual revenue in USD millions, EBITDA figures, margin percentages, growth rates, and key performance drivers. What are the main revenue streams and how have they evolved?"},
        {"role": "user", "content": "ebitda is 3 million"},
        
        # Here's where the AI should recognize we're still on Topic 3 (financial performance) 
        # but instead it's talking about management team
        {"role": "assistant", "content": "Netflix's management team is led by Co-CEOs Ted Sarandos and Greg Peters, supported by key executives including CFO Spencer Neumann, Chief Content Officer Bela Bajaria, and Chief Technology Officer Elizabeth Stone[1][2][3][4][5]. This leadership has deep experience across content, technology, finance, and global expansion..."}
    ]
    
    print("📋 Conversation Timeline:")
    for i, msg in enumerate(messages[1:], 1):  # Skip system message
        role_icon = "🤖" if msg['role'] == 'assistant' else "👤"
        content_preview = msg['content'][:80] + "..." if len(msg['content']) > 80 else msg['content']
        print(f"  {i}. {role_icon} {msg['role']}: {content_preview}")
    
    print(f"\n🎯 ANALYSIS:")
    
    # Test what the analyze_conversation_progress function returns at key points
    test_points = [
        {"name": "After 'Netflix' response", "end_index": 3},
        {"name": "After first 'next topic'", "end_index": 5}, 
        {"name": "After second 'next topic'", "end_index": 7},
        {"name": "After 'ebitda is 3 million'", "end_index": 9},
        {"name": "After management team response", "end_index": 10}
    ]
    
    for point in test_points:
        test_messages = messages[:point['end_index']]
        progress = analyze_conversation_progress(test_messages)
        
        print(f"\n📊 {point['name']}:")
        print(f"   Current Topic: {progress.get('current_topic', 'unknown')}")
        print(f"   Topics Completed: {progress.get('topics_covered', 0)}")
        print(f"   Current Position: {progress.get('current_position', 0)}")
        print(f"   Expected Next Question: {progress.get('next_question', 'No question')[:80]}...")
    
    print(f"\n❌ PROBLEM IDENTIFIED:")
    print(f"   The AI should recognize that after 'ebitda is 3 million', we're still on Topic 3")
    print(f"   (historical_financial_performance) and should ask follow-up questions about")  
    print(f"   missing financial data like revenue, margins, growth rates.")
    print(f"   ")
    print(f"   Instead, it's jumping to Topic 4 (management_team) content.")
    
    print(f"\n🔧 EXPECTED BEHAVIOR:")
    print(f"   User: 'ebitda is 3 million'")
    print(f"   AI Should Say: 'Thanks! I also need revenue figures, margin percentages, and growth rates'")
    print(f"   AI Should NOT Say: Information about management team")
    
    return True

if __name__ == "__main__":
    debug_topic_tracking()