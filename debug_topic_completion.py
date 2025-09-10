#!/usr/bin/env python3

def debug_topic_completion():
    """Debug the topic completion detection logic step by step"""
    
    print("🔍 DEBUGGING TOPIC COMPLETION LOGIC")
    print("=" * 60)
    
    messages = [
        {"role": "assistant", "content": "What is your company name and give me a brief overview of what your business does?"},
        {"role": "user", "content": "prypco"},  
        {"role": "assistant", "content": "PRYPCO, founded in 2022 by Amira Sajwani, is a proptech company based in the UAE that's reshaping real estate accessibility and investment. Their platform spans the full real estate lifecycle..."},  
        {"role": "user", "content": "next topic"}  
    ]
    
    print("=== CONVERSATION MESSAGES ===")
    for i, msg in enumerate(messages):
        role = msg["role"]
        content = msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
        print(f"{i}: {role.upper()}: {content}")
    
    # Simulate the logic step by step
    print(f"\n=== SIMULATING TOPIC DETECTION LOGIC ===")
    
    completed_topics = 0
    satisfaction_responses = ["yes", "ok", "okay", "correct", "satisfied", "good", "right", "sure", "proceed", "continue", "next", "go ahead"]
    
    i = 0
    while i < len(messages):
        msg = messages[i]
        print(f"\n--- Processing message {i}: {msg['role']} ---")
        
        # Look for AI asking a topic question
        if msg["role"] == "assistant" and ("?" in msg["content"] or "let's" in msg["content"].lower()):
            print(f"✓ Found assistant question at index {i}")
            
            # Case 1: User provides direct answer
            if i + 1 < len(messages) and messages[i + 1]["role"] == "user":
                user_response = messages[i + 1]["content"].lower()
                print(f"✓ Found user response at index {i+1}: '{user_response}'")
                
                # Case 1a: Direct informational response (not research request)
                if "research" not in user_response and len(user_response) > 10:
                    print(f"✗ User response is NOT a research request, length = {len(user_response)}")
                    
                    # Check if AI provided research response anyway (automatic research)
                    if (i + 2 < len(messages) and messages[i + 2]["role"] == "assistant" and 
                        len(messages[i + 2]["content"]) > 200):
                        print(f"✓ AI provided detailed research response at index {i+2}, length = {len(messages[i+2]['content'])}")
                        
                        # Check for advancement request
                        if (i + 3 < len(messages) and messages[i + 3]["role"] == "user"):
                            next_user_response = messages[i + 3]["content"].lower().strip()
                            print(f"✓ Found next user response at index {i+3}: '{next_user_response}'")
                            
                            if "next topic" in next_user_response or any(resp in next_user_response for resp in satisfaction_responses):
                                completed_topics += 1
                                print(f"✅ TOPIC {completed_topics} COMPLETED: Auto-research + advancement")
                                i += 4
                                continue
                            else:
                                print(f"✗ Next user response doesn't indicate completion")
                        else:
                            print(f"✗ No next user response found")
                    else:
                        print(f"✗ No detailed AI research response found")
                        # Normal direct response without research
                        completed_topics += 1
                        print(f"✅ TOPIC {completed_topics} COMPLETED: Direct response")
                        i += 2
                        continue
                        
                elif "research" in user_response:
                    print(f"✓ User response IS a research request")
                    # Handle explicit research request logic...
                else:
                    print(f"✗ User response too short: length = {len(user_response)}")
        
        i += 1
    
    print(f"\n=== FINAL RESULTS ===")
    print(f"Topics completed: {completed_topics}")
    print(f"Current position should be: {completed_topics + 1}")
    
    # Test with actual function
    print(f"\n=== ACTUAL FUNCTION RESULTS ===")
    from app import analyze_conversation_progress
    result = analyze_conversation_progress(messages)
    print(f"Function says topics completed: {result.get('topics_completed')}")
    print(f"Function says current position: {result.get('current_position')}")

if __name__ == "__main__":
    debug_topic_completion()