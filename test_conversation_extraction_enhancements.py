#!/usr/bin/env python3
"""
Test the enhanced conversation extraction system for Investment Banking Research App
"""

import json
from bulletproof_json_generator_clean import CleanBulletproofJSONGenerator

def test_conversation_extraction():
    """Test the enhanced conversation extraction with mock conversation data"""
    
    # Mock conversation data with rich investment banking details
    mock_messages = [
        {
            "role": "user",
            "content": """
            Let's discuss the Netflix acquisition opportunity. Netflix is a leading streaming entertainment company 
            with $31.6B in revenue and strong growth trajectory. 
            
            For valuation, I see three main approaches:
            1. DCF Analysis suggests enterprise value of $85-120M with 12% WACC and 3% terminal growth
            2. Trading Multiples show EV/Revenue of 8.5x and EV/EBITDA of 15.2x for comparable streaming companies
            3. Precedent Transactions in the streaming space show deals at 10-12x revenue multiples
            
            For precedent transactions, we have:
            - Disney acquired Hulu valued at $27.5B with 11.2x revenue multiple in 2023
            - Amazon acquired MGM for $8.45B at 9.8x revenue multiple in 2021 
            - Apple acquired Shazam for $400M strategic acquisition in 2018
            
            Strategic buyers include major tech companies like Apple, Amazon, Google for content distribution synergies.
            Regional opportunities exist with Asian conglomerates like Tencent and Alibaba for market expansion.
            
            Key risks include content cost inflation and competitive margin pressure from new streaming entrants.
            """
        }
    ]
    
    # Mock LLM API function
    def mock_llm_api(messages):
        return json.dumps({
            "company_name": "Netflix, Inc.",
            "industry": "Streaming Entertainment",
            "business_description_detailed": "Leading global streaming entertainment service",
            "annual_revenue_usd_m": 31600,
            
            # Enhanced extraction fields
            "precedent_transactions_detailed": [
                {
                    "target": "Hulu", 
                    "acquirer": "Disney", 
                    "date": "2023", 
                    "enterprise_value": "$27.5B", 
                    "revenue": "$2.45B", 
                    "ev_revenue_multiple": "11.2x", 
                    "strategic_rationale": "Content distribution and streaming portfolio expansion"
                },
                {
                    "target": "MGM", 
                    "acquirer": "Amazon", 
                    "date": "2021", 
                    "enterprise_value": "$8.45B", 
                    "revenue": "$862M", 
                    "ev_revenue_multiple": "9.8x", 
                    "strategic_rationale": "Content library expansion for Prime Video"
                }
            ],
            
            "dcf_valuation_details": {
                "enterprise_value": "$85-120M", 
                "wacc": "12%", 
                "terminal_growth": "3%", 
                "commentary": "DCF analysis assuming strong growth trajectory and improving margins"
            },
            
            "trading_multiples_details": {
                "enterprise_value": "$95-115M",
                "ev_revenue_multiple": "8.5x",
                "ev_ebitda_multiple": "15.2x", 
                "commentary": "Based on comparable streaming companies trading multiples"
            },
            
            "precedent_transaction_valuation_details": {
                "enterprise_value": "$100-130M",
                "ev_revenue_multiple": "10-12x",
                "commentary": "Precedent streaming M&A transactions indicate premium valuations"
            },
            
            "strategic_buyers_mentioned": ["Apple", "Amazon", "Google"],
            "regional_strategic_buyers": ["Tencent", "Alibaba"],
            "geographic_regions_mentioned": ["Asia", "North America", "Global"],
            "regional_market_context": ["Asian market expansion", "Global content distribution"],
            
            "risk_factors_discussed": ["Content cost inflation", "Competitive margin pressure"],
            "challenges_mentioned": ["New streaming entrants", "Rising content costs"]
        })
    
    # Test the enhanced extraction
    generator = CleanBulletproofJSONGenerator()
    
    print("🔧 Testing enhanced conversation extraction...")
    result = generator.extract_conversation_data(mock_messages, mock_llm_api)
    
    print(f"\n✅ Extraction completed with {len(result)} fields")
    
    # Check key enhancements
    print("\n🔍 Testing Enhanced Fields:")
    
    # 1. Precedent transactions from conversation
    precedent_transactions = result.get('precedent_transactions', [])
    print(f"• Precedent Transactions: {len(precedent_transactions)} found")
    if precedent_transactions:
        print(f"  - First transaction: {precedent_transactions[0].get('target', 'N/A')} acquired by {precedent_transactions[0].get('acquirer', 'N/A')}")
    
    # 2. Valuation methodologies from conversation
    valuation_data = result.get('valuation_data', [])
    print(f"• Valuation Methodologies: {len(valuation_data)} found")
    for val in valuation_data:
        print(f"  - {val.get('methodology', 'Unknown')}: {val.get('enterprise_value', 'N/A')}")
    
    # 3. Regional conglomerates from conversation
    regional_conglomerates = result.get('sea_conglomerates', [])
    print(f"• Regional Conglomerates: {len(regional_conglomerates)} found")
    for regional in regional_conglomerates:
        print(f"  - {regional.get('buyer_name', 'Unknown')}")
    
    # 4. Margin cost resilience from conversation
    margin_data = result.get('margin_cost_data', {})
    print(f"• Margin Cost Data: {'Found' if margin_data else 'Not found'}")
    if margin_data:
        print(f"  - Banker view: {margin_data.get('banker_view', 'N/A')[:50]}...")
    
    print(f"\n📊 All extracted fields:")
    print(f"Keys: {list(result.keys())}")
    
    # Show some key detailed fields
    for key in ['precedent_transactions_detailed', 'dcf_valuation_details', 'trading_multiples_details', 'regional_strategic_buyers']:
        if key in result:
            print(f"\n{key}: {result[key]}")
    
    print(f"\n📊 Sample valuation data structure:")
    if valuation_data:
        print(json.dumps(valuation_data[0], indent=2))
    
    return result

if __name__ == "__main__":
    test_conversation_extraction()