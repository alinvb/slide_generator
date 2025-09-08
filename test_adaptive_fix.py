#!/usr/bin/env python3
"""
Test the fixed adaptive slide generator with minimal conversation
"""

from adaptive_slide_generator import generate_adaptive_presentation

# Test with minimal conversation (like user's case)
minimal_messages = [
    {"role": "user", "content": "My company is Qi Card"},
    {"role": "assistant", "content": "What does your company do?"},
    {"role": "user", "content": "We're a fintech company in Iraq"},
    {"role": "assistant", "content": "Tell me about your business model"},
    {"role": "user", "content": "We provide digital payments and cards"}
]

print("🧪 Testing Adaptive Slide Generator with Minimal Conversation")
print("=" * 60)

slide_list, render_plan, analysis_report = generate_adaptive_presentation(minimal_messages)

print(f"📊 Conversation has {len(minimal_messages)} messages")
print(f"📋 Slides Generated: {len(slide_list)}")
print(f"📝 Slide List: {slide_list}")
print(f"📈 Quality Summary: {analysis_report['quality_summary']}")

# Check for buyer slides inappropriately included
buyer_slides = [s for s in slide_list if 'buyer' in s.lower()]
if buyer_slides:
    print(f"❌ ERROR: Buyer slides included inappropriately: {buyer_slides}")
else:
    print("✅ GOOD: No buyer slides included (as expected)")

# Should be around 3-5 slides max for this minimal conversation
if len(slide_list) > 6:
    print(f"❌ ERROR: Too many slides ({len(slide_list)}) for minimal conversation")
elif len(slide_list) >= 3:
    print(f"✅ GOOD: Appropriate slide count ({len(slide_list)}) for minimal conversation")
else:
    print(f"⚠️  WARNING: Very few slides ({len(slide_list)})")

print("\n" + "=" * 60)
print("Expected: 3-5 slides, no buyer profiles, high-quality content only")