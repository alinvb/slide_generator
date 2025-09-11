#!/usr/bin/env python3
"""
Test Empty Arrays Fix - Verify that bulletproof generator now returns populated data
"""

import json
from bulletproof_json_generator_clean import generate_clean_bulletproof_json

def test_netflix_conversation():
    """Test Netflix conversation with fixed API function that uses fallback"""
    print("🧪 Testing Netflix conversation with fixed API fallback...")
    
    # Netflix conversation messages
    netflix_messages = [
        {"role": "user", "content": "I want to analyze Netflix as an investment opportunity"},
        {"role": "assistant", "content": "I'll help you analyze Netflix. Netflix is a leading streaming entertainment company founded in 1997, headquartered in Los Gatos, California. The company operates in over 190 countries with approximately 260 million subscribers as of 2024."},
        {"role": "user", "content": "What about their financial performance and management team?"},
        {"role": "assistant", "content": "Netflix has strong financial performance with around $31.6B in annual revenue and $9.4B EBITDA in 2023. Key executives include Co-CEO Ted Sarandos (Chief Content Officer) and Co-CEO Greg Peters, along with CFO Spencer Neumann. They've invested heavily in original content, spending over $15B annually on content production."}
    ]
    
    # Required slides for full investment banking analysis
    required_slides = [
        "business_overview",
        "investor_considerations", 
        "product_service_footprint",
        "historical_financial_performance",
        "management_team",
        "competitive_positioning",
        "precedent_transactions",
        "valuation_overview",
        "strategic_buyers",
        "financial_buyers",
        "investor_process_overview",
        "margin_cost_resilience",
        "growth_strategy_projections",
        "sea_conglomerates"
    ]
    
    # Mock API function that uses fallback (simulating no API key scenario)
    def mock_api_call_with_fallback(messages):
        """Mock API call that always uses fallback (like when no API key)"""
        from shared_functions import generate_fallback_response
        return generate_fallback_response(messages)
    
    # Test the bulletproof generator
    try:
        print(f"🔍 Testing with {len(netflix_messages)} Netflix messages and {len(required_slides)} slides...")
        
        response, content_ir, render_plan = generate_clean_bulletproof_json(
            netflix_messages, 
            required_slides,
            mock_api_call_with_fallback
        )
        
        print(f"✅ Bulletproof generation completed!")
        print(f"📊 Content IR keys: {len(content_ir) if content_ir else 0}")
        
        if content_ir:
            # Check key investment banking fields for populated data
            strategic_buyers = content_ir.get('strategic_buyers', [])
            financial_buyers = content_ir.get('financial_buyers', []) 
            management_team_data = content_ir.get('management_team', {})
            left_profiles = management_team_data.get('left_column_profiles', [])
            right_profiles = management_team_data.get('right_column_profiles', [])
            total_management = len(left_profiles) + len(right_profiles)
            precedent_transactions = content_ir.get('precedent_transactions', [])
            facts = content_ir.get('facts', {})
            entities = content_ir.get('entities', {})
            
            print(f"\n📈 Key Fields Analysis:")
            print(f"   Strategic Buyers: {len(strategic_buyers)} items")
            print(f"   Financial Buyers: {len(financial_buyers)} items") 
            print(f"   Management Profiles: {total_management} items (L:{len(left_profiles)}+R:{len(right_profiles)})")
            print(f"   Precedent Transactions: {len(precedent_transactions)} items")
            print(f"   Facts: {len(facts)} keys")
            print(f"   Entities: {len(entities)} keys")
            
            # Detailed analysis
            if len(strategic_buyers) > 0:
                print(f"\n✅ STRATEGIC BUYERS POPULATED:")
                for i, buyer in enumerate(strategic_buyers[:2]):
                    buyer_name = buyer.get('buyer_name', 'Unknown')
                    print(f"   {i+1}. {buyer_name}")
            else:
                print(f"\n❌ STRATEGIC BUYERS EMPTY!")
                
            if len(financial_buyers) > 0:
                print(f"\n✅ FINANCIAL BUYERS POPULATED:")
                for i, buyer in enumerate(financial_buyers[:2]):
                    buyer_name = buyer.get('buyer_name', 'Unknown')
                    print(f"   {i+1}. {buyer_name}")
            else:
                print(f"\n❌ FINANCIAL BUYERS EMPTY!")
                
            # Check if the fix worked
            total_populated_fields = len(strategic_buyers) + len(financial_buyers) + total_management + len(precedent_transactions)
            
            if total_populated_fields > 10:
                print(f"\n🎉 SUCCESS: Fix works! Total populated items: {total_populated_fields}")
                print(f"✅ Empty arrays issue resolved - bulletproof generator returns populated data")
                return True
            else:
                print(f"\n❌ ISSUE PERSISTS: Still getting empty/minimal data - {total_populated_fields} items")
                return False
        else:
            print(f"❌ No content_ir returned")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Empty Arrays Fix...")
    print("=" * 60)
    
    success = test_netflix_conversation()
    
    print("\n" + "=" * 60)
    if success:
        print("🎯 DIAGNOSIS: Fix successful - populated data arrays returned")
        print("✅ Users should now see strategic buyers, financial buyers, management team, etc.")
    else:
        print("❌ DIAGNOSIS: Fix unsuccessful - arrays still empty or minimal")
        print("🔍 Further debugging needed")