#!/usr/bin/env python3
"""
Debug the keyword matching issue
"""

def debug_keyword_matching():
    print("🔍 Debugging Keyword Matching")
    print("=" * 50)
    
    question = "let's analyze your historical financial performance. can you provide your revenue, ebitda, margins?"
    
    # Test historical_financial_performance keywords
    financial_topic_keywords = ["revenue", "financial", "ebitda", "margin"]
    financial_patterns = ["financial performance", "analyze your historical", "revenue", "ebitda", "financial metrics"]
    
    # Test product_service_footprint keywords  
    product_topic_keywords = ["products", "services", "offerings", "footprint"]
    product_patterns = ["product", "service", "footprint", "offerings", "geographic"]
    
    print(f"Question: {question}")
    print()
    
    # Financial matching
    print("🔸 FINANCIAL PERFORMANCE:")
    financial_keyword_matches = [kw for kw in financial_topic_keywords if kw in question]
    financial_pattern_matches = [pattern for pattern in financial_patterns if pattern in question]
    financial_score = len(financial_keyword_matches) + len(financial_pattern_matches)
    
    print(f"  Keywords: {financial_topic_keywords}")
    print(f"  Matches: {financial_keyword_matches} (count: {len(financial_keyword_matches)})")
    print(f"  Patterns: {financial_patterns}")
    print(f"  Pattern matches: {financial_pattern_matches} (count: {len(financial_pattern_matches)})")
    print(f"  Total score: {financial_score}")
    print(f"  Meets threshold (≥2): {financial_score >= 2}")
    
    print()
    
    # Product matching
    print("🔸 PRODUCT/SERVICE FOOTPRINT:")
    product_keyword_matches = [kw for kw in product_topic_keywords if kw in question]
    product_pattern_matches = [pattern for pattern in product_patterns if pattern in question]
    product_score = len(product_keyword_matches) + len(product_pattern_matches)
    
    print(f"  Keywords: {product_topic_keywords}")
    print(f"  Matches: {product_keyword_matches} (count: {len(product_keyword_matches)})")
    print(f"  Patterns: {product_patterns}")
    print(f"  Pattern matches: {product_pattern_matches} (count: {len(product_pattern_matches)})")  
    print(f"  Total score: {product_score}")
    print(f"  Meets threshold (≥2): {product_score >= 2}")
    
    print()
    
    print(f"🎯 Winner: {'Financial Performance' if financial_score > product_score else 'Product/Service Footprint'}")
    
    # Test "margins" vs "margin" issue
    print()
    print("🔸 MARGIN vs MARGINS issue:")
    print(f"  'margin' in question: {'margin' in question}")
    print(f"  'margins' in question: {'margins' in question}")

if __name__ == "__main__":
    debug_keyword_matching()