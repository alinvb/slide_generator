#!/usr/bin/env python3
"""
Test the operational highlights and strategic positioning fixes
"""

import json
from bulletproof_json_generator_clean import CleanBulletproofJSONGenerator

def test_operational_highlights_extraction():
    """Test that operational highlights are extracted properly from conversation"""
    print("🔧 Testing operational highlights extraction...")
    
    # Create mock conversation with NVIDIA-like operational details
    conversation_messages = [
        {
            "role": "user",
            "content": "Tell me about NVIDIA's business performance"
        },
        {
            "role": "assistant", 
            "content": """NVIDIA dominates the AI computing market with 90%+ market share in AI training chips. The company has built a 3.5 million developer ecosystem around its CUDA software platform, creating massive switching barriers. Their data center revenue reached $47.5B in 2024, representing 217% year-over-year growth. NVIDIA maintains strategic partnerships with all major cloud providers including Microsoft Azure, Google Cloud, and AWS. The company achieves industry-leading 73% gross margins on its premium AI products. With 25+ years of GPU architecture leadership, NVIDIA has established itself as the foundational platform for AI infrastructure globally."""
        },
        {
            "role": "user", 
            "content": "What's NVIDIA's strategic market position?"
        },
        {
            "role": "assistant",
            "content": """NVIDIA's strategic market positioning centers on being the essential AI computing infrastructure provider. Unlike competitors who focus on individual chips, NVIDIA provides a complete platform ecosystem spanning hardware, software, and developer tools. Their positioning as 'the AI platform company' differentiates them from traditional semiconductor manufacturers. The company has successfully transformed from a gaming GPU maker into the foundational layer for enterprise AI, autonomous vehicles, and next-generation computing workloads."""
        }
    ]
    
    # Create generator instance
    generator = CleanBulletproofJSONGenerator()
    
    # Mock API function that should extract operational highlights
    def mock_llm_api_call(messages):
        """Mock LLM response for operational highlights testing"""
        prompt_content = messages[0]['content'] if messages else ""
        
        if "operational_highlights" in prompt_content.lower():
            return '''
{
  "business_overview_data": {
    "strategic_positioning": "NVIDIA serves as the foundational AI computing platform provider, offering complete ecosystem solutions spanning hardware, software, and developer tools - differentiating from traditional semiconductor manufacturers focused solely on chip sales.",
    "operational_highlights": [
      "90%+ market share dominance in AI training and inference chips globally",
      "3.5 million developer ecosystem built around proprietary CUDA software platform",
      "$47.5B data center revenue achieved in 2024 (+217% YoY growth)",
      "Strategic partnerships with all major cloud providers (Azure, GCP, AWS)",
      "Industry-leading 73% gross margins on premium AI chip products",
      "25+ years of established GPU architecture and parallel computing leadership"
    ],
    "key_value_propositions": [
      "Complete AI platform ecosystem (hardware + software + tools)",
      "Unmatched performance for AI training and inference workloads", 
      "High switching barriers through CUDA software lock-in effects"
    ],
    "market_opportunity": "AI semiconductor market projected $273B by 2029 (20% CAGR)"
  }
}
'''
        else:
            # Basic conversation extraction
            return '''
{
  "company_name": "NVIDIA",
  "business_description_detailed": "NVIDIA Corporation designs and manufactures graphics processing units, AI accelerators, and computing platforms for gaming, data centers, and professional visualization markets.",
  "industry": "Semiconductors/AI Computing",
  "strategic_market_positioning": "Essential AI computing infrastructure provider offering complete platform ecosystem spanning hardware, software, and developer tools",
  "operational_highlights": [
    "90%+ market share in AI training chips",
    "3.5M+ developer CUDA ecosystem", 
    "$47.5B data center revenue (+217% YoY)",
    "Partnerships with all major cloud providers",
    "73% gross margins on AI products",
    "25+ years GPU architecture leadership"
  ],
  "competitive_advantages_mentioned": ["CUDA software ecosystem", "AI chip performance leadership"],
  "key_achievements": ["Market leadership in AI computing", "Developer ecosystem growth"]
}
'''
    
    try:
        # Test conversation extraction
        print("🔍 Testing conversation extraction...")
        extracted_data = generator.extract_conversation_data(
            messages=conversation_messages,
            llm_api_call=mock_llm_api_call,
            company_name="NVIDIA"
        )
        
        print(f"✅ Conversation extraction completed")
        print(f"   - Company: {extracted_data.get('company_name')}")
        print(f"   - Business description length: {len(extracted_data.get('business_description_detailed', ''))}")
        print(f"   - Strategic positioning length: {len(extracted_data.get('strategic_market_positioning', ''))}")
        print(f"   - Operational highlights: {len(extracted_data.get('operational_highlights', []))}")
        
        # Check if descriptions are different
        business_desc = extracted_data.get('business_description_detailed', '')
        strategic_pos = extracted_data.get('strategic_market_positioning', '')
        
        if business_desc != strategic_pos and len(strategic_pos) > 0:
            print("✅ Strategic positioning is different from business description")
            print(f"   - Business: {business_desc[:80]}...")  
            print(f"   - Strategic: {strategic_pos[:80]}...")
        else:
            print("⚠️  Strategic positioning appears same as business description")
        
        # Test operational highlights quality
        op_highlights = extracted_data.get('operational_highlights', [])
        if len(op_highlights) >= 6:
            print(f"✅ Found {len(op_highlights)} operational highlights")
            
            # Check if highlights are specific (not generic)
            generic_terms = ['strong', 'proven', 'experienced', 'scalable', 'diversified']
            specific_count = 0
            
            for i, highlight in enumerate(op_highlights[:6]):
                has_generic = any(term in highlight.lower() for term in generic_terms)
                has_specific = any(char in highlight for char in ['%', '$', 'M', 'B', '+', '20', '30'])
                
                if not has_generic and has_specific:
                    specific_count += 1
                    
                print(f"   - Highlight {i+1}: {highlight}")
            
            if specific_count >= 4:
                print(f"✅ {specific_count}/6 highlights are specific with metrics/data")
            else:
                print(f"⚠️  Only {specific_count}/6 highlights are specific - need more concrete data")
        else:
            print(f"⚠️  Only {len(op_highlights)} operational highlights found, need 6")
        
        # Test chunk generation
        print("\n🔍 Testing growth/investor chunk generation...")
        chunk_result = generator._generate_growth_investor_chunk(
            company_name="NVIDIA",
            industry="Semiconductors/AI Computing", 
            description="Leading AI computing platform provider",
            extracted_data=extracted_data,
            llm_api_call=mock_llm_api_call
        )
        
        if chunk_result and 'business_overview_data' in chunk_result:
            business_data = chunk_result['business_overview_data']
            chunk_highlights = business_data.get('operational_highlights', [])
            chunk_positioning = business_data.get('strategic_positioning', '')
            
            print(f"✅ Chunk generation successful")
            print(f"   - Operational highlights: {len(chunk_highlights)}")
            print(f"   - Strategic positioning: {len(chunk_positioning)} chars")
            
            if len(chunk_highlights) == 6:
                print("✅ Exact 6 operational highlights generated")
                for i, highlight in enumerate(chunk_highlights):
                    print(f"   - {i+1}: {highlight}")
            else:
                print(f"⚠️  Generated {len(chunk_highlights)} highlights instead of 6")
        else:
            print("❌ Chunk generation failed")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_operational_highlights_extraction()
    if success:
        print("\n🎉 Operational highlights test completed!")
    else:
        print("\n💥 Operational highlights test failed!")