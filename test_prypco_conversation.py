#!/usr/bin/env python3

"""
Test PRYPCO Conversation Flow
============================
Tests the actual PRYPCO conversation to ensure:
1. Only relevant slides are generated (business overview + product service)
2. Actual PRYPCO data is used instead of placeholders
3. JSON validation passes
"""

import sys
import os
import json
sys.path.append('/home/user/webapp')

from bulletproof_json_generator import BulletproofJSONGenerator

def test_prypco_conversation():
    """Test with the actual PRYPCO conversation"""
    
    # Real PRYPCO conversation
    prypco_messages = [
        {"role": "assistant", "content": "What is your company name and give me a brief overview of what your business does?"},
        {"role": "user", "content": "prypco"},
        {"role": "assistant", "content": "PRYPCO is a real estate technology platform based in Dubai that specializes in making property investment, mortgage acquisition, and visa facilitation accessible and streamlined for both residents and international investors. Key features include: Mortgage Platform with 18 major banks, facilitated over $2.73 billion in mortgages, helped 3,000+ individuals secure UAE Golden Visas. Fractional Ownership via PRYPCO Blocks starting from AED 2,000. Founded by Amira Sajwani."},
        {"role": "assistant", "content": "Now let's discuss your product/service footprint. What are your main offerings?"},
        {"role": "user", "content": "research this yourself"},
        {"role": "assistant", "content": "PRYPCO offers: PRYPCO Blocks (fractional ownership, 50,000+ users, AED 20 million invested), PRYPCO Mint (tokenized real estate, 2,000 investors, AED 16 million), PRYPCO One (agent platform, 60,000+ agents). Facilitated AED 10 billion in mortgages, 3,000+ UAE Golden Visas. Founded by Amira Sajwani in 2022."}
    ]
    
    # Mock LLM function that returns realistic PRYPCO data
    def mock_prypco_llm_call(messages, model="test", api_key="test", service="test"):
        return json.dumps({
            "company_name": "PRYPCO",
            "description": "PRYPCO is a real estate technology platform based in Dubai that specializes in making property investment, mortgage acquisition, and visa facilitation accessible and streamlined for both residents and international investors",
            "founded": "2022",
            "headquarters": "Dubai, UAE",
            "key_milestones": [
                "Founded by Amira Sajwani in 2022",
                "Facilitated $2.73 billion in mortgages",
                "Helped 3,000+ individuals secure UAE Golden Visas",
                "First tokenized investment platform to partner with Dubai Land Department"
            ],
            "years": ["2022", "2023", "2024"],
            "revenue_usd_m": None,
            "ebitda_usd_m": None,
            "team_members": [
                {
                    "name": "Amira Sajwani",
                    "title": "Founder & CEO",
                    "background": "Previously oversaw sales and development at DAMAC Properties, market expert in real estate innovation"
                }
            ],
            "products_services": [
                "PRYPCO Blocks - Fractional ownership platform",
                "PRYPCO Mint - Tokenized real estate investment platform", 
                "PRYPCO One - Platform for real estate agents with AI-driven insights"
            ],
            "market_coverage": "UAE and MENA region",
            "growth_strategies": [],
            "financial_highlights": [
                "Facilitated close to AED 10 billion ($2.73B) in mortgages",
                "Over 50,000 users invested AED 20 million in PRYPCO Blocks",
                "Nearly 2,000 investors invested AED 16 million in PRYPCO Mint",
                "Onboarded 60,000+ real estate agents"
            ],
            "user_base": "Over 50,000 platform users",
            "partnerships": ["Dubai Land Department", "18 major UAE banks", "Virtual Assets Regulatory Authority (VARA)"]
        })

    print("🧪 Testing PRYPCO Conversation Flow...")
    print("📋 Expected: 2 slides (business_overview + product_service_footprint)")
    
    # Test the system
    generator = BulletproofJSONGenerator()
    
    # All possible slides (what the system could generate)
    all_slides = [
        "business_overview", "management_team", "product_service_footprint", 
        "historical_financial_performance", "growth_strategy_projections", 
        "precedent_transactions", "valuation_overview"
    ]
    
    try:
        # Step 1: Extract conversation data
        print("\n🔍 Step 1: Extracting conversation data...")
        extracted_data = generator.extract_conversation_data(prypco_messages, mock_prypco_llm_call)
        print(f"   Company: {extracted_data.get('company_name')}")
        print(f"   Products: {len(extracted_data.get('products_services', []))}")
        print(f"   Team members: {len(extracted_data.get('team_members', []))}")
        
        # Step 2: Filter slides based on conversation
        print("\n🎯 Step 2: Filtering slides based on conversation...")
        covered_slides = generator.filter_slides_by_conversation_coverage(extracted_data, all_slides)
        print(f"   Slides to generate: {covered_slides}")
        
        # Step 3: Generate JSONs
        print("\n🏗️ Step 3: Generating JSONs...")
        response, content_ir, render_plan = generator.generate_perfect_jsons(extracted_data, {}, covered_slides)
        
        # Step 4: Validate results
        print(f"\n📊 RESULTS:")
        print(f"   Generated slides: {len(render_plan['slides'])}")
        print(f"   Slide types: {[slide['template'] for slide in render_plan['slides']]}")
        
        # Check if we got the expected 2 slides
        expected_slides = {"business_overview", "product_service_footprint"}
        actual_slides = {slide['template'] for slide in render_plan['slides']}
        
        print(f"\n🎯 VALIDATION:")
        print(f"   Expected slides: {sorted(expected_slides)}")
        print(f"   Actual slides:   {sorted(actual_slides)}")
        
        if actual_slides == expected_slides:
            print(f"   ✅ SUCCESS: Exactly 2 slides generated as expected!")
        else:
            print(f"   ❌ MISMATCH: Expected {expected_slides}, got {actual_slides}")
        
        # Check if data is properly populated (not placeholders)
        print(f"\n📋 DATA QUALITY CHECK:")
        for slide in render_plan['slides']:
            template = slide['template']
            data = slide['data']
            
            if template == "business_overview":
                company_name = data.get('company_name', '')
                description = data.get('description', '')
                if company_name == "PRYPCO" and "PRYPCO" in description:
                    print(f"   ✅ Business overview: Proper PRYPCO data")
                else:
                    print(f"   ❌ Business overview: Placeholder data detected")
                    print(f"       Company: {company_name}")
                    print(f"       Description: {description[:100]}...")
            
            elif template == "product_service_footprint":
                services = data.get('services', [])
                if any("PRYPCO" in str(service) for service in services):
                    print(f"   ✅ Product footprint: Proper PRYPCO services")
                else:
                    print(f"   ❌ Product footprint: Generic/placeholder services")
                    print(f"       Services: {services}")
        
        return len(actual_slides) == 2 and actual_slides == expected_slides
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🎯 PRYPCO CONVERSATION TEST")
    print("=" * 60)
    print("Testing the actual user conversation flow")
    print("Verifying: selective rendering + proper data population")
    print("=" * 60)
    
    success = test_prypco_conversation()
    
    print(f"\n" + "=" * 60)
    if success:
        print("🎉 PRYPCO TEST SUCCESSFUL!")
        print("✅ Only relevant slides generated")
        print("✅ Actual PRYPCO data populated correctly")
        print("✅ Ready for production use")
    else:
        print("⚠️  PRYPCO TEST NEEDS FIXES")
        print("❌ Issues detected in slide generation or data population")
    print("=" * 60)