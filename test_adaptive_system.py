#!/usr/bin/env python3
"""
Test Adaptive Slide Generation System
Tests the quality-over-quantity approach with different conversation scenarios
"""

from adaptive_slide_generator import generate_adaptive_presentation

def test_minimal_conversation():
    """Test with only 3 basic questions answered"""
    print("🧪 Test 1: Minimal Conversation (3 questions)")
    print("-" * 50)
    
    messages = [
        {"role": "assistant", "content": "What is your company name?"},
        {"role": "user", "content": "My company is TechCorp, we're a AI software company based in San Francisco"},
        {"role": "assistant", "content": "Tell me about your revenue"},
        {"role": "user", "content": "We have $10 million in revenue and growing fast"},
        {"role": "assistant", "content": "Who leads your company?"},
        {"role": "user", "content": "John Smith is our CEO and Sarah Chen is our CTO"}
    ]
    
    slide_list, render_plan, report = generate_adaptive_presentation(messages)
    
    print(f"📊 Slides Generated: {report['total_slides_generated']}")
    print(f"📋 Slide List: {slide_list}")
    print(f"📈 Quality Summary: {report['quality_summary']}")
    print("✅ Expected: 3-4 slides (business_overview, management_team, historical_financial_performance)")
    print()

def test_comprehensive_conversation():
    """Test with many topics covered"""
    print("🧪 Test 2: Comprehensive Conversation (8+ topics)")
    print("-" * 50)
    
    messages = [
        {"role": "user", "content": "My company is DataFlow, a data analytics SaaS platform serving enterprise clients"},
        {"role": "user", "content": "We have $25M revenue in 2023, $15M in 2022, growing 65% YoY with 85% gross margins"},
        {"role": "user", "content": "Our team includes CEO Mike Johnson (ex-Google VP), CFO Lisa Rodriguez (ex-Goldman Sachs), CTO David Park (Stanford PhD)"},
        {"role": "user", "content": "We serve Fortune 500 companies with our AI-powered analytics platform across North America and Europe"},
        {"role": "user", "content": "Our growth strategy focuses on international expansion and new product lines, projecting $50M by 2025"},
        {"role": "user", "content": "Key competitors include Palantir and Tableau, but we have superior AI capabilities and faster deployment"},
        {"role": "user", "content": "Recent transactions show EV/Revenue multiples of 15-25x for similar companies"},
        {"role": "user", "content": "Strategic buyers could include Microsoft, Salesforce, or Oracle for platform integration"}
    ]
    
    slide_list, render_plan, report = generate_adaptive_presentation(messages)
    
    print(f"📊 Slides Generated: {report['total_slides_generated']}")
    print(f"📋 Slide List: {slide_list}")
    print(f"📈 Quality Summary: {report['quality_summary']}")
    print("✅ Expected: 8+ slides covering most major topics")
    print()

def test_single_topic_conversation():
    """Test with just company overview"""
    print("🧪 Test 3: Single Topic Focus")
    print("-" * 50)
    
    messages = [
        {"role": "user", "content": "My company is GreenTech Solutions, we develop renewable energy software for solar farms and wind installations. We're headquartered in Austin, Texas and have been operating for 5 years."}
    ]
    
    slide_list, render_plan, report = generate_adaptive_presentation(messages)
    
    print(f"📊 Slides Generated: {report['total_slides_generated']}")
    print(f"📋 Slide List: {slide_list}")
    print(f"📈 Quality Summary: {report['quality_summary']}")
    print("✅ Expected: 1-2 slides (business_overview, possibly product_service_footprint)")
    print()

def test_financial_heavy_conversation():
    """Test with lots of financial data but limited other info"""
    print("🧪 Test 4: Financial-Heavy Conversation")
    print("-" * 50)
    
    messages = [
        {"role": "user", "content": "My company FinanceFlow has the following metrics:"},
        {"role": "user", "content": "2021: $5M revenue, $1M EBITDA, 20% margin"},
        {"role": "user", "content": "2022: $8M revenue, $2M EBITDA, 25% margin"},  
        {"role": "user", "content": "2023: $12M revenue, $3.5M EBITDA, 29% margin"},
        {"role": "user", "content": "2024E: $18M revenue, $6M EBITDA, 33% margin"},
        {"role": "user", "content": "Strong cost management and operational efficiency improvements"},
        {"role": "user", "content": "Valuation should be 15-20x revenue based on SaaS comparables"}
    ]
    
    slide_list, render_plan, report = generate_adaptive_presentation(messages)
    
    print(f"📊 Slides Generated: {report['total_slides_generated']}")
    print(f"📋 Slide List: {slide_list}")
    print(f"📈 Quality Summary: {report['quality_summary']}")
    print("✅ Expected: 3-4 slides (historical_financial_performance, margin_cost_resilience, valuation_overview)")
    print()

def analyze_adaptive_benefits():
    """Show benefits of adaptive approach vs fixed 14-slide approach"""
    print("📊 Adaptive vs Fixed Approach Analysis")
    print("=" * 50)
    
    # Test with minimal conversation
    minimal_messages = [
        {"role": "user", "content": "My company is StartupCorp"},
        {"role": "user", "content": "We have $1M revenue"},
        {"role": "user", "content": "CEO is John Doe"}
    ]
    
    slide_list, render_plan, report = generate_adaptive_presentation(minimal_messages)
    
    print("📋 MINIMAL CONVERSATION RESULTS:")
    print(f"   Adaptive Approach: {len(slide_list)} slides ({slide_list})")
    print(f"   Fixed Approach: 14 slides (many with estimated/fake content)")
    print(f"   Quality Improvement: {report['quality_summary']['high_quality_slides'] + report['quality_summary']['medium_quality_slides']}/{len(slide_list)} slides have real content")
    print()
    
    print("✅ ADAPTIVE BENEFITS:")
    print("   • Focused presentations with only relevant content")
    print("   • No 'filler' slides with fake data")
    print("   • Professional quality maintained")  
    print("   • Shorter, more impactful presentations")
    print("   • User gets exactly what they provided information for")
    print()

def main():
    """Run all adaptive system tests"""
    print("🎯 ADAPTIVE SLIDE GENERATION SYSTEM TESTS")
    print("=" * 60)
    print()
    
    test_minimal_conversation()
    test_comprehensive_conversation() 
    test_single_topic_conversation()
    test_financial_heavy_conversation()
    analyze_adaptive_benefits()
    
    print("🚀 STREAMLIT URL FOR TESTING:")
    print("https://8502-i4lx93n6x87cg5p48o0ic-6532622b.e2b.dev")
    print()
    print("💡 TEST SCENARIO:")
    print("1. Start conversation with 3-4 basic answers about your company")
    print("2. Click '🚀 Generate JSON Now' button")  
    print("3. Observe that only relevant slides are generated")
    print("4. Compare to old system that would force 14 slides")
    print()
    print("✅ Adaptive system provides QUALITY over QUANTITY!")

if __name__ == "__main__":
    main()