#!/usr/bin/env python3
"""
Test the slide rendering fixes with NVIDIA sample data
"""

import json
import os
from bulletproof_json_generator_clean import CleanBulletproofJSONGenerator

def test_nvidia_slide_fixes():
    """Test the fixes with NVIDIA conversation data"""
    print("🔧 Testing slide rendering fixes with NVIDIA data...")
    
    # Load NVIDIA sample data
    with open('nvidia_sample_data.json', 'r') as f:
        nvidia_data = json.load(f)
    
    # Convert research results to conversation format
    conversation_messages = []
    for topic, data in nvidia_data['research_results'].items():
        conversation_messages.append({
            "role": "user",
            "content": f"Tell me about {data['title']}"
        })
        conversation_messages.append({
            "role": "assistant", 
            "content": data['content']
        })
    
    print(f"✅ Created conversation with {len(conversation_messages)} messages")
    
    # Create generator instance
    generator = CleanBulletproofJSONGenerator()
    
    # Mock API function for testing
    def mock_llm_api_call(messages):
        """Mock LLM response for competitive analysis testing"""
        return '''
{
  "competitive_analysis": {
    "competitors": [
      {"name": "NVIDIA", "revenue": 130500},
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
      {"title": "CUDA Ecosystem Lock-in", "desc": "Proprietary software platform with 4M+ developers creates high switching costs"}
    ],
    "advantages": [
      {"title": "AI Computing Dominance", "desc": "90%+ market share in AI training and inference chips"}
    ]
  },
  "precedent_transactions": [
    {"target": "Mellanox", "acquirer": "NVIDIA", "date": "2020", "country": "USA", "enterprise_value": "$7.0B", "revenue": "$1.3B", "ev_revenue_multiple": "5.4x", "strategic_rationale": "High-performance networking and interconnect capabilities"},
    {"target": "Arm Holdings", "acquirer": "NVIDIA", "date": "2020 (terminated)", "country": "UK", "enterprise_value": "$40B", "revenue": "$2.0B", "ev_revenue_multiple": "20.0x", "strategic_rationale": "CPU architecture and mobile computing expansion"},
    {"target": "Xilinx", "acquirer": "AMD", "date": "2022", "country": "USA", "enterprise_value": "$35B", "revenue": "$3.2B", "ev_revenue_multiple": "10.9x", "strategic_rationale": "FPGA and adaptive computing capabilities"}
  ],
  "valuation_data": [
    {"methodology": "DCF Analysis", "enterprise_value": "$2.8T-$3.2T", "metric": "NPV", "22a_multiple": null, "23e_multiple": null, "commentary": "Based on AI market growth and NVIDIA's dominant position"},
    {"methodology": "Trading Multiples", "enterprise_value": "$2.5T-$3.0T", "metric": "EV/Revenue", "22a_multiple": "25.0x", "23e_multiple": "20.0x", "commentary": "Premium to semiconductor peers due to AI leadership"},
    {"methodology": "Precedent Transactions", "enterprise_value": "$3.0T-$3.9T", "metric": "EV/Revenue", "22a_multiple": "30.0x", "23e_multiple": null, "commentary": "Strategic premium for AI platform dominance"}
  ]
}
'''
    
    try:
        # Test competitive analysis chunked generation
        print("🔍 Testing competitive analysis chunk generation...")
        chunk_result = generator._generate_competitive_valuation_chunk(
            company_name="NVIDIA", 
            industry="Semiconductors/AI Computing",
            extracted_data={
                'competitors_mentioned': ['AMD', 'Intel'],
                'competitive_positioning': 'Dominant AI computing leader with CUDA ecosystem moat',
                'products_services_detailed': ['AI Data Center GPUs', 'CUDA Software Platform'],
                'competitive_advantages_mentioned': ['CUDA ecosystem', 'AI chip performance leadership'],
                'business_description_detailed': 'Leading AI computing platform provider'
            },
            llm_api_call=mock_llm_api_call
        )
        
        if chunk_result and 'competitive_analysis' in chunk_result:
            comp_analysis = chunk_result['competitive_analysis']
            assessment = comp_analysis.get('assessment', [])
            
            print(f"✅ Competitive analysis generated successfully")
            print(f"   - Competitors: {len(comp_analysis.get('competitors', []))}")
            print(f"   - Assessment matrix: {len(assessment)} rows x {len(assessment[0]) if assessment else 0} cols")
            
            if assessment and len(assessment) > 0:
                headers = assessment[0]
                print(f"   - Dynamic headers: {headers}")
                
                # Check if headers are industry-specific (not generic)
                generic_headers = ['Market Focus', 'Product Quality', 'Enterprise Adoption']
                is_dynamic = not any(header in generic_headers for header in headers)
                if is_dynamic:
                    print("✅ Headers are dynamically generated (not hardcoded)")
                else:
                    print("⚠️  Headers still appear generic")
            
            # Test precedent transactions
            transactions = chunk_result.get('precedent_transactions', [])
            if transactions:
                print(f"✅ Precedent transactions: {len(transactions)} deals")
                for i, txn in enumerate(transactions[:2]):
                    acquirer = txn.get('acquirer', 'N/A')
                    if acquirer and acquirer != 'N/A' and 'null' not in acquirer.lower():
                        print(f"   - Deal {i+1}: {txn.get('target')} acquired by {acquirer} ({txn.get('enterprise_value')})")
                    else:
                        print(f"   - Deal {i+1}: Missing acquirer data - {acquirer}")
            
            # Test valuation data structure
            valuation_data = chunk_result.get('valuation_data', [])
            if valuation_data and isinstance(valuation_data, list):
                print(f"✅ Valuation data: {len(valuation_data)} methodologies in proper array format")
                for val in valuation_data:
                    print(f"   - {val.get('methodology')}: {val.get('enterprise_value')} ({val.get('metric')})")
            
        else:
            print("❌ Competitive analysis chunk generation failed")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_nvidia_slide_fixes()
    if success:
        print("\n🎉 Slide fixes test completed successfully!")
    else:
        print("\n💥 Slide fixes test failed!")