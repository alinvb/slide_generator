#!/usr/bin/env python3
"""
Test the data generation and slide rendering for the problematic slides:
1. SEA conglomerates slide 
2. Precedent transactions slide
3. Valuation overview slide
"""

import json
from bulletproof_json_generator_clean import CleanBulletproofJSONGenerator

def mock_llm_api_call(messages):
    """Mock LLM response with comprehensive data"""
    
    # Determine what type of request this is based on content
    prompt_content = messages[0]['content'] if messages else ""
    
    if "sea_conglomerates" in prompt_content or "buyers" in prompt_content.lower():
        # Chunk 1: Buyers and SEA conglomerates data
        return '''
{
  "strategic_buyers": [
    {"buyer_name": "Samsung Electronics", "description": "Global electronics and semiconductor leader", "strategic_rationale": "Vertical integration of supply chain capabilities", "key_synergies": "Technology and manufacturing synergies", "fit": "High (8-9/10)", "financial_capacity": "Very High"},
    {"buyer_name": "Tencent Holdings", "description": "Chinese technology and gaming conglomerate", "strategic_rationale": "Expand technology portfolio and cloud services", "key_synergies": "Digital platform integration", "fit": "High (8-9/10)", "financial_capacity": "Very High"}
  ],
  "financial_buyers": [
    {"buyer_name": "KKR & Co", "description": "Global investment firm focused on growth capital", "strategic_rationale": "Scale technology operations globally", "key_synergies": "Operational improvements and market expansion", "fit": "High (8-9/10)", "financial_capacity": "Very High"},
    {"buyer_name": "Blackstone Group", "description": "Private equity leader in technology investments", "strategic_rationale": "Technology portfolio expansion", "key_synergies": "Platform optimization and growth acceleration", "fit": "High (7-8/10)", "financial_capacity": "High"}
  ],
  "management_team_profiles": [
    {"name": "Jensen Huang", "role_title": "CEO", "experience_bullets": ["Founded NVIDIA in 1993", "Led company through AI revolution", "30+ years semiconductor experience", "Pioneer in GPU computing", "Stanford University engineering background"]}
  ],
  "facts": {
    "years": ["2020", "2021", "2022", "2023", "2024E"],
    "revenue_usd_m": [16675, 26974, 27000, 60922, 60900],
    "ebitda_usd_m": [5631, 8000, 12000, 34000, 73000],
    "ebitda_margins": [33.8, 29.6, 44.4, 55.8, 55.9]
  },
  "sea_conglomerates": [
    {"name": "Softbank Group", "country": "Japan", "description": "Technology investment and telecommunications conglomerate", "key_shareholders": "Masayoshi Son (27.2%), Public shareholders", "key_financials": "Revenue: $43.8B, Market Cap: $65B", "contact": "N/A"},
    {"name": "Tencent Holdings", "country": "China", "description": "Internet services, gaming, and social media platform", "key_shareholders": "Prosus (28.9%), Public shareholders", "key_financials": "Revenue: $86.5B, Market Cap: $345B", "contact": "N/A"},
    {"name": "Alibaba Group", "country": "China", "description": "E-commerce, cloud computing, and digital services", "key_shareholders": "SoftBank (14.8%), Altaba Inc", "key_financials": "Revenue: $134.6B, Market Cap: $195B", "contact": "N/A"},
    {"name": "Samsung Group", "country": "South Korea", "description": "Electronics manufacturing and technology services", "key_shareholders": "Lee family, Public shareholders", "key_financials": "Revenue: $279B, Market Cap: $325B", "contact": "N/A"}
  ]
}
'''
    
    elif "competitive_analysis" in prompt_content or "precedent_transactions" in prompt_content:
        # Chunk 2: Competitive and valuation data  
        return '''
{
  "competitive_analysis": {
    "competitors": [
      {"name": "NVIDIA", "revenue": 60900},
      {"name": "AMD", "revenue": 23500}, 
      {"name": "Intel", "revenue": 76000},
      {"name": "Qualcomm", "revenue": 44200}
    ],
    "assessment": [
      ["Company", "AI Computing Leadership", "Software Ecosystem Strength", "Data Center Market Share", "Innovation Pipeline"],
      ["NVIDIA", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"],
      ["AMD", "⭐⭐⭐⭐", "⭐⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐"],
      ["Intel", "⭐⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐"],
      ["Qualcomm", "⭐⭐⭐", "⭐⭐", "⭐⭐", "⭐⭐⭐⭐"]
    ],
    "barriers": [
      {"title": "CUDA Ecosystem Lock-in", "desc": "Proprietary software platform with 4M+ developers creates significant switching costs"},
      {"title": "R&D Investment Scale", "desc": "$7.3B annual R&D spending requirement for competitive AI chip development"},
      {"title": "Advanced Manufacturing Access", "desc": "TSMC leading-edge node capacity constraints and multi-billion wafer commitments"},
      {"title": "AI Talent Acquisition", "desc": "Competition for specialized AI/GPU engineers with 25+ years parallel computing expertise"}
    ],
    "advantages": [
      {"title": "AI Market Leadership", "desc": "90%+ market share in AI training and inference with technological superiority"},
      {"title": "CUDA Software Moat", "desc": "Extensive developer ecosystem with 3.5M+ developers creates network effects"},
      {"title": "Cloud Partnership Strategy", "desc": "Exclusive relationships with AWS, Azure, GCP for AI infrastructure deployment"},
      {"title": "Gross Margin Excellence", "desc": "73% gross margins vs industry average 45% enables continued R&D reinvestment"}
    ]
  },
  "precedent_transactions": [
    {"target": "Mellanox Technologies", "acquirer": "NVIDIA Corporation", "date": "2020", "country": "USA", "enterprise_value": "$6.9B", "revenue": "$1.3B", "ev_revenue_multiple": "5.3x", "strategic_rationale": "Data center networking and interconnect technology acquisition"},
    {"target": "Xilinx Inc", "acquirer": "Advanced Micro Devices", "date": "2022", "country": "USA", "enterprise_value": "$49.0B", "revenue": "$3.2B", "ev_revenue_multiple": "15.3x", "strategic_rationale": "FPGA technology and data center acceleration capabilities"},
    {"target": "Altera Corporation", "acquirer": "Intel Corporation", "date": "2015", "country": "USA", "enterprise_value": "$16.7B", "revenue": "$1.9B", "ev_revenue_multiple": "8.8x", "strategic_rationale": "FPGA integration with CPU products for programmable solutions"},
    {"target": "Mobileye NV", "acquirer": "Intel Corporation", "date": "2017", "country": "Israel", "enterprise_value": "$15.3B", "revenue": "$358M", "ev_revenue_multiple": "42.7x", "strategic_rationale": "Autonomous driving and computer vision technology acquisition"}
  ],
  "valuation_data": [
    {"methodology": "Discounted Cash Flow", "enterprise_value": "$2,850B-$3,200B", "metric": "NPV", "22a_multiple": null, "23e_multiple": null, "commentary": "Based on projected free cash flows and terminal value assumptions"},
    {"methodology": "Trading Multiples", "enterprise_value": "$2,600B-$3,100B", "metric": "EV/Revenue", "22a_multiple": "42.7x", "23e_multiple": "19.9x", "commentary": "Peer group analysis of semiconductor and AI companies"},
    {"methodology": "Precedent Transactions", "enterprise_value": "$3,100B-$3,600B", "metric": "EV/Revenue", "22a_multiple": "51.0x", "23e_multiple": null, "commentary": "Recent M&A transactions in AI and semiconductor sectors"}
  ]
}
'''
    
    else:
        # Default/other chunks
        return '{"status": "success"}'

