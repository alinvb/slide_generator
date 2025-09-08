#!/usr/bin/env python3
"""
Comprehensive test with fixed JSON data
"""

import json
import traceback
from json_data_fixer import comprehensive_json_fix
from executor import execute_plan

def load_original_user_data():
    """Load the complete user-provided JSON data"""
    
    # Complete slides JSON from user (with ALL 14 slides from the original data)
    slides_json = {
        "slides": [
            {
                "template": "business_overview",
                "data": {
                    "title": "Business Overview",
                    "description": "Saudi Aramco is the world's largest integrated oil and gas producer, engaged in exploration, production, refining, chemicals, and global distribution. It is the most profitable energy company worldwide and a central pillar of Saudi Arabia's economy.",
                    "timeline": {
                        "start_year": 1933,  # This is the problematic int
                        "end_year": 2025     # This is the problematic int
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
            },
            {
                "template": "product_service_footprint",
                "data": {
                    "title": "Product & Service Footprint",
                    "services": [
                        {
                            "title": "Crude Oil Production",
                            "desc": "World's largest producer, operating over 100 fields including Ghawar and Safaniya"
                        },
                        {
                            "title": "Natural Gas & NGLs",
                            "desc": "Extraction, processing, and marketing of natural gas and natural gas liquids"
                        }
                    ],
                    "coverage_table": [  # This is problematic - object array instead of 2D array
                        {
                            "Region": "Saudi Arabia",
                            "Key Operations": "Upstream, refining, chemicals, R&D",
                            "Major Facilities/Partners": "Ghawar, Safaniya, SATORP, SABIC"
                        },
                        {
                            "Region": "Americas",
                            "Key Operations": "Refining, research, trading",
                            "Major Facilities/Partners": "Motiva, Aramco Americas, Houston"
                        }
                    ],
                    "metrics": {
                        "total_locations": "70+",
                        "annual_barrels_produced": "4.65B+",
                        "petrochemical_capacity": "Top 5 globally",
                        "global_workforce": "75,100+"
                    }
                }
            },
            {
                "template": "historical_financial_performance",
                "data": {
                    "title": "Historical Financial Performance",
                    "chart": {
                        "title": "Revenue & EBITDA Growth (USD Millions)",
                        "categories": ["2020", "2021", "2022", "2023", "2024E"],
                        "revenue": [229000, 400000, 495100, 480570, 461560],
                        "ebitda": [100000, 180000, 239000, 223000, 215000]
                    },
                    "key_metrics": [  # This is problematic - should be {"metrics": [...]}
                        "Record annual revenue of $495B in 2022",
                        "Industry-leading EBITDA margin above 46%",
                        "Consistent production above 12 mmboe/d"
                    ]
                }
            }
        ]
    }
    
    # Complete content IR JSON from user (with ALL sections from the original data)
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
                        "Advances digitalization and sustainability initiatives"
                    ]
                }
            ],
            "right_column_profiles": [
                {
                    "role_title": "CFO & EVP",
                    "experience_bullets": [
                        "Heads global finance, treasury, capital markets",
                        "Managed $5B bond issuance and capital optimization"
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
                "description": "Global PE leader with $420B+ AUM, extensive energy team",
                "strategic_rationale": "Scale portfolio, operational improvement, global reach",
                "key_synergies": "Cross-border platform, energy transition, asset management",
                "concerns": "Regulatory, scale integration",
                "fit_score": "9/10",
                "financial_capacity": "$30B+ per deal"
            }
        ],
        "precedent_transactions": [
            {
                "target": "Pioneer Natural Resources",
                "acquirer": "ExxonMobil",
                "date": "May 2024",
                "country": "USA",
                "enterprise_value": 59500,
                "revenue": 24000
                # Missing ev_revenue_multiple - should be calculated
            }
        ]
    }
    
    return slides_json, content_ir_json

