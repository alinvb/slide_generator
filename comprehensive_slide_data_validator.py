"""
Comprehensive tool to validate all slide data extraction and identify missing data issues
"""

import json
from bulletproof_json_generator_clean import CleanBulletproofJSONGenerator

def validate_all_slide_types():
    """Validate data extraction for all investment banking slide types"""
    
    # Sample comprehensive content_ir that should contain all data
    comprehensive_content_ir = {
        "business_overview_data": {
            "strategic_positioning": "Leading streaming entertainment service with global presence",
            "key_value_propositions": [
                "Market-leading content library with 15,000+ titles",
                "230M+ subscribers across 190+ countries",  
                "Award-winning original programming"
            ],
            "key_offerings": [
                "Streaming Entertainment", 
                "Original Content Production",
                "International Expansion",
                "Technology Platform"
            ]
        },
        "facts": {
            "years": ["2020", "2021", "2022", "2023", "2024E"],
            "revenue_usd_m": [25000, 29698, 31616, 33723, 36000],
            "ebitda_usd_m": [4585, 5116, 5632, 6954, 8200]
        },
        "investor_considerations": {
            "considerations": [
                "Streaming market saturation risk",
                "Increased competition from Disney+, HBO Max",
                "Content acquisition cost inflation"
            ],
            "mitigants": [
                "Strong brand loyalty and retention metrics", 
                "Diversified global revenue streams",
                "Data-driven content investment strategy"
            ]
        },
        "product_service_data": {
            "offerings": [
                {"category": "Streaming Platform", "description": "Core video streaming service with personalized recommendations"},
                {"category": "Original Content", "description": "Exclusive series and movies produced in-house"},  
                {"category": "Gaming Integration", "description": "Mobile games included with subscription"},
                {"category": "Global Expansion", "description": "Localized content for international markets"}
            ]
        },
        "strategic_buyers": [
            {
                "name": "Disney",
                "type": "Media Conglomerate",
                "rationale": "Streaming platform consolidation",
                "synergies": "Content library combination",
                "considerations": "Regulatory scrutiny"
            },
            {
                "name": "Apple",
                "type": "Technology Giant", 
                "rationale": "Services ecosystem expansion",
                "synergies": "Hardware integration",
                "considerations": "Antitrust concerns"
            }
        ],
        "financial_buyers": [
            {
                "name": "KKR & Co",
                "type": "Private Equity",
                "rationale": "Cash flow generation potential",
                "synergies": "Operational improvements",
                "considerations": "Large deal size"
            },
            {
                "name": "Blackstone",
                "type": "Private Equity",
                "rationale": "Market leadership position", 
                "synergies": "Portfolio synergies",
                "considerations": "Public market volatility"
            }
        ],
        "management_team": [
            {
                "name": "Reed Hastings",
                "title": "Co-CEO & Chairman",
                "experience": "25+ years in technology and media",
                "background": "Founded Netflix in 1997, transformed from DVD to streaming"
            },
            {
                "name": "Ted Sarandos", 
                "title": "Co-CEO & Chief Content Officer",
                "experience": "20+ years in content and entertainment",
                "background": "Joined Netflix 2000, built original programming strategy"
            },
            {
                "name": "Spencer Neumann",
                "title": "Chief Financial Officer", 
                "experience": "20+ years in media finance",
                "background": "Former CFO at Activision Blizzard, Disney veteran"
            }
        ],
        "precedent_transactions": [
            {
                "target": "Time Warner",
                "acquirer": "AT&T",
                "date": "2018",
                "country": "USA",
                "enterprise_value": "$85.4B",
                "revenue": "$28.3B",
                "ev_revenue_multiple": "3.0x"
            },
            {
                "target": "21st Century Fox Assets",
                "acquirer": "Disney", 
                "date": "2019",
                "country": "USA",
                "enterprise_value": "$71.3B",
                "revenue": "$17.1B",
                "ev_revenue_multiple": "4.2x"
            },
            {
                "target": "MGM Holdings",
                "acquirer": "Amazon",
                "date": "2022", 
                "country": "USA",
                "enterprise_value": "$8.5B",
                "revenue": "$1.5B", 
                "ev_revenue_multiple": "5.7x"
            }
        ],
        "valuation_data": [
            {"method": "Precedent Transactions", "low": 25.0, "high": 35.0, "mean": 30.0},
            {"method": "Comparable Companies", "low": 20.0, "high": 30.0, "mean": 25.0},
            {"method": "DCF Analysis", "low": 22.0, "high": 32.0, "mean": 27.0}
        ],
        "competitive_landscape": [
            {
                "name": "Disney+",
                "market_share": "15%", 
                "subscribers": "150M",
                "positioning": "Family entertainment focus"
            },
            {
                "name": "HBO Max",
                "market_share": "8%",
                "subscribers": "75M", 
                "positioning": "Premium content strategy"
            },
            {
                "name": "Amazon Prime Video",
                "market_share": "12%",
                "subscribers": "200M",
                "positioning": "Bundled with e-commerce"
            }
        ],
        "growth_strategy_data": {
            "growth_strategy": {
                "strategies": [
                    "International market expansion",
                    "Original content investment", 
                    "Technology platform enhancement",
                    "Strategic partnerships",
                    "Gaming integration",
                    "Ad-supported tier launch"
                ]
            },
            "financial_projections": {
                "categories": ["2023", "2024E", "2025E"],
                "revenue": [33.7, 36.0, 42.5],
                "ebitda": [6.9, 8.2, 11.8]
            }
        }
    }
    
    # List of all slide types to validate
    slide_types = [
        "business_overview",
        "investor_considerations", 
        "product_service_footprint",
        "historical_financial_performance",
        "strategic_buyers",
        "financial_buyers", 
        "management_team",
        "precedent_transactions",
        "valuation_overview",
        "competitive_positioning",
        "growth_strategy_projections",
        "margin_cost_resilience",
        "risk_factors",
        "transaction_overview"
    ]
    
    generator = CleanBulletproofJSONGenerator()
    
    # Replicate the extract_slide_data function from bulletproof_json_generator_clean.py
    def extract_slide_data(slide_type: str, content_ir: dict) -> dict:
        """Extract slide data using the same logic as the main generator"""
        
        if slide_type == "business_overview":
            business_data = content_ir.get('business_overview_data', {})
            
            services = business_data.get('key_offerings', business_data.get('services', []))
            if not services:
                product_data = content_ir.get('product_service_data', {})
                offerings = product_data.get('offerings', [])
                services = [offering.get('category', '') for offering in offerings if offering.get('category')]
            
            return {
                "title": "Business Overview",
                "description": business_data.get('strategic_positioning', business_data.get('description', '')),
                "timeline": business_data.get('timeline', {}),
                "highlights": business_data.get('key_value_propositions', business_data.get('highlights', [])),
                "services": services,
                "positioning_desc": business_data.get('strategic_positioning', business_data.get('positioning_desc', ''))
            }
        
        elif slide_type in ["investment_considerations", "investor_considerations"]:
            return {
                "title": "Investor Considerations", 
                "considerations": content_ir.get('investor_considerations', {}).get('considerations', []),
                "mitigants": content_ir.get('investor_considerations', {}).get('mitigants', [])
            }
        
        elif slide_type == "product_service_footprint":
            product_data = content_ir.get('product_service_data', {})
            
            if not isinstance(product_data, dict):
                product_data = {}
            
            offerings = product_data.get('offerings', [])
            services = []
            
            if isinstance(offerings, list):
                for offering in offerings:
                    if isinstance(offering, dict):
                        service_name = offering.get('category', offering.get('name', ''))
                        service_desc = offering.get('description', '')
                        if service_name:
                            services.append(f"{service_name}: {service_desc}"[:100] + "..." if len(f"{service_name}: {service_desc}") > 100 else f"{service_name}: {service_desc}")
                    elif isinstance(offering, str):
                        services.append(offering)
            
            if not services and 'services' in product_data:
                fallback_services = product_data.get('services', [])
                if isinstance(fallback_services, list):
                    services = [str(s) for s in fallback_services if s]
            
            return {
                "title": "Product & Service Footprint",
                "services": services or [],
                "coverage_table": product_data.get('coverage_table', []) if isinstance(product_data.get('coverage_table', []), list) else [],
                "metrics": product_data.get('metrics', {}) if isinstance(product_data.get('metrics', {}), dict) else {}
            }
        
        elif slide_type in ["financial_performance", "historical_financial_performance"]:
            return {
                "title": "Historical Financial Performance",
                "chart": {
                    "title": "Revenue & EBITDA (2020-2024E)",
                    "categories": content_ir.get('facts', {}).get('years', []),
                    "revenue": content_ir.get('facts', {}).get('revenue_usd_m', []),
                    "ebitda": content_ir.get('facts', {}).get('ebitda_usd_m', [])
                }
            }
        
        elif slide_type == "strategic_buyers":
            buyers_data = content_ir.get('strategic_buyers', [])
            
            table_rows = []
            for buyer in buyers_data:
                if isinstance(buyer, dict):
                    table_rows.append({
                        "buyer_name": buyer.get('name', 'Strategic Buyer'),
                        "buyer_type": buyer.get('type', 'Corporate'),
                        "rationale": buyer.get('rationale', 'Strategic fit'),
                        "synergies": buyer.get('synergies', 'Operational synergies'),
                        "considerations": buyer.get('considerations', 'Integration risk')
                    })
            
            return {
                "title": "Strategic Buyers",
                "table_rows": table_rows
            }
        
        elif slide_type == "financial_buyers":
            buyers_data = content_ir.get('financial_buyers', [])
            
            table_rows = []
            for buyer in buyers_data:
                if isinstance(buyer, dict):
                    table_rows.append({
                        "buyer_name": buyer.get('name', 'Financial Buyer'),
                        "buyer_type": buyer.get('type', 'Private Equity'),
                        "rationale": buyer.get('rationale', 'Strong returns potential'),
                        "synergies": buyer.get('synergies', 'Operational improvements'),
                        "considerations": buyer.get('considerations', 'Market conditions')
                    })
            
            return {
                "title": "Financial Buyers",
                "table_rows": table_rows
            }
        
        elif slide_type == "management_team":
            team_data = content_ir.get('management_team', [])
            
            left_profiles = []
            right_profiles = []
            
            for i, member in enumerate(team_data):
                if isinstance(member, dict):
                    profile = {
                        "name": member.get('name', f'Executive {i+1}'),
                        "title": member.get('title', 'Senior Executive'),
                        "experience": member.get('experience', '10+ years experience'),
                        "background": member.get('background', 'Industry veteran')
                    }
                    
                    if i % 2 == 0:
                        left_profiles.append(profile)
                    else:
                        right_profiles.append(profile)
            
            return {
                "title": "Management Team",
                "left_column_profiles": left_profiles,
                "right_column_profiles": right_profiles
            }
        
        elif slide_type == "precedent_transactions":
            transactions = content_ir.get('precedent_transactions', [])
            
            processed_transactions = []
            
            for txn in transactions:
                if isinstance(txn, dict):
                    processed_txn = {
                        "target": txn.get('target', 'Target Company'),
                        "acquirer": txn.get('acquirer', 'Acquirer'),
                        "date": txn.get('date', 'N/A'),
                        "country": txn.get('country', 'N/A'),
                        "enterprise_value": txn.get('enterprise_value', 'Data Issue'),
                        "revenue": txn.get('revenue', 'Data Issue'),
                        "ev_revenue_multiple": txn.get('ev_revenue_multiple', 'N/A')
                    }
                    processed_transactions.append(processed_txn)
            
            return {
                "title": "Precedent Transactions",
                "transactions": processed_transactions
            }
        
        elif slide_type == "valuation_overview":
            valuation_data = content_ir.get('valuation_data', [])
            
            return {
                "title": "Valuation Overview",
                "valuation_data": valuation_data
            }
        
        elif slide_type == "competitive_positioning":
            competitors_data = content_ir.get('competitive_landscape', [])
            
            return {
                "title": "Competitive Positioning",
                "competitors": competitors_data
            }
        
        elif slide_type == "growth_strategy_projections":
            growth_data = content_ir.get('growth_strategy_data', {})
            
            return {
                "title": "Growth Strategy & Projections",
                "growth_strategy": growth_data.get('growth_strategy', {}),
                "financial_projections": growth_data.get('financial_projections', {})
            }
        
        else:
            # Default fallback for unhandled slide types
            return {
                "title": slide_type.replace('_', ' ').title(),
                "placeholder": "Data will be available when generated"
            }
    
    print("=== COMPREHENSIVE SLIDE DATA VALIDATION ===")
    print(f"Testing {len(slide_types)} slide types...")
    print()
    
    validation_results = {}
    
    for slide_type in slide_types:
        print(f"🔍 Validating: {slide_type}")
        
        # Extract slide data
        slide_data = extract_slide_data(slide_type, comprehensive_content_ir)
        
        # Analyze the extracted data
        data_issues = []
        data_summary = {}
        
        for key, value in slide_data.items():
            if key == "title":
                continue
                
            if isinstance(value, list):
                if len(value) == 0:
                    data_issues.append(f"Empty list: {key}")
                else:
                    data_summary[key] = f"{len(value)} items"
            elif isinstance(value, dict):
                if len(value) == 0:
                    data_issues.append(f"Empty dict: {key}")
                else:
                    data_summary[key] = f"Dict with {len(value)} fields"
            elif isinstance(value, str):
                if not value or value.strip() == "":
                    data_issues.append(f"Empty string: {key}")
                else:
                    data_summary[key] = f"Text ({len(value)} chars)"
            else:
                data_summary[key] = f"{type(value).__name__}: {value}"
        
        validation_results[slide_type] = {
            "data_summary": data_summary,
            "data_issues": data_issues,
            "slide_data": slide_data
        }
        
        if data_issues:
            print(f"  ⚠️ Issues found: {', '.join(data_issues)}")
        else:
            print(f"  ✅ Data looks good: {', '.join([f'{k}={v}' for k,v in data_summary.items()])}")
        
        print()
    
    # Summary
    print("=== VALIDATION SUMMARY ===")
    slides_with_issues = [slide for slide, result in validation_results.items() if result['data_issues']]
    slides_ok = [slide for slide, result in validation_results.items() if not result['data_issues']]
    
    print(f"✅ Slides OK: {len(slides_ok)}")
    for slide in slides_ok:
        print(f"   - {slide}")
    
    if slides_with_issues:
        print(f"\n⚠️ Slides with Issues: {len(slides_with_issues)}")
        for slide in slides_with_issues:
            issues = validation_results[slide]['data_issues']
            print(f"   - {slide}: {', '.join(issues)}")
    
    # Save detailed results
    with open('slide_validation_results.json', 'w') as f:
        json.dump(validation_results, f, indent=2)
    
    print(f"\n📄 Detailed results saved to 'slide_validation_results.json'")
    
    return validation_results

if __name__ == "__main__":
    validate_all_slide_types()
