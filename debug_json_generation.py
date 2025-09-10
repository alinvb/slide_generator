#!/usr/bin/env python3
"""
Debug JSON Generation Issue
Test the topic-based slide generator with sample conversation to see what slides are generated
"""

import json
import sys
import os

# Add the current directory to path
sys.path.append(os.getcwd())

from topic_based_slide_generator import generate_topic_based_presentation

# Sample conversation that should generate multiple slides
test_messages = [
    {"role": "assistant", "content": "What is your company name and give me a brief overview of what your business does?"},
    {"role": "user", "content": "My company is TechCorp, we're a software company founded in 2020 with headquarters in Dubai"},
    
    {"role": "assistant", "content": "Tell me about your product/service footprint and where you operate geographically"},
    {"role": "user", "content": "We offer AI software products and have operations in UAE, Saudi Arabia, and Kuwait"},
    
    {"role": "assistant", "content": "What are your key financial metrics - revenue, EBITDA margins, and financial performance?"},
    {"role": "user", "content": "We have $10M revenue in 2023, $15M projected for 2024, with 15% EBITDA margins"},
    
    {"role": "assistant", "content": "Tell me about your management team and key executives"},
    {"role": "user", "content": "Our CEO is John Smith, CTO is Sarah Johnson, both have 10+ years experience in tech"},
    
    {"role": "assistant", "content": "What is your growth strategy and expansion plans?"},
    {"role": "user", "content": "We plan to expand to Egypt and Morocco, targeting 100% revenue growth by 2025"},
]

print("🧪 TESTING JSON Generation Debug")
print("=" * 50)
print(f"📝 Test conversation has {len(test_messages)} messages")

try:
    slide_list, render_plan, analysis_report = generate_topic_based_presentation(test_messages)
    
    print(f"\n📊 RESULTS:")
    print(f"   Total slides generated: {analysis_report.get('total_slides_generated', 0)}")
    print(f"   Slide list: {slide_list}")
    print(f"   Topics covered: {analysis_report.get('topics_covered', 0)}")
    print(f"   Covered topics: {analysis_report.get('covered_topics', [])}")
    
    print(f"\n📋 Render Plan Structure:")
    print(f"   Number of slides in render plan: {len(render_plan.get('slides', []))}")
    
    if len(slide_list) == 1:
        print(f"\n❌ BUG CONFIRMED: Only 1 slide generated when {analysis_report.get('topics_covered', 0)} topics were covered")
        print(f"   This is the issue the user reported!")
    else:
        print(f"\n✅ Working correctly: {len(slide_list)} slides generated for {analysis_report.get('topics_covered', 0)} topics")
    
    print(f"\n📊 Full Analysis Report:")
    print(json.dumps(analysis_report, indent=2))
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    print(traceback.format_exc())

