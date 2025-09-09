#!/usr/bin/env python3
"""
Debug the current topic detection issue
"""

from app import analyze_conversation_progress

def debug_topic_detection():
    print("🔍 Debugging Current Topic Detection")
    print("=" * 60)
    
    # Simulate the exact problematic conversation
    messages = [
        {"role": "system", "content": "You are an investment banker conducting an interview."},
        {"role": "assistant", "content": "What is your company name and give me a brief overview of what your business does?"},
        {"role": "user", "content": "Aramco"},
        {"role": "assistant", "content": "Now let's discuss your product/service footprint. What are your main offerings?"},
        {"role": "user", "content": "research yourself"},
        {"role": "assistant", "content": "Based on research, Aramco's main offerings include crude oil production, refining, petrochemicals. Are you satisfied with this information?"},
        {"role": "user", "content": "ok"},
        {"role": "assistant", "content": "Let's analyze your historical financial performance. Can you provide your revenue, EBITDA, margins?"},
        {"role": "user", "content": "research yourself"},
    ]
    
    print("📊 Messages in conversation:")
    for i, msg in enumerate(messages):
        if msg["role"] != "system":
            print(f"  {i}: {msg['role']}: {msg['content'][:80]}...")
    
    print("\n🎯 Testing topic detection at this point...")
    
    # Manual extraction of recent questions (mirroring the logic in analyze_conversation_progress)
    recent_questions = []
    for i, msg in enumerate(messages[-10:]):
        if msg["role"] == "assistant" and "?" in msg["content"]:
            content = msg["content"]
            if "let's discuss" in content.lower() or "now let's" in content.lower() or "let's analyze" in content.lower():
                recent_questions.append(content.lower())
                print(f"📝 Recent question {len(recent_questions)}: {content[:100]}...")
    
    if recent_questions:
        most_recent = recent_questions[-1]
        print(f"\n🎯 Most recent AI question: {most_recent[:150]}...")
        
        # Test if it contains financial performance keywords
        financial_keywords = ["financial performance", "analyze your historical", "revenue", "ebitda", "financial metrics"]
        matches = [kw for kw in financial_keywords if kw in most_recent]
        print(f"📊 Financial keywords found: {matches}")
        
        # Test if it contains product/service keywords  
        product_keywords = ["product", "service", "footprint", "offerings", "geographic"]
        product_matches = [kw for kw in product_keywords if kw in most_recent]
        print(f"🛍️ Product keywords found: {product_matches}")
    else:
        print("❌ No recent questions found!")
        
    print("\n🧪 Running full analyze_conversation_progress...")
    progress_info = analyze_conversation_progress(messages)
    
    print(f"\n🎯 Detected current topic: {progress_info.get('current_topic', 'None')}")
    print(f"📝 Next question starts with: {progress_info.get('next_question', 'None')[:100]}...")

if __name__ == "__main__":
    debug_topic_detection()