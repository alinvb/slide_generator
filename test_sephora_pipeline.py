#!/usr/bin/env python3
"""
Test Sephora pipeline to replicate user's issue
"""

import json
from bulletproof_json_generator_clean import generate_clean_bulletproof_json
from shared_functions import call_llm_api

def test_sephora_pipeline():
    """Test Sephora pipeline that was producing empty JSONs"""
    
    print("🧪 Testing Sephora pipeline to replicate empty JSON issue...")
    
    # Create realistic Sephora conversation
    sephora_messages = [
        {
            "role": "user", 
            "content": "I want to create an investment banking presentation for Sephora"
        },
        {
            "role": "assistant", 
            "content": "I'll help you create a comprehensive investment banking presentation for Sephora. Let me gather the key information about the company."
        },
        {
            "role": "user", 
            "content": """Sephora is the world's leading global prestige beauty retail brand, operating over 3,200 stores and iconic flagships in 35 markets. It offers a curated selection of more than 300 brands and its own Sephora Collection, spanning fragrance, make-up, haircare, skincare, and beauty tools. 

Founded in 1969 in Limoges, France, Sephora has been part of the LVMH Group since 1997. The company is recognized for its omnichannel network, digital innovation, and immersive customer experiences.

Key Financial Information:
- Annual Revenue: Approximately $17 billion globally (2024E)  
- EBITDA: Estimated $2.89 billion
- Strong growth trajectory with digital transformation

Sephora has disrupted the prestige beauty retail industry and champions inspiration and inclusion in beauty. The company operates in North America, Europe, Asia Pacific, and the Middle East."""
        }
    ]
    
    # Full slide list for comprehensive presentation
    required_slides = [
        "business_overview",
        "product_service_footprint", 
        "management_team",
        "historical_financial_performance",
        "growth_strategy_projections",
        "competitive_positioning", 
        "valuation_overview",
        "precedent_transactions",
        "strategic_buyers",
        "financial_buyers",
        "margin_cost_resilience", 
        "investor_considerations",
        "financial_summary",
        "transaction_overview",
        "sea_conglomerates",
        "investor_process_overview"
    ]
    
    def sephora_llm_call(messages):
        """LLM call function for Sephora test"""
        print(f"🤖 [SEPHORA] LLM call for {len(messages)} messages")
        
        # Simulate what happens in real app - no API key, use fallback
        try:
            response = call_llm_api(messages, timeout=180)
            print(f"✅ [SEPHORA] LLM response: {len(response)} chars")
            
            # Check if response contains JSON for gap-filling
            if any(keyword in response for keyword in ['strategic_buyers', 'financial_buyers', 'entities']):
                print(f"🔍 [SEPHORA] Gap-filling response detected")
                # Update company name in the response to Sephora
                if 'TechCorp Solutions' in response:
                    response = response.replace('TechCorp Solutions', 'Sephora')
                    print(f"🔄 [SEPHORA] Updated company name to Sephora in response")
            
            return response
        except Exception as e:
            print(f"❌ [SEPHORA] LLM call error: {e}")
            return f"Error: {e}"
    
    print(f"\n🚀 Starting Sephora bulletproof JSON generation...")
    
    try:
        # Generate comprehensive Sephora presentation data
        response, content_ir, render_plan = generate_clean_bulletproof_json(
            sephora_messages,
            required_slides, 
            sephora_llm_call
        )
        
        print(f"\n✅ Sephora generation completed!")
        print(f"📝 Response: {response[:200]}...")
        
        if isinstance(content_ir, dict):
            print(f"\n📊 Content IR Analysis:")
            print(f"  Total sections: {len(content_ir)}")
            
            # Check company name
            company_name = content_ir.get('entities', {}).get('company', {}).get('name', 'Unknown')
            print(f"  Company name: {company_name}")
            
            # Check for empty arrays (the original issue)
            empty_checks = {
                "management_team.left_column_profiles": content_ir.get('management_team', {}).get('left_column_profiles', []),
                "management_team.right_column_profiles": content_ir.get('management_team', {}).get('right_column_profiles', []),
                "strategic_buyers": content_ir.get('strategic_buyers', []),
                "financial_buyers": content_ir.get('financial_buyers', []),
                "competitive_analysis.assessment": content_ir.get('competitive_analysis', {}).get('assessment', []),
                "precedent_transactions": content_ir.get('precedent_transactions', []),
                "valuation_data": content_ir.get('valuation_data', []),
                "product_service_data.services": content_ir.get('product_service_data', {}).get('services', []),
                "investor_process_data.diligence_topics": content_ir.get('investor_process_data', {}).get('diligence_topics', [])
            }
            
            print(f"\n🔍 Empty Array Check (Original Issue):")
            has_empty = False
            for field, value in empty_checks.items():
                if isinstance(value, list) and len(value) == 0:
                    print(f"  ❌ {field}: EMPTY (0 items)")
                    has_empty = True
                else:
                    count = len(value) if isinstance(value, list) else "N/A"
                    print(f"  ✅ {field}: {count} items")
            
            if not has_empty:
                print(f"\n🎉 SUCCESS: No empty arrays found - Original issue RESOLVED!")
            else:
                print(f"\n❌ ISSUE PERSISTS: Some arrays still empty")
            
            # Create output similar to user's example for comparison
            print(f"\n📋 Sample Output (like user's example):")
            sample_output = {
                "entities": content_ir.get("entities", {}),
                "facts": content_ir.get("facts", {}),
                "management_team": {
                    "left_column_profiles": content_ir.get("management_team", {}).get("left_column_profiles", []),
                    "right_column_profiles": content_ir.get("management_team", {}).get("right_column_profiles", [])
                },
                "strategic_buyers": content_ir.get("strategic_buyers", [])[:1],  # Just first item
                "financial_buyers": content_ir.get("financial_buyers", [])[:1],   # Just first item
                "competitive_analysis": content_ir.get("competitive_analysis", {}),
                "precedent_transactions": content_ir.get("precedent_transactions", [])[:1]  # Just first item
            }
            
            print(json.dumps(sample_output, indent=2)[:1000] + "..." if len(json.dumps(sample_output, indent=2)) > 1000 else json.dumps(sample_output, indent=2))
            
        else:
            print(f"❌ Content IR is not a dictionary: {type(content_ir)}")
        
        return response, content_ir, render_plan
        
    except Exception as e:
        print(f"❌ Sephora test failed: {e}")
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}")
        return None, None, None

if __name__ == "__main__":
    test_sephora_pipeline()