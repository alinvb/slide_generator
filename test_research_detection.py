#!/usr/bin/env python3

"""
Test if research detection is working in the enhanced conversation handler
"""

import sys
sys.path.append('/home/user/webapp')

def test_research_detection():
    """Test if the enhanced conversation handler detects research requests correctly"""
    
    print("🧪 TESTING RESEARCH DETECTION")
    print("=" * 40)
    
    from enhanced_conversation_handler import create_information_verification_system
    
    # Mock LLM API that should not be called for research requests  
    def mock_llm_api(messages, model, api_key, service):
        print("❌ ERROR: LLM API called for research request - should not happen!")
        return "This should not be returned for research requests"
    
    enhanced_handler = create_information_verification_system()
    
    # Test research detection
    test_cases = [
        "research for me",
        "research this for me", 
        "research this",
        "please research",
        "can you research this topic for me"
    ]
    
    for i, test_message in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}: '{test_message}'")
        
        result = enhanced_handler(
            messages=[],
            current_topic="historical_financial_performance",
            company_name="TestCorp",
            user_message=test_message,
            call_llm_api=mock_llm_api,
            api_key="test",
            api_service="test", 
            selected_model="test"
        )
        
        print(f"   Action: {result['action']}")
        print(f"   Needs Research: {result['needs_research']}")
        print(f"   Response: {result.get('response', 'None')}")
        
        if result['action'] == 'research' and result['needs_research']:
            print("   ✅ CORRECT: Detected as research request")
        else:
            print("   ❌ WRONG: Not detected as research request")

def test_main_app_integration():
    """Test if the main app would handle research correctly"""
    
    print(f"\n🧪 TESTING MAIN APP INTEGRATION")
    print("=" * 40)
    
    # Test the research request pattern matching in main app
    user_message_lower = "research for me"
    
    # This is the pattern from the main app
    research_request = any(phrase in user_message_lower for phrase in [
        "research this", "research for me", "research it", "research yourself",
        "find information", "look up", "investigate", "do research", "search for"
    ])
    
    print(f"User message: '{user_message_lower}'")
    print(f"Research detected: {research_request}")
    
    if research_request:
        print("✅ MAIN APP: Would detect research request")
    else:
        print("❌ MAIN APP: Would NOT detect research request")

if __name__ == "__main__":
    test_research_detection()
    test_main_app_integration()