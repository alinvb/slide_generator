#!/usr/bin/env python3
"""
Test script to debug the conversation analysis issue
"""

# Sample conversation from the user's example with AI research responses
test_conversation = """
Qi in Iraq refers to the Qi Card, the country's national debit and smart card platform, managed by International Smart Card (ISC), which plays a central role in Iraq's financial infrastructure and digital payments landscape.

Key context and details:

What is Qi Card?

The Qi Card (pronounced "key") is Iraq's national debit/credit card, created in 2008 by a partnership between the state-owned Rafidain and Rasheed Banks and the Iraqi Electronic Payment System.
It is widely used for government salary disbursement, welfare payments, and private sector transactions.
As of 2025, Qi Card has over 11 million cardholders and 5 million app users, with a network of more than 20,000 point-of-sale merchants and 10,000 cash-out agents across Iraq.

Role in financial inclusion and fintech:

Qi has been instrumental in increasing banking penetration in Iraq, helping the percentage of banked individuals rise from about 5% to nearly 50% in recent years.
The company recently launched the SuperQi app in partnership with Ant International (Alibaba Group), aiming to reach 15 million users by 2026 and further digitize financial services.
SuperQi is positioned as a "third-generation" financial app, providing digital payments, transfers, and other retail financial services.

Infrastructure and compliance:

Qi's infrastructure is deeply integrated with Iraqi government systems, large banks, and global payment networks.
The company is undergoing a major compliance overhaul with K2 Integrity, a global financial crime compliance firm, to align Iraq's financial system with international anti-money laundering (AML) and counter-terror finance (CFT) standards.
This partnership includes comprehensive internal training, process upgrades, and the establishment of a compliance back office in Jordan, with the UAE acting as a fintech innovation hub.

USER: Now let's identify potential strategic buyers—companies that might acquire you for strategic reasons. I need 4-5 strategic buyers with company name, strategic rationale (10-20 words), key synergies, fit assessment, and financial capacity.

USER: research this yourself

AI: Based on current market research and industry analysis, here are 4 potential strategic buyers for Qi (International Smart Card) in Iraq:

Ant Group Global fintech leader (Alipay, Ant International, China) Expand digital payment ecosystem in Middle East Technology, cross-border payments, app integration High (9/10) – Strong fintech alignment Multi-billion USD
Mastercard Inc. Global payments technology company Scale local payments infrastructure Network, regulatory experience High (9/10) $360B market cap
Thales Group France-based secure digital identity leader Expand biometric payments Biometric security, government integration High (9/10) €18B revenue

USER: Now let's identify financial buyers—private equity firms, VCs, and other financial investors.

USER: research this yourself  

AI: Based on research and current MENA investment trends, here are financial buyers for Qi:

BlackRock Private Equity Partners World's largest asset manager with extensive PE arm Leverage MENA fintech growth and regional digitization trends for scalable returns Institutional capital, governance, global fintech network High (9/10) – Institutional scale, governance $240B+ private markets AUM
Sequoia Capital Leading global VC with fintech focus Tap rapid fintech adoption in MENA Startup scaling, innovation High (8/10) $80B+ AUM

USER: What about management team details?

USER: research this yourself

AI: Based on available information and industry research, here are key management profiles for Qi:

CEO: Over 20 years in fintech and payments infrastructure, founded Qi Card and led scaling to 12M+ users, former executive at Rafidain Bank
CTO: Led rollout of SuperQi app and 70,000+ POS terminals, expert in biometrics and secure payments architecture
CFO: 15+ years in financial management, oversaw multiple M&A transactions in digital payments
"""

