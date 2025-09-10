#!/usr/bin/env python3

"""
Debug the full conversation with detailed step-by-step analysis
"""

import sys
sys.path.append('/home/user/webapp')

def analyze_conversation_debug(messages):
    """Debug version of analyze_conversation_progress with detailed logging"""
    
    # Official topic patterns from the fix
    official_topic_patterns = [
        "what is your company name",  # Topic 1
        "product/service footprint",  # Topic 2  
        "historical financial performance",  # Topic 3
        "management team",  # Topic 4
        "growth strategy and projections",  # Topic 5
        "positioned competitively",  # Topic 6
        "precedent transactions",  # Topic 7
        "valuation methodologies",  # Topic 8
        "strategic buyers",  # Topic 9
        "private equity firms", # Topic 10
        "conglomerates",  # Topic 11
        "margin and cost data",  # Topic 12
        "investor considerations",  # Topic 13
        "investment/acquisition process"  # Topic 14
    ]
    
    completed_topics = 0
    satisfaction_responses = ["yes", "ok", "okay", "correct", "satisfied", "good", "right", "sure", "proceed", "continue", "next", "go ahead", "sufficient"]
    
    print(f"🔍 ANALYZING {len(messages)} MESSAGES")
    print("=" * 50)
    
    i = 0
    while i < len(messages):
        msg = messages[i]
        
        print(f"\n📍 MESSAGE {i}: {msg['role']}")
        print(f"   Content: '{msg['content'][:80]}...'")
        
        if msg["role"] == "assistant":
            # Check if this is an official topic question
            is_official_topic_question = False
            msg_content_lower = msg["content"].lower()
            matched_pattern = None
            
            for pattern in official_topic_patterns:
                if pattern in msg_content_lower:
                    is_official_topic_question = True
                    matched_pattern = pattern
                    print(f"   🎯 OFFICIAL TOPIC QUESTION: Pattern '{pattern}' found")
                    break
            
            if is_official_topic_question:
                # Check for user response
                if i + 1 < len(messages) and messages[i + 1]["role"] == "user":
                    user_response = messages[i + 1]["content"].lower()
                    print(f"   👤 USER RESPONSE: '{user_response}'")
                    
                    # Case 1a: Direct response (not research)
                    if "research" not in user_response and len(user_response) > 2:
                        print(f"   ✅ DIRECT RESPONSE DETECTED")
                        # Check for auto-research
                        if (i + 2 < len(messages) and messages[i + 2]["role"] == "assistant" and 
                            len(messages[i + 2]["content"]) > 200):
                            print(f"   🔍 AUTO-RESEARCH DETECTED (length: {len(messages[i + 2]['content'])})")
                            if (i + 3 < len(messages) and messages[i + 3]["role"] == "user"):
                                next_user_response = messages[i + 3]["content"].lower().strip()
                                print(f"   👤 ADVANCEMENT RESPONSE: '{next_user_response}'")
                                if "next topic" in next_user_response or any(resp in next_user_response for resp in satisfaction_responses):
                                    completed_topics += 1
                                    print(f"   ✅ TOPIC {completed_topics} COMPLETED: Auto-research + advancement")
                                    i += 4
                                    continue
                        else:
                            completed_topics += 1
                            print(f"   ✅ TOPIC {completed_topics} COMPLETED: Direct response")
                            i += 2
                            continue
                    
                    # Case 1b: Research request
                    elif "research" in user_response:
                        print(f"   🔍 RESEARCH REQUEST DETECTED")
                        if (i + 2 < len(messages) and messages[i + 2]["role"] == "assistant" and
                            i + 3 < len(messages) and messages[i + 3]["role"] == "user"):
                            satisfaction_response = messages[i + 3]["content"].lower().strip()
                            print(f"   👤 SATISFACTION RESPONSE: '{satisfaction_response}'")
                            if any(resp in satisfaction_response for resp in satisfaction_responses):
                                completed_topics += 1
                                print(f"   ✅ TOPIC {completed_topics} COMPLETED: Research + satisfaction")
                                i += 4
                                continue
                            else:
                                print(f"   ❌ NO SATISFACTION DETECTED")
                        else:
                            print(f"   ❌ INCOMPLETE RESEARCH PATTERN")
            else:
                print(f"   ⏭️ SKIPPING: Follow-up question, not official topic")
        
        i += 1
    
    print(f"\n📊 FINAL RESULT: {completed_topics} topics completed")
    return completed_topics

def main():
    """Test with the actual conversation"""
    
    # Actual conversation from user's report
    messages = [
        {
            "role": "assistant",
            "content": "What is your company name and give me a brief overview of what your business does?"
        },
        {
            "role": "user", 
            "content": "Nvidia"
        },
        {
            "role": "assistant",
            "content": "Now let's discuss your product/service footprint. What are your main offerings? Please provide the title and description for each product/service. Also, where do you operate geographically and what's your market coverage?"
        },
        {
            "role": "user",
            "content": "research this for me"
        },
        {
            "role": "assistant",
            "content": "Nvidia is the global leader in AI semiconductors, commanding unmatched market share and growth metrics due to soaring demand for its data center and AI products[1][2][4]. Its strategic positioning and technological leadership have propelled its market capitalization past $4 trillion in 2025, underscoring its dominance and relevance in the semiconductor industry[3]. [VERY LONG RESEARCH CONTENT - 1000+ chars]"
        },
        {
            "role": "user",
            "content": "next topic"
        },
        {
            "role": "assistant",
            "content": "Let's analyze your historical financial performance. Can you provide your revenue, EBITDA, margins, and key financial metrics for the last 3-5 years? I need specific numbers: annual revenue in USD millions, EBITDA figures, margin percentages, growth rates, and key performance drivers. What are the main revenue streams and how have they evolved?"
        },
        {
            "role": "user",
            "content": "research this for me"
        },
        {
            "role": "assistant",
            "content": "Thanks for that information! To complete the financial analysis, I additionally need revenue figures and EBITDA margins and growth rates. Do you have this data, or should I research it?"
        }
    ]
    
    completed_topics = analyze_conversation_debug(messages)
    
    print(f"\n🎯 EXPECTED: 2 topics completed (business_overview + product_service_footprint)")
    print(f"🎯 ACTUAL: {completed_topics} topics completed")
    
    if completed_topics == 2:
        print("✅ SUCCESS: Logic is working correctly")
        print("❓ ISSUE: Must be elsewhere in the system")
    else:
        print("❌ ISSUE: Topic completion detection is broken")

if __name__ == "__main__":
    main()