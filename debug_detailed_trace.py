#!/usr/bin/env python3
"""
Detailed trace of the conversation flow issue
"""

from app import analyze_conversation_progress

def detailed_trace():
    print("🔍 Detailed Trace of Conversation Flow")
    print("=" * 60)
    
    # Step-by-step conversation simulation
    print("\n1️⃣ After business overview...")
    messages_step1 = [
        {"role": "system", "content": "You are an investment banker conducting an interview."},
        {"role": "assistant", "content": "What is your company name and give me a brief overview of what your business does?"},
        {"role": "user", "content": "Aramco"},
    ]
    progress1 = analyze_conversation_progress(messages_step1)
    print(f"Next topic: {progress1.get('next_topic')}")
    print(f"Next question contains: {progress1.get('next_question', '')[:100]}")
    
    print("\n2️⃣ After product/service question...")
    messages_step2 = messages_step1 + [
        {"role": "assistant", "content": "Now let's discuss your product/service footprint. What are your main offerings?"},
        {"role": "user", "content": "research yourself"},
    ]
    progress2 = analyze_conversation_progress(messages_step2)
    print(f"Next topic: {progress2.get('next_topic')}")
    print(f"Next question contains: {progress2.get('next_question', '')[:100]}")
    
    print("\n3️⃣ After product/service research + OK...")
    messages_step3 = messages_step2 + [
        {"role": "assistant", "content": "Based on research, Aramco's main offerings include crude oil production, refining, petrochemicals. Are you satisfied with this information?"},
        {"role": "user", "content": "ok"},
    ]
    progress3 = analyze_conversation_progress(messages_step3)
    print(f"Next topic: {progress3.get('next_topic')}")
    print(f"Next question contains: {progress3.get('next_question', '')[:100]}")
    
    print("\n4️⃣ After financial performance question...")
    messages_step4 = messages_step3 + [
        {"role": "assistant", "content": "Let's analyze your historical financial performance. Can you provide your revenue, EBITDA, margins?"},
        {"role": "user", "content": "research yourself"},
    ]
    progress4 = analyze_conversation_progress(messages_step4)
    print(f"Next topic: {progress4.get('next_topic')}")
    print(f"Next question contains: {progress4.get('next_question', '')[:100]}")
    
    print("\n5️⃣ After financial research + OK...")
    messages_step5 = messages_step4 + [
        {"role": "assistant", "content": "Based on research, Aramco's financial performance shows: Revenue of $535 billion (2022), EBITDA margins around 50-60%. Are you satisfied with these financial figures?"},
        {"role": "user", "content": "ok"},
    ]
    progress5 = analyze_conversation_progress(messages_step5)
    print(f"Next topic: {progress5.get('next_topic')}")
    print(f"Next question contains: {progress5.get('next_question', '')[:100]}")
    
    # Check if financial is still being asked
    if "financial" in progress5.get('next_question', '').lower():
        print("🚨 BUG CONFIRMED: Financial performance being asked again!")
    else:
        print("✅ SUCCESS: Moving to next topic correctly")

if __name__ == "__main__":
    detailed_trace()