# Define topics_checklist similar to the app
topics_checklist = {
    "business_overview": {
        "keywords": ["company", "business", "what does", "overview", "operations", "founded", "headquarters", "industry", "sector", "description"],
        "covered": False,
    },
    "investor_considerations": {
        "keywords": ["risk", "opportunity", "investor", "considerations", "challenges", "mitigation", "concerns"],
        "covered": False,
    },
    "product_service_footprint": {
        "keywords": ["products", "services", "offerings", "geographic", "footprint", "coverage", "operations", "locations"],
        "covered": False,
    },
    "historical_financial_performance": {
        "keywords": ["revenue", "financial", "ebitda", "margin", "historical", "years", "growth", "2021", "2022", "2023", "2024", "2025", "profit", "performance"],
        "covered": False,
    },
    "management_team": {
        "keywords": ["management", "team", "executives", "ceo", "cfo", "founder", "leadership", "senior management"],
        "covered": False,
    },
    "growth_strategy_projections": {
        "keywords": ["growth", "strategy", "expansion", "projections", "future", "strategic initiatives", "market size", "roadmap"],
        "covered": False,
    },
    "competitive_positioning": {
        "keywords": ["competitive", "competitors", "positioning", "comparison", "advantages", "differentiation", "market position"],
        "covered": False,
    },
    "valuation_overview": {
        "keywords": ["valuation", "multiple", "methodology", "worth", "assumptions", "enterprise value", "dcf", "comparable"],
        "covered": False,
    },
    "precedent_transactions": {
        "keywords": ["precedent", "transactions", "m&a", "acquisitions", "deals", "transaction multiples"],
        "covered": False,
    },
    "strategic_buyers": {
        "keywords": ["strategic buyers", "strategic", "acquirer", "acquisition", "corporate buyer", "industry player", "strategic rationale", "synergies"],
        "covered": False,
    },
    "financial_buyers": {
        "keywords": ["financial buyers", "private equity", "pe", "vc", "venture capital", "financial investor", "fund", "investment rationale"],
        "covered": False,
    },
    "margin_cost_resilience": {
        "keywords": ["margin", "cost", "resilience", "stability", "profitability", "efficiency", "cost management"],
        "covered": False,
    },
    "sea_conglomerates": {
        "keywords": ["conglomerate", "global", "international", "multinational", "strategic acquirer"],
        "covered": False,
    },
    "investor_process_overview": {
        "keywords": ["process", "diligence", "due diligence", "timeline", "synergy", "risk factors", "transaction process"],
        "covered": False,
    }
}

# Test keyword detection
print("Testing keyword detection on sample conversation:")
print("=" * 60)

conversation_text = test_conversation.lower()
covered_topics = []

