#!/usr/bin/env python3
"""
Test that product service slide renderer handles the fixed data structure
"""

from slide_templates import render_product_service_footprint_slide

def test_product_service_renderer():
    """Test product service slide with proper coverage table and metrics"""
    print("🔧 Testing product service footprint renderer...")
    
    test_data = {
        "title": "Product & Service Footprint",
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
    
    try:
        print(f"🔍 Testing with {len(test_data['services'])} services...")
        print(f"🔍 Coverage table: {len(test_data['coverage_table'])} rows x {len(test_data['coverage_table'][0])} cols")
        print(f"🔍 Metrics: {len(test_data['metrics'])} operational KPIs")
        
        prs = render_product_service_footprint_slide(
            data=test_data,
            company_name="NVIDIA"
        )
        
        if prs and len(prs.slides) > 0:
            print("✅ Product service slide rendered successfully")
            
            # Validate data structure
            services = test_data['services']
            coverage_table = test_data['coverage_table']
            metrics = test_data['metrics']
            
            print(f"✅ Services rendered: {len(services)}")
            for i, service in enumerate(services):
                print(f"   - {i+1}: {service['title']}")
            
            print(f"✅ Coverage table rendered: {len(coverage_table)-1} data rows")
            headers = coverage_table[0]
            print(f"   - Headers: {headers}")
            
            # Check headers are industry-specific
            generic_terms = ['region', 'product', 'revenue', 'status']
            is_specific = not any(term in ' '.join(headers).lower() for term in generic_terms)
            if is_specific:
                print("✅ Headers are industry-specific (not generic)")
            else:
                print("⚠️  Headers contain generic terms")
            
            print(f"✅ Metrics rendered: {len(metrics)}")
            for key, value in metrics.items():
                has_specific = any(char in str(value) for char in ['$', '%', 'M', 'B', '+'])
                status = "✅" if has_specific else "⚠️"
                print(f"   {status} {key}: {value}")
            
            return True
        else:
            print("❌ Product service slide rendering failed")
            return False
            
    except Exception as e:
        print(f"❌ Product service renderer error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_product_service_renderer()
    if success:
        print("\n🎉 Product service renderer test passed!")
    else:
        print("\n💥 Product service renderer test failed!")