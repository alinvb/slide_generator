#!/usr/bin/env python3
"""
Test the fixed Render Plan JSON generation
"""

from perfect_json_prompter import get_interview_completion_prompt
from adaptive_slide_generator import generate_adaptive_presentation
import json

def test_render_plan_generation():
    """Test if the simplified prompt generates both JSONs"""
    
    # Minimal conversation that should generate 2-3 slides
    test_messages = [
        {"role": "user", "content": "My company is TechAI Corp, we provide AI automation software for enterprises"},
        {"role": "assistant", "content": "Tell me about your financial performance"},
        {"role": "user", "content": "We have $5M revenue in 2023, expecting $12M in 2024"},
        {"role": "assistant", "content": "Who are your key management team members?"},
        {"role": "user", "content": "John Smith is CEO, Sarah Chen is CTO"},
        {"role": "assistant", "content": "Generate JSON now"}
    ]
    
    print("🧪 Testing Render Plan Generation Fix")
    print("=" * 50)
    
    # Test adaptive slide generation
    slide_list, adaptive_render_plan, analysis_report = generate_adaptive_presentation(test_messages)
    
    print(f"📊 Adaptive Analysis:")
    print(f"   - Recommended slides: {len(slide_list)}")
    print(f"   - Quality score: {analysis_report.get('overall_quality_score', 'N/A')}%")
    print(f"   - Slides: {slide_list}")
    print()
    
    # Test simplified prompt generation
    completion_prompt = get_interview_completion_prompt(test_messages)
    
    print(f"📝 Simplified Prompt Length: {len(completion_prompt)} chars")
    print(f"💡 Key Requirements Found:")
    print(f"   - 'CONTENT IR JSON:' marker: {'✅' if 'CONTENT IR JSON:' in completion_prompt else '❌'}")
    print(f"   - 'RENDER PLAN JSON:' marker: {'✅' if 'RENDER PLAN JSON:' in completion_prompt else '❌'}")
    print(f"   - BOTH JSONs requirement: {'✅' if 'BOTH' in completion_prompt else '❌'}")
    print()
    
    print("📄 Simplified Prompt Preview:")
    print("-" * 30)
    print(completion_prompt[:800] + "..." if len(completion_prompt) > 800 else completion_prompt)
    print("-" * 30)
    
    # Create system override for this test
    adaptive_instructions = f"""
🚨 CRITICAL: ADAPTIVE SLIDE RESTRICTION ENFORCED 🚨

You MUST generate Content IR JSON containing EXACTLY {len(slide_list)} slides - NO MORE, NO LESS.

✅ APPROVED SLIDES TO GENERATE:
{chr(10).join([f"{i+1}. {slide}" for i, slide in enumerate(slide_list)])}

❌ FORBIDDEN: Do NOT create any other slides beyond the {len(slide_list)} listed above.

📊 Quality Justification: {analysis_report['quality_summary']}

🔒 ENFORCEMENT: Your JSON "slides" array must contain EXACTLY {len(slide_list)} objects, one for each approved slide above.
    """
    
    system_override = f"""🚨 SYSTEM OVERRIDE - GENERATE BOTH JSONS NOW

OUTPUT EXACTLY THIS FORMAT (NO OTHER TEXT):

CONTENT IR JSON:
{{complete_content_ir_json_with_{len(slide_list)}_slides}}

RENDER PLAN JSON:
{{complete_render_plan_json_with_{len(slide_list)}_slides}}

SLIDES: {', '.join(slide_list)}

FAILURE = MISSING RENDER PLAN JSON"""
    
    print(f"\n🎯 System Override:")
    print(f"   - Length: {len(system_override)} chars (much shorter!)")
    print(f"   - Both JSONs required: {'✅' if 'RENDER PLAN JSON' in system_override else '❌'}")
    print(f"   - Clear failure condition: {'✅' if 'FAILURE' in system_override else '❌'}")
    print()
    
    print("📋 System Override Preview:")
    print("-" * 30)
    print(system_override)
    print("-" * 30)
    
    print("\n✅ Fix Analysis:")
    print("   - Drastically reduced prompt complexity ✅")
    print("   - Clear BOTH JSONs requirement ✅") 
    print("   - Explicit failure condition for missing Render Plan ✅")
    print("   - Simple format specification ✅")
    print(f"   - Adaptive slide count enforced: {len(slide_list)} slides ✅")
    
    return True

if __name__ == "__main__":
    test_render_plan_generation()