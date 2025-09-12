#!/usr/bin/env python3
"""
Create Netflix conversation data to replace sample data
"""

def create_netflix_conversation():
    """Create realistic Netflix investment banking conversation"""
    
    netflix_conversation = [
        {"role": "system", "content": "Investment banking research assistant"},
        {"role": "assistant", "content": "Let's conduct comprehensive research on Netflix, Inc. for your investment banking analysis and potential acquisition scenarios."},
        
        {"role": "user", "content": "I want to analyze Netflix for a potential acquisition. It's the leading global streaming entertainment service with over 260 million subscribers worldwide. Founded in 1997, headquartered in Los Gatos, California. They've transformed from DVD-by-mail to the dominant streaming platform."},
        
        {"role": "assistant", "content": "**Business Overview Research Complete**\n\nCompany: Netflix, Inc.\nFounded: 1997\nHeadquarters: Los Gatos, California\nIndustry: Streaming Entertainment / Media Technology\nBusiness Model: Subscription-based streaming service\nGlobal Reach: 260+ million subscribers\nKey Differentiator: Original content production + global streaming platform\n\nNow let's discuss your financial performance. What's the current revenue and profitability situation?"},
        
        {"role": "user", "content": "Netflix's financials are strong. 2024 revenue around $39 billion, growing to projected $63 billion by 2029. EBITDA margins have improved significantly - from $9.75B in 2024 to projected $15.7B by 2029. They're highly profitable now with strong cash generation from the subscriber base."},
        
        {"role": "assistant", "content": "**Financial Performance Research Complete**\n\nStrong financial trajectory:\n- Revenue: $39B (2024) → $63B (2029E)\n- EBITDA: $9.75B → $15.7B\n- Margin expansion and cash generation\n- Subscription model provides recurring revenue\n\nNow let's identify the management team. Who are the key executives driving Netflix's strategy?"},
        
        {"role": "user", "content": "Key management includes Co-CEO Ted Sarandos (Chief Content Officer background, Hollywood relationships), Co-CEO Greg Peters (former Chief Product Officer, tech/product focus), CFO Spencer Neumann (former Activision CFO, finance expertise), and Chief Marketing Officer Bela Bajaria (content strategy and global expansion)."},
        
        {"role": "assistant", "content": "**Management Team Research Complete**\n\nStrong dual-CEO leadership structure:\n- Co-CEO Ted Sarandos: Content/Hollywood expertise\n- Co-CEO Greg Peters: Technology/Product focus  \n- CFO Spencer Neumann: Finance/Operations (ex-Activision)\n- CMO Bela Bajaria: Global content strategy\n\nNow let's discuss potential strategic buyers. Which companies would be interested in acquiring Netflix?"},
        
        {"role": "user", "content": "Strategic buyers could include Apple (has $200B+ cash, needs content for Apple TV+), Amazon (content for Prime Video, cloud synergies), Microsoft (gaming + content convergence, Azure integration), Disney (streaming consolidation, content library combination), and potentially Google/Alphabet (YouTube synergies, cloud infrastructure)."},
        
        {"role": "assistant", "content": "**Strategic Buyers Research Complete**\n\nIdentified 5 major strategic buyers:\n- Apple: $200B+ cash position, Apple TV+ content needs\n- Amazon: Prime Video integration, AWS cloud synergies\n- Microsoft: Gaming convergence, Azure infrastructure\n- Disney: Streaming consolidation, content library merger\n- Google/Alphabet: YouTube integration, cloud capabilities\n\nNow let's identify financial buyers. Which private equity or investment firms would consider Netflix?"},
        
        {"role": "user", "content": "Financial buyers are limited given Netflix's $200B+ market cap, but potential buyers include Berkshire Hathaway (Warren Buffett likes media/content businesses), Apollo Global Management (large media deals), KKR (has media expertise), Blackstone (infrastructure/content assets), and sovereign wealth funds like Saudi PIF or Singapore GIC who can handle mega-deals."},
        
        {"role": "assistant", "content": "**Financial Buyers Research Complete**\n\nLimited to mega-cap capable buyers:\n- Berkshire Hathaway: Buffett's media preference\n- Apollo Global Management: Large media deal experience\n- KKR: Media sector expertise\n- Blackstone: Content/infrastructure focus\n- Sovereign funds: Saudi PIF, Singapore GIC (mega-deal capacity)\n\nNow let's discuss valuation. What multiples and methodologies are relevant for Netflix?"},
        
        {"role": "user", "content": "Netflix should be valued using multiple approaches: DCF analysis based on subscriber growth and cash flow projections, comparable company analysis vs Disney, Amazon Prime, Apple TV+ (probably 8-12x revenue), and precedent transactions like Disney-Fox ($71B), AT&T-WarnerMedia ($85B), and Amazon-MGM ($8.45B). Given streaming leadership and global scale, Netflix could command 10-15x revenue multiple."},
        
        {"role": "assistant", "content": "**Valuation Research Complete**\n\nThree valuation methodologies:\n- DCF Analysis: Subscriber-based cash flow projections\n- Comparable Companies: 8-12x revenue vs Disney/Amazon\n- Precedent Transactions: Disney-Fox ($71B), AT&T-Warner ($85B), Amazon-MGM ($8.45B)\n- Target Multiple: 10-15x revenue given market leadership\n\nLet's discuss competitive positioning. How does Netflix compete in streaming?"},
        
        {"role": "user", "content": "Netflix competes against Disney+ (family content), Amazon Prime Video (bundled offering), Apple TV+ (premium originals), HBO Max/Discovery+ (premium content), YouTube (free/ad-supported), and international players like Tencent Video. Netflix's advantages are global scale, original content production capabilities, recommendation algorithm, and first-mover advantage in streaming."},
        
        {"role": "assistant", "content": "**Competitive Analysis Complete**\n\nMain competitors and Netflix advantages:\n- vs Disney+: Broader content vs family focus\n- vs Amazon Prime: Standalone vs bundled model\n- vs Apple TV+: Scale vs premium positioning\n- vs HBO Max: Volume vs prestige content\n- vs YouTube: Paid vs ad-supported\n\nKey advantages: Global scale, original content, ML algorithms, first-mover\n\nFinally, what are the key investment considerations and risks?"},
        
        {"role": "user", "content": "Investment considerations include Netflix's market leadership position, strong content pipeline with $15B+ annual content spend, global subscriber growth potential especially in emerging markets, and pricing power. Key risks are increased competition from tech giants, content cost inflation, subscriber saturation in mature markets, and potential regulation of content or pricing in key markets."},
        
        {"role": "assistant", "content": "**Investment Considerations & Risk Assessment Complete**\n\nInvestment Highlights:\n- Market leadership in streaming\n- $15B+ annual content investment\n- Global growth potential\n- Subscription pricing power\n\nKey Risks:\n- Tech giant competition (Apple, Amazon, Google)\n- Content cost inflation\n- Subscriber saturation in mature markets\n- Regulatory risks in key jurisdictions\n\n✅ **Netflix Research Complete!** All 14 topics covered including business overview, financials, management, strategic buyers, financial buyers, competitive positioning, valuation methodologies, and investment considerations.\n\n✅ **Ready for JSON Generation**: You can now click 'Generate JSON Now' to create your comprehensive Netflix investment banking presentation."}
    ]
    
    return netflix_conversation

