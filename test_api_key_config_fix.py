#!/usr/bin/env python3
"""
Test script to verify that the new API key configuration resolves the empty JSON issue
"""

import json
import sys
import os

# Import our new configuration system
from config import get_working_api_key, get_default_settings

def test_api_key_configuration():
    """Test that API key is properly configured"""
    print("🔍 Testing API Key Configuration...")
    print("=" * 50)
    
    # Test config system
    settings = get_default_settings()
    api_key = settings['api_key']
    
    print(f"✅ API Key Found: {'*' * len(api_key) if api_key else 'None'}")
    print(f"✅ Model: {settings['model']}")
    print(f"✅ Service: {settings['service']}")
    
    if not api_key:
        print("🚨 FAILED: No API key found!")
        return False
        
    print("✅ SUCCESS: API key properly configured!")
    return True

def test_bulletproof_json_generation():
    """Test JSON generation with properly configured API key"""
    print("\n🔍 Testing Bulletproof JSON Generation...")
    print("=" * 50)
    
    try:
        from bulletproof_json_generator_clean import generate_clean_bulletproof_json
        
        # Use Netflix conversation data for testing
        from create_netflix_conversation_data import create_netflix_conversation
        conversation_messages = create_netflix_conversation()
        
        # Convert messages to text format for the bulletproof generator
        conversation_text = ""
        for msg in conversation_messages:
            role = msg.get('role', '')
            content = msg.get('content', '')
            if role in ['user', 'assistant']:
                conversation_text += f"{role}: {content}\n\n"
        
        print(f"📝 Using Netflix conversation ({len(conversation_text)} chars)")
        
        # Define a minimal LLM call function using our config
        def test_llm_call(messages):
            """Test LLM call using configured API key"""
            from shared_functions import call_llm_api as shared_call_llm_api
            import streamlit as st
            
            # Get API key from our config system
            settings = get_default_settings()
            api_key = settings['api_key']
            model = settings['model'] 
            service = settings['service']
            
            print(f"🔍 [TEST_LLM] Using API key: {'*' * len(api_key) if api_key else 'None'}")
            print(f"🔍 [TEST_LLM] Using model: {model}")
            print(f"🔍 [TEST_LLM] Using service: {service}")
            
            if not api_key:
                print("🚨 [TEST_LLM] NO API KEY - Cannot make real API call")
                return "TEST FALLBACK: API key not configured"
            
            # Make real API call
            try:
                response = shared_call_llm_api(messages, model, api_key, service)
                print(f"✅ [TEST_LLM] Got response: {len(response) if response else 0} chars")
                return response
            except Exception as e:
                print(f"🚨 [TEST_LLM] API call failed: {e}")
                return f"API_ERROR: {str(e)}"
        
        # Generate JSON with real API calls
        print("🚀 Generating JSON with real API calls...")
        
        # Required slides for investment banking presentation
        required_slides = [
            "business_overview", "product_service_footprint", 
            "historical_financial_performance", "management_team",
            "growth_strategy_projections", "competitive_positioning",
            "precedent_transactions", "valuation_overview",
            "strategic_buyers", "financial_buyers", "global_conglomerates",
            "margin_cost_resilience", "investor_considerations", "investor_process_overview"
        ]
        
        content_ir, render_plan = generate_clean_bulletproof_json(
            conversation_messages, 
            required_slides,
            test_llm_call
        )
        
        # Check results
        print(f"\n📊 Results:")
        print(f"✅ Content IR: {len(str(content_ir)) if content_ir else 0} chars")
        print(f"✅ Render Plan: {len(str(render_plan)) if render_plan else 0} chars")
        
        # Check for strategic/financial buyers
        if content_ir and isinstance(content_ir, dict):
            strategic_buyers = content_ir.get('strategic_buyers', [])
            financial_buyers = content_ir.get('financial_buyers', [])
            
            print(f"\n🎯 Strategic Buyers Found: {len(strategic_buyers)}")
            for i, buyer in enumerate(strategic_buyers[:3]):  # Show first 3
                if isinstance(buyer, dict):
                    name = buyer.get('buyer_name', 'Unknown')
                    rationale = buyer.get('strategic_rationale', 'No rationale')[:100]
                    print(f"  {i+1}. {name}: {rationale}...")
            
            print(f"\n💰 Financial Buyers Found: {len(financial_buyers)}")
            for i, buyer in enumerate(financial_buyers[:3]):  # Show first 3
                if isinstance(buyer, dict):
                    name = buyer.get('buyer_name', 'Unknown')
                    rationale = buyer.get('strategic_rationale', 'No rationale')[:100]
                    print(f"  {i+1}. {name}: {rationale}...")
            
            # Check if we got real data vs fallback/demo data
            has_real_data = True
            for buyer in strategic_buyers:
                if isinstance(buyer, dict):
                    rationale = buyer.get('strategic_rationale', '')
                    if 'demo data' in rationale.lower() or 'add api key' in rationale.lower():
                        has_real_data = False
                        break
            
            if has_real_data and (strategic_buyers or financial_buyers):
                print("✅ SUCCESS: Got real buyer data from API calls!")
                return True
            else:
                print("⚠️ WARNING: Still getting fallback/demo data")
                return False
        else:
            print("🚨 FAILED: No valid content_ir generated")
            return False
            
    except Exception as e:
        print(f"🚨 FAILED: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing API Key Configuration Fix")
    print("=" * 60)
    
    # Test 1: API Key Configuration
    config_success = test_api_key_configuration()
    
    if not config_success:
        print("\n❌ OVERALL RESULT: FAILED - API key not configured")
        sys.exit(1)
    
    # Test 2: JSON Generation with Real API Calls
    json_success = test_bulletproof_json_generation()
    
    if json_success:
        print("\n✅ OVERALL RESULT: SUCCESS - API key fix resolved the empty JSON issue!")
        print("🎉 Strategic and financial buyers should now appear in your presentations!")
    else:
        print("\n⚠️ OVERALL RESULT: PARTIAL - API key configured but still issues with JSON generation")
        print("💡 Check the logs above for specific errors")

if __name__ == "__main__":
    main()