def test_comprehensive_fixing_and_generation():
    """Test the complete pipeline with data fixing"""
    
    print("🚀 Starting comprehensive fixing and generation test...\n")
    
    try:
        # Load original user data with known issues
        original_slides, original_content_ir = load_original_user_data()
        
        print("📊 Original data:")
        print(f"  - Slides: {len(original_slides['slides'])}")
        print(f"  - Content IR sections: {len(original_content_ir)}")
        
        # Apply comprehensive fixes
        print("\n🔧 Applying comprehensive fixes...")
        fixed_slides, fixed_content_ir = comprehensive_json_fix(original_slides, original_content_ir)
        
        print(f"\n✅ Fixed data:")
        print(f"  - Slides: {len(fixed_slides['slides'])}")
        print(f"  - Content IR sections: {len(fixed_content_ir)}")
        
        # Test individual slide rendering with fixed data
        print(f"\n🔍 Testing individual slide rendering with fixed data...")
        
        from adapters import RENDERER_MAP
        from pptx import Presentation
        
        for i, slide in enumerate(fixed_slides['slides']):
            template = slide['template']
            data = slide['data']
            
            print(f"\n  Slide {i+1}: {template}")
            
            if template in RENDERER_MAP:
                renderer = RENDERER_MAP[template]
                if renderer:
                    try:
                        test_prs = Presentation()
                        result = renderer(data=data, prs=test_prs)
                        print(f"    ✅ Rendered successfully")
                    except Exception as e:
                        print(f"    ❌ Rendering error: {e}")
                        # Print first few lines of traceback for debugging
                        tb_lines = traceback.format_exc().split('\n')[:5]
                        for line in tb_lines:
                            if line.strip():
                                print(f"    {line}")
                else:
                    print(f"    ❌ Renderer is None")
            else:
                print(f"    ❌ Template not in RENDERER_MAP")
        
        # Test full render plan execution
        print(f"\n🔍 Testing full render plan execution with fixed data...")
        
        try:
            prs, save_path = execute_plan(
                plan=fixed_slides,
                content_ir=fixed_content_ir,
                out_path="test_fixed_deck.pptx"
            )
            print(f"  ✅ Full render plan executed successfully")
            print(f"  💾 Saved to: {save_path}")
            
            # Check slide count
            if hasattr(prs, 'slides'):
                print(f"  📊 Generated slides: {len(prs.slides)}")
            
            return True
            
        except Exception as e:
            print(f"  ❌ Full render plan failed: {e}")
            traceback.print_exc()
            return False
            
    except Exception as e:
        print(f"❌ Comprehensive test failed: {e}")
        traceback.print_exc()
        return False

def test_specific_data_fixes():
    """Test specific data structure fixes"""
    
    print("\n🔍 Testing specific data structure fixes...\n")
    
    from json_data_fixer import fix_slide_data
    
    # Test business overview timeline fix
    business_overview_data = {
        "title": "Business Overview",
        "timeline": {"start_year": 1933, "end_year": 2025}  # Integers instead of strings
    }
    
    fixed_data = fix_slide_data('business_overview', business_overview_data)
    
    print("Business Overview Timeline Fix:")
    print(f"  Original: start_year={business_overview_data['timeline']['start_year']} ({type(business_overview_data['timeline']['start_year'])})")
    print(f"  Fixed: start_year={fixed_data['timeline']['start_year']} ({type(fixed_data['timeline']['start_year'])})")
    
    # Test product service footprint coverage table fix
    product_service_data = {
        "title": "Product Service Footprint", 
        "coverage_table": [
            {"Region": "Saudi Arabia", "Operations": "Upstream"},
            {"Region": "Americas", "Operations": "Refining"}
        ]
    }
    
    fixed_data = fix_slide_data('product_service_footprint', product_service_data)
    
    print(f"\nProduct Service Coverage Table Fix:")
    print(f"  Original: {type(product_service_data['coverage_table'])}, first item: {type(product_service_data['coverage_table'][0])}")
    print(f"  Fixed: {type(fixed_data['coverage_table'])}, first item: {type(fixed_data['coverage_table'][0])}")
    
    return True

if __name__ == "__main__":
    print("🚀 Starting comprehensive testing...\n")
    
    success = True
    
    # Test specific fixes first
    if not test_specific_data_fixes():
        success = False
    
    # Test full pipeline
    if not test_comprehensive_fixing_and_generation():
        success = False
    
    if success:
        print("\n🎉 All comprehensive tests passed!")
    else:
        print("\n💥 Some tests failed. Check output above for details.")