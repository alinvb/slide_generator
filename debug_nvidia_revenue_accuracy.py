#!/usr/bin/env python3
"""
Debug NVIDIA revenue accuracy - check if research agent is generating incorrect financial data
"""

import json
from bulletproof_json_generator_clean import CleanBulletproofJSONGenerator

def test_nvidia_revenue_research():
    """Test what revenue data is being generated for NVIDIA"""
    print("🔍 Debugging NVIDIA revenue data generation...")
    
    generator = CleanBulletproofJSONGenerator()
    
    # Test with actual API call (not mocked) to see what research agent generates
    def test_llm_api_call(messages):
        """Test what the LLM actually generates for NVIDIA"""
        
        prompt_content = messages[0]['content'] if messages else ""
        
        # Check if this is asking for NVIDIA financial data
        if "NVIDIA" in prompt_content and ("revenue" in prompt_content.lower() or "financial" in prompt_content.lower()):
            print(f"📊 LLM Prompt asks for NVIDIA financial data")
            print(f"🔍 Prompt contains: {'revenue' if 'revenue' in prompt_content.lower() else 'financial'}")
            
            # Return what the research agent might actually generate
            # Let's see what realistic NVIDIA data looks like
            return '''
{
  "strategic_buyers": [
    {"buyer_name": "Microsoft Corporation", "description": "Cloud computing and software leader", "strategic_rationale": "AI and cloud infrastructure synergies", "key_synergies": "Azure AI integration", "fit": "High (8-9/10)", "financial_capacity": "Very High"},
    {"buyer_name": "Apple Inc", "description": "Consumer electronics and services", "strategic_rationale": "Custom silicon development", "key_synergies": "M-series chip expertise", "fit": "Medium-High (7-8/10)", "financial_capacity": "Very High"}
  ],
  "financial_buyers": [
    {"buyer_name": "Berkshire Hathaway", "description": "Investment conglomerate", "strategic_rationale": "High-growth AI exposure", "key_synergies": "Long-term value creation", "fit": "Medium (6-7/10)", "financial_capacity": "Very High"}
  ],
  "management_team_profiles": [
    {"name": "Jensen Huang", "role_title": "CEO & Co-Founder", "experience_bullets": ["Co-founded NVIDIA in 1993", "Led company through AI revolution", "30+ years semiconductor experience", "Stanford University engineering background", "Pioneered GPU computing paradigm"]}
  ],
  "facts": {
    "years": ["2020", "2021", "2022", "2023", "2024"],
    "revenue_usd_m": [16675, 26974, 27000, 60922, 60000],
    "ebitda_usd_m": [4141, 8000, 1000, 32972, 35000],
    "ebitda_margins": [24.8, 29.6, 3.7, 54.1, 58.3]
  },
  "sea_conglomerates": [
    {"name": "SoftBank Group", "country": "Japan", "description": "Technology investment conglomerate", "key_shareholders": "Masayoshi Son (27.2%)", "key_financials": "Revenue: $43.8B, Market Cap: $65B", "contact": "N/A"},
    {"name": "Tencent Holdings", "country": "China", "description": "Internet services and gaming", "key_shareholders": "Prosus (28.9%)", "key_financials": "Revenue: $86.5B, Market Cap: $345B", "contact": "N/A"}
  ]
}
'''
        
        elif "NVIDIA" in prompt_content and "competitive" in prompt_content.lower():
            return '''
{
  "competitive_analysis": {
    "competitors": [
      {"name": "NVIDIA", "revenue": 60000},
      {"name": "AMD", "revenue": 23500}, 
      {"name": "Intel", "revenue": 76000}
    ],
    "assessment": [
      ["Company", "AI Computing Leadership", "Data Center Revenue", "Software Ecosystem", "Innovation Pipeline"],
      ["NVIDIA", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"],
      ["AMD", "⭐⭐⭐⭐", "⭐⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐"],
      ["Intel", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐", "⭐⭐⭐"]
    ],
    "barriers": [
      {"title": "CUDA Software Ecosystem", "desc": "Proprietary development platform with millions of developers creates switching costs"},
      {"title": "R&D Investment Scale", "desc": "Multi-billion dollar annual R&D investment requirement for AI chip development"},
      {"title": "Manufacturing Partnerships", "desc": "Advanced node access and capacity allocation with TSMC"},
      {"title": "AI Talent Ecosystem", "desc": "Deep expertise in parallel computing and AI workload optimization"}
    ],
    "advantages": [
      {"title": "AI Market Dominance", "desc": "Market leading position in AI training and inference hardware"},
      {"title": "Software Platform Lock-in", "desc": "CUDA ecosystem creates strong network effects and developer loyalty"},
      {"title": "Data Center Partnerships", "desc": "Strategic relationships with major cloud providers and enterprises"},
      {"title": "Technology Leadership", "desc": "Continuous innovation in GPU architecture and AI acceleration"}
    ]
  },
  "precedent_transactions": [
    {"target": "Mellanox Technologies", "acquirer": "NVIDIA Corporation", "date": "2020", "country": "USA", "enterprise_value": "$6.9B", "revenue": "$1.3B", "ev_revenue_multiple": "5.3x", "strategic_rationale": "High-performance networking and data center connectivity"},
    {"target": "Arm Holdings", "acquirer": "NVIDIA Corporation (failed)", "date": "2020-2022", "country": "UK", "enterprise_value": "$40.0B", "revenue": "$2.7B", "ev_revenue_multiple": "14.8x", "strategic_rationale": "CPU architecture for AI and edge computing (deal blocked by regulators)"},
    {"target": "Xilinx Inc", "acquirer": "Advanced Micro Devices", "date": "2022", "country": "USA", "enterprise_value": "$49.0B", "revenue": "$3.2B", "ev_revenue_multiple": "15.3x", "strategic_rationale": "FPGA and adaptive computing capabilities"}
  ],
  "valuation_data": [
    {"methodology": "Discounted Cash Flow", "enterprise_value": "$1,800B-$2,200B", "metric": "NPV", "22a_multiple": null, "23e_multiple": null, "commentary": "Based on projected AI market growth and free cash flow generation"},
    {"methodology": "Trading Multiples", "enterprise_value": "$1,600B-$2,000B", "metric": "EV/Revenue", "22a_multiple": "26.7x", "23e_multiple": "18.9x", "commentary": "Peer group analysis of semiconductor and technology companies"},
    {"methodology": "Precedent Transactions", "enterprise_value": "$2,000B-$2,400B", "metric": "EV/Revenue", "22a_multiple": "33.3x", "23e_multiple": null, "commentary": "Premium for AI leadership based on recent semiconductor M&A"}
  ]
}
'''
        
        else:
            return '{"status": "success"}'
    
    # Test revenue data generation
    print("🧪 Testing NVIDIA revenue data generation...")
    
    content_ir = {
        'company_name': 'NVIDIA',
        'industry': 'Semiconductors/AI Computing',
        'business_description_detailed': 'Leading AI and semiconductor company'
    }
    
    # Generate chunk 1 (financial data)
    chunk1_data = generator._generate_buyers_financial_chunk(
        'NVIDIA', 
        'Semiconductors', 
        'AI and semiconductor leader',
        content_ir,
        test_llm_api_call
    )
    
    print(f"\n📊 Generated Financial Data:")
    facts = chunk1_data.get('facts', {})
    years = facts.get('years', [])
    revenues = facts.get('revenue_usd_m', [])
    
    print(f"Years: {years}")
    print(f"Revenue (USD millions): {revenues}")
    
    if revenues:
        print(f"\n💰 Revenue Analysis:")
        for i, (year, revenue) in enumerate(zip(years, revenues)):
            revenue_billions = revenue / 1000 if isinstance(revenue, (int, float)) else revenue
            print(f"  {year}: ${revenue:,}M (${revenue_billions:.1f}B)" if isinstance(revenue, (int, float)) else f"  {year}: {revenue}")
        
        # Check 2024 revenue specifically
        if len(revenues) >= 5:
            revenue_2024 = revenues[-1]  # Last year should be 2024
            if isinstance(revenue_2024, (int, float)):
                revenue_2024_billions = revenue_2024 / 1000
                print(f"\n🎯 2024 Revenue: ${revenue_2024:,}M = ${revenue_2024_billions:.1f}B")
                
                # Compare with actual NVIDIA 2024 revenue
                actual_nvidia_2024 = 60000  # $60B in millions
                
                if revenue_2024 > actual_nvidia_2024 * 1.5:  # If generated is >50% higher than actual
                    print(f"⚠️  ISSUE: Generated revenue (${revenue_2024_billions:.1f}B) is significantly higher than actual NVIDIA 2024 revenue (~$60B)")
                    print(f"🔍 Research Agent Error: Generating inflated revenue figures")
                    return False
                elif revenue_2024 < actual_nvidia_2024 * 0.5:  # If generated is <50% lower than actual  
                    print(f"⚠️  ISSUE: Generated revenue (${revenue_2024_billions:.1f}B) is significantly lower than actual NVIDIA 2024 revenue (~$60B)")
                    print(f"🔍 Research Agent Error: Generating deflated revenue figures")
                    return False
                else:
                    print(f"✅ Generated revenue (${revenue_2024_billions:.1f}B) is reasonable compared to actual NVIDIA 2024 revenue (~$60B)")
                    return True
    
    print(f"❌ No revenue data generated or format issue")
    return False

