#!/usr/bin/env python3
"""
Test slide generation logic to see why only 3 slides are generated
"""

# Sample Netflix conversation messages (extracted from user's conversation)
netflix_messages = [
    {"role": "assistant", "content": "What is your company name and give me a brief overview of what your business does?"},
    {"role": "user", "content": "Netflix"},
    {"role": "assistant", "content": "Netflix is the world's most-subscribed streaming service..."},
    {"role": "user", "content": "ok"},
    
    {"role": "assistant", "content": "Now let's discuss your product/service footprint. What are your main offerings?"},
    {"role": "user", "content": "research this yourself"},
    {"role": "assistant", "content": "Netflix is a global streaming entertainment company offering a vast catalog of original and licensed TV series, movies, and documentaries, with operations in over 190 countries..."},
    {"role": "user", "content": "ok"},
    
    {"role": "assistant", "content": "Let's analyze your historical financial performance. Can you provide your revenue, EBITDA, margins..."},
    {"role": "user", "content": "research this for me"},
    {"role": "assistant", "content": "Netflix's financial performance over the last 3–5 years has shown strong, sustained growth in revenue, margins, and profitability... Annual Revenue: 2022: $31.6 billion... 2024: $39.00 billion..."},
    {"role": "user", "content": "ok"},
    
    {"role": "assistant", "content": "Now I need information about your management team. Can you provide names, titles, and brief backgrounds for 4-6 key executives including CEO, CFO, and other senior leaders?"},
    {"role": "user", "content": "research this for me"},
    {"role": "assistant", "content": "Netflix's management team consists of experienced executives... Ted Sarandos – Co-CEO... Greg Peters – Co-CEO... Spencer Neumann – Chief Financial Officer..."},
    {"role": "user", "content": "add more information about Crete Willems"},
    {"role": "user", "content": "ok"},
    
    {"role": "assistant", "content": "Let's discuss your growth strategy and projections..."},
    {"role": "user", "content": "research this for me"},
    {"role": "assistant", "content": "Netflix's growth strategy for the next 3–5 years centers on aggressive international expansion... Financial projections are ambitious, with a target to nearly double annual revenue..."},
    {"role": "user", "content": "ok"},
    
    {"role": "assistant", "content": "How is your company positioned competitively? I need information about key competitors..."},
    {"role": "user", "content": "research this for me"},
    {"role": "assistant", "content": "Netflix is positioned as the global leader in subscription-based streaming video... Key Competitors (2025): Disney+... Prime Video... Hulu..."},
    {"role": "user", "content": "ok"},
    
    {"role": "assistant", "content": "Now let's examine precedent transactions..."},
    {"role": "user", "content": "research this for me"},
    {"role": "assistant", "content": "Recent precedent M&A transactions in the streaming and media sector (2024–2025)... Disney acquires Fubo..."},
    {"role": "user", "content": "ok"},
    
    {"role": "assistant", "content": "What valuation methodologies would be most appropriate for your business?"},
    {"role": "user", "content": "research this for me"},
    {"role": "assistant", "content": "The most appropriate valuation methodologies for a streaming and media company like Netflix are Discounted Cash Flow (DCF) analysis, Trading Multiples..."},
    {"role": "user", "content": "ok"},
    
    {"role": "assistant", "content": "Based on your valuation range, let's identify strategic buyers..."},
    {"role": "user", "content": "research this for me"},
    {"role": "assistant", "content": "Strategic buyers most likely to afford and value Netflix's strategic assets... Amazon (Prime Video)... Disney..."},
    {"role": "user", "content": "ok"},
    
    {"role": "assistant", "content": "Now let's identify private equity firms that can afford your valuation..."},
    {"role": "user", "content": "research this for me"},
    {"role": "assistant", "content": "Leading private equity firms with the financial capacity and sector experience... KKR... Blackstone... TPG..."},
    {"role": "user", "content": "ok"},
    
    {"role": "assistant", "content": "Finally, let's identify large conglomerates..."},
    {"role": "user", "content": "research this for me"},
    {"role": "assistant", "content": "The largest conglomerates operating in the media and entertainment sector... The Walt Disney Company... Comcast Corporation..."},
    {"role": "user", "content": "ok"},
    
    {"role": "assistant", "content": "Let's discuss margin and cost data..."},
    {"role": "user", "content": "research this for me"},
    {"role": "assistant", "content": "Netflix's EBITDA margins have shown significant improvement... 2022 EBITDA Margin: 19.95%... 2024 EBITDA Margin: 26.4%..."},
    {"role": "user", "content": "ok"},
    
    {"role": "assistant", "content": "Now let's discuss investor considerations. What are the key RISKS and OPPORTUNITIES..."},
    {"role": "user", "content": "research this for mer"},
    {"role": "assistant", "content": "Key risks for Netflix investors in 2025 include high valuation expectations... Key opportunities include strong international growth..."},
    {"role": "user", "content": "ok"},
    
    {"role": "assistant", "content": "Finally, what would the investment/acquisition process look like?"},
    {"role": "user", "content": "research this for me"},
    {"role": "assistant", "content": "The investment or acquisition process for a company like Netflix typically follows... Due diligence topics... Synergy opportunities..."},
    {"role": "user", "content": "ok"}
]

def analyze_topics():
    """Analyze the conversation to see which topics should be detected"""
    
    # Get all conversation text
    conversation_text = " ".join([msg["content"] for msg in netflix_messages if msg["role"] != "system"]).lower()
    
    print("🔍 ANALYZING NETFLIX CONVERSATION")
    print("=" * 60)
    print(f"📝 Total conversation length: {len(conversation_text)} characters")
    
    # Topic keywords from the slide generator
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
    
    # Check for research indicators
    research_indicators = ["research", "based on", "according to", "here is", "here are", "analysis shows"]
    has_research_response = any(indicator in conversation_text for indicator in research_indicators)
    
    print(f"🔬 Has research responses: {has_research_response}")
    print(f"📊 Research indicator count: {sum(1 for indicator in research_indicators if indicator in conversation_text)}")
    
    covered_topics = []
    
    for topic_name, keywords in topics_with_keywords.items():
        # Check if enough keywords are present to indicate topic coverage
        keywords_found = sum(1 for keyword in keywords if keyword in conversation_text)
        
        # Enhanced coverage detection
        is_covered = (
            keywords_found >= 2 or  # Direct keyword match
            (keywords_found >= 1 and has_research_response) or  # Research provided for topic
            (keywords_found >= 1 and len(conversation_text.split()) > 100)  # Substantial discussion
        )
        
        print(f"📋 {topic_name:<30} | Keywords: {keywords_found:>2}/{len(keywords)} | Covered: {'✅' if is_covered else '❌'}")
        
        if is_covered:
            covered_topics.append(topic_name)
    
    print("\n🎯 RESULTS:")
    print(f"📊 Topics covered: {len(covered_topics)}/14")
    print(f"📋 Covered topics: {covered_topics}")
    
    return covered_topics

if __name__ == "__main__":
    covered_topics = analyze_topics()
    print(f"\n🚀 Expected slides to generate: {len(covered_topics)}")
    print(f"🎯 Should generate slides for: {', '.join(covered_topics)}")