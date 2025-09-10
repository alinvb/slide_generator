#!/usr/bin/env python3

"""
Test Smart Selective Rendering System
=====================================
Tests that the application generates slides only for topics the user actually discussed,
as per the requirement: "if the user only answers 3 questions then the render plan should only have those 3 topics."

This test simulates a conversation where a user discusses only:
1. Business overview (company name + basic info)
2. Management team (leadership details)
3. Financial performance (revenue, profitability)

Expected result: Only these 3 slides should be in the render plan.
"""

import sys
import os
sys.path.append('/home/user/webapp')

from bulletproof_json_generator import BulletproofJSONGenerator
import json

def test_selective_rendering():
    """Test that only discussed topics generate slides"""
    
    # Simulate a conversation where user only discusses 3 topics
    mock_messages = [
        {"role": "assistant", "content": "What company would you like to create an investment banking presentation for?"},
        {"role": "user", "content": "Netflix"},
        {"role": "assistant", "content": "Great! Can you tell me about Netflix's business model and main services?"},
        {"role": "user", "content": "Netflix is a streaming entertainment service with over 230 million subscribers worldwide. They offer movies, TV shows, and original content through monthly subscriptions."},
        {"role": "assistant", "content": "Who are the key executives and management team members at Netflix?"},
        {"role": "user", "content": "Reed Hastings co-founded Netflix and served as CEO. Ted Sarandos is Co-CEO and Chief Content Officer. Greg Peters is also Co-CEO. Spencer Neumann is the CFO."},
        {"role": "assistant", "content": "What's Netflix's financial performance? Can you share revenue and profitability details?"},
        {"role": "user", "content": "Netflix reported $31.6 billion in revenue for 2022 with $4.5 billion in net income. They have strong cash flow and profitable operations with over 230 million subscribers generating consistent recurring revenue."},
        {"role": "assistant", "content": "Thank you! Let me generate your presentation now."}
    ]

    # All possible slide types (what could be generated)
    all_possible_slides = [
        "business_overview", "management_team", "financial_performance", 
        "growth_strategy", "market_analysis", "competitive_landscape",
        "product_roadmap", "swot_analysis", "risk_factors",
        "esg_initiatives", "technology_infrastructure", "customer_segments",
        "revenue_model", "investment_thesis"
    ]

    # Create bulletproof generator
    generator = BulletproofJSONGenerator()
    
    # Mock LLM function for testing
    def mock_llm_call(messages, model="test", api_key="test", service="test"):
        # Return structured data that matches what the extraction expects
        return json.dumps({
            "company_name": "Netflix",
            "description": "Netflix is a streaming entertainment service with over 230 million subscribers worldwide. They offer movies, TV shows, and original content through monthly subscriptions.",
            "founded": "1997",
            "headquarters": "Los Gatos, California",
            "key_milestones": ["Started as DVD service", "Launched streaming 2007", "Original content 2013"],
            "years": ["2020", "2021", "2022"],
            "revenue_usd_m": [25000, 29700, 31600],
            "ebitda_usd_m": [4500, 6000, 6500],
            "team_members": [
                {"name": "Reed Hastings", "title": "Co-founder and Executive Chairman", "background": "Co-founded Netflix and served as CEO"},
                {"name": "Ted Sarandos", "title": "Co-CEO and Chief Content Officer", "background": "Leads content strategy"},
                {"name": "Greg Peters", "title": "Co-CEO", "background": "Product and technology leadership"},
                {"name": "Spencer Neumann", "title": "CFO", "background": "Chief Financial Officer"}
            ],
            "products_services": ["Streaming video service", "Original content production", "Global entertainment platform"],
            "market_coverage": "Global with 230+ million subscribers",
            "growth_strategies": [],  # Not discussed in detail
            "strategic_buyers": [],   # Not discussed
            "financial_buyers": [],  # Not discussed  
            "transactions": [],      # Not discussed
            "user_preferences": {"exclude_buyers": [], "highlight_areas": []}
        })

    # Test the filtering system
    print("🧪 Testing Smart Selective Rendering...")
    print(f"📊 Mock conversation covers: Business Overview, Management Team, Financial Performance")
    print(f"📋 Total possible slides: {len(all_possible_slides)}")
    
    try:
        # Extract conversation data
        complete_data = generator.extract_conversation_data(mock_messages, mock_llm_call)
        print(f"✅ Data extraction successful")
        
        # Filter slides based on conversation coverage
        covered_slides = generator.filter_slides_by_conversation_coverage(complete_data, all_possible_slides)
        
        print(f"\n📈 RESULTS:")
        print(f"   Slides that should be generated: {len(covered_slides)}")
        print(f"   Slide types: {covered_slides}")
        
        # Verify the expected behavior
        expected_slides = {"business_overview", "management_team", "financial_performance"}
        actual_slides = set(covered_slides)
        
        print(f"\n🎯 VALIDATION:")
        print(f"   Expected slides: {sorted(expected_slides)}")
        print(f"   Actual slides:   {sorted(actual_slides)}")
        
        if actual_slides == expected_slides:
            print(f"   ✅ SUCCESS: Exactly {len(expected_slides)} slides generated as expected!")
            print(f"   ✅ Smart selective rendering is working correctly")
        elif expected_slides.issubset(actual_slides):
            extra_slides = actual_slides - expected_slides
            print(f"   ⚠️  PARTIAL: Expected slides included, but {len(extra_slides)} extra: {extra_slides}")
        else:
            missing_slides = expected_slides - actual_slides
            print(f"   ❌ FAILURE: Missing expected slides: {missing_slides}")
        
        # Test business overview inclusion (should always be there if company name exists)
        if "business_overview" in covered_slides:
            print(f"   ✅ Business overview correctly included (company name: Netflix)")
        else:
            print(f"   ❌ Business overview missing despite company name being provided")
            
        return len(covered_slides) == 3 and actual_slides == expected_slides
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_conversation_coverage_logic():
    """Test the specific logic for determining conversation coverage"""
    print(f"\n🔍 Testing Conversation Coverage Logic...")
    
    generator = BulletproofJSONGenerator()
    
    # Test data with specific patterns
    test_cases = [
        {
            "name": "Management Team Detection",
            "data": {"team_members": ["Reed Hastings", "Ted Sarandos"], "left_column_profiles": ["CEO", "Co-CEO"]},
            "slides": ["management_team"],
            "should_include": ["management_team"]
        },
        {
            "name": "Financial Performance Detection", 
            "data": {"revenue_usd_m": [25000, 29700, 31600], "ebitda_usd_m": [4500, 6000, 6500], "revenue": "31.6B revenue", "net_income": "4.5B net income"},
            "slides": ["financial_performance"],
            "should_include": ["financial_performance"]
        },
        {
            "name": "Empty Data Detection",
            "data": {"growth_strategy": "", "market_analysis": None},
            "slides": ["growth_strategy", "market_analysis"],  
            "should_include": []
        }
    ]
    
    for case in test_cases:
        print(f"\n   Testing: {case['name']}")
        covered = generator.filter_slides_by_conversation_coverage(case["data"], case["slides"])
        expected = case["should_include"]
        
        if set(covered) == set(expected):
            print(f"   ✅ PASS: {covered}")
        else:
            print(f"   ❌ FAIL: Expected {expected}, got {covered}")

if __name__ == "__main__":
    print("=" * 60)
    print("🎯 SMART SELECTIVE RENDERING TEST")
    print("=" * 60)
    print("Testing the core requirement:")
    print('"if the user only answers 3 questions then the render plan should only have those 3 topics"')
    print("=" * 60)
    
    # Run main test
    success = test_selective_rendering()
    
    # Run detailed logic tests  
    test_conversation_coverage_logic()
    
    print(f"\n" + "=" * 60)
    if success:
        print("🎉 OVERALL RESULT: SMART SELECTIVE RENDERING WORKING CORRECTLY!")
        print("✅ System will generate exactly the slides that were discussed")
        print("✅ No filler content or empty slides will be created")
    else:
        print("⚠️  OVERALL RESULT: NEEDS ADJUSTMENT")
        print("❌ System may generate too many or too few slides")
    print("=" * 60)