def test_sea_conglomerates_data():
    """Test SEA conglomerates data generation and slide rendering"""
    print("🧪 Testing SEA Conglomerates slide data generation...")
    
    generator = CleanBulletproofJSONGenerator()
    
    # Mock conversation data
    content_ir = {
        'company_name': 'NVIDIA',
        'industry': 'Semiconductors/AI Computing',
        'business_description_detailed': 'Leading AI and semiconductor company'
    }
    
    # Test chunk 1 generation (includes sea_conglomerates)
    print("🔍 Testing buyers/financial chunk generation...")
    chunk1_data = generator._generate_buyers_financial_chunk(
        'NVIDIA', 
        'Semiconductors', 
        'AI and semiconductor leader',
        content_ir,
        mock_llm_api_call
    )
    
    print(f"✅ Chunk 1 generated {len(chunk1_data)} fields")
    print(f"📊 Available keys: {list(chunk1_data.keys())}")
    
    # Check SEA conglomerates specifically
    sea_conglomerates = chunk1_data.get('sea_conglomerates', [])
    print(f"🌏 SEA Conglomerates found: {len(sea_conglomerates)} items")
    
    if sea_conglomerates:
        for i, item in enumerate(sea_conglomerates):
            print(f"   {i+1}. {item.get('name')} ({item.get('country')}) - {item.get('key_financials')}")
        
        # Test slide rendering
        print("\n🎨 Testing slide rendering...")
        from slide_templates import render_sea_conglomerates_slide
        
        # Test with data
        try:
            prs = render_sea_conglomerates_slide(
                data={'sea_conglomerates': sea_conglomerates},
                company_name="NVIDIA"
            )
            print("✅ SEA conglomerates slide rendered successfully with data")
        except Exception as e:
            print(f"❌ Slide rendering failed: {e}")
            
        # Test with direct array (alternative format)
        try:
            prs = render_sea_conglomerates_slide(
                data=sea_conglomerates,
                company_name="NVIDIA" 
            )
            print("✅ SEA conglomerates slide rendered successfully with direct array")
        except Exception as e:
            print(f"❌ Direct array rendering failed: {e}")
    else:
        print("❌ No SEA conglomerates data generated")
    
    return sea_conglomerates

