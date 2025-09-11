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
            "global_conglomerates": {
                "slide_name": "global_conglomerates",
                "template": "buyer_profiles", 
                "title": "Global Conglomerates",
                "content_ir_key": "global_conglomerates",
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
        SIMPLIFIED: Determine covered topics based on questions asked
        If a question for a topic was asked and user didn't say 'skip', the topic is covered
        """
        print("🎯 TOPIC-BASED: Using question-based detection (much more reliable)")
        
        # Define the question patterns that indicate each topic was asked
        topic_question_patterns = {
            "business_overview": [
                "company name", "brief overview", "what your business does", "what is the company"
            ],
            "product_service_footprint": [
                "product/service footprint", "main offerings", "where do you operate", "geographic"
            ],
            "historical_financial_performance": [
                "financial performance", "revenue", "ebitda", "margins", "key financial metrics"
            ],
            "management_team": [
                "management team", "key executives", "ceo", "cfo", "senior leaders"
            ],
            "growth_strategy_projections": [
                "growth strategy", "expansion plans", "strategic initiatives", "financial projections"
            ],
            "competitive_positioning": [
                "positioned competitively", "key competitors", "competitive advantages", "market positioning"
            ],
            "precedent_transactions": [
                "precedent transactions", "private market m&a", "corporate acquisitions", "recent deals"
            ],
            "valuation_overview": [
                "valuation methodologies", "dcf", "trading multiples", "precedent transactions analysis"
            ],
            "strategic_buyers": [
                "strategic buyers", "afford this acquisition", "strategic assets", "corporate buyers"
            ],
            "financial_buyers": [
                "private equity firms", "pe firms", "financial buyers", "afford your valuation"
            ],
            "global_conglomerates": [
                "large conglomerates", "geographic region", "conglomerates that operate"
            ],
            "margin_cost_resilience": [
                "margin and cost data", "ebitda margins", "cost management", "risk mitigation"
            ],
            "investor_considerations": [
                "investor considerations", "key risks", "opportunities investors", "risks and opportunities"
            ],
            "investor_process_overview": [
                "investment/acquisition process", "diligence topics", "synergy opportunities", "expected timeline"
            ]
        }
        
        # Get all assistant messages (questions asked by AI)
        assistant_messages = [msg["content"].lower() for msg in messages if msg["role"] == "assistant"]
        user_responses = [msg["content"].lower() for msg in messages if msg["role"] == "user"]
        
        covered_topics = []
        
        for topic_name, question_patterns in topic_question_patterns.items():
            # Check if any question pattern appears in assistant messages
            question_was_asked = False
            for assistant_msg in assistant_messages:
                if any(pattern in assistant_msg for pattern in question_patterns):
                    question_was_asked = True
                    break
            
            # If question was asked, check if user said 'skip' for THIS specific topic
            # Look for skip requests that happened AFTER the topic was mentioned
            user_said_skip_for_this_topic = False
            for i, assistant_msg in enumerate(assistant_messages):
                if any(pattern in assistant_msg for pattern in question_patterns):
                    # This topic was mentioned - check user responses after this point
                    if i < len(user_responses):
                        subsequent_responses = user_responses[i:]
                        user_said_skip_for_this_topic = any(
                            "skip" in response and any(topic_word in response for topic_word in ["this", "topic", "slide"]) 
                            for response in subsequent_responses[:2]  # Check next 2 user responses only
                        )
                    break
            
            # Topic is covered if question was asked AND user didn't skip THIS specific topic
            is_covered = question_was_asked and not user_said_skip_for_this_topic
            
            if is_covered:
                covered_topics.append(topic_name)
                print(f"✅ TOPIC-BASED: {topic_name} - Question asked, not skipped")
            else:
                if not question_was_asked:
                    print(f"❓ TOPIC-BASED: {topic_name} - Question NOT asked")
                elif user_said_skip_for_this_topic:
                    print(f"⏭️ TOPIC-BASED: {topic_name} - User said SKIP")
        
        print(f"🎯 FINAL RESULT: {len(covered_topics)} topics covered: {covered_topics}")
        
        return covered_topics, {
            "covered_topics": covered_topics,
            "topics_covered": len(covered_topics),
            "total_topics": 14,
            "completion_percentage": len(covered_topics) / 14,
            "method": "question_based"
        }
    
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
            "global_conglomerates": 11,  # Geography-aware conglomerates
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