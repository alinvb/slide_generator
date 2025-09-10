#!/usr/bin/env python3

"""
Debug why the topic pattern matching isn't working correctly
"""

def test_pattern_matching():
    """Test which patterns are being matched in the actual conversation"""
    
    # Official topic patterns from the fix
    official_topic_patterns = [
        "what is your company name",  # Topic 1
        "product/service footprint",  # Topic 2  
        "historical financial performance",  # Topic 3
        "management team",  # Topic 4
        "growth strategy and projections",  # Topic 5
        "positioned competitively",  # Topic 6
        "precedent transactions",  # Topic 7
        "valuation methodologies",  # Topic 8
        "strategic buyers",  # Topic 9
        "private equity firms", # Topic 10
        "conglomerates",  # Topic 11
        "margin and cost data",  # Topic 12
        "investor considerations",  # Topic 13
        "investment/acquisition process"  # Topic 14
    ]
    
    # Test messages from the actual conversation
    test_messages = [
        "What is your company name and give me a brief overview of what your business does?",
        "Now let's discuss your product/service footprint. What are your main offerings? Please provide the title and description for each product/service. Also, where do you operate geographically and what's your market coverage?",
        "Let's analyze your historical financial performance. Can you provide your revenue, EBITDA, margins, and key financial metrics for the last 3-5 years? I need specific numbers: annual revenue in USD millions, EBITDA figures, margin percentages, growth rates, and key performance drivers. What are the main revenue streams and how have they evolved?",
        "Thanks for that information! To complete the financial analysis, I additionally need revenue figures and EBITDA margins and growth rates. Do you have this data, or should I research it?"
    ]
    
    print("🔍 TESTING PATTERN MATCHING")
    print("=" * 40)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n📝 Message {i}: '{message[:60]}...'")
        
        msg_content_lower = message.lower()
        matches = []
        
        for j, pattern in enumerate(official_topic_patterns, 1):
            if pattern in msg_content_lower:
                matches.append(f"Topic {j} ({pattern})")
        
        if matches:
            print(f"✅ MATCHES: {', '.join(matches)}")
        else:
            print(f"❌ NO MATCH: Not an official topic question")

def main():
    test_pattern_matching()

if __name__ == "__main__":
    main()