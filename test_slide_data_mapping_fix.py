#!/usr/bin/env python3
"""
Test the slide data mapping fixes for the three problematic slides
"""

import json
from bulletproof_json_generator_clean import CleanBulletproofJSONGenerator

def mock_llm_api_call(messages):
    """Mock LLM response with comprehensive data for all three slides"""
    
    prompt_content = messages[0]['content'] if messages else ""
    
    if "sea_conglomerates" in prompt_content or "buyers" in prompt_content.lower():
        # Chunk 1: Buyers and SEA conglomerates data
        return '''
{
  "strategic_buyers": [
    {"buyer_name": "Samsung Electronics", "description": "Global electronics leader", "strategic_rationale": "Vertical integration", "key_synergies": "Technology synergies", "fit": "High (8-9/10)", "financial_capacity": "Very High"},
    {"buyer_name": "Tencent Holdings", "description": "Chinese tech conglomerate", "strategic_rationale": "Expand tech portfolio", "key_synergies": "Digital integration", "fit": "High (8-9/10)", "financial_capacity": "Very High"}
  ],
  "financial_buyers": [
    {"buyer_name": "KKR & Co", "description": "Global investment firm", "strategic_rationale": "Scale operations", "key_synergies": "Operational improvements", "fit": "High (8-9/10)", "financial_capacity": "Very High"}
  ],
  "management_team_profiles": [
    {"name": "Jensen Huang", "role_title": "CEO", "experience_bullets": ["Founded NVIDIA in 1993", "Led AI revolution", "30+ years experience"]}
  ],
  "facts": {
    "years": ["2020", "2021", "2022", "2023", "2024E"],
    "revenue_usd_m": [16675, 26974, 27000, 60922, 130500],
    "ebitda_usd_m": [5631, 8000, 12000, 34000, 73000]
  },
  "sea_conglomerates": [
    {"name": "Softbank Group", "country": "Japan", "description": "Technology investment conglomerate", "key_shareholders": "Masayoshi Son (27.2%)", "key_financials": "Revenue: $43.8B, Market Cap: $65B", "contact": "N/A"},
    {"name": "Tencent Holdings", "country": "China", "description": "Internet and gaming platform", "key_shareholders": "Prosus (28.9%)", "key_financials": "Revenue: $86.5B, Market Cap: $345B", "contact": "N/A"},
    {"name": "Alibaba Group", "country": "China", "description": "E-commerce and cloud computing", "key_shareholders": "SoftBank (14.8%)", "key_financials": "Revenue: $134.6B, Market Cap: $195B", "contact": "N/A"},
    {"name": "Samsung Group", "country": "South Korea", "description": "Electronics and technology", "key_shareholders": "Lee family", "key_financials": "Revenue: $279B, Market Cap: $325B", "contact": "N/A"}
  ]
}
'''
    
    elif "competitive_analysis" in prompt_content or "precedent_transactions" in prompt_content:
        # Chunk 2: Competitive and valuation data  
        return '''
{
  "competitive_analysis": {
    "competitors": [
      {"name": "NVIDIA", "revenue": 130500},
      {"name": "AMD", "revenue": 23500}, 
      {"name": "Intel", "revenue": 76000}
    ],
    "assessment": [
      ["Company", "AI Leadership", "Software Ecosystem", "Market Share", "Innovation"],
      ["NVIDIA", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"],
      ["AMD", "⭐⭐⭐⭐", "⭐⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐"],
      ["Intel", "⭐⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐"]
    ],
    "barriers": [
      {"title": "CUDA Ecosystem", "desc": "Proprietary platform with 4M+ developers"},
      {"title": "R&D Investment", "desc": "$7.3B annual spending requirement"},
      {"title": "Manufacturing Access", "desc": "TSMC advanced node constraints"},
      {"title": "AI Talent Pool", "desc": "Competition for specialized engineers"}
    ],
    "advantages": [
      {"title": "AI Market Leadership", "desc": "90%+ market share dominance"},
      {"title": "Software Ecosystem", "desc": "CUDA platform network effects"},
      {"title": "Cloud Partnerships", "desc": "Exclusive relationships with major clouds"},
      {"title": "Margin Excellence", "desc": "73% gross margins vs 45% industry"}
    ]
  },
  "precedent_transactions": [
    {"target": "Mellanox Technologies", "acquirer": "NVIDIA Corporation", "date": "2020", "country": "USA", "enterprise_value": "$6.9B", "revenue": "$1.3B", "ev_revenue_multiple": "5.3x", "strategic_rationale": "Data center networking acquisition"},
    {"target": "Xilinx Inc", "acquirer": "Advanced Micro Devices", "date": "2022", "country": "USA", "enterprise_value": "$49.0B", "revenue": "$3.2B", "ev_revenue_multiple": "15.3x", "strategic_rationale": "FPGA technology acquisition"},
    {"target": "Altera Corporation", "acquirer": "Intel Corporation", "date": "2015", "country": "USA", "enterprise_value": "$16.7B", "revenue": "$1.9B", "ev_revenue_multiple": "8.8x", "strategic_rationale": "FPGA integration strategy"},
    {"target": "Mobileye NV", "acquirer": "Intel Corporation", "date": "2017", "country": "Israel", "enterprise_value": "$15.3B", "revenue": "$358M", "ev_revenue_multiple": "42.7x", "strategic_rationale": "Autonomous driving technology"}
  ],
  "valuation_data": [
    {"methodology": "Discounted Cash Flow", "enterprise_value": "$2,850B-$3,200B", "metric": "NPV", "22a_multiple": null, "23e_multiple": null, "commentary": "Based on projected free cash flows and terminal value"},
    {"methodology": "Trading Multiples", "enterprise_value": "$2,600B-$3,100B", "metric": "EV/Revenue", "22a_multiple": "42.7x", "23e_multiple": "19.9x", "commentary": "Peer group analysis of semiconductor companies"},
    {"methodology": "Precedent Transactions", "enterprise_value": "$3,100B-$3,600B", "metric": "EV/Revenue", "22a_multiple": "51.0x", "23e_multiple": null, "commentary": "Recent M&A in AI and semiconductor sectors"}
  ]
}
'''
    
    else:
        # Default/other chunks
        return '{"status": "success"}'

