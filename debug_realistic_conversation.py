#!/usr/bin/env python3

"""
Debug script with more realistic conversation flow
Testing what happens when user provides information then says "sufficient. next topic"
"""

# Copy the analyze_conversation_progress function from app.py
def analyze_conversation_progress(messages):
    """SIMPLIFIED: Clean sequential interview progress tracking"""
    
    # The 14 mandatory topics in order
    topics = [
        {
            "id": "business_overview", "position": 1,
            "question": "What is your company name and give me a brief overview of what your business does?",
            "next_question": "Now let's discuss your product/service footprint. What are your main offerings? Please provide the title and description for each product/service. Also, where do you operate geographically and what's your market coverage?"
        },
        {
            "id": "product_service_footprint", "position": 2, 
            "question": "Now let's discuss your product/service footprint. What are your main offerings? Please provide the title and description for each product/service. Also, where do you operate geographically and what's your market coverage?",
            "next_question": "Let's analyze your historical financial performance. Can you provide your revenue, EBITDA, margins, and key financial metrics for the last 3-5 years? I need specific numbers: annual revenue in USD millions, EBITDA figures, margin percentages, growth rates, and key performance drivers. What are the main revenue streams and how have they evolved?"
        },
        {
            "id": "historical_financial_performance", "position": 3,
            "question": "Let's analyze your historical financial performance. Can you provide your revenue, EBITDA, margins, and key financial metrics for the last 3-5 years? I need specific numbers: annual revenue in USD millions, EBITDA figures, margin percentages, growth rates, and key performance drivers. What are the main revenue streams and how have they evolved?",
            "next_question": "Now I need information about your management team. Can you provide names, titles, and brief backgrounds for 4-6 key executives including CEO, CFO, and other senior leaders?"
        }
    ]
    
    # SIMPLIFIED: Count completed topics by analyzing conversation flow
    completed_topics = 0
    satisfaction_responses = ["yes", "ok", "okay", "correct", "satisfied", "good", "right", "sure", "proceed", "continue", "next", "go ahead", "sufficient"]
    
    i = 0
    while i < len(messages):
        msg = messages[i]
        
        print(f"🔍 Processing message {i}: {msg['role']} - {msg['content'][:50]}...")
        
        # Look for AI asking a topic question
        if msg["role"] == "assistant" and ("?" in msg["content"] or "let's" in msg["content"].lower()):
            print(f"  📝 Found AI question at position {i}")
            
            # Case 1: User provides direct answer
            if i + 1 < len(messages) and messages[i + 1]["role"] == "user":
                user_response = messages[i + 1]["content"].lower()
                print(f"  👤 User response: '{user_response}' (length: {len(user_response)})")
                
                # Case 1a: Direct informational response (not research request)
                if "research" not in user_response and len(user_response) > 2:
                    print(f"  ✅ Valid direct response detected")
                    # Check if AI provided research response anyway (automatic research)
                    if (i + 2 < len(messages) and messages[i + 2]["role"] == "assistant" and 
                        len(messages[i + 2]["content"]) > 200):
                        print(f"  🔍 AI provided auto-research, checking for advancement...")
                        # AI provided detailed research response - treat like research completion
                        if (i + 3 < len(messages) and messages[i + 3]["role"] == "user"):
                            next_user_response = messages[i + 3]["content"].lower().strip()
                            print(f"  👤 Next response: '{next_user_response}'")
                            if "next topic" in next_user_response or any(resp in next_user_response for resp in satisfaction_responses):
                                completed_topics += 1
                                print(f"✅ TOPIC {completed_topics} COMPLETED: Auto-research + advancement")
                                i += 4
                                continue
                    else:
                        # Normal direct response without research
                        completed_topics += 1
                        print(f"✅ TOPIC {completed_topics} COMPLETED: Direct response")
                        i += 2
                        continue
                
                # Case 1b: Explicit research request
                elif "research" in user_response:
                    print(f"  🔍 Research request detected")
                    # Look for AI research response + user satisfaction
                    if (i + 2 < len(messages) and messages[i + 2]["role"] == "assistant" and
                        i + 3 < len(messages) and messages[i + 3]["role"] == "user"):
                        satisfaction_response = messages[i + 3]["content"].lower().strip()
                        if any(resp in satisfaction_response for resp in satisfaction_responses):
                            completed_topics += 1
                            print(f"✅ TOPIC {completed_topics} COMPLETED: Research + satisfaction")
                            i += 4
                            continue
        i += 1
    
    # Current position = completed topics + 1 (next topic to ask)
    current_position = min(completed_topics + 1, 14)
    is_complete = current_position > 14
    
    print(f"\n📊 FINAL RESULTS:")
    print(f"   Completed topics: {completed_topics}")
    print(f"   Current position: {current_position}")
    print(f"   Is complete: {is_complete}")
    
    # Build result in format expected by existing code
    result = {
        "current_topic": topics[current_position - 1]["id"] if current_position <= len(topics) else "completed",
        "next_topic": topics[current_position - 1]["id"] if current_position <= len(topics) else "completed", 
        "next_question": topics[current_position - 1]["question"] if current_position <= len(topics) else "Interview complete!",
        "is_complete": is_complete,
        "topics_completed": completed_topics,
        "current_position": current_position,
        "completion_percentage": completed_topics / 14.0,
        "topics_covered": completed_topics,
        "applicable_topics": 14,
        "topics_skipped": 0
    }
    
    print(f"🎯 SIMPLE PROGRESS: {completed_topics} topics completed, asking topic {current_position} ({result['current_topic']})")
    return result

