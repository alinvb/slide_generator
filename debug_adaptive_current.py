#!/usr/bin/env python3
"""
Debug the current adaptive behavior with a real conversation similar to user's
"""

from adaptive_slide_generator import generate_adaptive_presentation

# Simulate user's actual conversation (3 basic questions)
user_messages = [
    {"role": "assistant", "content": "Hi! I'm here to help you create an investment banking pitch deck. Let's start with your company - what's the name and what do you do?"},
    {"role": "user", "content": "Qi Card, we're a fintech company in Iraq providing digital payments"},
    {"role": "assistant", "content": "Great! Can you tell me more about your business model and services?"},
    {"role": "user", "content": "We provide cards and digital payments to 12 million users, work with government for salaries"},
    {"role": "assistant", "content": "Interesting! What about your management team and key executives?"},
    {"role": "user", "content": "Bahaa Abdul Hadi is Chairman and co-founder, Ahmed Khadum is CIO"}
]

print("🚨 DEBUG: Current Adaptive Behavior")
print("=" * 60)

slide_list, render_plan, analysis_report = generate_adaptive_presentation(user_messages)

print(f"📊 Input: {len(user_messages)} conversation messages")
print(f"📋 Output: {len(slide_list)} slides generated")
print(f"📝 Slides: {slide_list}")
print(f"📈 Quality: {analysis_report['quality_summary']}")

print("\n🔍 DETAILED ANALYSIS:")
for slide, info in analysis_report['slides_analysis'].items():
    score = info.get('score', 0)
    recommended = info.get('recommended', False)
    keywords = info.get('found_keywords', [])
    print(f"  {slide}: {score:.2f} | Recommended: {recommended} | Keywords: {keywords[:3]}")

print("\n" + "=" * 60)

if len(slide_list) > 6:
    print("❌ PROBLEM: Still generating too many slides!")
else:
    print("✅ GOOD: Reasonable slide count")

buyer_slides = [s for s in slide_list if 'buyer' in s]
if buyer_slides:
    print(f"❌ PROBLEM: Buyer slides included: {buyer_slides}")
else:
    print("✅ GOOD: No inappropriate buyer slides")