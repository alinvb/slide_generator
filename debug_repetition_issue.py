#!/usr/bin/env python3
"""
Debug the repetition issue with financial performance topic
"""

from app import analyze_conversation_progress

def test_repetition_issue():
    print("🧪 Testing Financial Performance Topic Repetition Issue")
    print("=" * 60)
    
    # Simulate conversation with Aramco where financial performance is discussed
    messages = [
        {"role": "system", "content": "You are an investment banker conducting an interview."},
        {"role": "assistant", "content": "What is your company name and give me a brief overview of what your business does?"},
        {"role": "user", "content": "Aramco"},
        {"role": "assistant", "content": "Now let's discuss your product/service footprint. What are your main offerings?"},
        {"role": "user", "content": "research yourself"},
        {"role": "assistant", "content": "Based on research, Aramco's main offerings include crude oil production, refining, petrochemicals, and integrated energy services. They operate globally with significant presence in Saudi Arabia, Asia, and international markets. Are you satisfied with this information, or would you like me to research something more specific?"},
        {"role": "user", "content": "ok"},
        {"role": "assistant", "content": "Let's analyze your historical financial performance. Can you provide your revenue, EBITDA, margins, and key financial metrics for the last 3-5 years?"},
        {"role": "user", "content": "research yourself"},
        {"role": "assistant", "content": "Based on research, Aramco's financial performance shows: Revenue of $535 billion (2022), $400 billion (2021). EBITDA margins around 50-60%. Strong cash flow generation. Net income of $161 billion (2022). Key drivers include oil prices, production volumes, and downstream integration. Are you satisfied with these financial figures, or would you like me to research more details about their revenue breakdown, growth drivers, or profitability trends?"},
        {"role": "user", "content": "ok"},
        # This should NOT ask about financial performance again, but it does
    ]
    
    print("📊 Analyzing conversation progress...")
    progress_info = analyze_conversation_progress(messages)
    
    print(f"\n🎯 Next topic: {progress_info.get('next_topic')}")
    print(f"📝 Next question: {progress_info.get('next_question', 'None')[:150]}...")
    
    # Check if financial performance is marked as covered
    if "financial" in progress_info.get('next_question', '').lower():
        print("🚨 ERROR: Financial performance is being asked again!")
        return False
    else:
        print("✅ SUCCESS: Moving to next topic (management team)")
        return True

if __name__ == "__main__":
    success = test_repetition_issue()
    if success:
        print("\n✅ Test PASSED - No repetition detected")
    else:
        print("\n❌ Test FAILED - Repetition issue confirmed")