def test_scenario_1():
    """Test: User answers business_overview, then says 'sufficient. next topic'"""
    print("🧪 TEST SCENARIO 1: Basic conversation with 'sufficient. next topic'")
    messages = [
        {
            "role": "assistant",
            "content": "What is your company name and give me a brief overview of what your business does?"
        },
        {
            "role": "user", 
            "content": "prypco - we provide HR software solutions for small businesses"
        },
        {
            "role": "user",
            "content": "sufficient. next topic"
        }
    ]
    
    result = analyze_conversation_progress(messages)
    print(f"📊 Result: Should ask about '{result['current_topic']}'")
    return result

def test_scenario_2():
    """Test: User answers business_overview, AI asks follow-up, user says 'sufficient. next topic'"""
    print("\n🧪 TEST SCENARIO 2: AI follow-up question scenario")
    messages = [
        {
            "role": "assistant",
            "content": "What is your company name and give me a brief overview of what your business does?"
        },
        {
            "role": "user", 
            "content": "prypco - we provide HR software solutions for small businesses"
        },
        {
            "role": "assistant",
            "content": "Can you tell me more about your target customers and geographic coverage?"
        },
        {
            "role": "user",
            "content": "sufficient. next topic"
        }
    ]
    
    result = analyze_conversation_progress(messages)
    print(f"📊 Result: Should ask about '{result['current_topic']}'")
    return result

def test_scenario_3():
    """Test: Business overview -> Product footprint -> Next topic"""
    print("\n🧪 TEST SCENARIO 3: Complete first two topics")
    messages = [
        {
            "role": "assistant",
            "content": "What is your company name and give me a brief overview of what your business does?"
        },
        {
            "role": "user", 
            "content": "prypco - we provide HR software solutions for small businesses"
        },
        {
            "role": "assistant",
            "content": "Now let's discuss your product/service footprint. What are your main offerings?"
        },
        {
            "role": "user", 
            "content": "We have 3 main products: payroll management, employee tracking, and performance reviews"
        },
        {
            "role": "user",
            "content": "sufficient. next topic"
        }
    ]
    
    result = analyze_conversation_progress(messages)
    print(f"📊 Result: Should ask about '{result['current_topic']}'")
    return result

def main():
    """Run all test scenarios"""
    print("🔬 DEBUGGING TOPIC PROGRESSION WITH REALISTIC CONVERSATIONS")
    print("=" * 60)
    
    result1 = test_scenario_1()
    result2 = test_scenario_2() 
    result3 = test_scenario_3()
    
    print("\n📝 SUMMARY:")
    print(f"   Scenario 1 (basic): {result1['current_topic']}")
    print(f"   Scenario 2 (follow-up): {result2['current_topic']}")
    print(f"   Scenario 3 (two topics): {result3['current_topic']}")

if __name__ == "__main__":
    main()