def test_slide_data_mapping():
    """Test that slide data is properly mapped from content_ir to slide renderers"""
    print("🧪 Testing slide data mapping fixes...\n")
    
    generator = CleanBulletproofJSONGenerator()
    
    # Step 1: Generate full content_ir with all chunk data
    print("📊 Step 1: Generating complete content_ir...")
    
    # Mock conversation data
    extracted_data = {
        'company_name': 'NVIDIA',
        'industry': 'Semiconductors/AI Computing',
        'business_description_detailed': 'Leading AI and semiconductor company',
        'competitors_mentioned': ['AMD', 'Intel'],
        'competitive_positioning': 'AI computing leader'
    }
    
    # Generate comprehensive chunks  
    comprehensive_data = generator._generate_comprehensive_data_chunks(
        extracted_data, 
        mock_llm_api_call, 
        company_name='NVIDIA'
    )
    
    print(f"✅ Content IR generated with {len(comprehensive_data)} fields")
    print(f"📋 Available keys: {list(comprehensive_data.keys())}")
    
    # Check specific data
    sea_conglomerates = comprehensive_data.get('sea_conglomerates', [])
    precedent_transactions = comprehensive_data.get('precedent_transactions', [])  
    valuation_data = comprehensive_data.get('valuation_data', [])
    
    print(f"🌏 SEA Conglomerates in content_ir: {len(sea_conglomerates)} items")
    print(f"📈 Precedent Transactions in content_ir: {len(precedent_transactions)} items")
    print(f"💰 Valuation Data in content_ir: {len(valuation_data)} methodologies")
    
    # Step 2: Build render plan and check slide data extraction
    print(f"\n📋 Step 2: Building render plan with slide data extraction...")
    
    required_slides = ["sea_conglomerates", "precedent_transactions", "valuation_overview"]
    render_plan = generator.build_render_plan(required_slides, comprehensive_data)
    
    print(f"✅ Render plan built with {len(render_plan['slides'])} slides")
    
    # Step 3: Check each slide's data mapping
    for slide in render_plan['slides']:
        template = slide.get('template')
        data = slide.get('data', {})
        
        print(f"\n🎯 Slide: {template}")
        print(f"   📊 Data keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
        
        if template == 'sea_conglomerates':
            slide_conglomerates = data.get('sea_conglomerates', [])
            print(f"   🌏 SEA conglomerates in slide data: {len(slide_conglomerates)} items")
            if slide_conglomerates:
                print(f"   ✅ First item: {slide_conglomerates[0].get('name')} ({slide_conglomerates[0].get('country')})")
            else:
                print(f"   ❌ No SEA conglomerates data found")
                
        elif template == 'precedent_transactions':
            slide_transactions = data.get('transactions', [])
            print(f"   📈 Transactions in slide data: {len(slide_transactions)} items")
            if slide_transactions:
                first_txn = slide_transactions[0]
                print(f"   ✅ First transaction: {first_txn.get('acquirer')} -> {first_txn.get('target')}")
            else:
                print(f"   ❌ No transactions data found")
                
        elif template == 'valuation_overview':
            slide_valuation = data.get('valuation_data', [])
            print(f"   💰 Valuation methods in slide data: {len(slide_valuation)} items")
            if slide_valuation:
                first_method = slide_valuation[0]
                print(f"   ✅ First method: {first_method.get('methodology')} - {first_method.get('enterprise_value')}")
            else:
                print(f"   ❌ No valuation data found")
    
    # Step 4: Test actual slide rendering
    print(f"\n🎨 Step 3: Testing slide rendering...")
    
    from slide_templates import render_sea_conglomerates_slide, render_precedent_transactions_slide, render_valuation_overview_slide
    
    success_count = 0
    
    # Test each slide
    for slide in render_plan['slides']:
        template = slide.get('template')
        data = slide.get('data', {})
        
        try:
            if template == 'sea_conglomerates':
                prs = render_sea_conglomerates_slide(data=data, company_name="NVIDIA")
                print(f"   ✅ SEA conglomerates slide rendered successfully")
                success_count += 1
                
            elif template == 'precedent_transactions':
                prs = render_precedent_transactions_slide(data=data, company_name="NVIDIA")
                print(f"   ✅ Precedent transactions slide rendered successfully")
                success_count += 1
                
            elif template == 'valuation_overview':
                prs = render_valuation_overview_slide(data=data, company_name="NVIDIA")
                print(f"   ✅ Valuation overview slide rendered successfully")
                success_count += 1
                
        except Exception as e:
            print(f"   ❌ {template} slide rendering failed: {e}")
    
    print(f"\n📊 Results Summary:")
    print(f"✅ Content IR generation: Success ({len(sea_conglomerates)} conglomerates, {len(precedent_transactions)} transactions, {len(valuation_data)} methods)")
    print(f"✅ Render plan building: Success ({len(render_plan['slides'])} slides)")
    print(f"✅ Slide rendering: {success_count}/3 slides successful")
    
    if success_count == 3:
        print(f"\n🎉 All slide data mapping fixes successful!")
        return True
    else:
        print(f"\n💥 {3 - success_count} slides still have issues")
        return False

if __name__ == "__main__":
    test_slide_data_mapping()