def test_precedent_transactions_data():
    """Test precedent transactions data generation and slide rendering"""
    print("\n🧪 Testing Precedent Transactions slide data generation...")
    
    generator = CleanBulletproofJSONGenerator()
    
    # Mock conversation data
    content_ir = {
        'company_name': 'NVIDIA',
        'industry': 'Semiconductors/AI Computing', 
        'competitors_mentioned': ['AMD', 'Intel']
    }
    
    # Test chunk 2 generation (includes precedent_transactions)
    print("🔍 Testing competitive/valuation chunk generation...")
    chunk2_data = generator._generate_competitive_valuation_chunk(
        'NVIDIA',
        'Semiconductors', 
        content_ir,
        mock_llm_api_call
    )
    
    print(f"✅ Chunk 2 generated {len(chunk2_data)} fields")
    print(f"📊 Available keys: {list(chunk2_data.keys())}")
    
    # Check precedent transactions specifically
    precedent_transactions = chunk2_data.get('precedent_transactions', [])
    print(f"📈 Precedent Transactions found: {len(precedent_transactions)} items")
    
    if precedent_transactions:
        for i, item in enumerate(precedent_transactions):
            acquirer = item.get('acquirer', 'N/A')
            target = item.get('target', 'N/A') 
            ev = item.get('enterprise_value', 'N/A')
            multiple = item.get('ev_revenue_multiple', 'N/A')
            print(f"   {i+1}. {acquirer} -> {target}: {ev} ({multiple})")
        
        # Test slide rendering
        print("\n🎨 Testing precedent transactions slide rendering...")
        from slide_templates import render_precedent_transactions_slide
        
        try:
            prs = render_precedent_transactions_slide(
                data={'transactions': precedent_transactions, 'title': 'Precedent Transactions Analysis'},
                company_name="NVIDIA"
            )
            print("✅ Precedent transactions slide rendered successfully")
        except Exception as e:
            print(f"❌ Precedent transactions slide rendering failed: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("❌ No precedent transactions data generated")
    
    return precedent_transactions

def test_valuation_overview_data():
    """Test valuation overview data generation and slide rendering"""
    print("\n🧪 Testing Valuation Overview slide data generation...")
    
    generator = CleanBulletproofJSONGenerator()
    
    # Mock conversation data
    content_ir = {
        'company_name': 'NVIDIA',
        'industry': 'Semiconductors/AI Computing',
        'competitors_mentioned': ['AMD', 'Intel']
    }
    
    # Test chunk 2 generation (includes valuation_data)
    print("🔍 Testing competitive/valuation chunk generation...")
    chunk2_data = generator._generate_competitive_valuation_chunk(
        'NVIDIA',
        'Semiconductors',
        content_ir, 
        mock_llm_api_call
    )
    
    # Check valuation data specifically
    valuation_data = chunk2_data.get('valuation_data', [])
    print(f"💰 Valuation Data found: {len(valuation_data)} methodologies")
    
    if valuation_data:
        for i, item in enumerate(valuation_data):
            methodology = item.get('methodology', 'N/A')
            ev = item.get('enterprise_value', 'N/A')
            metric = item.get('metric', 'N/A')
            commentary = item.get('commentary', 'N/A')
            print(f"   {i+1}. {methodology}: {ev} ({metric}) - {commentary[:60]}...")
        
        # Test slide rendering
        print("\n🎨 Testing valuation overview slide rendering...")
        from slide_templates import render_valuation_overview_slide
        
        try:
            prs = render_valuation_overview_slide(
                data={
                    'title': 'Valuation Overview',
                    'subtitle': 'Implied EV/Revenue Multiples',
                    'valuation_data': valuation_data
                },
                company_name="NVIDIA"
            )
            print("✅ Valuation overview slide rendered successfully")
        except Exception as e:
            print(f"❌ Valuation overview slide rendering failed: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("❌ No valuation data generated")
    
    return valuation_data

if __name__ == "__main__":
    print("🧪 Testing slide data generation and rendering...\n")
    
    sea_conglomerates = test_sea_conglomerates_data()
    precedent_transactions = test_precedent_transactions_data()
    valuation_data = test_valuation_overview_data()
    
    print("\n📊 Summary:")
    print(f"✅ SEA Conglomerates: {len(sea_conglomerates)} items generated")
    print(f"✅ Precedent Transactions: {len(precedent_transactions)} items generated")
    print(f"✅ Valuation Data: {len(valuation_data)} methodologies generated")
    
    if all([sea_conglomerates, precedent_transactions, valuation_data]):
        print("\n🎉 All slide data generation tests passed!")
    else:
        print(f"\n💥 Some tests failed. Missing data for slides.")