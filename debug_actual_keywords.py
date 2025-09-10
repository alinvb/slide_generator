#!/usr/bin/env python3
"""
Debug using the actual keywords from topics_checklist
"""

from app import analyze_conversation_progress

def debug_actual_keywords():
    print("🔍 Debugging Actual Keywords from topics_checklist")
    print("=" * 60)
    
    # Create minimal conversation to get access to topics_checklist
    messages = [
        {"role": "system", "content": "test"},
        {"role": "assistant", "content": "Let's analyze your historical financial performance. Can you provide your revenue, EBITDA, margins?"},
    ]
    
    # Extract the topics_checklist from analyze_conversation_progress
    # We'll need to import and check the actual structure
    
    question = "let's analyze your historical financial performance. can you provide your revenue, ebitda, margins?"
    
    # These should match what's in the actual function
    from app import analyze_conversation_progress
    
    # I'll copy the actual topic definitions from the function
    topics_checklist = {
        "historical_financial_performance": {
            "topic_keywords": ["revenue", "financial", "ebitda", "margin"],
        },
        "product_service_footprint": {
            "topic_keywords": ["products", "services", "offerings", "footprint"],
        }
    }
    
    # Pattern definitions (copied from the function)
    topic_patterns = {
        "product_service_footprint": ["product", "service", "footprint", "offerings", "geographic"],
        "historical_financial_performance": ["financial performance", "analyze your historical", "revenue", "ebitda", "financial metrics"],
    }
    
    print(f"Question: {question}")
    print()
    
    for topic_name in ["product_service_footprint", "historical_financial_performance"]:
        print(f"🔸 {topic_name.upper()}:")
        
        # Method 1: Check topic keywords
        topic_info = topics_checklist[topic_name]
        topic_keywords_in_question = sum(1 for kw in topic_info["topic_keywords"] if kw in question)
        keyword_matches = [kw for kw in topic_info["topic_keywords"] if kw in question]
        
        # Method 2: Check patterns
        pattern_matches = 0
        pattern_match_list = []
        if topic_name in topic_patterns:
            for pattern in topic_patterns[topic_name]:
                if pattern in question:
                    pattern_matches += 1
                    pattern_match_list.append(pattern)
        
        total_score = topic_keywords_in_question + pattern_matches
        
        print(f"  Keywords: {topic_info['topic_keywords']}")
        print(f"  Keyword matches: {keyword_matches} (count: {topic_keywords_in_question})")
        print(f"  Patterns: {topic_patterns.get(topic_name, [])}")
        print(f"  Pattern matches: {pattern_match_list} (count: {pattern_matches})")
        print(f"  Total score: {total_score}")
        print(f"  Meets threshold: {total_score >= 2 or topic_keywords_in_question >= 2}")
        print()

if __name__ == "__main__":
    debug_actual_keywords()