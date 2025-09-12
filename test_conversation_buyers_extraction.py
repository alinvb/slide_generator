#!/usr/bin/env python3
"""
Test why strategic and financial buyers mentioned in conversation aren't being extracted
"""

def analyze_conversation_extraction_gaps():
    """Analyze what's missing from the conversation extraction"""
    
    print("🔍 ANALYZING CONVERSATION EXTRACTION GAPS")
    print("=" * 60)
    
    # What the current extraction prompt includes
    current_extraction_fields = [
        "company_name",
        "business_description", 
        "industry",
        "founded_year",
        "headquarters_location",
        "annual_revenue_usd_m",
        "ebitda_usd_m", 
        "financial_years",
        "key_executives",
        "products_services",
        "competitors_mentioned",
        "financial_details",
        "growth_details",
        "market_details",
        "business_model",
        "key_achievements",
        "challenges_mentioned", 
        "key_discussion_points"
    ]
    
    # What users often mention that should be extracted
    missing_critical_fields = [
        "strategic_buyers_mentioned",      # 🚨 MISSING!
        "financial_buyers_mentioned",     # 🚨 MISSING!
        "potential_acquirers_mentioned",  # 🚨 MISSING!
        "valuation_estimates_mentioned",  # 🚨 MISSING!
        "transaction_comps_mentioned",    # 🚨 MISSING!
        "management_team_details",        # 🚨 MISSING!
        "investment_thesis_points",       # 🚨 MISSING!
        "synergies_mentioned",           # 🚨 MISSING!
        "risk_factors_discussed",        # 🚨 MISSING!
        "exit_strategies_mentioned"      # 🚨 MISSING!
    ]
    
    print(f"📋 CURRENT EXTRACTION FIELDS: {len(current_extraction_fields)}")
    for field in current_extraction_fields:
        print(f"   ✅ {field}")
    
    print(f"\n🚨 MISSING CRITICAL FIELDS: {len(missing_critical_fields)}")  
    for field in missing_critical_fields:
        print(f"   ❌ {field}")
    
    print(f"\n💡 THE PROBLEM:")
    print(f"   • Conversation extraction only captures basic company info")
    print(f"   • Investment banking-specific fields are ignored")
    print(f"   • User mentions of buyers, valuations, synergies are lost")
    print(f"   • System falls back to generic research instead of using conversation")
    
    return current_extraction_fields, missing_critical_fields

def simulate_conversation_with_buyers():
    """Simulate a conversation that mentions buyers to show the gap"""
    
    print(f"\n📝 CONVERSATION SIMULATION")
    print("=" * 40)
    
    conversation_example = """
    User: "I want to analyze TechCorp for acquisition. We've identified several potential buyers:
    
    Strategic buyers include Microsoft, Google, and Salesforce - they all need our AI capabilities.
    Microsoft would pay the most due to Azure synergies, probably 15-20x revenue.
    
    Financial buyers we're talking to include Vista Equity Partners, Thoma Bravo, and KKR.
    Vista knows our space well and could add value through their portfolio companies.
    
    Our management team has CEO John Smith (ex-Microsoft), CTO Sarah Lee (PhD Stanford), 
    and CFO Mike Chen (former Goldman Sachs).
    
    Main risks are customer concentration (top 3 clients = 60% revenue) and competition from OpenAI."
    """
    
    print("💬 EXAMPLE CONVERSATION:")
    print(conversation_example)
    
    print("\n🔍 WHAT SHOULD BE EXTRACTED:")
    should_extract = {
        "strategic_buyers_mentioned": ["Microsoft", "Google", "Salesforce"],
        "financial_buyers_mentioned": ["Vista Equity Partners", "Thoma Bravo", "KKR"],
        "valuation_estimates_mentioned": ["15-20x revenue"],
        "synergies_mentioned": ["Azure synergies", "Vista portfolio companies"],
        "management_team_details": ["CEO John Smith (ex-Microsoft)", "CTO Sarah Lee (PhD Stanford)", "CFO Mike Chen (former Goldman Sachs)"],
        "risk_factors_discussed": ["customer concentration (top 3 clients = 60% revenue)", "competition from OpenAI"]
    }
    
    for field, items in should_extract.items():
        print(f"   ✅ {field}: {len(items)} items")
        for item in items:
            print(f"      • {item}")
    
    print("\n❌ WHAT CURRENT SYSTEM DOES:")
    print("   • Ignores all buyer mentions → generates generic Microsoft/Salesforce research")
    print("   • Ignores valuation discussion → generates generic valuation methods")  
    print("   • Ignores management details → generates generic exec profiles")
    print("   • Ignores risk factors → generates generic investment risks")
    print("   • User's specific knowledge is completely lost!")

def propose_enhanced_extraction():
    """Propose enhanced conversation extraction"""
    
    print(f"\n🔧 PROPOSED SOLUTION: ENHANCED CONVERSATION EXTRACTION")
    print("=" * 65)
    
    enhanced_prompt_fields = """
    BASIC COMPANY INFO (existing):
    - company_name, business_description, industry, etc.
    
    INVESTMENT BANKING SPECIFIC (NEW):
    - strategic_buyers_mentioned: [list of strategic acquirers mentioned]
    - financial_buyers_mentioned: [list of PE/VC firms mentioned] 
    - potential_acquirers_mentioned: [any other buyers discussed]
    - valuation_estimates_mentioned: [multiples, ranges, estimates discussed]
    - transaction_comps_mentioned: [comparable transactions referenced]
    - management_team_details: [executive names, backgrounds, experience]
    - synergies_mentioned: [specific synergies or value-add discussed]
    - investment_thesis_points: [key investment reasons mentioned]
    - risk_factors_discussed: [specific risks or concerns raised]
    - exit_strategies_mentioned: [IPO, acquisition, or other exit discussions]
    - competitive_advantages_mentioned: [moats, differentiators discussed]
    - market_opportunity_details: [TAM, SAM, growth rates mentioned]
    """
    
    print("📝 ENHANCED EXTRACTION WOULD INCLUDE:")
    print(enhanced_prompt_fields)
    
    print("💪 BENEFITS:")
    print("   ✅ Captures user's domain expertise")
    print("   ✅ Uses specific buyer knowledge instead of generic research")
    print("   ✅ Preserves valuation discussions") 
    print("   ✅ Maintains management team insights")
    print("   ✅ Includes user's risk analysis")
    print("   ✅ Reduces need for generic LLM research")
    print("   ✅ Produces more accurate, personalized presentations")

if __name__ == "__main__":
    current, missing = analyze_conversation_extraction_gaps()
    simulate_conversation_with_buyers()
    propose_enhanced_extraction()
    
    print(f"\n🎯 SUMMARY:")
    print(f"   🚨 Critical Issue: Investment banking conversations not properly extracted")
    print(f"   📊 Current extraction: {len(current)} basic fields only")
    print(f"   ❌ Missing fields: {len(missing)} investment banking specific")
    print(f"   💡 Solution: Enhance conversation extraction prompt with IB fields")
    print(f"   🎁 Result: User expertise captured instead of generic research")