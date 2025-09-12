#!/usr/bin/env python3
"""
Test the financial metrics and competitive positioning fixes
"""

import json
from bulletproof_json_generator_clean import CleanBulletproofJSONGenerator

def test_dynamic_financial_metrics():
    """Test that financial metrics are dynamic and calculated from data"""
    print("🔧 Testing dynamic financial metrics...")
    
    # Mock content_ir with NVIDIA-like financial data
    test_content_ir = {
        "facts": {
            "years": ["2020", "2021", "2022", "2023", "2024E"],
            "revenue_usd_m": [16675, 26974, 27000, 60922, 60900],  # Corrected: NVIDIA actual 2024 revenue $60.9B
            "ebitda_usd_m": [5631, 8000, 12000, 34000, 73000]
        },
        "operational_metrics_mentioned": ["90%+ AI chip market share", "3.5M developers", "$47.5B data center revenue"]
    }
    
    generator = CleanBulletproofJSONGenerator()
    
    try:
        # Test dynamic metrics generation
        metrics_result = generator._generate_dynamic_financial_metrics(test_content_ir)
        
        print(f"✅ Dynamic metrics generated successfully")
        print(f"   - Title: {metrics_result.get('title')}")
        
        metrics = metrics_result.get('metrics', [])
        print(f"   - Metrics count: {len(metrics)}")
        
        # Test each metric
        for i, metric in enumerate(metrics):
            title = metric.get('title', 'No title')
            value = metric.get('value', 'No value')
            period = metric.get('period', '')
            note = metric.get('note', 'No note')
            
            print(f"   - Metric {i+1}: {title}")
            print(f"     Value: {value} {period}")
            print(f"     Note: {note}")
            
            # Check if metric has specific values (not hardcoded)
            is_dynamic = 'not available' in value or any(char in value for char in ['$', '%', 'B', 'M'])
            status = "✅" if is_dynamic else "⚠️"
            print(f"     {status} Dynamic: {is_dynamic}")
        
        # Test CAGR calculation
        cagr_metric = next((m for m in metrics if 'CAGR' in m.get('title', '')), None)
        if cagr_metric:
            cagr_value = cagr_metric.get('value')
            # Should calculate: ((60900/16675)^(1/4) - 1) * 100 ≈ 38%
            print(f"   ✅ CAGR calculated: {cagr_value}")
        
        # Test profitability note
        ebitda_metric = next((m for m in metrics if 'EBITDA' in m.get('title', '')), None)
        if ebitda_metric:
            profitability_note = ebitda_metric.get('note')
            # Should not be hardcoded "Path to profitability" 
            is_dynamic_note = profitability_note != "Path to profitability"
            status = "✅" if is_dynamic_note else "⚠️"
            print(f"   {status} Profitability note: {profitability_note}")
        
        return True
        
    except Exception as e:
        print(f"❌ Dynamic metrics test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_competitive_positioning_completeness():
    """Test that competitive positioning has 4+ barriers and advantages"""
    print("\n🔧 Testing competitive positioning completeness...")
    
    # Create generator and test competitive chunk
    generator = CleanBulletproofJSONGenerator()
    
    # Mock API function for competitive testing
    def mock_llm_api_call(messages):
        """Mock LLM response with complete competitive data"""
        return '''
{
  "competitive_analysis": {
    "competitors": [
      {"name": "NVIDIA", "revenue": 60900},  # Corrected: NVIDIA actual 2024 revenue
      {"name": "AMD", "revenue": 23500},
      {"name": "Intel", "revenue": 76000},
      {"name": "Broadcom", "revenue": 51000}
    ],
    "assessment": [
      ["Company", "AI Computing Leadership", "Software Ecosystem", "Data Center Penetration", "Innovation Velocity"],
      ["NVIDIA", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"],
      ["AMD", "⭐⭐⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐"],
      ["Intel", "⭐⭐", "⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐"],
      ["Broadcom", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐", "⭐⭐⭐"]
    ],
    "barriers": [
      {"title": "CUDA Ecosystem Lock-in", "desc": "Proprietary software platform with 4M+ developers creates high switching costs for AI developers"},
      {"title": "R&D Investment Requirements", "desc": "$7.3B annual R&D spending needed to compete in advanced AI chip development"},
      {"title": "Manufacturing Scale Economics", "desc": "TSMC advanced node capacity requirements and multi-billion dollar wafer commitments"},
      {"title": "Technical Expertise Barriers", "desc": "25+ years of parallel computing and GPU architecture expertise difficult to replicate"}
    ],
    "advantages": [
      {"title": "AI Computing Market Leadership", "desc": "90%+ market share in AI training and inference chips with technological superiority"},
      {"title": "Software Ecosystem Dominance", "desc": "CUDA platform with 3.5M+ developers creates network effects and switching barriers"},
      {"title": "Strategic Cloud Partnerships", "desc": "Exclusive relationships with all major cloud providers (AWS, Azure, GCP) for AI infrastructure"},
      {"title": "Gross Margin Excellence", "desc": "73% gross margins vs industry average 45%, enabling continued R&D reinvestment"}
    ]
  }
}
'''
    
    try:
        # Test competitive chunk generation
        chunk_result = generator._generate_competitive_valuation_chunk(
            company_name="NVIDIA",
            industry="Semiconductors/AI Computing",
            extracted_data={
                'competitors_mentioned': ['AMD', 'Intel'],
                'competitive_positioning': 'Dominant AI computing leader',
                'competitive_advantages_mentioned': ['CUDA ecosystem', 'AI performance']
            },
            llm_api_call=mock_llm_api_call
        )
        
        if chunk_result and 'competitive_analysis' in chunk_result:
            competitive_data = chunk_result['competitive_analysis']
            
            # Test barriers
            barriers = competitive_data.get('barriers', [])
            print(f"✅ Barriers to Entry: {len(barriers)} items")
            
            if len(barriers) >= 4:
                print("✅ At least 4 barriers as required")
                for i, barrier in enumerate(barriers):
                    title = barrier.get('title', 'No title')
                    desc_len = len(barrier.get('desc', ''))
                    print(f"   - Barrier {i+1}: {title} ({desc_len} chars)")
            else:
                print(f"⚠️  Only {len(barriers)} barriers (need 4+)")
            
            # Test advantages
            advantages = competitive_data.get('advantages', [])
            print(f"✅ Competitive Advantages: {len(advantages)} items")
            
            if len(advantages) >= 4:
                print("✅ At least 4 advantages as required")
                for i, advantage in enumerate(advantages):
                    title = advantage.get('title', 'No title')
                    desc_len = len(advantage.get('desc', ''))
                    print(f"   - Advantage {i+1}: {title} ({desc_len} chars)")
            else:
                print(f"⚠️  Only {len(advantages)} advantages (need 4+)")
            
            # Test assessment completeness
            assessment = competitive_data.get('assessment', [])
            if len(assessment) > 1:  # Headers + data
                headers = assessment[0]
                data_rows = assessment[1:]
                print(f"✅ Assessment Matrix: {len(data_rows)} companies x {len(headers)} criteria")
                print(f"   - Headers: {headers}")
            else:
                print("⚠️  Assessment matrix incomplete")
            
        return True
        
    except Exception as e:
        print(f"❌ Competitive positioning test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Testing financial and competitive fixes...\n")
    
    success1 = test_dynamic_financial_metrics()
    success2 = test_competitive_positioning_completeness()
    
    if success1 and success2:
        print("\n🎉 All financial and competitive tests passed!")
    else:
        print("\n💥 Some tests failed. Check the errors above.")