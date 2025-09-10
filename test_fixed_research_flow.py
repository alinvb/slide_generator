#!/usr/bin/env python3
"""
Test the fixed research flow to ensure it works properly
"""

import sys
sys.path.append('/home/user/webapp')
from app import analyze_conversation_progress, get_enhanced_interview_response

def test_fixed_research_flow():
    """Test that research requests now work properly"""
    
    print("🧪 TESTING FIXED RESEARCH FLOW")
    print("=" * 50)
    
    # Test Case 1: User requests research for Topic 2
    print("\n📋 Test Case 1: Research request for Product/Service Footprint")
    messages = [
        {"role": "assistant", "content": "What is your company name and give me a brief overview?"},
        {"role": "user", "content": "databricks"},
        {"role": "assistant", "content": "Databricks research response..."},
        {"role": "user", "content": "ok"},
        {"role": "assistant", "content": "Now let's discuss your product/service footprint. What are your main offerings?"},
        {"role": "user", "content": "research this yourself"}
    ]
    
    # Test the enhanced interview response
    try:
        # Mock parameters for testing
        model = "gpt-4"
        api_key = "test_key"
        service = "perplexity"
        
        response = get_enhanced_interview_response(messages, "research this yourself", model, api_key, service)
        
        if response and "satisfied" in response.lower():
            print("   ✅ PASS: Research response includes satisfaction check")
            print(f"   📄 Response preview: {response[:100]}...")
        else:
            print("   ❌ FAIL: Research response missing satisfaction check")
            print(f"   📄 Response: {response}")
            
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
    
    # Test Case 2: After research satisfaction, should move to next topic
    print("\n📋 Test Case 2: After research satisfaction, advance to next topic")
    messages_after_research = [
        {"role": "assistant", "content": "What is your company name and give me a brief overview?"},
        {"role": "user", "content": "databricks"},
        {"role": "assistant", "content": "Databricks research response..."},
        {"role": "user", "content": "ok"},
        {"role": "assistant", "content": "Now let's discuss your product/service footprint. What are your main offerings?"},
        {"role": "user", "content": "research this yourself"},
        {"role": "assistant", "content": "Databricks is a leading data analytics platform... Are you satisfied with this research?"},
        {"role": "user", "content": "yes, satisfied"}
    ]
    
    result = analyze_conversation_progress(messages_after_research)
    next_topic = result.get('next_topic')
    
    if next_topic == 'historical_financial_performance':
        print("   ✅ PASS: Correctly advances to next topic after research satisfaction")
    else:
        print(f"   ❌ FAIL: Expected 'historical_financial_performance', got '{next_topic}'")
    
    print("\n" + "=" * 50)
    print("🎯 RESEARCH FLOW FIX TEST COMPLETE")

if __name__ == "__main__":
    test_fixed_research_flow()