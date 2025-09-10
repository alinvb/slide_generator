#!/usr/bin/env python3

"""
Debug the research completion detection logic
"""

def test_research_pattern():
    """Test the specific research completion pattern"""
    
    # The exact pattern from the conversation
    messages = [
        # Topic 2 question (index 2)
        {
            "role": "assistant",
            "content": "Now let's discuss your product/service footprint. What are your main offerings? Please provide the title and description for each product/service. Also, where do you operate geographically and what's your market coverage?"
        },
        # User research request (index 3) 
        {
            "role": "user",
            "content": "research this for me"
        },
        # AI research response (index 4) - long content
        {
            "role": "assistant",
            "content": "Nvidia is the global leader in AI semiconductors, commanding unmatched market share and growth metrics due to soaring demand for its data center and AI products. [1000+ chars of research content]"
        },
        # User satisfaction/advancement (index 5)
        {
            "role": "user",
            "content": "next topic"
        }
    ]
    
    print("🔍 TESTING RESEARCH COMPLETION PATTERN")
    print("=" * 40)
    
    satisfaction_responses = ["yes", "ok", "okay", "correct", "satisfied", "good", "right", "sure", "proceed", "continue", "next", "go ahead", "sufficient"]
    
    # Test the current logic
    i = 0  # Starting at the topic question
    print(f"📝 Topic question at index {i}: '{messages[i]['content'][:50]}...'")
    
    if i + 1 < len(messages) and messages[i + 1]["role"] == "user":
        user_response = messages[i + 1]["content"].lower()
        print(f"👤 User response at index {i + 1}: '{user_response}'")
        
        if "research" in user_response:
            print("🔍 Research request detected!")
            
            # Current logic check
            if (i + 2 < len(messages) and messages[i + 2]["role"] == "assistant" and
                i + 3 < len(messages) and messages[i + 3]["role"] == "user"):
                
                satisfaction_response = messages[i + 3]["content"].lower().strip()
                print(f"📊 Satisfaction response at index {i + 3}: '{satisfaction_response}'")
                
                if any(resp in satisfaction_response for resp in satisfaction_responses):
                    print("✅ TOPIC COMPLETION: Research + satisfaction detected!")
                    return True
                else:
                    print(f"❌ TOPIC INCOMPLETE: '{satisfaction_response}' not in satisfaction responses")
                    print(f"📋 Satisfaction responses: {satisfaction_responses}")
                    return False
            else:
                print("❌ PATTERN INCOMPLETE: Missing AI response or user satisfaction")
                return False
    
    return False

def main():
    """Test the research completion logic"""
    result = test_research_pattern()
    print(f"\n🎯 RESULT: {'✅ WORKING' if result else '❌ BROKEN'}")

if __name__ == "__main__":
    main()