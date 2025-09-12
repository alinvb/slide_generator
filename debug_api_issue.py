#!/usr/bin/env python3
"""
Debug why API calls are failing and JSON remains empty
"""

import os
import sys
from bulletproof_json_generator_clean import CleanBulletproofJSONGenerator

def test_simple_extraction():
    """Test with a simple conversation to debug API issues"""
    
    print("🐛 DEBUGGING API ISSUE - WHY JSON IS EMPTY")
    print("=" * 60)
    
    # Simple test conversation with strategic buyers mentioned
    test_messages = [
        {
            "role": "user", 
            "content": "I want to analyze TechFlow for acquisition. Strategic buyers include Microsoft and Salesforce. Financial buyers are Vista Equity and Thoma Bravo. Revenue is $50M growing 30%. Management team has CEO John Smith from Oracle."
        }
    ]
    
    print("💬 TEST CONVERSATION:")
    print(f"   '{test_messages[0]['content'][:100]}...'")
    
    # Create a mock LLM API function to test extraction logic
    def mock_llm_api_call(messages):
        """Mock LLM call that returns a proper JSON response"""
        return '''
        {
            "company_name": "TechFlow",
            "business_description_detailed": "Technology company being analyzed for acquisition",
            "strategic_buyers_mentioned": ["Microsoft", "Salesforce"],
            "financial_buyers_mentioned": ["Vista Equity Partners", "Thoma Bravo"],
            "annual_revenue_usd_m": [50],
            "revenue_growth_rates": ["30%"],
            "management_team_detailed": ["CEO John Smith (ex-Oracle)"],
            "valuation_estimates_mentioned": [],
            "dcf_valuation_mentioned": [],
            "comparable_company_valuation": [],
            "precedent_transaction_valuation": []
        }
        '''
    
    # Test the extraction
    try:
        generator = CleanBulletproofJSONGenerator()
        
        print("\n🤖 TESTING CONVERSATION EXTRACTION...")
        result = generator.extract_conversation_data(test_messages, mock_llm_api_call)
        
        print("\n📊 EXTRACTION RESULT:")
        if result:
            print("   ✅ SUCCESS: Data extracted!")
            for key, value in result.items():
                print(f"      {key}: {value}")
        else:
            print("   ❌ FAILED: No data extracted")
            
    except Exception as e:
        print(f"   💥 ERROR: {e}")
        import traceback
        traceback.print_exc()

def check_api_configuration():
    """Check if API keys are properly configured"""
    
    print(f"\n🔑 CHECKING API CONFIGURATION")
    print("=" * 40)
    
    # Check environment variables
    perplexity_key = os.getenv('PERPLEXITY_API_KEY', '')
    
    print(f"📋 API KEY STATUS:")
    if perplexity_key:
        print(f"   ✅ PERPLEXITY_API_KEY: {'*' * (len(perplexity_key) - 4) + perplexity_key[-4:]}")
    else:
        print(f"   ❌ PERPLEXITY_API_KEY: Not found")
    
    # Check if shared_functions has working API call
    try:
        from shared_functions import llm_api_call
        print(f"   ✅ llm_api_call function: Available")
        
        # Test a simple API call
        print(f"\n🧪 TESTING SIMPLE API CALL...")
        test_response = llm_api_call([{"role": "user", "content": "Say 'API working' if you can respond"}])
        if test_response and len(test_response) > 0:
            print(f"   ✅ API Response: {test_response[:50]}...")
        else:
            print(f"   ❌ API Response: Empty or failed")
            
    except Exception as e:
        print(f"   ❌ llm_api_call function: {e}")

def diagnose_empty_json_issue():
    """Diagnose why the JSON is coming back empty"""
    
    print(f"\n🔍 DIAGNOSING EMPTY JSON ISSUE")
    print("=" * 50)
    
    # The JSON you showed
    empty_json_example = {
        "strategic_buyers": [],
        "financial_buyers": [], 
        "management_team": {"left_column_profiles": [], "right_column_profiles": []},
        "valuation_data": [],
        "business_overview_data": {"description": "", "highlights": []},
        "competitive_analysis": {"competitors": [], "assessment": [], "barriers": [], "advantages": []}
    }
    
    print("❌ PROBLEM IDENTIFIED:")
    print("   • All arrays are empty []")
    print("   • All descriptions are empty strings")
    print("   • Only basic revenue/EBITDA numbers populated")
    
    print(f"\n🔍 LIKELY CAUSES:")
    print(f"   1. API calls failing silently")
    print(f"   2. Conversation extraction not running")
    print(f"   3. Research generation not working")
    print(f"   4. Fallback data not being used")
    print(f"   5. JSON structure mapping issues")
    
    print(f"\n💡 DEBUGGING STEPS:")
    print(f"   1. Test API key configuration")
    print(f"   2. Test simple conversation extraction")
    print(f"   3. Check if research generation is called")
    print(f"   4. Verify fallback data population")
    print(f"   5. Test end-to-end JSON generation")

if __name__ == "__main__":
    check_api_configuration()
    test_simple_extraction()
    diagnose_empty_json_issue()
    
    print(f"\n🎯 NEXT ACTIONS:")
    print(f"   1. Fix API configuration if keys missing")
    print(f"   2. Test actual conversation extraction with real API")
    print(f"   3. Ensure research generation populates all fields")
    print(f"   4. Verify bulletproof generator covers all JSON sections")