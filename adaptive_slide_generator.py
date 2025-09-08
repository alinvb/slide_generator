#!/usr/bin/env python3
"""
Adaptive Slide Generator
Creates only relevant slides based on available conversation data
Quality over quantity approach - better 5 great slides than 14 mediocre ones
"""

import json
from typing import Dict, List, Any, Tuple

class AdaptiveSlideGenerator:
    """
    Generates slides adaptively based on available conversation content
    Only creates slides where we have substantial, meaningful information
    """
    
    def __init__(self):
        # Define slide templates and their required information
        self.slide_requirements = {
            "business_overview": {
                "required_keywords": ["company", "business", "overview", "what does", "industry", "sector"],
                "min_keywords": 2,
                "content_sections": ["entities", "business_overview_data"],
                "description": "Company overview and business description"
            },
            "management_team": {
                "required_keywords": ["management", "team", "ceo", "cfo", "founder", "executive", "leadership"],
                "min_keywords": 2,
                "content_sections": ["management_team"],
                "description": "Management team profiles and leadership"
            },
            "historical_financial_performance": {
                "required_keywords": ["revenue", "financial", "ebitda", "growth", "profit", "sales", "million", "billion", "$"],
                "min_keywords": 3,
                "content_sections": ["facts", "charts"],
                "description": "Historical financial metrics and performance"
            },
            "product_service_footprint": {
                "required_keywords": ["products", "services", "offerings", "geographic", "footprint", "coverage", "operations"],
                "min_keywords": 2,
                "content_sections": ["product_service_data"],
                "description": "Product/service offerings and geographic presence"
            },
            "growth_strategy_projections": {
                "required_keywords": ["growth", "strategy", "expansion", "projections", "future", "roadmap", "plans"],
                "min_keywords": 2,
                "content_sections": ["growth_strategy_data"],
                "description": "Growth strategy and future projections"
            },
            "competitive_positioning": {
                "required_keywords": ["competitive", "competitors", "positioning", "advantages", "differentiation", "market position"],
                "min_keywords": 2,
                "content_sections": ["competitive_analysis"],
                "description": "Competitive landscape and positioning"
            },
            "valuation_overview": {
                "required_keywords": ["valuation", "multiple", "worth", "value", "enterprise value", "methodology"],
                "min_keywords": 2,
                "content_sections": ["valuation_data"],
                "description": "Valuation methodologies and estimates"
            },
            "precedent_transactions": {
                "required_keywords": ["transaction", "acquisition", "deal", "m&a", "precedent", "multiple"],
                "min_keywords": 2,
                "content_sections": ["precedent_transactions"],
                "description": "Comparable M&A transactions and multiples"
            },
            "buyer_profiles": {
                "required_keywords": ["buyer", "strategic", "financial", "private equity", "acquirer", "investment"],
                "min_keywords": 2,
                "content_sections": ["strategic_buyers", "financial_buyers"],
                "description": "Strategic and financial buyer profiles",
                "variants": ["strategic_buyers", "financial_buyers"]
            },
            "investor_considerations": {
                "required_keywords": ["risk", "opportunity", "challenges", "considerations", "mitigation"],
                "min_keywords": 2,
                "content_sections": ["investor_considerations"],
                "description": "Key risks, opportunities, and mitigating factors"
            },
            "margin_cost_resilience": {
                "required_keywords": ["margin", "cost", "resilience", "efficiency", "profitability", "cost management"],
                "min_keywords": 2,
                "content_sections": ["margin_cost_data"],
                "description": "Cost structure and margin analysis"
            },
            "investor_process_overview": {
                "required_keywords": ["process", "diligence", "timeline", "synergy", "due diligence"],
                "min_keywords": 2,
                "content_sections": ["investor_process_data"],
                "description": "Investment process and due diligence overview"
            },
            "sea_conglomerates": {
                "required_keywords": ["conglomerate", "global", "multinational", "international", "diversified"],
                "min_keywords": 1,
                "content_sections": ["sea_conglomerates"],
                "description": "Global conglomerates and strategic acquirers"
            }
        }
    
    def analyze_conversation_content(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze conversation to determine which slides have substantial content
        Returns analysis of available content quality and coverage
        """
        # Extract conversation text (exclude system messages)
        conversation_text = " ".join([
            msg.get("content", "") for msg in messages 
            if msg.get("role") != "system"
        ]).lower()
        
        slide_analysis = {}
        
        for slide_name, requirements in self.slide_requirements.items():
            # Count keyword matches
            found_keywords = [
                keyword for keyword in requirements["required_keywords"]
                if keyword in conversation_text
            ]
            
            # Calculate content quality score
            keyword_score = len(found_keywords) / len(requirements["required_keywords"])
            has_minimum = len(found_keywords) >= requirements["min_keywords"]
            
            # Enhanced scoring for detailed content
            content_length_bonus = 0
            if any(keyword in conversation_text for keyword in found_keywords):
                # Check for detailed responses (longer explanations)
                keyword_contexts = [
                    conversation_text[max(0, conversation_text.find(keyword)-50):
                                   conversation_text.find(keyword)+200]
                    for keyword in found_keywords[:3]  # Check top 3 keywords
                ]
                avg_context_length = sum(len(ctx.split()) for ctx in keyword_contexts) / max(len(keyword_contexts), 1)
                content_length_bonus = min(0.3, avg_context_length / 100)  # Up to 30% bonus
            
            final_score = keyword_score + content_length_bonus
            
            slide_analysis[slide_name] = {
                "score": final_score,
                "found_keywords": found_keywords,
                "has_minimum": has_minimum,
                "keyword_count": len(found_keywords),
                "description": requirements["description"],
                "recommended": final_score >= 0.6 and has_minimum  # 60% threshold + minimum keywords for high confidence
            }
        
        return slide_analysis
    
    def generate_adaptive_slide_list(self, messages: List[Dict[str, Any]]) -> Tuple[List[str], Dict[str, Any]]:
        """
        Generate list of slides to include based on conversation analysis
        Returns (slide_list, analysis_report)
        """
        analysis = self.analyze_conversation_content(messages)
        
        # Always include business overview if we have any company information
        core_slides = []
        optional_slides = []
        
        # Prioritize slides by importance and available content
        slide_priority = [
            "business_overview",  # Always try to include if minimal company info
            "management_team",
            "historical_financial_performance", 
            "product_service_footprint",
            "growth_strategy_projections",
            "competitive_positioning",
            "valuation_overview",
            "precedent_transactions",
            "buyer_profiles",
            "investor_considerations",
            "margin_cost_resilience",
            "investor_process_overview",
            "sea_conglomerates"
        ]
        
        for slide_name in slide_priority:
            slide_info = analysis.get(slide_name, {})
            
            if slide_info.get("recommended", False):
                core_slides.append(slide_name)
            elif slide_info.get("score", 0) >= 0.5:  # Higher threshold for optional - must have substantial content
                optional_slides.append(slide_name)
        
        # Start with only high-quality core slides
        selected_slides = core_slides
        
        # Only add optional slides if they have very high scores (real content, not just keyword matches)
        if len(selected_slides) < 8:  # Only consider adding more if we don't already have many
            high_quality_optional = [
                slide for slide in optional_slides 
                if analysis.get(slide, {}).get("score", 0) >= 0.65  # Very high threshold - must have detailed content
            ]
            selected_slides.extend(high_quality_optional)
        
        # Ensure minimum viable deck (at least 3 slides) ONLY if we don't have enough high-quality slides
        if len(selected_slides) < 3:
            # Add highest scoring slides to reach minimum
            all_slides_by_score = sorted(
                slide_priority,
                key=lambda x: analysis.get(x, {}).get("score", 0),
                reverse=True
            )
            for slide in all_slides_by_score:
                if slide not in selected_slides:
                    selected_slides.append(slide)
                if len(selected_slides) >= 3:
                    break
        
        # Handle buyer profiles - ONLY include if explicitly discussed
        if "buyer_profiles" in selected_slides:
            buyer_analysis = analysis.get("buyer_profiles", {})
            conversation_text = " ".join([msg.get("content", "") for msg in messages if msg.get("role") != "system"]).lower()
            
            # STRICT CHECK: Only include buyer slides if there's substantial buyer discussion
            has_detailed_buyer_discussion = (
                buyer_analysis.get("score", 0) >= 0.7 and  # Very high score required
                buyer_analysis.get("keyword_count", 0) >= 3  # Multiple buyer-related keywords
            )
            
            selected_slides.remove("buyer_profiles")
            
            if has_detailed_buyer_discussion:
                # Check for specific buyer type mentions
                has_strategic = any(term in conversation_text for term in ["strategic buyer", "corporate acquirer", "industry player", "strategic acquisition"])
                has_financial = any(term in conversation_text for term in ["private equity", "pe fund", "financial buyer", "vc fund", "investment fund"])
                
                if has_strategic:
                    selected_slides.append("strategic_buyers")
                if has_financial:
                    selected_slides.append("financial_buyers")
                
                # Only add both if there was explicit discussion about both types
                if not has_strategic and not has_financial:
                    # Don't assume - only add if there was general buyer discussion
                    if any(term in conversation_text for term in ["buyers", "acquirers", "who would buy", "potential buyers"]):
                        selected_slides.extend(["strategic_buyers", "financial_buyers"])
            # If no detailed buyer discussion, don't add any buyer slides
        
        # Generate analysis report
        report = {
            "total_slides_generated": len(selected_slides),
            "slides_included": selected_slides,
            "slides_analysis": analysis,
            "quality_summary": {
                "high_quality_slides": len([s for s in selected_slides if analysis.get(s, {}).get("score", 0) >= 0.6]),
                "medium_quality_slides": len([s for s in selected_slides if 0.4 <= analysis.get(s, {}).get("score", 0) < 0.6]),
                "estimated_slides": len([s for s in selected_slides if analysis.get(s, {}).get("score", 0) < 0.4])
            }
        }
        
        return selected_slides, report
    
    def create_adaptive_render_plan(self, slide_list: List[str], conversation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create render plan with only the selected slides
        """
        slides = []
        
        slide_templates = {
            "business_overview": {
                "template": "business_overview",
                "data": {
                    "title": "Business Overview",
                    "content_ir_key": "business_overview_data"
                }
            },
            "management_team": {
                "template": "management_team", 
                "data": {
                    "title": "Management Team",
                    "content_ir_key": "management_team"
                }
            },
            "historical_financial_performance": {
                "template": "historical_financial_performance",
                "data": {
                    "title": "Historical Financial Performance", 
                    "content_ir_key": "facts"
                }
            },
            "product_service_footprint": {
                "template": "product_service_footprint",
                "data": {
                    "title": "Product & Service Footprint",
                    "content_ir_key": "product_service_data"
                }
            },
            "growth_strategy_projections": {
                "template": "growth_strategy_projections",
                "data": {
                    "title": "Growth Strategy & Projections",
                    "content_ir_key": "growth_strategy_data"
                }
            },
            "competitive_positioning": {
                "template": "competitive_positioning",
                "data": {
                    "title": "Competitive Positioning",
                    "content_ir_key": "competitive_analysis"
                }
            },
            "valuation_overview": {
                "template": "valuation_overview",
                "data": {
                    "title": "Valuation Overview", 
                    "content_ir_key": "valuation_data"
                }
            },
            "precedent_transactions": {
                "template": "precedent_transactions",
                "data": {
                    "title": "Precedent Transactions",
                    "content_ir_key": "precedent_transactions"
                }
            },
            "strategic_buyers": {
                "template": "buyer_profiles",
                "content_ir_key": "strategic_buyers",
                "data": {
                    "title": "Strategic Buyer Profiles",
                    "table_headers": ["Buyer Name", "Description", "Strategic Rationale", "Key Synergies", "Fit"],
                    "table_rows": []  # Will be populated from content_ir
                }
            },
            "financial_buyers": {
                "template": "buyer_profiles", 
                "content_ir_key": "financial_buyers",
                "data": {
                    "title": "Financial Buyer Profiles",
                    "table_headers": ["Buyer Name", "Description", "Investment Rationale", "Key Synergies", "Fit"],
                    "table_rows": []  # Will be populated from content_ir
                }
            },
            "investor_considerations": {
                "template": "investor_considerations",
                "data": {
                    "title": "Investor Considerations",
                    "content_ir_key": "investor_considerations"
                }
            },
            "margin_cost_resilience": {
                "template": "margin_cost_resilience",
                "data": {
                    "title": "Margin & Cost Resilience",
                    "content_ir_key": "margin_cost_data"
                }
            },
            "investor_process_overview": {
                "template": "investor_process_overview",
                "data": {
                    "title": "Investor Process Overview",
                    "content_ir_key": "investor_process_data"
                }
            },
            "sea_conglomerates": {
                "template": "buyer_profiles",
                "content_ir_key": "sea_conglomerates", 
                "data": {
                    "title": "Global Conglomerates",
                    "table_headers": ["Company", "Country", "Description", "Key Financials"],
                    "table_rows": []  # Will be populated from content_ir
                }
            }
        }
        
        for slide_name in slide_list:
            if slide_name in slide_templates:
                slides.append(slide_templates[slide_name])
        
        return {
            "slides": slides,
            "metadata": {
                "generation_type": "adaptive",
                "total_slides": len(slides),
                "generated_from": f"{len(slide_list)} conversation topics"
            }
        }


# Global instance for use in app
adaptive_generator = AdaptiveSlideGenerator()


def generate_adaptive_presentation(messages: List[Dict[str, Any]]) -> Tuple[List[str], Dict[str, Any], Dict[str, Any]]:
    """
    Main function to generate adaptive presentation based on conversation
    Returns: (slide_list, render_plan, analysis_report)
    """
    slide_list, report = adaptive_generator.generate_adaptive_slide_list(messages)
    render_plan = adaptive_generator.create_adaptive_render_plan(slide_list, {})
    
    return slide_list, render_plan, report


if __name__ == "__main__":
    # Test with sample conversation
    test_messages = [
        {"role": "user", "content": "My company is TechCorp, we're a software company"},
        {"role": "assistant", "content": "Tell me about your financials"},
        {"role": "user", "content": "We have $10M revenue and strong growth"},
        {"role": "assistant", "content": "Who are your key executives?"},
        {"role": "user", "content": "John Smith is CEO, Sarah Johnson is CTO"}
    ]
    
    slide_list, render_plan, report = generate_adaptive_presentation(test_messages)
    
    print("🎯 Adaptive Slide Generation Test")
    print("=" * 50)
    print(f"📊 Slides Generated: {report['total_slides_generated']}")
    print(f"📋 Slide List: {slide_list}")
    print(f"📈 Quality Summary: {report['quality_summary']}")
    print("\n✅ Adaptive slide generation working!")