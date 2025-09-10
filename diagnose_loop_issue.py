#!/usr/bin/env python3

def diagnose_conversation_loop():
    """Diagnose why the system is stuck in a loop asking the first question"""
    
    print("=== DIAGNOSING CONVERSATION LOOP ISSUE ===")
    
    # This represents the actual conversation that's looping
    messages = [
        {"role": "assistant", "content": "What is your company name and give me a brief overview of what your business does?"},
        {"role": "user", "content": "alibaba group"},
        {"role": "assistant", "content": "Alibaba Group's product and service footprint is vast..."},
        {"role": "user", "content": "next topic"},
        {"role": "assistant", "content": "What is your company name and give me a brief overview of what your business does?"}
    ]
    
    from app import analyze_conversation_progress
    
    # Test the progression logic
    result = analyze_conversation_progress(messages)
    print(f"Topics completed: {result.get('topics_completed')}")
    print(f"Current position: {result.get('current_position')}")
    print(f"Current topic: {result.get('current_topic')}")
    
    return result

if __name__ == "__main__":
    diagnose_conversation_loop()