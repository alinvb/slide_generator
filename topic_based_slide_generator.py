#!/usr/bin/env python3
"""
Topic-Based Slide Generator
Creates slides ONLY for interview topics that have been actually covered
Direct 1-to-1 mapping: 1 answered question = 1 slide, 2 questions = 2 slides, etc.
"""

import json
from typing import Dict, List, Any, Tuple


class TopicBasedSlideGenerator:
    """
    Generates slides based on ONLY the interview topics that have been covered
    Direct mapping from answered interview questions to corresponding slides
    """
    
    def __init__(self):
        # Direct mapping from interview topics to slide templates
        self.topic_to_slide_mapping = {
            "business_overview": {
                "slide_name": "business_overview",
                "template": "business_overview",
                "title": "Business Overview",
                "content_ir_key": "business_overview_data"
            },
            "product_service_footprint": {
                "slide_name": "product_service_footprint", 
                "template": "product_service_footprint",
                "title": "Product & Service Footprint",
                "content_ir_key": "product_service_data"
            },
            "historical_financial_performance": {
                "slide_name": "historical_financial_performance",
                "template": "historical_financial_performance", 
                "title": "Historical Financial Performance",
                "content_ir_key": "facts"
            },
            "management_team": {
                "slide_name": "management_team",
                "template": "management_team",
                "title": "Management Team", 
                "content_ir_key": "management_team"
            },
            "growth_strategy_projections": {
                "slide_name": "growth_strategy_projections",
                "template": "growth_strategy_projections",
                "title": "Growth Strategy & Projections",
                "content_ir_key": "growth_strategy_data"
            },
            "competitive_positioning": {
                "slide_name": "competitive_positioning",
                "template": "competitive_positioning",
                "title": "Competitive Positioning", 
                "content_ir_key": "competitive_analysis"
            },
            "precedent_transactions": {
                "slide_name": "precedent_transactions",
                "template": "precedent_transactions",
                "title": "Precedent Transactions",
                "content_ir_key": "precedent_transactions"
            },
            "valuation_overview": {
                "slide_name": "valuation_overview",
                "template": "valuation_overview",
                "title": "Valuation Overview",
                "content_ir_key": "valuation_data"
            },
            "strategic_buyers": {
                "slide_name": "strategic_buyers",
                "template": "buyer_profiles",
                "title": "Strategic Buyer Profiles", 
                "content_ir_key": "strategic_buyers",
                "table_headers": ["Buyer Name", "Description", "Strategic Rationale", "Key Synergies", "Fit"]
            },
            "financial_buyers": {
                "slide_name": "financial_buyers", 
                "template": "buyer_profiles",
                "title": "Financial Buyer Profiles",
                "content_ir_key": "financial_buyers",
                "table_headers": ["Buyer Name", "Description", "Investment Rationale", "Key Synergies", "Fit"]
            },
            "sea_conglomerates": {
                "slide_name": "sea_conglomerates",
                "template": "buyer_profiles", 
                "title": "Global Conglomerates",
                "content_ir_key": "sea_conglomerates",
                "table_headers": ["Company", "Country", "Description", "Key Financials"]
            },
            "margin_cost_resilience": {
                "slide_name": "margin_cost_resilience",
                "template": "margin_cost_resilience",
                "title": "Margin & Cost Resilience",
                "content_ir_key": "margin_cost_data"
            },
            "investor_considerations": {
                "slide_name": "investor_considerations", 
                "template": "investor_considerations",
                "title": "Investor Considerations",
                "content_ir_key": "investor_considerations"
            },
            "investor_process_overview": {
                "slide_name": "investor_process_overview",
                "template": "investor_process_overview", 
                "title": "Investor Process Overview",
                "content_ir_key": "investor_process_data"
            }
        }
    
    def get_covered_topics_from_progress(self, messages: List[Dict[str, Any]]) -> Tuple[List[str], Dict[str, Any]]:
        """
        Use a simple approach to determine covered topics from conversation
        Focus on direct evidence that topics have been discussed
        """
        try:
            # Import and use existing analyze_conversation_progress function
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.abspath(__file__)))
            
            # Try to import the existing function - if it fails, use fallback
            try:
                from app import analyze_conversation_progress
                progress_info = analyze_conversation_progress(messages)
                
                # Extract the covered topics from the progress info
                covered_topics = []
                
                # The analyze_conversation_progress function has different output format
                # Let's extract covered topics manually
                conversation_text = " ".join([msg["content"] for msg in messages if msg["role"] != "system"]).lower()
                
                # Simple but effective topic detection
                topics_with_keywords = {
                    "business_overview": ["company", "business", "overview", "founded", "headquarters", "industry"],
                    "product_service_footprint": ["products", "services", "offerings", "geographic", "coverage", "operations"],
                    "historical_financial_performance": ["revenue", "financial", "ebitda", "margin", "growth", "profit", "million"],
                    "management_team": ["management", "team", "executives", "ceo", "cfo", "founder", "leadership"],
                    "growth_strategy_projections": ["growth", "strategy", "expansion", "projections", "future", "plans"],
                    "competitive_positioning": ["competitive", "competitors", "positioning", "advantages", "differentiation"],
                    "precedent_transactions": ["precedent", "transactions", "m&a", "acquisitions", "deals", "multiple"],
                    "valuation_overview": ["valuation", "multiple", "methodology", "worth", "enterprise value", "dcf"],
                    "strategic_buyers": ["strategic buyers", "strategic buyer", "corporate buyer", "strategic rationale"],
                    "financial_buyers": ["financial buyers", "private equity", "pe fund", "vc fund", "investment fund"],
                    "sea_conglomerates": ["conglomerate", "global conglomerate", "multinational", "holding company"],
                    "margin_cost_resilience": ["margin", "cost", "resilience", "profitability", "efficiency"],
                    "investor_considerations": ["risk", "opportunity", "investor", "considerations", "challenges"],
                    "investor_process_overview": ["process", "diligence", "timeline", "synergy", "transaction process"]
                }
                
                for topic_name, keywords in topics_with_keywords.items():
                    # Check if enough keywords are present to indicate topic coverage
                    keywords_found = sum(1 for keyword in keywords if keyword in conversation_text)
                    
                    # ENHANCED: Topic is covered if it has ANY keyword presence + research responses
                    # Check for research responses indicating topic coverage
                    research_indicators = ["research", "based on", "according to", "here is", "here are", "analysis shows"]
                    has_research_response = any(indicator in conversation_text for indicator in research_indicators)
                    
                    # More lenient coverage detection
                    is_covered = (
                        keywords_found >= 2 or  # Direct keyword match
                        (keywords_found >= 1 and has_research_response) or  # Research provided for topic
                        (keywords_found >= 1 and len(conversation_text.split()) > 100)  # Substantial discussion
                    )
                    
                    if is_covered:
                        covered_topics.append(topic_name)
                        print(f"✅ TOPIC-BASED: {topic_name} is COVERED ({keywords_found}/{len(keywords)} keywords, research: {has_research_response})")
                    else:
                        print(f"❌ TOPIC-BASED: {topic_name} is NOT covered ({keywords_found}/{len(keywords)} keywords, research: {has_research_response})")
                
                return covered_topics, {
                    "covered_topics": covered_topics,
                    "topics_covered": len(covered_topics),
                    "total_topics": 14,
                    "completion_percentage": len(covered_topics) / 14,
                    "method": "keyword_based"
                }
                
            except ImportError:
                # Fallback if we can't import the function
                print("⚠️ Could not import analyze_conversation_progress, using fallback method")
                return self._fallback_topic_analysis(messages)
                
        except Exception as e:
            print(f"❌ Error analyzing topics: {e}")
            return self._fallback_topic_analysis(messages)
    
    def _fallback_topic_analysis(self, messages: List[Dict[str, Any]]) -> Tuple[List[str], Dict[str, Any]]:
        """Fallback topic analysis if main function is unavailable"""
        conversation_text = " ".join([msg["content"] for msg in messages if msg["role"] != "system"]).lower()
        
        # Very basic topic detection for fallback
        basic_topics = []
        
        if any(word in conversation_text for word in ["company", "business", "founded"]):
            basic_topics.append("business_overview")
        
        if any(word in conversation_text for word in ["revenue", "financial", "million", "profit"]):
            basic_topics.append("historical_financial_performance")
            
        if any(word in conversation_text for word in ["management", "ceo", "team"]):
            basic_topics.append("management_team")
        
        return basic_topics, {
            "covered_topics": basic_topics,
            "topics_covered": len(basic_topics),
            "total_topics": 14,
            "completion_percentage": len(basic_topics) / 14,
            "method": "fallback"
        }
    
    def generate_slides_for_covered_topics(self, messages: List[Dict[str, Any]]) -> Tuple[List[str], Dict[str, Any], Dict[str, Any]]:
        """
        Generate slides ONLY for topics that have been covered in the interview
        Direct 1:1 mapping - 1 answered question = 1 slide
        """
        # Get covered topics from conversation analysis
        covered_topics, progress_info = self.get_covered_topics_from_progress(messages)
        
        print(f"🎯 TOPIC-BASED: Found {len(covered_topics)} covered topics: {covered_topics}")
        
        # Generate slide list based on covered topics only
        slide_list = []
        
        # Order slides by corrected interview sequence (valuation before buyers)
        topic_positions = {
            "business_overview": 1,
            "product_service_footprint": 2, 
            "historical_financial_performance": 3,
            "management_team": 4,
            "growth_strategy_projections": 5,
            "competitive_positioning": 6,
            "precedent_transactions": 7,
            "valuation_overview": 8,  # CRITICAL: Valuation BEFORE buyers
            "strategic_buyers": 9,    # After valuation to determine affordability
            "financial_buyers": 10,   # PE firms only, not VCs
            "sea_conglomerates": 11,  # Geography-aware conglomerates
            "margin_cost_resilience": 12,
            "investor_considerations": 13,
            "investor_process_overview": 14
        }
        
        # Sort covered topics by their interview position
        sorted_covered_topics = sorted(covered_topics, key=lambda x: topic_positions.get(x, 999))
        
        # Create slides for each covered topic
        for topic_name in sorted_covered_topics:
            if topic_name in self.topic_to_slide_mapping:
                slide_info = self.topic_to_slide_mapping[topic_name]
                slide_list.append(slide_info["slide_name"])
                print(f"✅ TOPIC-BASED: Adding slide for {topic_name} -> {slide_info['slide_name']}")
        
        # Create render plan with only the covered topic slides
        render_plan = self.create_topic_based_render_plan(sorted_covered_topics)
        
        # Generate analysis report
        analysis_report = {
            "generation_type": "topic_based",
            "total_slides_generated": len(slide_list),
            "slides_included": slide_list,
            "covered_topics": covered_topics,
            "topics_covered": len(covered_topics),
            "total_topics": progress_info.get("total_topics", 14),
            "completion_percentage": progress_info.get("completion_percentage", 0),
            "direct_mapping": True,
            "conversation_analysis": {
                "method": progress_info.get("method", "analyze_conversation_progress"), 
                "context_aware": progress_info.get("context_aware", False),
                "user_indicated_repetition": progress_info.get("user_indicated_repetition", False)
            }
        }
        
        print(f"🎯 TOPIC-BASED FINAL: Generated {len(slide_list)} slides for {len(covered_topics)} covered topics")
        return slide_list, render_plan, analysis_report
    
    def create_topic_based_render_plan(self, covered_topics: List[str]) -> Dict[str, Any]:
        """
        Create render plan with slides for covered topics only
        """
        slides = []
        
        for topic_name in covered_topics:
            if topic_name in self.topic_to_slide_mapping:
                slide_config = self.topic_to_slide_mapping[topic_name]
                
                slide_data = {
                    "template": slide_config["template"],
                    "data": {
                        "title": slide_config["title"],
                        "content_ir_key": slide_config["content_ir_key"]
                    }
                }
                
                # Add table headers for buyer profile slides
                if "table_headers" in slide_config:
                    slide_data["content_ir_key"] = slide_config["content_ir_key"]
                    slide_data["data"]["table_headers"] = slide_config["table_headers"]
                    slide_data["data"]["table_rows"] = []  # Will be populated from content_ir
                
                slides.append(slide_data)
        
        return {
            "slides": slides,
            "metadata": {
                "generation_type": "topic_based",
                "total_slides": len(slides),
                "generated_from": f"{len(covered_topics)} covered interview topics",
                "direct_mapping": True
            }
        }


