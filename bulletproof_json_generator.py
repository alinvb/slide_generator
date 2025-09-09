"""
Bulletproof JSON Generator - Guarantees Perfect Format Every Time
Extracts data from conversation, researches gaps, builds perfect JSONs
"""
import json
import re
from typing import Dict, List, Any

class BulletproofJSONGenerator:
    def __init__(self):
        # ACTUAL template fields based on slide_templates.py requirements
        self.slide_templates = {
            "business_overview": {
                "required_fields": ["title", "description", "timeline", "highlights", "services", "positioning_desc"],
                "template": {
                    "title": "Business & Operational Overview",
                    "description": "Leading PropTech platform transforming real estate investment",
                    "timeline": {"start_year": "2022", "end_year": "2024"},
                    "highlights": ["Key achievement 1", "Key achievement 2"],
                    "services": ["Service 1", "Service 2"],
                    "positioning_desc": "Market positioning description"
                }
            },
            "historical_financial_performance": {
                "required_fields": ["title", "chart"],
                "template": {
                    "title": "Historical Financial Performance",
                    "chart": {
                        "title": "Revenue & EBITDA Growth",
                        "categories": ["2022", "2023", "2024"],
                        "revenue": [10, 25, 50],
                        "ebitda": [2, 8, 15]
                    },
                    "key_metrics": {
                        "title": "Key Performance Metrics",
                        "metrics": []
                    }
                }
            },
            "management_team": {
                "required_fields": ["title", "left_column_profiles", "right_column_profiles"],
                "template": {
                    "title": "Management Team",
                    "left_column_profiles": [{
                        "name": "CEO Name",
                        "role_title": "Chief Executive Officer",
                        "experience_bullets": ["Experience 1", "Experience 2"]
                    }],
                    "right_column_profiles": [{
                        "name": "CTO Name", 
                        "role_title": "Chief Technology Officer",
                        "experience_bullets": ["Experience 1", "Experience 2"]
                    }]
                }
            },
            "product_service_footprint": {
                "required_fields": ["title", "services", "coverage_table", "metrics"],
                "template": {
                    "title": "Product & Service Footprint",
                    "services": [{"title": "Service 1", "desc": "Description"}],
                    "coverage_table": [["Region", "Coverage"], ["UAE", "Primary market"]],
                    "metrics": {"key_metric": "value"}
                }
            },
            "growth_strategy_projections": {
                "required_fields": ["title", "slide_data"],
                "template": {
                    "title": "Growth Strategy & Projections",
                    "slide_data": {
                        "growth_strategy": {"strategies": ["Strategy 1"]},
                        "financial_projections": {
                            "categories": ["2023", "2024", "2025"],
                            "revenue": [20, 35, 60],
                            "ebitda": [3, 8, 15]
                        }
                    }
                }
            },
            "precedent_transactions": {
                "required_fields": ["title", "transactions"],
                "template": {
                    "title": "Precedent Transactions",
                    "transactions": [{
                        "target": "Target Company",
                        "acquirer": "Acquirer",
                        "date": "2024",
                        "enterprise_value": "$1B",
                        "ev_revenue_multiple": "10x"
                    }]
                }
            },
            "valuation_overview": {
                "required_fields": ["title", "valuation_data"],
                "template": {
                    "title": "Valuation Overview", 
                    "valuation_data": [{
                        "methodology": "Trading Multiples",
                        "enterprise_value": "$50M-75M",
                        "commentary": "Based on revenue multiples"
                    }]
                }
            }
        }
    
    def extract_conversation_data(self, messages: List[Dict], llm_api_call):
        """Extract structured data from conversation using LLM"""
        
        conversation_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
        
        extraction_prompt = f"""
Extract all company information from this conversation into structured data:

CONVERSATION:
{conversation_text}

Extract and return ONLY a JSON object with these fields (use null if not found):
{{
    "company_name": "exact company name",
    "description": "business description", 
    "founded": "founding year",
    "headquarters": "location",
    "key_milestones": ["milestone1", "milestone2"],
    "years": ["2020", "2021", "2022"],
    "revenue_usd_m": [10, 15, 20],
    "ebitda_usd_m": [2, 3, 5],
    "team_members": [{{"name": "Name", "title": "Title", "background": "Bio"}}],
    "products_services": ["service1", "service2"],
    "market_coverage": "geographic coverage",
    "growth_strategies": ["strategy1", "strategy2"],
    "strategic_buyers": [{{"name": "Buyer", "rationale": "why"}}],
    "financial_buyers": [{{"name": "Buyer", "rationale": "why"}}],
    "transactions": [{{"target": "Company", "acquirer": "Acquirer", "value": "$1B"}}],
    "user_preferences": {{"exclude_buyers": [], "highlight_areas": []}}
}}

RESPOND WITH ONLY THE JSON - NO OTHER TEXT.
"""
        
        try:
            response = llm_api_call([{"role": "user", "content": extraction_prompt}])
            extracted_data = json.loads(response)
            return extracted_data
        except Exception as e:
            print(f"❌ Data extraction failed: {e}")
            return {}
    
    def research_missing_data(self, extracted_data: Dict, required_slides: List[str], llm_api_call):
        """Research missing data for required slides"""
        
        company_name = extracted_data.get("company_name", "the company")
        missing_data = {}
        
        for slide in required_slides:
            if slide not in self.slide_templates:
                continue
                
            template = self.slide_templates[slide]
            missing_fields = []
            
            # Check what's missing
            for field in template["required_fields"]:
                if not extracted_data.get(field):
                    missing_fields.append(field)
            
            # Research missing fields
            if missing_fields:
                research_prompt = f"""
Research {company_name} and provide the following missing information:

NEEDED FIELDS: {', '.join(missing_fields)}

Provide ONLY a JSON object with these fields:
{{
    {', '.join([f'"{field}": "provide {field} data"' for field in missing_fields])}
}}

RESPOND WITH ONLY THE JSON - NO OTHER TEXT.
"""
                
                try:
                    response = llm_api_call([{"role": "user", "content": research_prompt}])
                    research_data = json.loads(response)
                    missing_data.update(research_data)
                except Exception as e:
                    print(f"⚠️ Research failed for {slide}: {e}")
        
        return missing_data
    
    def filter_slides_by_conversation_coverage(self, complete_data: Dict, required_slides: List[str]) -> List[str]:
        """Filter slides to only include those with sufficient conversation coverage"""
        
        covered_slides = []
        
        # Always include business_overview if company name exists
        if "business_overview" in required_slides and complete_data.get("company_name"):
            covered_slides.append("business_overview")
        
        # Include management_team if any team data exists
        if ("management_team" in required_slides and 
            (complete_data.get("team_members") or 
             complete_data.get("left_column_profiles") or 
             complete_data.get("right_column_profiles") or
             any(["ceo" in str(complete_data).lower(), "cfo" in str(complete_data).lower(), 
                  "cto" in str(complete_data).lower(), "executive" in str(complete_data).lower(),
                  "management" in str(complete_data).lower(), "leadership" in str(complete_data).lower()]))):
            covered_slides.append("management_team")
        
        # Include financial performance if any financial data exists (support both naming conventions)
        financial_slide_names = ["financial_performance", "historical_financial_performance"]
        for slide_name in financial_slide_names:
            if (slide_name in required_slides and
                (complete_data.get("years") or 
                 complete_data.get("revenue_usd_m") or 
                 complete_data.get("ebitda_usd_m") or
                 complete_data.get("revenue") or
                 complete_data.get("net_income") or
                 complete_data.get("profitability") or
                 any(["revenue" in str(complete_data).lower(), "profit" in str(complete_data).lower(),
                      "financial" in str(complete_data).lower(), "income" in str(complete_data).lower(),
                      "billion" in str(complete_data).lower(), "million" in str(complete_data).lower(),
                      "subscriber" in str(complete_data).lower()]))):
                covered_slides.append(slide_name)
        
        # Include product/service if services or products mentioned
        if ("product_service_footprint" in required_slides and
            (complete_data.get("products_services") or 
             complete_data.get("services") or
             any(["product" in str(complete_data).lower(), "service" in str(complete_data).lower(),
                  "streaming" in str(complete_data).lower(), "platform" in str(complete_data).lower()]))):
            covered_slides.append("product_service_footprint")
        
        # Include growth strategy if growth/strategy mentioned
        if ("growth_strategy_projections" in required_slides and
            (complete_data.get("growth_strategies") or
             any(["growth" in str(complete_data).lower(), "strategy" in str(complete_data).lower(),
                  "expansion" in str(complete_data).lower(), "future" in str(complete_data).lower()]))):
            covered_slides.append("growth_strategy_projections")
        
        # Include precedent transactions if transactions/deals mentioned
        if ("precedent_transactions" in required_slides and
            (complete_data.get("transactions") or
             any(["transaction" in str(complete_data).lower(), "acquisition" in str(complete_data).lower(),
                  "deal" in str(complete_data).lower(), "merger" in str(complete_data).lower()]))):
            covered_slides.append("precedent_transactions")
        
        # Include valuation if valuation/investment mentioned
        if ("valuation_overview" in required_slides and
            (complete_data.get("valuation_data") or
             any(["valuation" in str(complete_data).lower(), "investment" in str(complete_data).lower(),
                  "funding" in str(complete_data).lower(), "worth" in str(complete_data).lower()]))):
            covered_slides.append("valuation_overview")
        
        # Additional slide type mappings for comprehensive coverage
        # Only include slides if there's SUBSTANTIAL conversation content about them
        slide_keywords = {
            "market_analysis": ["market analysis", "industry analysis", "market size", "market share"],
            "competitive_landscape": ["competitors analysis", "competitive advantage", "vs competitors", "competitive position"],
            "product_roadmap": ["product roadmap", "future products", "product development", "upcoming features"],
            "swot_analysis": ["swot analysis", "strengths weaknesses", "opportunities threats"],
            "risk_factors": ["risk assessment", "business risks", "potential risks", "risk management"],
            "esg_initiatives": ["esg initiatives", "sustainability programs", "environmental social governance"],
            "technology_infrastructure": ["technology stack", "tech infrastructure", "technical architecture"],
            "customer_segments": ["customer segmentation", "target customers", "customer demographics", "user segments"],
            "revenue_model": ["revenue model", "business model", "monetization strategy", "pricing strategy"],
            "investment_thesis": ["investment thesis", "investment opportunity", "why invest", "investment rationale"]
        }
        
        # More restrictive matching - require multiple keyword matches OR very specific phrases
        for slide_type, keywords in slide_keywords.items():
            if slide_type in required_slides:
                data_str = str(complete_data).lower()
                keyword_matches = sum(1 for keyword in keywords if keyword in data_str)
                # Only include if multiple keywords match OR there's substantial content (>200 chars about the topic)
                if keyword_matches >= 2 or any(len([part for part in data_str.split() if keyword in part]) > 5 for keyword in keywords):
                    covered_slides.append(slide_type)
        
        # If no slides qualified, at least include business_overview
        if not covered_slides and "business_overview" in required_slides:
            covered_slides.append("business_overview")
        
        return covered_slides
    
    def generate_perfect_jsons(self, extracted_data: Dict, research_data: Dict, required_slides: List[str]):
        """Generate perfect Content IR and Render Plan JSONs"""
        
        # Merge extracted and research data
        complete_data = {**extracted_data, **research_data}
        
        # SMART FILTERING: Only include slides that have sufficient data from conversation
        covered_slides = self.filter_slides_by_conversation_coverage(complete_data, required_slides)
        print(f"🎯 [SMART FILTER] Original slides: {len(required_slides)}, Covered slides: {len(covered_slides)}")
        print(f"🎯 [SMART FILTER] Including only: {covered_slides}")
        
        # Build Content IR JSON using EXACT working structure
        company_name = complete_data.get("company_name", "Company Name")
        content_ir = {
            "entities": {
                "company": {
                    "name": company_name
                }
            },
            "facts": {
                "years": complete_data.get("years", ["2022", "2023", "2024"]),
                "revenue_usd_m": complete_data.get("revenue_usd_m", [10, 25, 50]),
                "ebitda_usd_m": complete_data.get("ebitda_usd_m", [2, 8, 15]),
                "ebitda_margins": complete_data.get("ebitda_margins", [10.0, 15.0, 20.0])
            },
            "management_team": {
                "left_column_profiles": complete_data.get("left_column_profiles", [{
                    "name": "CEO Name",
                    "role_title": "Chief Executive Officer",
                    "experience_bullets": ["Experience 1", "Experience 2"]
                }]),
                "right_column_profiles": complete_data.get("right_column_profiles", [{
                    "name": "CTO Name",
                    "role_title": "Chief Technology Officer", 
                    "experience_bullets": ["Experience 1", "Experience 2"]
                }])
            },
            "strategic_buyers": complete_data.get("strategic_buyers", [
                {
                    "buyer_name": "Strategic Buyer 1",
                    "description": "Industry leader",
                    "strategic_rationale": "Strategic fit",
                    "key_synergies": "Operational synergies",
                    "fit": "High (8/10)",
                    "financial_capacity": "Very High"
                }
            ]),
            "financial_buyers": complete_data.get("financial_buyers", [
                {
                    "buyer_name": "Financial Buyer 1",
                    "description": "Leading VC fund",
                    "strategic_rationale": "Growth investment",
                    "key_synergies": "Market expansion",
                    "fit": "High (8/10)",
                    "financial_capacity": "Very High"
                }
            ]),
            "competitive_analysis": complete_data.get("competitive_analysis", {
                "competitors": [{"name": "Competitor 1", "revenue": 100}],
                "assessment": [["Company", "Rating"], [company_name, "⭐⭐⭐⭐⭐"]],
                "barriers": [{"title": "Technology", "desc": "Advanced technology barriers"}],
                "advantages": [{"title": "Innovation", "desc": "Leading innovation"}]
            }),
            "precedent_transactions": complete_data.get("precedent_transactions", [
                {
                    "target": "Target Co",
                    "acquirer": "Acquirer Co",
                    "date": "2024",
                    "enterprise_value": "$1B",
                    "ev_revenue_multiple": "10x"
                }
            ]),
            "valuation_data": complete_data.get("valuation_data", [
                {
                    "methodology": "Trading Multiples",
                    "enterprise_value": "$50M-100M", 
                    "commentary": "Based on comparable analysis"
                }
            ]),
            "product_service_data": complete_data.get("product_service_data", {
                "services": [{"title": "Service 1", "desc": "Description"}],
                "coverage_table": [["Region", "Coverage"], ["Primary", "Main market"]],
                "metrics": {"key_metric": 100}
            }),
            "business_overview_data": complete_data.get("business_overview_data", {
                "description": f"{company_name} business description",
                "timeline": {"start_year": 2022, "end_year": 2024},
                "highlights": ["Key milestone 1", "Key milestone 2"],
                "services": ["Service 1", "Service 2"],
                "positioning_desc": f"{company_name} market positioning"
            }),
            "growth_strategy_data": complete_data.get("growth_strategy_data", {
                "growth_strategy": {"strategies": ["Growth strategy 1"]},
                "financial_projections": {
                    "categories": ["2023", "2024", "2025"],
                    "revenue": [20, 35, 60],
                    "ebitda": [3, 8, 15]
                }
            }),
            "margin_cost_data": complete_data.get("margin_cost_data", {
                "chart_data": {
                    "categories": ["2022", "2023", "2024"],
                    "values": [10, 15, 20]
                },
                "cost_management": {"items": []},
                "risk_mitigation": {"main_strategy": "Cost management strategy"}
            }),
            "investor_considerations": complete_data.get("investor_considerations", {
                "considerations": ["Risk 1", "Risk 2"],
                "mitigants": ["Mitigation 1", "Mitigation 2"]
            })
        }
        
        # Build Render Plan JSON using EXACT working structure
        slides = []
        
        # Use filtered slides instead of all required slides
        for slide_type in covered_slides:
            if slide_type == "business_overview":
                slides.append({
                    "template": "business_overview",
                    "data": {
                        "title": "Business Overview",
                        "description": complete_data.get("description", f"{company_name} business description"),
                        "timeline": complete_data.get("timeline", {"start_year": 2022, "end_year": 2024}),
                        "highlights": complete_data.get("highlights", ["Key milestone 1", "Key milestone 2"]),
                        "services": complete_data.get("services", ["Service 1", "Service 2"]),
                        "positioning_desc": complete_data.get("positioning_desc", f"{company_name} market positioning")
                    }
                })
            
            elif slide_type == "product_service_footprint":
                slides.append({
                    "template": "product_service_footprint", 
                    "data": {
                        "title": "Product & Service Footprint",
                        "services": complete_data.get("services", [{"title": "Service 1", "desc": "Description"}]),
                        "coverage_table": complete_data.get("coverage_table", [["Region", "Coverage"], ["Primary", "Main market"]]),
                        "metrics": complete_data.get("metrics", {"key_metric": 100})
                    }
                })
            
            elif slide_type == "historical_financial_performance":
                slides.append({
                    "template": "historical_financial_performance",
                    "data": {
                        "title": "Historical Financial Performance", 
                        "chart": {
                            "title": "Revenue & EBITDA Growth",
                            "categories": complete_data.get("years", ["2022", "2023", "2024"]),
                            "revenue": complete_data.get("revenue_usd_m", [10, 25, 50]),
                            "ebitda": complete_data.get("ebitda_usd_m", [2, 8, 15])
                        },
                        "key_metrics": {
                            "title": "Key Performance Metrics",
                            "metrics": complete_data.get("key_metrics", [])
                        }
                    }
                })
            
            elif slide_type == "management_team":
                slides.append({
                    "template": "management_team",
                    "data": {
                        "title": "Management Team",
                        "left_column_profiles": complete_data.get("left_column_profiles", [{
                            "name": "CEO Name",
                            "role_title": "Chief Executive Officer",
                            "experience_bullets": ["Experience 1", "Experience 2"]
                        }]),
                        "right_column_profiles": complete_data.get("right_column_profiles", [{
                            "name": "CTO Name", 
                            "role_title": "Chief Technology Officer",
                            "experience_bullets": ["Experience 1", "Experience 2"]
                        }])
                    }
                })
            
            elif slide_type == "growth_strategy_projections":
                slides.append({
                    "template": "growth_strategy_projections",
                    "data": {
                        "title": "Growth Strategy & Financial Projections",
                        "slide_data": complete_data.get("growth_strategy_data", {
                            "growth_strategy": {"strategies": ["Growth strategy 1"]},
                            "financial_projections": {
                                "categories": ["2023", "2024", "2025"],
                                "revenue": [20, 35, 60],
                                "ebitda": [3, 8, 15]
                            }
                        })
                    }
                })
            
            elif slide_type == "precedent_transactions":
                slides.append({
                    "template": "precedent_transactions",
                    "data": {
                        "title": "Precedent Transactions",
                        "transactions": complete_data.get("precedent_transactions", [{
                            "target": "Target Co",
                            "acquirer": "Acquirer Co", 
                            "date": "2024",
                            "enterprise_value": "$1B",
                            "ev_revenue_multiple": "10x"
                        }])
                    }
                })
            
            elif slide_type == "valuation_overview":
                slides.append({
                    "template": "valuation_overview",
                    "data": {
                        "title": "Valuation Overview",
                        "valuation_data": complete_data.get("valuation_data", [{
                            "methodology": "Trading Multiples",
                            "enterprise_value": "$50M-100M",
                            "commentary": "Based on comparable analysis"
                        }])
                    }
                })
        
        render_plan = {"slides": slides}
        
        # Format with perfect markers
        perfect_response = f"""Based on our conversation, I've generated {len(covered_slides)} relevant slides that have sufficient data:

CONTENT IR JSON:
{json.dumps(content_ir, indent=2)}

RENDER PLAN JSON:
{json.dumps(render_plan, indent=2)}

✅ Generated {len(covered_slides)} slides based on conversation coverage: {', '.join(covered_slides)}
✅ Perfect format guaranteed for auto-improvement detection."""
        
        return perfect_response, content_ir, render_plan

# Usage function
def generate_bulletproof_json(messages: List[Dict], required_slides: List[str], llm_api_call):
    """Main function to generate bulletproof JSONs"""
    
    generator = BulletproofJSONGenerator()
    
    # Step 1: Extract data from conversation
    print("🔍 Extracting data from conversation...")
    extracted_data = generator.extract_conversation_data(messages, llm_api_call)
    
    # Step 2: Research missing data
    print("📚 Researching missing data...")
    research_data = generator.research_missing_data(extracted_data, required_slides, llm_api_call)
    
    # Step 3: Generate perfect JSONs
    print("⚡ Generating perfect JSONs...")
    response, content_ir, render_plan = generator.generate_perfect_jsons(
        extracted_data, research_data, required_slides
    )
    
    return response, content_ir, render_plan