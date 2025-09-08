#!/usr/bin/env python3
"""
Complete end-to-end test using the original user data with all 14 slides as provided
"""

import json
import traceback
from executor import execute_plan

def load_complete_user_data():
    """Load the complete user data with ALL slides and content as originally provided"""
    
    # Complete 14 slides JSON as provided by the user
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
                        },
                        {
                            "title": "Refining & Petrochemicals",
                            "desc": "Integrated refining and petrochemical operations, including SABIC acquisition"
                        },
                        {
                            "title": "Lubricants & Premium Products",
                            "desc": "Branded lubricants, base oils, and specialty products for automotive and industrial customers"
                        }
                    ],
                    "coverage_table": [
                        {
                            "Region": "Saudi Arabia",
                            "Key Operations": "Upstream, refining, chemicals, R&D",
                            "Major Facilities/Partners": "Ghawar, Safaniya, SATORP, SABIC"
                        },
                        {
                            "Region": "Americas",
                            "Key Operations": "Refining, research, trading",
                            "Major Facilities/Partners": "Motiva, Aramco Americas, Houston"
                        },
                        {
                            "Region": "Asia",
                            "Key Operations": "Petrochemicals, refining, marketing",
                            "Major Facilities/Partners": "Hyundai Oilbank, Idemitsu Kosan"
                        },
                        {
                            "Region": "Europe",
                            "Key Operations": "Refining, chemicals, partnerships",
                            "Major Facilities/Partners": "SATORP JV (France), TotalEnergies"
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
                    "key_metrics": [
                        "Record annual revenue of $495B in 2022",
                        "Industry-leading EBITDA margin above 46%",
                        "Consistent production above 12 mmboe/d"
                    ],
                    "revenue_growth": {
                        "title": "Revenue Growth Drivers",
                        "points": [
                            "Growth in gas and chemicals output",
                            "Expansion in high-growth international markets",
                            "Efficiency gains from digital transformation"
                        ]
                    },
                    "banker_view": {
                        "title": "Banker View",
                        "text": "Saudi Aramco demonstrates resilient performance through commodity cycles, backed by scale, cost leadership, and diversified downstream assets."
                    }
                }
            },
            {
                "template": "management_team",
                "data": {
                    "title": "Management Team",
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
                        },
                        {
                            "role_title": "Downstream President",
                            "experience_bullets": [
                                "Oversees refining, chemicals, and distribution",
                                "Led major acquisitions including SABIC integration",
                                "Focused on efficiency and portfolio diversification",
                                "Drives global chemicals expansion",
                                "Key driver of downstream strategy"
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
                        },
                        {
                            "role_title": "EVP Technology & Innovation",
                            "experience_bullets": [
                                "Leads R&D and digital transformation",
                                "Invests in sustainability and advanced materials",
                                "Oversees global research centers",
                                "Architect of energy transition strategy",
                                "Expert in deploying new technologies"
                            ]
                        },
                        {
                            "role_title": "CEO, Aramco Ventures",
                            "experience_bullets": [
                                "Leads strategic venturing and tech investments",
                                "Manages Prosperity7 fund and startup acceleration",
                                "Portfolio management and innovation ecosystem",
                                "Background in upstream and downstream ops",
                                "Drives global innovation partnerships"
                            ]
                        }
                    ]
                }
            },
            {
                "template": "growth_strategy_projections",
                "data": {
                    "title": "Growth Strategy & Financial Projections",
                    "slide_data": {
                        "title": "Growth Strategy & Projections",
                        "growth_strategy": {
                            "strategies": [
                                "Expand natural gas production and unconventional fields (Jafurah)",
                                "Scale-up blue/green hydrogen and CCUS facilities",
                                "Diversify downstream and chemicals with new global JVs",
                                "Invest in digital transformation and operational efficiency",
                                "Accelerate renewables and green financing"
                            ]
                        },
                        "financial_projections": {
                            "categories": ["2024E", "2025E", "2026E"],
                            "revenue": [461560, 480000, 495000],
                            "ebitda": [215000, 230000, 246000]
                        }
                    }
                }
            },
            {
                "template": "competitive_positioning",
                "data": {
                    "title": "Competitive Positioning",
                    "competitors": [
                        {"name": "ExxonMobil", "revenue": 509000},
                        {"name": "Chevron", "revenue": 288000},
                        {"name": "Shell", "revenue": 225000},
                        {"name": "BP", "revenue": 103000},
                        {"name": "PetroChina", "revenue": 243000},
                        {"name": "TotalEnergies", "revenue": 165000}
                    ],
                    "assessment": [
                        {
                            "category": "Market Cap (2024)",
                            "our_company": "$1,570B",
                            "competitor_a": "$509B",
                            "competitor_b": "$288B"
                        },
                        {
                            "category": "Oil Production",
                            "our_company": "Highest, concentrated",
                            "competitor_a": "Top 3, diversified",
                            "competitor_b": "Top 5, diversified"
                        }
                    ],
                    "barriers": [
                        {
                            "title": "Vast Reserve Base",
                            "desc": "Largest oil reserves globally with low-cost extraction"
                        }
                    ],
                    "advantages": [
                        {
                            "title": "Lowest Production Cost",
                            "desc": "Unique geology and scale yield industry-leading margins"
                        }
                    ]
                }
            },
            {
                "template": "valuation_overview",
                "data": {
                    "title": "Valuation Overview",
                    "valuation_data": [
                        {
                            "methodology": "Public Market",
                            "enterprise_value": "$1.57T",
                            "metric": "P/E",
                            "22a_multiple": "16x",
                            "23e_multiple": "15.5x",
                            "commentary": "Premium to Asian peers; in line with global majors"
                        }
                    ]
                }
            },
            {
                "template": "precedent_transactions",
                "data": {
                    "title": "Precedent Transactions",
                    "transactions": [
                        {
                            "target": "Pioneer Natural Resources",
                            "acquirer": "ExxonMobil",
                            "date": "May 2024",
                            "country": "USA",
                            "enterprise_value": 59500,
                            "revenue": 24000,
                            "ev_revenue_multiple": 2.5
                        }
                    ]
                }
            },
            {
                "template": "margin_cost_resilience",
                "data": {
                    "title": "Margin & Cost Resilience",
                    "chart_title": "EBITDA Margin Trend",
                    "chart_data": {
                        "categories": ["2020", "2021", "2022", "2023", "2024E"],
                        "values": [43.7, 45.0, 48.3, 46.4, 46.6]
                    },
                    "cost_management": {
                        "items": [
                            {
                                "title": "Shariah-Compliant Debt",
                                "description": "Issued sukuk to optimize capital structure and reduce cost of capital"
                            }
                        ]
                    },
                    "risk_mitigation": {
                        "main_strategy": "Debt restructuring, dividend adjustment, and diversification into green energy projects, supported by government policy flexibility and operational scalability"
                    }
                }
            },
            {
                "template": "sea_conglomerates",
                "data": {
                    "title": "Southeast Asian Conglomerates",
                    "data": [
                        {
                            "name": "Petronas",
                            "country": "Malaysia",
                            "description": "State-owned, largest integrated oil & gas company in Southeast Asia",
                            "key_shareholders": "Government of Malaysia",
                            "key_financials": "Revenue: ~$70B; Assets: $160B; Net Profit: $10B",
                            "moelis_contact": "John Lee"
                        }
                    ]
                }
            },
            {
                "template": "buyer_profiles",
                "content_ir_key": "strategic_buyers",
                "data": {
                    "title": "Strategic Buyer Profiles",
                    "table_headers": [
                        "Buyer Name",
                        "Description",
                        "Strategic Rationale",
                        "Key Synergies",
                        "Concerns",
                        "Fit Score",
                        "Financial Capacity"
                    ],
                    "table_rows": [
                        {
                            "buyer_name": "ExxonMobil",
                            "description": "Largest US-based integrated oil & gas major, global operations",
                            "strategic_rationale": "Expand reserves, access low-cost supply, enhance scale",
                            "key_synergies": "Upstream scale, cost leadership, technology",
                            "concerns": "Regulatory scrutiny, integration",
                            "fit_score": "10/10",
                            "financial_capacity": "$60B+ deal capacity"
                        }
                    ]
                }
            },
            {
                "template": "buyer_profiles",
                "content_ir_key": "financial_buyers",
                "data": {
                    "title": "Financial Buyer Profiles",
                    "table_headers": [
                        "Buyer Name",
                        "Description",
                        "Strategic Rationale",
                        "Key Synergies",
                        "Concerns",
                        "Fit Score",
                        "Financial Capacity"
                    ],
                    "table_rows": [
                        {
                            "buyer_name": "The Carlyle Group",
                            "description": "Global PE leader with $420B+ AUM, extensive energy team",
                            "strategic_rationale": "Scale portfolio, operational improvement, global reach",
                            "key_synergies": "Cross-border platform, energy transition, asset management",
                            "concerns": "Regulatory, scale integration",
                            "fit_score": "9/10",
                            "financial_capacity": "$30B+ per deal"
                        }
                    ]
                }
            }
        ]
    }
    
    # Complete content IR JSON as provided by the user
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
                        "Led company through historic IPO and global expansion"
                    ]
                }
            ],
            "right_column_profiles": [
                {
                    "role_title": "CFO & EVP",
                    "experience_bullets": [
                        "Heads global finance, treasury, capital markets"
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
        "competitive_analysis": {
            "competitors": [
                {"name": "ExxonMobil", "revenue": 509000},
                {"name": "Chevron", "revenue": 288000}
            ]
        },
        "precedent_transactions": [
            {
                "target": "Pioneer Natural Resources",
                "acquirer": "ExxonMobil",
                "date": "May 2024",
                "country": "USA",
                "enterprise_value": 59500,
                "revenue": 24000
            }
        ],
        "valuation_data": [
            {
                "methodology": "Public Market",
                "enterprise_value": "$1.57T",
                "metric": "P/E",
                "22a_multiple": "16x",
                "23e_multiple": "15.5x",
                "commentary": "Premium to Asian peers"
            }
        ]
    }
    
    return slides_json, content_ir_json

def test_complete_user_data_pipeline():
    """Test the complete pipeline with all 13 slides from user data"""
    
    print("🚀 Testing complete user data pipeline...\n")
    
    try:
        # Load complete user data
        slides_json, content_ir_json = load_complete_user_data()
        
        print(f"📊 Loaded user data:")
        print(f"  - Slides: {len(slides_json['slides'])}")
        print(f"  - Content IR sections: {len(content_ir_json)}")
        
        # List all slide templates
        slide_templates = [slide['template'] for slide in slides_json['slides']]
        print(f"  - Slide templates: {slide_templates}")
        
        # Test execution with the complete validation pipeline
        print(f"\n🔧 Testing execution with validation pipeline...")
        
        prs, save_path = execute_plan(
            plan=slides_json,
            content_ir=content_ir_json,
            out_path="complete_user_deck.pptx"
        )
        
        print(f"  ✅ Full pipeline executed successfully")
        print(f"  💾 Saved to: {save_path}")
        
        if hasattr(prs, 'slides'):
            print(f"  📊 Generated slides: {len(prs.slides)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Complete pipeline test failed: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Testing complete user data pipeline...\n")
    
    if test_complete_user_data_pipeline():
        print("\n🎉 Complete user data pipeline test passed!")
    else:
        print("\n💥 Complete user data pipeline test failed.")