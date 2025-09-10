#!/usr/bin/env python3

"""
Enhanced conversation handler with information verification and intelligent follow-ups
"""

def create_information_verification_system():
    """
    Create an intelligent conversation system that:
    1. Verifies user-provided information
    2. Responds with correctness assessment  
    3. Asks intelligent follow-up questions
    4. Handles user choices (provide more info OR research)
    """
    
    def verify_and_followup_prompt(topic, user_info, company_name):
        """Create a prompt for information verification and intelligent follow-up"""
        
        return f"""You are a senior investment banking analyst conducting a thorough pitch deck interview. 

CURRENT TOPIC: {topic}
COMPANY: {company_name}
USER PROVIDED: {user_info}

YOUR TASK - INTELLIGENT VERIFICATION & FOLLOW-UP:

1. VERIFICATION PHASE:
   - Fact-check the provided information for accuracy
   - Cross-reference with known industry data if applicable
   - Identify any obvious errors or inconsistencies

2. ASSESSMENT RESPONSE:
   - Start with verification: "That's correct" OR "Actually, there's an issue with..."
   - If incorrect, politely correct with accurate information
   - If partially correct, acknowledge the correct parts

3. INTELLIGENT FOLLOW-UP:
   - Identify what additional information is needed for this topic
   - Ask specific, targeted questions for missing details
   - Be thorough but not overwhelming (2-3 key questions max)

4. INTELLIGENT FOLLOW-UP ONLY:
   - Ask for specific missing information needed for this topic
   - Be direct and focused on what's needed
   - Do NOT offer research options (this prevents infinite loops)

EXAMPLE RESPONSE FORMAT:
"That's correct - [company] does operate in those markets. However, I notice you mentioned [specific detail to verify/correct]. 

For a complete analysis, I also need:
- [Specific question 1]
- [Specific question 2] 
- [Specific question 3]

Please provide these additional details when you're ready."

BE PROFESSIONAL, ACCURATE, AND HELPFUL. MAINTAIN INVESTMENT BANKING STANDARDS.
"""

    def enhanced_conversation_handler(messages, current_topic, company_name, user_message, call_llm_api, api_key, api_service, selected_model):
        """
        Enhanced conversation handler with verification and follow-ups
        
        Args:
            messages: Conversation history
            current_topic: Current interview topic
            company_name: Company being discussed
            user_message: User's latest message
            call_llm_api: LLM API function
            api_key: API key
            api_service: API service
            selected_model: Model to use
            
        Returns:
            dict: {
                'response': AI response text,
                'action': 'verification' | 'research' | 'advancement' | 'clarification',
                'needs_research': bool,
                'topic_complete': bool
            }
        """
        
        user_lower = user_message.lower().strip()
        
        # Check for explicit research request
        if any(phrase in user_lower for phrase in ["research for me", "research this", "please research", "research it", "do research", "find information"]):
            return {
                'response': None,  # Will trigger research flow
                'action': 'research',
                'needs_research': True,
                'topic_complete': False
            }
        
        # Check for topic advancement
        if any(phrase in user_lower for phrase in ["next topic", "sufficient. next topic", "move on"]):
            return {
                'response': None,  # Will trigger advancement flow
                'action': 'advancement', 
                'needs_research': False,
                'topic_complete': True
            }
        
        # Check if this looks like informational input (not a question)
        is_informational_input = (
            len(user_message) > 10 and
            not user_message.strip().endswith('?') and
            not user_lower.startswith(('how', 'what', 'where', 'when', 'why', 'who', 'can you', 'could you', 'would you'))
        )
        
        if is_informational_input:
            # This is information provided by user - verify and follow up
            verification_prompt = verify_and_followup_prompt(current_topic, user_message, company_name)
            
            try:
                # Create messages for verification
                verification_messages = [
                    {"role": "system", "content": verification_prompt},
                    {"role": "user", "content": f"Please verify this information and provide intelligent follow-up questions: {user_message}"}
                ]
                
                # Get verification response
                verification_response = call_llm_api(
                    verification_messages,
                    selected_model,
                    api_key, 
                    api_service
                )
                
                return {
                    'response': verification_response,
                    'action': 'verification',
                    'needs_research': False,
                    'topic_complete': False
                }
                
            except Exception as e:
                print(f"❌ [VERIFICATION] Error: {str(e)}")
                return {
                    'response': f"Thank you for that information about {company_name}. Could you provide more details about this topic, or would you like me to research this for you?",
                    'action': 'clarification',
                    'needs_research': False, 
                    'topic_complete': False
                }
        
        else:
            # This looks like a question or request - handle naturally
            try:
                # Create natural conversation prompt
                conversation_context = " ".join([msg["content"] for msg in messages[-3:]])
                
                natural_messages = [
                    {"role": "system", "content": f"You are a senior investment banking advisor discussing {current_topic} for {company_name}. Respond naturally and professionally to the user's question or request. Stay focused on the current topic."},
                    {"role": "user", "content": f"Context: We're discussing {current_topic} for {company_name}.\n\nUser said: {user_message}\n\nPlease respond helpfully and ask relevant follow-up questions if needed."}
                ]
                
                natural_response = call_llm_api(
                    natural_messages,
                    selected_model,
                    api_key,
                    api_service  
                )
                
                return {
                    'response': natural_response,
                    'action': 'clarification',
                    'needs_research': False,
                    'topic_complete': False
                }
                
            except Exception as e:
                print(f"❌ [NATURAL RESPONSE] Error: {str(e)}")
                return {
                    'response': f"I understand you're asking about {current_topic}. Could you provide more specific information, or would you like me to research this topic for you?",
                    'action': 'clarification', 
                    'needs_research': False,
                    'topic_complete': False
                }
    
    return enhanced_conversation_handler

# Example usage and testing
if __name__ == "__main__":
    print("🧪 TESTING ENHANCED CONVERSATION HANDLER")
    print("=" * 50)
    
    # Mock LLM API for testing
    def mock_llm_api(messages, model, api_key, service):
        user_content = messages[-1]["content"] 
        if "verify this information" in user_content:
            return "That's correct - Apple does generate significant services revenue. However, for a complete analysis, I also need: What's the breakdown by service type (App Store vs iCloud vs Apple Music)? What are the growth rates for each service? What's the geographic distribution of services revenue? You can provide more details, or if you'd prefer, say 'research for me' and I'll gather comprehensive information on this topic."
        else:
            return "Thank you for that question. Let me provide some context and ask for additional details we need for the pitch deck analysis."
    
    # Create handler
    handler = create_information_verification_system()
    
    # Test scenarios
    test_cases = [
        {
            "user_message": "Apple generates $85 billion in services revenue annually",
            "expected_action": "verification"
        },
        {
            "user_message": "research for me", 
            "expected_action": "research"
        },
        {
            "user_message": "next topic",
            "expected_action": "advancement"
        },
        {
            "user_message": "What about their geographic breakdown?",
            "expected_action": "clarification"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}: '{test['user_message']}'")
        
        result = handler(
            messages=[],
            current_topic="product_service_footprint", 
            company_name="Apple",
            user_message=test["user_message"],
            call_llm_api=mock_llm_api,
            api_key="test",
            api_service="test",
            selected_model="test"
        )
        
        print(f"   Action: {result['action']}")
        print(f"   Expected: {test['expected_action']}")
        print(f"   Match: {'✅' if result['action'] == test['expected_action'] else '❌'}")
        
        if result['response']:
            print(f"   Response: {result['response'][:100]}...")
    
    print(f"\n✅ Enhanced conversation handler ready for integration!")