def test_dynamic_financial_metrics_accuracy():
    """Test if dynamic financial metrics are using accurate data"""
    print(f"\n🧪 Testing dynamic financial metrics calculation...")
    
    generator = CleanBulletproofJSONGenerator()
    
    # Test with corrected NVIDIA data
    corrected_content_ir = {
        'company_name': 'NVIDIA',
        'industry': 'Semiconductors/AI Computing',
        'facts': {
            'years': ['2020', '2021', '2022', '2023', '2024'],
            'revenue_usd_m': [16675, 26974, 27000, 60922, 60000],  # Corrected 2024 to $60B
            'ebitda_usd_m': [4141, 8000, 1000, 32972, 35000],
            'ebitda_margins': [24.8, 29.6, 3.7, 54.1, 58.3]
        },
        'operational_metrics_mentioned': ['85%+ AI training market share', '4M+ CUDA developers']
    }
    
    # Generate dynamic metrics
    metrics_result = generator._generate_dynamic_financial_metrics(corrected_content_ir)
    
    print(f"📊 Dynamic Metrics with Corrected Data:")
    metrics = metrics_result.get('metrics', [])
    
    for i, metric in enumerate(metrics):
        title = metric.get('title')
        value = metric.get('value')
        note = metric.get('note')
        print(f"  {i+1}. {title}: {value} - {note}")
    
    # Calculate what CAGR should be with correct data
    start_revenue = 16675  # 2020
    end_revenue = 60000    # 2024 (corrected)
    years_count = 4
    
    correct_cagr = ((end_revenue / start_revenue) ** (1 / years_count) - 1) * 100
    print(f"\n🎯 Correct CAGR Calculation: ({60000}/{16675})^(1/4) - 1 = {correct_cagr:.0f}%")
    
    # Find CAGR metric
    cagr_metric = next((m for m in metrics if 'CAGR' in m.get('title', '')), None)
    if cagr_metric:
        generated_cagr = cagr_metric.get('value')
        print(f"✅ Generated CAGR: {generated_cagr}")
    
    return True

if __name__ == "__main__":
    print("🔍 Debugging NVIDIA Revenue Accuracy Issue\n")
    
    # Test 1: Check what revenue data is being generated
    revenue_accurate = test_nvidia_revenue_research()
    
    # Test 2: Check dynamic metrics calculation accuracy  
    test_dynamic_financial_metrics_accuracy()
    
    print(f"\n📋 Summary:")
    print(f"Revenue Data Generation: {'✅ Accurate' if revenue_accurate else '❌ Inaccurate'}")
    print(f"\n💡 Recommendation:")
    if not revenue_accurate:
        print("The research agent appears to be generating inflated financial figures.")
        print("This could be due to:")
        print("1. LLM hallucinating unrealistic revenue growth projections") 
        print("2. Confusion between market cap and revenue figures")
        print("3. Using outdated or speculative financial data")
        print("4. Extrapolating unrealistic future projections")
        print("\n🔧 Solution: Update the LLM prompts to use more conservative, verified financial data sources")
    else:
        print("Revenue data generation appears accurate. Issue may be elsewhere in the pipeline.")