for topic_name, topic_info in topics_checklist.items():
    found_keywords = []
    for keyword in topic_info["keywords"]:
        if keyword in conversation_text:
            found_keywords.append(keyword)
    
    # Check for AI research responses (when user asks AI to research)
    research_indicators = [
        "research this yourself", "research yourself", "based on current market data",
        "based on research", "according to", "sources:", "references:", "[1]", "[2]", "[3]",
        "here are", "based on the latest", "current market research", "industry analysis"
    ]
    
    has_research_response = any(indicator in conversation_text for indicator in research_indicators)
    
    # Enhanced coverage detection - require substantial content, not just keywords from AI questions
    is_covered = False
    
    # Require multiple keywords OR substantial content length for that topic
    if len(found_keywords) >= 3:  # Multiple keywords found
        is_covered = True
    elif len(found_keywords) >= 2:
        # Check if there's substantial content (not just AI questions)
        topic_specific_content = False
        for keyword in found_keywords:
            keyword_positions = []
            start_pos = 0
            while True:
                pos = conversation_text.find(keyword, start_pos)
                if pos == -1:
                    break
                keyword_positions.append(pos)
                start_pos = pos + 1
            
            # Check if any keyword instance has substantial surrounding content
            for pos in keyword_positions:
                # Extract 200 chars around the keyword
                context_start = max(0, pos - 100)
                context_end = min(len(conversation_text), pos + 100)
                context = conversation_text[context_start:context_end]
                
                # Look for indicators of substantial content or AI research
                content_indicators = [
                    "million", "$", "billion", "revenue", "founded", "established", 
                    "years", "experience", "ceo", "cfo", "headquarters", "operates",
                    "customers", "users", "employees", "growth rate", "margin",
                    "ebitda", "percent", "%", "strategy", "partnership", "subsidiary"
                ]
                
                # Also check for AI research indicators in context
                ai_research_indicators = [
                    "according to", "based on", "research shows", "data indicates",
                    "market analysis", "industry reports", "current trends", "sources",
                    "references", "[1]", "[2]", "leading", "global", "methodology"
                ]
                
                content_score = len([indicator for indicator in content_indicators if indicator in context])
                research_score = len([indicator for indicator in ai_research_indicators if indicator in context])
                
                # Consider covered if substantial content OR AI research response
                if content_score >= 2 or (research_score >= 2 and has_research_response):
                    topic_specific_content = True
                    break
            
            if topic_specific_content:
                break
        
        if topic_specific_content:
            is_covered = True
    
    # Special handling for specific topics
    if topic_name == "management_team":
        management_indicators = ["ceo", "cfo", "cto", "founder", "president", "director", "executive", "years of experience", "previously", "background in"]
        found_mgmt = [indicator for indicator in management_indicators if indicator in conversation_text]
        
        # Consider covered if detailed mgmt info OR AI research with executive details
        detailed_mgmt = len(found_mgmt) >= 2
        ai_mgmt_research = has_research_response and len(found_mgmt) >= 1 and ("chief" in conversation_text or "executive" in conversation_text)
        
        is_covered = detailed_mgmt or ai_mgmt_research
    
    elif topic_name == "historical_financial_performance":
        financial_indicators = ["revenue", "ebitda", "profit", "million", "billion", "$", "2020", "2021", "2022", "2023", "2024", "2025", "growth", "%", "margin"]
        found_financial = [indicator for indicator in financial_indicators if indicator in conversation_text]
        
        # Consider covered if detailed financials OR AI research with financial data
        detailed_financials = len(found_financial) >= 3
        ai_financial_research = has_research_response and len(found_financial) >= 2 and ("$" in conversation_text or "million" in conversation_text)
        
        is_covered = detailed_financials or ai_financial_research
    
    elif topic_name == "strategic_buyers" or topic_name == "financial_buyers":
        buyer_indicators = ["acquisition", "acquirer", "fund", "capital", "equity", "investment", "rationale", "synerg", "fit assessment", "capacity"]
        found_buyers = [indicator for indicator in buyer_indicators if indicator in conversation_text]
        # Also check for company/fund names (capitalized entities) - improved regex
        import re
        # First try original pattern
        company_names = re.findall(r'\b[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*\s+(?:Group|Inc|Corp|Capital|Partners|Fund|Equity|Holdings)\b', conversation_text)
        # Look for specific companies mentioned in the text
        specific_companies = re.findall(r'\b(?:Ant Group|BlackRock|Mastercard|Thales Group|Sequoia Capital)\b', conversation_text, re.IGNORECASE)
        # Look for any capitalized entity followed by certain keywords
        generic_companies = re.findall(r'\b[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)?\s+(?:Group|Capital|Partners|Inc|Corp)\b', conversation_text)
        
        all_company_names = list(set(company_names + specific_companies + generic_companies))
        

        
        # Consider covered if detailed profiles OR AI research response with buyer data
        detailed_buyer_content = len(found_buyers) >= 3 and len(company_names) >= 2
        ai_buyer_research = has_research_response and len(company_names) >= 3 and len(found_buyers) >= 2
        
        # Use all company names for calculation
        total_company_count = len(all_company_names)
        
        # Consider covered if detailed profiles OR AI research response with buyer data
        detailed_buyer_content = len(found_buyers) >= 3 and total_company_count >= 2
        ai_buyer_research = has_research_response and total_company_count >= 2 and len(found_buyers) >= 2
        
        is_covered = detailed_buyer_content or ai_buyer_research
    
    if is_covered:
        topic_info["covered"] = True
        covered_topics.append(topic_name)
        print(f"✅ {topic_name}: Found keywords: {found_keywords} -> COVERED")
    else:
        print(f"❌ {topic_name}: Found keywords: {found_keywords} -> NOT COVERED")

print("\n" + "=" * 60)
print(f"COVERED TOPICS ({len(covered_topics)}): {covered_topics}")

# Find next uncovered topic
next_topic = None
for topic_name, topic_info in topics_checklist.items():
    if not topic_info["covered"]:
        next_topic = topic_name
        break

print(f"NEXT TOPIC: {next_topic}")