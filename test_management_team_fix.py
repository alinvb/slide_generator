#!/usr/bin/env python3
"""
Test script to verify management team names and centering fix
"""
import json
from executor import execute_plan

# Load the fixed JSONs
with open('/home/user/webapp/fixed_content_ir.json', 'r') as f:
    content_ir = json.load(f)

with open('/home/user/webapp/fixed_render_plan.json', 'r') as f:
    render_plan = json.load(f)

print("🔍 TESTING MANAGEMENT TEAM NAMES & CENTERING FIX")
print("="*60)

# Find the management team slide
management_slide = None
for slide in render_plan.get('slides', []):
    if slide.get('template') == 'management_team':
        management_slide = slide
        break

if management_slide:
    print(f"📋 Found management_team slide")
    
    slide_data = management_slide.get('data', {})
    left_profiles = slide_data.get('left_column_profiles', [])
    right_profiles = slide_data.get('right_column_profiles', [])
    
    print(f"\n👥 Management team structure:")
    print(f"   Left column profiles: {len(left_profiles)}")
    print(f"   Right column profiles: {len(right_profiles)}")
    print(f"   Total profiles: {len(left_profiles) + len(right_profiles)}")
    
    print(f"\n🏷️  Profile details:")
    all_profiles = left_profiles + right_profiles
    for i, profile in enumerate(all_profiles, 1):
        name = profile.get('name', 'No name')
        role = profile.get('role_title', 'No role')
        print(f"      Profile {i}: {name} - {role}")
    
    # Test generating just this slide
    print(f"\n🧪 Testing slide generation...")
    
    # Create a mini render plan with just this slide
    test_plan = {
        "slides": [management_slide]
    }
    
    try:
        prs, path = execute_plan(
            plan=test_plan,
            content_ir=content_ir,
            output_path="test_management_team_fix.pptx",
            company_name="LlamaIndex"
        )
        print(f"✅ Successfully generated test slide: {path}")
        print(f"   Slides created: {len(prs.slides)}")
        
    except Exception as e:
        print(f"❌ Error generating slide: {str(e)}")
        import traceback
        traceback.print_exc()
else:
    print("❌ No management_team slide found!")

print("\n🔍 Test complete")