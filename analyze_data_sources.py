#!/usr/bin/env python3
"""
Analyze how many fields are filled from conversation vs backup research
"""

import json
from bulletproof_json_generator_clean import generate_clean_bulletproof_json

def analyze_data_source_coverage():
    """Analyze what percentage of fields come from conversation vs LLM backup research"""
    
    print("📊 Analyzing data source coverage: Conversation vs Backup Research")
    print("=" * 70)
    
    # Define all the fields in a complete Content IR
    content_ir_structure = {
        "entities.company.name": "Company name",
        
        # Financial facts (often mentioned in conversations)
        "facts.years": "Financial years",
        "facts.revenue_usd_m": "Revenue figures",
        "facts.ebitda_usd_m": "EBITDA figures", 
        "facts.ebitda_margins": "EBITDA margin percentages",
        
        # Management team (rarely mentioned in detail)
        "management_team.left_column_profiles": "Left column executive profiles",
        "management_team.right_column_profiles": "Right column executive profiles",
        
        # Strategic analysis (mixed - company mentioned, buyers researched)
        "strategic_buyers": "Strategic buyer analysis",
        "financial_buyers": "Financial buyer analysis",
        
        # Competitive analysis (company positioning mentioned, competitors researched)
        "competitive_analysis.competitors": "Competitor list",
        "competitive_analysis.assessment": "Competitive assessment matrix",
        "competitive_analysis.barriers": "Barriers to entry",
        "competitive_analysis.advantages": "Competitive advantages",
        
        # Transactions (almost always researched)
        "precedent_transactions": "Precedent transaction analysis",
        
        # Valuation (always researched/calculated)
        "valuation_data": "Valuation methodologies",
        
        # Product/Service data (company description mentioned, details researched)  
        "product_service_data.services": "Service offerings",
        "product_service_data.coverage_table": "Market coverage table",
        "product_service_data.metrics": "Key business metrics",
        
        # Business overview (company description mentioned, details expanded)
        "business_overview_data.description": "Business description",
        "business_overview_data.timeline": "Company timeline",
        "business_overview_data.highlights": "Key achievements",
        "business_overview_data.services": "Service list",
        "business_overview_data.positioning_desc": "Market positioning",
        
        # Growth strategy (rarely mentioned in detail)
        "growth_strategy_data.growth_strategy.strategies": "Growth strategies",
        "growth_strategy_data.financial_projections": "Financial projections",
        
        # Investor process (always researched)
        "investor_process_data.diligence_topics": "Due diligence topics",
        "investor_process_data.synergy_opportunities": "Synergy opportunities", 
        "investor_process_data.risk_factors": "Risk factors",
        "investor_process_data.mitigants": "Risk mitigants",
        "investor_process_data.timeline": "Process timeline",
        
        # Cost/margin analysis (rarely mentioned in detail)
        "margin_cost_data.chart_data": "Margin trend data",
        "margin_cost_data.cost_management": "Cost management initiatives",
        "margin_cost_data.risk_mitigation": "Margin risk mitigation",
        
        # Regional analysis (almost always researched)
        "sea_conglomerates": "SEA conglomerate analysis",
        
        # Investor considerations (mixed)
        "investor_considerations.considerations": "Investment considerations",
        "investor_considerations.mitigants": "Investment risk mitigants"
    }
    
    # Categorize by typical data source
    conversation_likely = [
        "entities.company.name",
        "facts.revenue_usd_m", 
        "facts.ebitda_usd_m",
        "business_overview_data.description",
        "product_service_data.services",  # Basic service list
        "business_overview_data.services"
    ]
    
    mixed_sources = [
        "facts.years",  # Years mentioned, but need to align with revenue data
        "competitive_analysis.competitors",  # Some mentioned, others researched
        "business_overview_data.highlights",  # Some mentioned, others inferred
        "business_overview_data.positioning_desc",  # Basic mentioned, details researched
        "investor_considerations.considerations"  # Some obvious, others researched
    ]
    
    research_required = [
        "facts.ebitda_margins",  # Calculated from other data
        "management_team.left_column_profiles",
        "management_team.right_column_profiles", 
        "strategic_buyers",
        "financial_buyers",
        "competitive_analysis.assessment",
        "competitive_analysis.barriers",
        "competitive_analysis.advantages",
        "precedent_transactions",
        "valuation_data",
        "product_service_data.coverage_table",
        "product_service_data.metrics",
        "business_overview_data.timeline",
        "growth_strategy_data.growth_strategy.strategies",
        "growth_strategy_data.financial_projections",
        "investor_process_data.diligence_topics",
        "investor_process_data.synergy_opportunities",
        "investor_process_data.risk_factors", 
        "investor_process_data.mitigants",
        "investor_process_data.timeline",
        "margin_cost_data.chart_data",
        "margin_cost_data.cost_management",
        "margin_cost_data.risk_mitigation",
        "sea_conglomerates",
        "investor_considerations.mitigants"
    ]
    
    total_fields = len(content_ir_structure)
    conversation_fields = len(conversation_likely)
    mixed_fields = len(mixed_sources)
    research_fields = len(research_required)
    
    print(f"📋 TOTAL FIELDS IN INVESTMENT BANKING PRESENTATION: {total_fields}")
    print()
    
    print(f"🗣️  CONVERSATION-SOURCED FIELDS: {conversation_fields} ({conversation_fields/total_fields*100:.1f}%)")
    print("   Fields typically extracted from user conversation:")
    for field in conversation_likely:
        print(f"   • {field}: {content_ir_structure[field]}")
    print()
    
    print(f"🔄 MIXED-SOURCE FIELDS: {mixed_fields} ({mixed_fields/total_fields*100:.1f}%)")  
    print("   Fields partially from conversation, enhanced with research:")
    for field in mixed_sources:
        print(f"   • {field}: {content_ir_structure[field]}")
    print()
    
    print(f"🔬 RESEARCH-REQUIRED FIELDS: {research_fields} ({research_fields/total_fields*100:.1f}%)")
    print("   Fields that require LLM/AI research to generate:")
    for field in research_required[:8]:  # Show first 8 to save space
        print(f"   • {field}: {content_ir_structure[field]}")
    print(f"   • ... and {research_fields-8} more fields")
    print()
    
    print("📊 DATA SOURCE BREAKDOWN:")
    print(f"   🗣️  Pure Conversation: {conversation_fields/total_fields*100:5.1f}%")
    print(f"   🔄 Mixed Sources:     {mixed_fields/total_fields*100:5.1f}%") 
    print(f"   🔬 Research Required: {research_fields/total_fields*100:5.1f}%")
    print()
    
    print("🎯 KEY INSIGHTS:")
    print(f"   • Only ~{conversation_fields/total_fields*100:.0f}% of fields can be filled from conversation alone")
    print(f"   • ~{research_fields/total_fields*100:.0f}% of fields require AI research/analysis")
    print(f"   • Investment banking presentations are research-intensive documents")
    print(f"   • LLM gap-filling is essential for professional-quality output")
    print()
    
    return {
        "total": total_fields,
        "conversation": conversation_fields,
        "mixed": mixed_fields, 
        "research": research_fields,
        "conversation_pct": conversation_fields/total_fields*100,
        "research_pct": research_fields/total_fields*100
    }

