#!/usr/bin/env python3

"""
Debug script to reproduce the research request infinite loop at Topic 3
"""

def mock_call_llm_api(messages, model, api_key, service):
    """Mock LLM API that simulates the problematic response"""
    user_content = messages[-1]["content"]
    
    if "verify this information" in user_content.lower():
        # This is what's causing the loop - the verification response includes the research offer
        return "Thanks for that information! To complete the financial analysis, I additionally need revenue figures and EBITDA margins and growth rates. Do you have this data, or should I research it?"
    else:
        return "Mock LLM response"

def simulate_topic_3_conversation():
    """Simulate the exact conversation flow that causes the infinite loop"""
    
    print("🔍 DEBUGGING TOPIC 3 RESEARCH REQUEST INFINITE LOOP")
    print("=" * 60)
    
    # Import the enhanced conversation handler
    from enhanced_conversation_handler import create_information_verification_system
    enhanced_handler = create_information_verification_system()
    
    # Simulate conversation state
    messages = [
        {"role": "assistant", "content": "What is your company's historical financial performance? Please provide revenue figures, growth rates, and EBITDA margins for the past 3-5 years."},
        {"role": "user", "content": "We generated $10M revenue last year"}
    ]
    
    current_topic = "historical_financial_performance"
    company_name = "TestCompany"
    user_message = "research for me"
    
    print(f"📊 Current Topic: {current_topic}")
    print(f"🏢 Company: {company_name}")
    print(f"💬 User Message: '{user_message}'")
    print(f"📝 Conversation Length: {len(messages)} messages")
    
    print("\n🧪 TESTING ENHANCED CONVERSATION HANDLER:")
    print("-" * 40)
    
    # Test the enhanced conversation handler
    result = enhanced_handler(
        messages=messages,
        current_topic=current_topic,
        company_name=company_name,
        user_message=user_message,
        call_llm_api=mock_call_llm_api,
        api_key="test",
        api_service="test",
        selected_model="test"
    )
    
    print(f"Action: {result['action']}")
    print(f"Needs Research: {result['needs_research']}")
    print(f"Response: {result['response']}")
    
    if result['action'] == 'research':
        print("\n✅ RESEARCH REQUEST DETECTED CORRECTLY")
        print("🔍 Should trigger research flow in main app")
    else:
        print("\n❌ RESEARCH REQUEST NOT DETECTED")
        print("🔍 This would cause fallback to verification flow")
    
    print("\n" + "=" * 60)
    
    # Now simulate the verification flow that might be causing the loop
    print("🧪 TESTING VERIFICATION FLOW (POTENTIAL LOOP CAUSE):")
    print("-" * 40)
    
    # Simulate what happens if the user provides information first
    verification_result = enhanced_handler(
        messages=messages,
        current_topic=current_topic, 
        company_name=company_name,
        user_message="We had $10M revenue with 25% EBITDA margins",  # Information input
        call_llm_api=mock_call_llm_api,
        api_key="test",
        api_service="test", 
        selected_model="test"
    )
    
    print(f"Action: {verification_result['action']}")
    print(f"Response: {verification_result['response']}")
    
    if verification_result['action'] == 'verification' and verification_result['response']:
        print(f"\n🔄 VERIFICATION RESPONSE INCLUDES: 'should I research it?'")
        print(f"📝 This response is added to conversation")
        print(f"🔄 User then says 'research for me' again...")
        print(f"🔁 INFINITE LOOP DETECTED: System keeps asking same question!")
    
    print("\n" + "=" * 60)
    print("🎯 CONCLUSION: The issue is in the verification flow integration")
    print("🔧 SOLUTION: Need to prevent verification responses that ask about research")

if __name__ == "__main__":
    simulate_topic_3_conversation()