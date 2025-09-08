#!/usr/bin/env python3
"""
Test script to identify slide generation errors with actual user data
"""

import json
import traceback
from pathlib import Path
from executor import execute_plan

def load_user_data():
    """Load the complete user-provided JSON data"""
    
    # Complete slides JSON from user
    slides_json = {
        "slides": [
            {
                "template": "business_overview",
                "data": {
                    "title": "Business Overview",
                    "description": "Saudi Aramco is the world's largest integrated oil and gas producer, engaged in exploration, production, refining, chemicals, and global distribution. It is the most profitable energy company worldwide and a central pillar of Saudi Arabia's economy.",
                    "timeline": {
                        "start_year": 1933,
                        "end_year": 2025
                    },
                    "highlights": [
                        "Largest proven oil reserves and production globally",
                        "Industry-leading margins and financial strength",
                        "Extensive global downstream and chemicals operations"
                    ],
                    "services": [
                        "Upstream oil and gas production",
                        "Downstream refining and petrochemicals",
                        "Energy trading and logistics"
                    ],
                    "positioning_desc": "Aramco is positioned as the global leader in energy scale, operational efficiency, and profitability, with unmatched reserves and integrated infrastructure."
                }
            },
            {
                "template": "investor_considerations",
                "data": {
                    "title": "Investor Considerations & Mitigants",
                    "considerations": [
                        "Oil price volatility and impact on profitability",
                        "Rising operating and capital costs",
                        "Geopolitical risks and regional instability",
                        "Energy transition pressures and ESG requirements",
                        "Corporate governance and transparency",
                        "Fiscal dependence of Saudi government"
                    ],
                    "mitigants": [
                        "Downstream diversification and renewables investment",
                        "Operational efficiency and cost management",
                        "Global partnerships and expansion",
                        "Sustainability initiatives and ESG programs",
                        "Government support and policy flexibility",
                        "Robust supply chain and reserves"
                    ]
                }
            }
        ]
    }
    
    # Complete content IR JSON from user
    content_ir_json = {
        "entities": {
            "company": {
                "name": "Saudi Aramco"
            }
        },
        "facts": {
            "years": ["2020", "2021", "2022", "2023", "2024E"],
            "revenue_usd_m": [229000, 400000, 495100, 480570, 461560],
            "ebitda_usd_m": [100000, 180000, 239000, 223000, 215000],
            "ebitda_margins": [43.7, 45.0, 48.3, 46.4, 46.6]
        },
        "management_team": {
            "left_column_profiles": [
                {
                    "role_title": "President & CEO",
                    "experience_bullets": [
                        "Over 35 years at Aramco, CEO since 2015",
                        "Led company through historic IPO and global expansion",
                        "Advances digitalization and sustainability initiatives",
                        "Recognized global energy sector leader",
                        "Oversees upstream, downstream, and strategy"
                    ]
                },
                {
                    "role_title": "Upstream President",
                    "experience_bullets": [
                        "Responsible for global upstream operations",
                        "Increased output to sustain 10% of global supply",
                        "Drives operational excellence and safety",
                        "Expert in reservoir management",
                        "Leads advanced technology implementation"
                    ]
                }
            ],
            "right_column_profiles": [
                {
                    "role_title": "CFO & EVP",
                    "experience_bullets": [
                        "Heads global finance, treasury, capital markets",
                        "Managed $5B bond issuance and capital optimization",
                        "Oversees financial planning and investor relations",
                        "Champions fiscal discipline and risk management",
                        "Extensive experience in energy finance"
                    ]
                }
            ]
        },
        "strategic_buyers": [
            {
                "buyer_name": "ExxonMobil",
                "description": "Largest US-based integrated oil & gas major, global operations",
                "strategic_rationale": "Expand reserves, access low-cost supply, enhance scale",
                "key_synergies": "Upstream scale, cost leadership, technology",
                "concerns": "Regulatory scrutiny, integration",
                "fit_score": "10/10",
                "financial_capacity": "$60B+ deal capacity"
            }
        ],
        "financial_buyers": [
            {
                "buyer_name": "The Carlyle Group",
                "description": "Global PE leader with $420B+ AUM, extensive energy team, deep upstream and midstream experience",
                "strategic_rationale": "Scale portfolio, operational improvement, global reach",
                "key_synergies": "Cross-border platform, energy transition, asset management",
                "concerns": "Regulatory, scale integration",
                "fit_score": "9/10",
                "financial_capacity": "$30B+ per deal"
            }
        ]
    }
    
    return slides_json, content_ir_json