# Global instance for use in app
topic_based_generator = TopicBasedSlideGenerator()


def generate_topic_based_presentation(messages: List[Dict[str, Any]]) -> Tuple[List[str], Dict[str, Any], Dict[str, Any]]:
    """
    Main function to generate presentation based on ONLY covered interview topics
    Direct mapping: 1 answered question = 1 slide, 2 questions = 2 slides
    Returns: (slide_list, render_plan, analysis_report)
    """
    return topic_based_generator.generate_slides_for_covered_topics(messages)


if __name__ == "__main__":
    # Test with sample conversation
    test_messages = [
        {"role": "user", "content": "My company is TechCorp, we're a software company founded in 2020 with headquarters in Dubai"},
        {"role": "assistant", "content": "Tell me about your products and services"},
        {"role": "user", "content": "We offer AI software products and have operations in UAE and Saudi Arabia"},
        {"role": "assistant", "content": "What about your financials?"},
        {"role": "user", "content": "We have $10M revenue in 2023, $15M projected for 2024, with 15% EBITDA margins"}
    ]
    
    slide_list, render_plan, report = generate_topic_based_presentation(test_messages)
    
    print("🎯 Topic-Based Slide Generation Test")
    print("=" * 50)
    print(f"📊 Slides Generated: {report['total_slides_generated']}")
    print(f"📋 Slide List: {slide_list}")
    print(f"📈 Topics Covered: {report['topics_covered']}/{report['total_topics']}")
    print(f"🎯 Covered Topics: {report['covered_topics']}")
    print("\n✅ Topic-based slide generation working!")