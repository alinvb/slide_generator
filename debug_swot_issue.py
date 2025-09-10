#!/usr/bin/env python3
"""
Debug why SWOT is being asked instead of management team
"""

from app import analyze_conversation_progress

def debug_swot_issue():
    print("🔍 Debugging SWOT Issue - Why Not Management Team?")
    print("=" * 60)
    
    # Simulate the actual conversation from the user
    messages = [
        {"role": "system", "content": "You are an investment banker conducting an interview."},
        {"role": "assistant", "content": "What is your company name and give me a brief overview of what your business does?"},
        {"role": "user", "content": "Aramco"},
        {"role": "assistant", "content": "Saudi Aramco is the world's largest oil and gas company by production..."},
        {"role": "user", "content": "ok"},
        {"role": "assistant", "content": "Now let's discuss your product/service footprint. What are your main offerings?"},
        {"role": "user", "content": "research yourself"},
        {"role": "assistant", "content": "Saudi Aramco offers a wide range of energy, chemical, and refined hydrocarbon products... Are you satisfied with this research?"},
        {"role": "user", "content": "ok"},
        {"role": "assistant", "content": "Let's analyze your historical financial performance. Can you provide your revenue, EBITDA, margins?"},
        {"role": "user", "content": "research yourself"},
        {"role": "assistant", "content": "Saudi Aramco has demonstrated exceptional financial scale... Are you satisfied with this research?"},
        {"role": "user", "content": "ok"},
        # At this point, the next question should be about MANAGEMENT TEAM, NOT SWOT
    ]
    
    print("📊 Analyzing conversation progress...")
    progress_info = analyze_conversation_progress(messages)
    
    print(f"\n🎯 Next topic: {progress_info.get('next_topic')}")
    print(f"📝 Next question: {progress_info.get('next_question', 'None')}")
    
    # Check topic coverage
    print("\n📋 Topic Coverage Status:")
    topics_checklist = {
        1: "business_overview",
        2: "product_service_footprint", 
        3: "historical_financial_performance",
        4: "management_team",
        5: "growth_strategy_projections"
    }
    
    for pos, topic_name in topics_checklist.items():
        status = "✅" if f"Topic {pos}" in str(progress_info) else "❓"
        print(f"  {pos}. {topic_name}: {status}")
    
    # Check if management team should be next
    expected_next = "management_team"
    actual_next = progress_info.get('next_topic')
    
    if actual_next == expected_next:
        print(f"\n✅ SUCCESS: Correctly identified next topic as {expected_next}")
    else:
        print(f"\n🚨 ERROR: Expected {expected_next}, but got {actual_next}")
        print("This suggests the topic coverage detection is failing!")

if __name__ == "__main__":
    debug_swot_issue()