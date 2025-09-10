#!/usr/bin/env python3
"""
Debug Bulletproof JSON Generation 
Test the complete JSON generation pipeline step by step
"""

import json
import sys
import os

# Add the current directory to path
sys.path.append(os.getcwd())

from topic_based_slide_generator import generate_topic_based_presentation
from bulletproof_json_generator import generate_bulletproof_json

# Mock LLM API call for testing
def mock_llm_call(messages):
    """Mock LLM call that returns realistic responses"""
    if "extract data" in str(messages).lower():
        return "Company: TechCorp, founded 2020, Dubai HQ. Products: AI software. Revenue: $10M (2023)"
    elif "research" in str(messages).lower():
        return "Research data: TechCorp market position, AI industry trends, financial projections"
    else:
        return "Generic response for testing"

# Sample conversation with multiple topics
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

print("🧪 DEBUGGING COMPLETE JSON GENERATION PIPELINE")
print("=" * 60)

# Step 1: Test topic-based slide generation
print("📊 STEP 1: Topic-based slide generation")
slide_list, render_plan, analysis_report = generate_topic_based_presentation(test_messages)
print(f"   Generated slides: {len(slide_list)} - {slide_list}")

# Step 2: Test bulletproof JSON generation
print(f"\n⚡ STEP 2: Bulletproof JSON generation with {len(slide_list)} slides")
try:
    bulletproof_response, content_ir, render_plan_json = generate_bulletproof_json(
        test_messages, 
        slide_list,
        mock_llm_call
    )
    
    print(f"✅ Bulletproof generation completed")
    print(f"   Content IR keys: {list(content_ir.keys()) if isinstance(content_ir, dict) else 'Not a dict'}")
    print(f"   Render plan slides: {len(render_plan_json.get('slides', [])) if isinstance(render_plan_json, dict) else 'Not a dict'}")
    
    # Check for the single slide issue
    if isinstance(render_plan_json, dict) and 'slides' in render_plan_json:
        actual_slides = len(render_plan_json['slides'])
        expected_slides = len(slide_list)
        
        if actual_slides == 1 and expected_slides > 1:
            print(f"\n❌ BUG FOUND: Expected {expected_slides} slides but got {actual_slides}")
            print("   This confirms the user's reported issue!")
            
            # Show what's in the render plan
            print(f"   Render plan content: {json.dumps(render_plan_json, indent=2)}")
        else:
            print(f"\n✅ Slide count correct: {actual_slides} slides generated")
    
except Exception as e:
    print(f"❌ ERROR in bulletproof generation: {e}")
    import traceback
    print(traceback.format_exc())

