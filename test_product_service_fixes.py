#!/usr/bin/env python3
"""
Test the product service footprint fixes for coverage table and metrics
"""

import json
from bulletproof_json_generator_clean import CleanBulletproofJSONGenerator

def test_product_service_extraction():
    """Test that product service data generates proper coverage table and metrics"""
    print("🔧 Testing product service footprint extraction...")
    
    # Create mock conversation with NVIDIA-like service and market data
    conversation_messages = [
        {
            "role": "user",
            "content": "What are NVIDIA's main product lines and market coverage?"
        },
        {
            "role": "assistant", 
            "content": """NVIDIA operates across four key segments: Data Center ($47.5B revenue, 78% of total), Gaming ($10.4B), Professional Visualization ($1.5B), and Automotive ($1.1B). Their data center products include H100 and A100 GPUs for AI training and inference. Gaming offers GeForce RTX series for consumer market. Professional Visualization provides RTX workstations for creators. Automotive delivers DRIVE platforms for autonomous vehicles. Geographic revenue split: Americas 51%, China 16%, Europe 11%, Asia-Pacific 22%. The company maintains 90%+ market share in AI chips, serves 3.5M+ developers through CUDA, and achieved 73% gross margins in FY2024."""
        },
        {
            "role": "user", 
            "content": "What are NVIDIA's key operational metrics?"
        },
        {
            "role": "assistant",
            "content": """NVIDIA's key operational metrics include: $60.9B total revenue (+126% YoY), Data center revenue of $47.5B (+217% YoY), 73% gross margin (up from 62%), 90%+ AI chip market share, 3.5 million CUDA developers, Strategic partnerships with all major cloud providers, 29,600 global employees, and R&D spending of $7.3B (12% of revenue)."""
        }
    ]
    
    # Create generator instance
    generator = CleanBulletproofJSONGenerator()
    
    # Mock API function for product service testing
    def mock_llm_api_call(messages):
        """Mock LLM response for product service testing"""
        prompt_content = messages[0]['content'] if messages else ""
        
        if "product_service_data" in prompt_content.lower():
            return '''
{
  "product_service_data": {
    "services": [
      {"title": "AI Data Center Solutions", "desc": "Industry-leading H100 and A100 GPUs delivering breakthrough performance for AI training, inference, and large language model workloads with 90%+ market share"},
      {"title": "Gaming Graphics Platforms", "desc": "GeForce RTX 40-series GPUs providing real-time ray tracing and AI-enhanced gaming experiences for 130M+ gamers worldwide"},
      {"title": "Professional Visualization", "desc": "RTX workstation GPUs powering creative workflows, digital twins, and professional rendering for design and media industries"},
      {"title": "Autonomous Vehicle Platform", "desc": "End-to-end DRIVE Orin and DRIVE Thor solutions enabling Level 2-5 autonomous driving capabilities for automotive OEMs"},
      {"title": "Enterprise AI Software", "desc": "CUDA ecosystem, AI Enterprise suite, and Omniverse platform serving 3.5M+ developers across industries"}
    ],
    "coverage_table": [
      ["Business Segment", "Revenue FY2024", "Market Position", "Growth Trajectory"],
      ["Data Center AI", "$47.5B (78%)", "Market Leader (90%+)", "+217% YoY"],
      ["Gaming Graphics", "$10.4B (17%)", "Premium Segment Leader", "-20% (cyclical)"],
      ["Professional Viz", "$1.5B (2.5%)", "Workstation Leader", "+28% YoY"],
      ["Automotive AI", "$1.1B (1.8%)", "AV Platform Leader", "+21% YoY"]
    ],
    "metrics": {
      "Total Annual Revenue": "$60.9B (+126% YoY growth)",
      "Gross Margin Performance": "73% (industry-leading profitability)",  
      "Developer Ecosystem Size": "3.5M+ CUDA developers globally",
      "AI Market Dominance": "90%+ share in AI training chips"
    }
  }
}
'''
        else:
            # Basic conversation extraction
            return '''
{
  "company_name": "NVIDIA",
  "industry": "Semiconductors/AI Computing",
  "market_coverage_details": ["Americas 51%", "China 16%", "Europe 11%", "Asia-Pacific 22%"],
  "operational_metrics_mentioned": ["$60.9B revenue", "73% gross margin", "90% AI market share", "3.5M developers"],
  "key_offerings": ["Data Center GPUs", "Gaming Graphics", "Professional Visualization", "Automotive AI"],
  "service_footprint": ["Global coverage", "Cloud partnerships", "Developer ecosystem"]
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
        print(f"   - Market coverage details: {len(extracted_data.get('market_coverage_details', []))}")
        print(f"   - Operational metrics: {len(extracted_data.get('operational_metrics_mentioned', []))}")
        print(f"   - Key offerings: {len(extracted_data.get('key_offerings', []))}")
        
        # Test product service chunk generation  
        print("\n🔍 Testing product service chunk generation...")
        chunk_result = generator._generate_growth_investor_chunk(
            company_name="NVIDIA",
            industry="Semiconductors/AI Computing", 
            description="Leading AI computing platform provider with data center, gaming, and automotive solutions",
            extracted_data=extracted_data,
            llm_api_call=mock_llm_api_call
        )
        
        if chunk_result and 'product_service_data' in chunk_result:
            product_data = chunk_result['product_service_data']
            services = product_data.get('services', [])
            coverage_table = product_data.get('coverage_table', [])
            metrics = product_data.get('metrics', {})
            
            print(f"✅ Product service data generated successfully")
            
            # Test services
            if len(services) == 5:
                print(f"✅ Services: {len(services)} (exactly 5 as required)")
                for i, service in enumerate(services):
                    title = service.get('title', 'No title')
                    desc_len = len(service.get('desc', ''))
                    print(f"   - Service {i+1}: {title} ({desc_len} chars)")
            else:
                print(f"⚠️  Services: {len(services)} (should be 5)")
            
            # Test coverage table structure
            if coverage_table and len(coverage_table) > 0:
                headers = coverage_table[0] if coverage_table else []
                data_rows = coverage_table[1:] if len(coverage_table) > 1 else []
                
                print(f"✅ Coverage table: {len(coverage_table)} rows x {len(headers)} columns")
                print(f"   - Headers: {headers}")
                
                # Check if headers are industry-specific (not generic)
                generic_headers = ['region', 'product', 'revenue', 'status']
                is_specific = not any(header.lower() in generic_headers for header in headers)
                
                if is_specific and len(headers) == 4:
                    print("✅ Headers are industry-specific and 4 columns as required")
                elif len(headers) != 4:
                    print(f"⚠️  Headers count: {len(headers)} (should be 4)")
                else:
                    print("⚠️  Headers appear generic, should be industry-specific")
                
                # Check data rows have real content
                if len(data_rows) >= 3:
                    print(f"✅ Data rows: {len(data_rows)} (sufficient coverage)")
                    for i, row in enumerate(data_rows[:3]):
                        print(f"   - Row {i+1}: {row}")
                else:
                    print(f"⚠️  Data rows: {len(data_rows)} (need at least 3)")
            else:
                print("❌ Coverage table is empty")
            
            # Test metrics
            if len(metrics) == 4:
                print(f"✅ Metrics: {len(metrics)} (exactly 4 as required)")
                
                # Check if metrics have specific values (not generic)
                specific_count = 0
                for key, value in metrics.items():
                    has_specific = any(char in str(value) for char in ['$', '%', 'M', 'B', '+', '20', '30'])
                    if has_specific:
                        specific_count += 1
                    print(f"   - {key}: {value}")
                
                if specific_count >= 3:
                    print(f"✅ {specific_count}/4 metrics have specific values")
                else:
                    print(f"⚠️  Only {specific_count}/4 metrics have specific values")
            else:
                print(f"⚠️  Metrics: {len(metrics)} (should be 4)")
        else:
            print("❌ Product service chunk generation failed")
            
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_product_service_extraction()
    if success:
        print("\n🎉 Product service footprint test completed!")
    else:
        print("\n💥 Product service footprint test failed!")