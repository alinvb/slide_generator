"""
Test JSON parsing with control character issues
"""

import json
from app import clean_json_string, advanced_json_repair

def test_control_character_fix():
    """Test fixing invalid control characters in JSON"""
    
    print("🧪 TESTING JSON CONTROL CHARACTER FIXES")
    print("="*50)
    
    # Test case 1: JSON with control characters (simulated)
    json_with_control_chars = """{
  "entities": {"company": {"name": "Test\x08Company"}},
  "facts": {"revenue": [100, 200\x0c, 300]},
  "management_team": {"title": "Management\x07Team"}
}"""
    
    print("📝 Original JSON (with control chars):")
    print(repr(json_with_control_chars))
    
    print("\n🔧 Cleaning JSON...")
    cleaned = clean_json_string(json_with_control_chars)
    
    print("✅ Cleaned JSON:")
    print(repr(cleaned))
    
    # Try to parse
    try:
        parsed = json.loads(cleaned)
        print("✅ JSON parsing: SUCCESS")
        print(f"   Company name: {parsed['entities']['company']['name']}")
        return True
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing failed: {e}")
        return False

def test_complete_working_json():
    """Generate a complete working JSON for testing slides"""
    
    print("\n🚀 GENERATING COMPLETE WORKING JSON")
    print("="*50)
    
    # Create minimal but complete content IR
    content_ir = {
        "entities": {
            "company": {
                "name": "Test Company Ltd",
                "description": "A test company for demonstration",
                "founded": "2020",
                "headquarters": "Singapore"
            }
        },
        "facts": {
            "years": ["2021", "2022", "2023", "2024E"],
            "revenue_usd_m": [10, 15, 22, 30],
            "ebitda_usd_m": [2, 3.5, 5.5, 8],
            "ebitda_margins": [20.0, 23.3, 25.0, 26.7]
        },
        "management_team": {
            "left_column_profiles": [
                {
                    "role_title": "Chief Executive Officer",
                    "experience_bullets": [
                        "15+ years of experience in technology and business development",
                        "Previously served as VP at leading tech companies",
                        "Expert in scaling startup organizations",
                        "MBA from top business school"
                    ]
                },
                {
                    "role_title": "Chief Financial Officer", 
                    "experience_bullets": [
                        "12+ years of finance and accounting experience",
                        "Previously CFO at successful startup",
                        "Expert in financial planning and fundraising",
                        "CPA certified"
                    ]
                }
            ],
            "right_column_profiles": [
                {
                    "role_title": "Chief Technology Officer",
                    "experience_bullets": [
                        "20+ years of technology leadership experience",
                        "Previously CTO at major software company",
                        "Expert in cloud architecture and AI/ML",
                        "Computer Science PhD"
                    ]
                }
            ]
        },
        "strategic_buyers": [
            {
                "buyer_name": "TechCorp Inc",
                "strategic_rationale": "Technology synergies and market expansion",
                "fit": "High (9/10)"
            },
            {
                "buyer_name": "Global Solutions Ltd",
                "strategic_rationale": "Product portfolio complementarity",
                "fit": "Medium (7/10)"
            }
        ],
        "financial_buyers": [
            {
                "buyer_name": "Growth Capital Partners",
                "strategic_rationale": "Strong growth potential in target sector",
                "fit": "High (8/10)"
            },
            {
                "buyer_name": "Tech Investment Fund",
                "strategic_rationale": "Specialized technology investment focus",
                "fit": "High (9/10)"
            }
        ],
        "sea_conglomerates": [
            {
                "buyer_name": "Singapore Holdings Pte Ltd",
                "strategic_rationale": "Regional expansion and technology integration",
                "fit": "High (8/10)"
            }
        ],
        "competitive_analysis": {
            "competitors": ["Competitor A", "Competitor B", "Competitor C"],
            "assessment": [
                ["Company", "Market Share", "Technology", "Revenue"],
                ["Test Company", "15%", "Advanced", "$30M"],
                ["Competitor A", "25%", "Standard", "$45M"],
                ["Competitor B", "20%", "Advanced", "$40M"]
            ]
        },
        "precedent_transactions": [
            {
                "target": "Similar Company A",
                "acquirer": "Large Corp",
                "date": "2024",
                "enterprise_value": 150,
                "revenue": 25,
                "ev_revenue_multiple": 6.0
            }
        ],
        "valuation_data": {
            "methodologies": ["DCF", "Comparable Companies", "Precedent Transactions"],
            "dcf_assumptions": {
                "growth_rates": [15, 12, 10],
                "discount_rate": 12.0
            }
        }
    }
    
    # Create render plan
    render_plan = {
        "slides": [
            {"template": "business_overview", "data": {"title": "Business Overview"}},
            {"template": "management_team", "data": {"title": "Management Team"}},
            {"template": "historical_financial_performance", "data": {"title": "Financial Performance"}},
            {"template": "competitive_positioning", "data": {"title": "Competitive Positioning"}},
            {"template": "buyer_profiles", "data": {"title": "Strategic Buyers"}},
            {"template": "sea_conglomerates", "data": {"title": "SEA Conglomerates"}},
            {"template": "valuation_overview", "data": {"title": "Valuation Overview"}}
        ]
    }
    
    # Save to files
    with open('test_content_ir.json', 'w') as f:
        json.dump(content_ir, f, indent=2)
    
    with open('test_render_plan.json', 'w') as f:
        json.dump(render_plan, f, indent=2)
    
    print("✅ Generated test files:")
    print("   - test_content_ir.json")
    print("   - test_render_plan.json")
    
    print(f"\n📊 Content IR Summary:")
    print(f"   Company: {content_ir['entities']['company']['name']}")
    print(f"   Revenue years: {len(content_ir['facts']['years'])}")
    print(f"   Management profiles: {len(content_ir['management_team']['left_column_profiles']) + len(content_ir['management_team']['right_column_profiles'])}")
    print(f"   Strategic buyers: {len(content_ir['strategic_buyers'])}")
    print(f"   Financial buyers: {len(content_ir['financial_buyers'])}")
    print(f"   SEA conglomerates: {len(content_ir['sea_conglomerates'])}")
    
    print(f"\n📋 Render Plan Summary:")
    print(f"   Total slides: {len(render_plan['slides'])}")
    for i, slide in enumerate(render_plan['slides'], 1):
        print(f"   {i}. {slide['template']}")
    
    return content_ir, render_plan

if __name__ == "__main__":
    print("🧪 JSON PARSING AND GENERATION TESTS")
    print("="*60)
    
    # Test 1: Control character fix
    success = test_control_character_fix()
    
    # Test 2: Complete working JSON
    content_ir, render_plan = test_complete_working_json()
    
    print(f"\n📊 TEST RESULTS:")
    print(f"{'✅' if success else '❌'} Control character fix: {'PASSED' if success else 'FAILED'}")
    print(f"✅ Complete JSON generation: PASSED")
    
    print(f"\n🎯 NEXT STEPS:")
    print(f"1. Use the generated test files to verify slide generation works")
    print(f"2. Test with the app's JSON editor to ensure compatibility")
    print(f"3. Generate actual PowerPoint slides to confirm end-to-end functionality")