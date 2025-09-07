#!/usr/bin/env python3
"""
Test enhanced management team validation requirements
"""

from app import validate_management_team_slide

print("=== Testing Enhanced Management Team Validation ===")

# Test Case 1: PROBLEMATIC content (should generate warnings)
problematic_slide = {
    "template": "management_team",
    "content_ir_key": "management_team"
}

problematic_content_ir = {
    "management_team": {
        "left_column_profiles": [
            {
                "role_title": "Chief Executive Officer",  # Missing name
                "experience_bullets": [
                    "Over 30 years at Aramco, CEO since 2015 leading the company through IPO and international expansion with strategic foresight",  # Too long
                    "Led the company through IPO and international expansion with strategic foresight and operational excellence",
                    "Recognized for strategic foresight and operational excellence that has driven record financial performance",
                    "Oversaw scale-up to 12 million barrels/day production while maintaining industry-leading cost efficiency",
                    "Drove digital transformation and decarbonization initiatives that position Aramco as an energy transition leader",  # 5 bullets (too many)
                    "Champion of technology innovation and sustainability programs that enhance operational efficiency"  # 6 bullets
                ]
            },
            {
                "role_title": "Executive Vice President & Chief Financial Officer - Ziad T. Al-Murshed Ahmed Hassan",  # Too long (>50 chars)
                "experience_bullets": [
                    "Finance experience",  # Too short
                    "Led bond issuance"    # Too short
                ]
            }
        ],
        "right_column_profiles": [
            {
                "role_title": "COO - John Smith",
                "experience_bullets": [
                    "Operations experience",
                    "Leadership background"
                ]
            }
        ]
    }
}

# Test Case 2: OPTIMIZED content (should pass validation)
optimized_slide = {
    "template": "management_team", 
    "content_ir_key": "management_team"
}

optimized_content_ir = {
    "management_team": {
        "left_column_profiles": [
            {
                "role_title": "CEO - Amin H. Nasser",  # Good format with name
                "experience_bullets": [
                    "30+ years at Aramco, CEO since 2015",  # Concise, under 80 chars
                    "Led company through IPO and international expansion",
                    "Oversaw scale-up to 12M barrels/day production",
                    "Champion of digital transformation initiatives"  # Exactly 4 bullets
                ]
            },
            {
                "role_title": "CFO - Ziad Al-Murshed",
                "experience_bullets": [
                    "Leads global finance and investor relations",
                    "Led $5B bond issuance attracting global capital", 
                    "20+ years Aramco finance leadership experience",
                    "Expert in treasury and risk management"
                ]
            }
        ],
        "right_column_profiles": [
            {
                "role_title": "COO - David Park",
                "experience_bullets": [
                    "20+ years multi-site operations experience",
                    "Successfully scaled 50+ locations across regions",
                    "Lean Six Sigma Master Black Belt certification",
                    "Former Regional Operations Director"
                ]
            }
        ]
    }
}

print("\n--- Testing PROBLEMATIC Content (Should Generate Warnings) ---")
prob_validation = validate_management_team_slide(problematic_slide, problematic_content_ir)
print("Issues:", prob_validation.get('issues', []))
print("Warnings:", prob_validation.get('warnings', []))
print("Missing Fields:", prob_validation.get('missing_fields', []))
print("Empty Fields:", prob_validation.get('empty_fields', []))

print(f"\n📊 Problematic Content Results:")
print(f"- Total warnings: {len(prob_validation.get('warnings', []))}")
print(f"- Total issues: {len(prob_validation.get('issues', []))}")

print("\n--- Testing OPTIMIZED Content (Should Pass) ---")
opt_validation = validate_management_team_slide(optimized_slide, optimized_content_ir)
print("Issues:", opt_validation.get('issues', []))
print("Warnings:", opt_validation.get('warnings', []))
print("Missing Fields:", opt_validation.get('missing_fields', []))
print("Empty Fields:", opt_validation.get('empty_fields', []))

print(f"\n📊 Optimized Content Results:")
print(f"- Total warnings: {len(opt_validation.get('warnings', []))}")
print(f"- Total issues: {len(opt_validation.get('issues', []))}")

print("\n=== Validation Enhancement Summary ===")
if len(prob_validation.get('warnings', [])) > len(opt_validation.get('warnings', [])):
    print("✅ SUCCESS: Enhanced validation correctly identifies problematic content")
    print("✅ Optimized content passes validation with fewer/no warnings") 
    print("\n🎯 Enhanced validation now checks for:")
    print("- Management team member names in role_title field")
    print("- Role title length limits (max 50 characters)")
    print("- Experience bullet length limits (max 80 characters)")
    print("- Optimal number of profiles (2-3 per column)")
    print("- Optimal number of bullets (max 4 per profile)")
    print("- Content quality (warns about very brief bullets)")
else:
    print("❌ ISSUE: Validation may need further adjustment")

print("\n🚀 AI will now automatically generate:")
print("- Role titles with executive names (e.g., 'CEO - John Smith')")
print("- Concise bullet points optimized for slide layout")
print("- Content that prevents text overlap issues")
print("- Professional management team presentations")