def test_slide_rendering():
    """Test actual slide rendering with user data"""
    
    print("🔍 Testing slide generation with user data...\n")
    
    try:
        slides_json, content_ir_json = load_user_data()
        
        print(f"📊 Loaded {len(slides_json['slides'])} slides")
        print(f"📊 Loaded content IR with {len(content_ir_json)} sections")
        
        # Test individual slide templates
        import slide_templates
        from adapters import RENDERER_MAP
        
        for i, slide in enumerate(slides_json['slides']):
            print(f"\n🔍 Testing slide {i+1}: {slide['template']}")
            
            try:
                # Check if template exists in renderer map
                if slide['template'] in RENDERER_MAP:
                    renderer = RENDERER_MAP[slide['template']]
                    if renderer:
                        print(f"  ✅ Renderer found: {renderer.__name__}")
                        
                        # Try to create the slide with a test presentation
                        from pptx import Presentation
                        test_prs = Presentation()
                        
                        # Test with slide data
                        result = renderer(data=slide['data'], prs=test_prs)
                        print(f"  ✅ Slide rendered successfully")
                    else:
                        print(f"  ❌ Renderer is None for template: {slide['template']}")
                else:
                    print(f"  ❌ Template not found in RENDERER_MAP: {slide['template']}")
                    
            except Exception as e:
                print(f"  ❌ Error rendering slide: {e}")
                traceback.print_exc()
        
        # Test full render plan execution
        print(f"\n🔍 Testing full render plan execution...")
        
        try:
            result = execute_plan(slides_json, content_ir_json)
            print(f"  ✅ Render plan executed successfully")
            return True
            
        except Exception as e:
            print(f"  ❌ Error executing render plan: {e}")
            traceback.print_exc()
            return False
            
    except Exception as e:
        print(f"❌ Error in slide rendering test: {e}")
        traceback.print_exc()
        return False

def test_data_structure_mapping():
    """Test how user data maps to expected slide template structures"""
    
    print("\n🔍 Testing data structure mapping...\n")
    
    slides_json, content_ir_json = load_user_data()
    
    # Check expected vs actual structures
    expected_structures = {
        "business_overview": [
            "title", "description", "timeline", "highlights", 
            "services", "positioning_desc"
        ],
        "investor_considerations": [
            "title", "considerations", "mitigants"
        ]
    }
    
    for slide in slides_json['slides']:
        template = slide['template']
        data = slide['data']
        
        print(f"📋 Slide: {template}")
        
        if template in expected_structures:
            expected_fields = expected_structures[template]
            actual_fields = list(data.keys())
            
            missing_fields = set(expected_fields) - set(actual_fields)
            extra_fields = set(actual_fields) - set(expected_fields)
            
            if missing_fields:
                print(f"  ❌ Missing fields: {missing_fields}")
            if extra_fields:
                print(f"  ⚠️ Extra fields: {extra_fields}")
            if not missing_fields and not extra_fields:
                print(f"  ✅ All required fields present")
        else:
            print(f"  ⚠️ No structure defined for template: {template}")
        
        print(f"  📊 Actual fields: {list(data.keys())}")

if __name__ == "__main__":
    print("🚀 Starting slide generation analysis...\n")
    
    success = True
    
    # Test data structure mapping
    test_data_structure_mapping()
    
    # Test slide rendering
    if not test_slide_rendering():
        success = False
    
    if success:
        print("\n🎉 Slide generation test completed successfully!")
    else:
        print("\n💥 Slide generation errors found. Check output above for details.")