def analyze_typical_user_conversations():
    """Analyze what users typically provide vs what needs research"""
    
    print("👤 TYPICAL USER CONVERSATION ANALYSIS")
    print("=" * 50)
    
    typical_scenarios = {
        "Quick Company Mention": {
            "user_provides": ["Company name", "Basic industry"],
            "needs_research": "Everything else (90%+ of fields)",
            "example": "User says: 'Analyze Tesla for investment banking'"
        },
        
        "Basic Business Description": {
            "user_provides": ["Company name", "Business description", "Industry", "Basic financials"],
            "needs_research": "Management, competitors, transactions, valuation (80%+ of fields)", 
            "example": "User provides: Company overview paragraph with revenue"
        },
        
        "Detailed Company Brief": {
            "user_provides": ["Company details", "Some financials", "Key executives", "Market info"],
            "needs_research": "Analysis, research, transactions, detailed profiles (60%+ of fields)",
            "example": "User provides: Comprehensive company brief"
        },
        
        "Expert Domain Knowledge": {
            "user_provides": ["Deep company knowledge", "Industry insights", "Financial details"],
            "needs_research": "Formatted analysis, transaction research, buyer analysis (40%+ of fields)",
            "example": "Industry expert provides detailed company information"
        }
    }
    
    for scenario, details in typical_scenarios.items():
        print(f"📝 {scenario.upper()}:")
        print(f"   User Provides: {', '.join(details['user_provides'])}")
        print(f"   Needs Research: {details['needs_research']}")
        print(f"   Example: {details['example']}")
        print()
    
    print("💡 CONCLUSION:")
    print("   • Even detailed conversations only cover 20-40% of required fields")
    print("   • LLM research is critical for professional investment banking output")
    print("   • Fallback data ensures no empty fields when research fails")
    print("   • Real API calls provide much richer, more accurate research")

if __name__ == "__main__":
    stats = analyze_data_source_coverage()
    print()
    analyze_typical_user_conversations()
    
    print()
    print("🎊 SUMMARY:")
    print(f"   📊 Total fields: {stats['total']}")
    print(f"   🗣️  Conversation-sourced: {stats['conversation']} ({stats['conversation_pct']:.1f}%)")
    print(f"   🔬 Research-required: {stats['research']} ({stats['research_pct']:.1f}%)")
    print(f"   💪 System handles both seamlessly with bulletproof fallbacks!")