def print_conversation_summary():
    """Print summary of Netflix conversation"""
    
    conversation = create_netflix_conversation()
    
    print("🎬 NETFLIX CONVERSATION DATA CREATED")
    print("=" * 50)
    
    print(f"📊 CONVERSATION STATS:")
    print(f"   • Total messages: {len(conversation)}")
    print(f"   • User messages: {len([m for m in conversation if m['role'] == 'user'])}")
    print(f"   • Assistant messages: {len([m for m in conversation if m['role'] == 'assistant'])}")
    
    print(f"\n🎯 KEY NETFLIX DATA POINTS:")
    netflix_data_points = [
        "Company: Netflix, Inc. (1997, Los Gatos, CA)",
        "Revenue: $39B (2024) → $63B (2029E)", 
        "EBITDA: $9.75B → $15.7B",
        "Subscribers: 260+ million globally",
        "Management: Co-CEOs Ted Sarandos & Greg Peters",
        "Strategic Buyers: Apple, Amazon, Microsoft, Disney, Google",
        "Financial Buyers: Berkshire, Apollo, KKR, Blackstone, Sovereign funds",
        "Valuation: 10-15x revenue, DCF + Comps + Precedents",
        "Competition: Disney+, Prime Video, Apple TV+, HBO Max",
        "Investment Thesis: Market leader, content pipeline, global growth"
    ]
    
    for point in netflix_data_points:
        print(f"   ✅ {point}")
    
    print(f"\n📋 CONVERSATION TOPICS COVERED:")
    topics = [
        "Business Overview", "Financial Performance", "Management Team",
        "Strategic Buyers", "Financial Buyers", "Valuation Methodologies", 
        "Competitive Positioning", "Investment Considerations & Risks"
    ]
    
    for i, topic in enumerate(topics, 1):
        print(f"   {i}. {topic}")
    
    return conversation

if __name__ == "__main__":
    conversation = print_conversation_summary()
    
    print(f"\n🚀 READY TO REPLACE SAMPLE DATA:")
    print(f"   This Netflix conversation will replace TechCorp sample data")
    print(f"   Contains real investment banking analysis structure")
    print(f"   Includes strategic/financial buyers, valuations, competitive analysis")
    print(f"   Perfect for testing conversation extraction and JSON generation")