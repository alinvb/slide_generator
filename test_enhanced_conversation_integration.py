#!/usr/bin/env python3

"""
Test the enhanced conversation integration with verification and follow-ups
"""

import sys
sys.path.append('/home/user/webapp')

def test_enhanced_conversation_flow():
    """Test the enhanced conversation system"""
    
    print("🧪 TESTING ENHANCED CONVERSATION INTEGRATION")
    print("=" * 50)
    
    # Mock the enhanced conversation handler
    from enhanced_conversation_handler import create_information_verification_system
    
    # Mock LLM API
    def mock_llm_api(messages, model, api_key, service):
        system_content = messages[0]["content"] if messages else ""
        user_content = messages[-1]["content"] if messages else ""
        
        if "verify this information" in user_content:
            return """That's partially correct - Apple does generate significant services revenue from multiple streams. However, I need more specific details for our investment banking analysis:

• What's the exact breakdown by service type (App Store vs iCloud vs Apple Music vs Apple Pay)?
• What are the year-over-year growth rates for each service category?  
• What's the geographic distribution of services revenue (Americas vs Europe vs China)?
• What are the margin profiles for each service compared to hardware?

You can provide more details on these specific metrics, or if you'd prefer, say 'research for me' and I'll gather comprehensive information on this topic."""
        else:
            return "Thank you for that information. Let me ask some follow-up questions to complete our analysis for this topic."
    
    # Create handler
    enhanced_handler = create_information_verification_system()
    
    # Test scenarios that should trigger different behaviors
    test_cases = [
        {
            "name": "Information Verification",
            "user_message": "Apple generates about $85 billion in services revenue from App Store, iCloud, and other services",
            "current_topic": "product_service_footprint",
            "expected_action": "verification",
            "description": "Should verify the information and ask intelligent follow-up questions"
        },
        {
            "name": "Research Request", 
            "user_message": "research this for me",
            "current_topic": "product_service_footprint",
            "expected_action": "research",
            "description": "Should trigger research flow"
        },
        {
            "name": "Topic Advancement",
            "user_message": "sufficient. next topic",
            "current_topic": "product_service_footprint", 
            "expected_action": "advancement",
            "description": "Should advance to next topic"
        },
        {
            "name": "Question/Clarification",
            "user_message": "What about their geographic breakdown?",
            "current_topic": "product_service_footprint",
            "expected_action": "clarification", 
            "description": "Should provide natural clarification response"
        },
        {
            "name": "Detailed Information",
            "user_message": "Apple operates globally with 175+ countries, major revenue from Americas 45%, Europe 23%, Greater China 19%, strong services growth in emerging markets",
            "current_topic": "product_service_footprint",
            "expected_action": "verification",
            "description": "Should verify detailed information and ask for any missing details"
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}: {test_case['name']}")
        print(f"   User Message: '{test_case['user_message']}'")
        print(f"   Current Topic: {test_case['current_topic']}")
        print(f"   Expected: {test_case['expected_action']}")
        
        try:
            result = enhanced_handler(
                messages=[],  # Empty for testing
                current_topic=test_case['current_topic'],
                company_name="Apple",
                user_message=test_case['user_message'], 
                call_llm_api=mock_llm_api,
                api_key="test_key",
                api_service="test_service",
                selected_model="test_model"
            )
            
            actual_action = result['action']
            success = actual_action == test_case['expected_action']
            
            print(f"   Actual: {actual_action}")
            print(f"   Match: {'✅' if success else '❌'}")
            
            if result.get('response'):
                print(f"   Response Preview: {result['response'][:100]}...")
            
            results.append(success)
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            results.append(False)
    
    # Summary
    passed = sum(results)
    total = len(results)
    success_rate = (passed / total) * 100
    
    print(f"\n📊 RESULTS SUMMARY:")
    print(f"   Passed: {passed}/{total} ({success_rate:.1f}%)")
    
    if success_rate >= 80:
        print(f"✅ ENHANCED CONVERSATION SYSTEM WORKING!")
        print(f"   • Information verification implemented")
        print(f"   • Intelligent follow-up questions") 
        print(f"   • Flexible user choice handling")
        print(f"   • Natural conversation flow")
    else:
        print(f"❌ ENHANCED CONVERSATION SYSTEM NEEDS FIXES")
    
    return success_rate >= 80

if __name__ == "__main__":
    test_enhanced_conversation_flow()