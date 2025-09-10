#!/usr/bin/env python3
"""
Debug the exact Netflix conversation flow to see where SWOT comes from
"""

import sys
sys.path.append('/home/user/webapp')

from app import analyze_conversation_progress, get_enhanced_interview_response

def debug_netflix_flow():
    print("🔍 Debugging Netflix SWOT Issue - Exact Flow Analysis")
    print("=" * 70)
    
    # The EXACT conversation from user where SWOT appeared
    messages = [
        {"role": "system", "content": "Investment banking system prompt..."},
        {"role": "assistant", "content": "What is your company name and give me a brief overview of what your business does?"},
        {"role": "user", "content": "Netflix - leading streaming service"},
        {"role": "assistant", "content": "Now let's discuss your product/service footprint..."},
        {"role": "user", "content": "research this yourself"},
        {"role": "assistant", "content": "Netflix's ability to deliver timely, culturally relevant, and genre-spanning content has solidified its status as the leading streaming service globally, with a strong presence in both original production and content licensing. Are you satisfied with this research, or would you like me to investigate any specific areas further?"},
        {"role": "user", "content": "ok"},
        {"role": "assistant", "content": "Let's analyze your historical financial performance..."},
        {"role": "user", "content": "research this yourself"},
        {"role": "assistant", "content": "Netflix's historical financial performance from 2021 to 2025 demonstrates robust growth... Are you satisfied with this research, or would you like me to investigate any specific areas further?"},
        {"role": "user", "content": "ok"}
    ]
    
    print("📊 Analyzing what should happen after user says 'ok' to financial research...")
    progress_info = analyze_conversation_progress(messages)
    
    print(f"🎯 Current Topic: {progress_info.get('current_topic', 'UNKNOWN')}")
    print(f"🎯 Next Topic: {progress_info.get('next_topic', 'UNKNOWN')}")
    print(f"📝 Next Question Preview: {progress_info.get('next_question', 'NONE')[:150]}...")
    
    print("\n📋 Topics Coverage Status:")
    topics_info = progress_info.get('topics', {})
    for topic_name in ['business_overview', 'product_service_footprint', 'historical_financial_performance', 'management_team']:
        if topic_name in topics_info:
            covered = topics_info[topic_name].get('covered', False)
            position = topics_info[topic_name].get('position', 0)
            status = "✅ COVERED" if covered else "❌ NOT COVERED"
            print(f"  {position}. {topic_name:<35} {status}")
    
    print(f"\n🔍 Is Interview Complete: {progress_info.get('is_complete', False)}")
    
    # Check what the enhanced interview response would generate
    print("\n" + "="*70)
    print("🤖 Testing Enhanced Interview Response Generation...")
    
    # This simulates what happens when user says "ok" after research
    try:
        # Mock the enhanced response function parameters
        user_message = "ok"
        model = "llama-3.1-sonar-large-128k-online"
        api_key = "mock"
        service = "perplexity"
        
        print(f"📝 User Message: '{user_message}'")
        print(f"🧠 Expected Behavior: Should ask about management team next")
        
        # Check if it's a brief confirmatory response
        brief_confirmatory = user_message.strip().lower() in ["yes", "correct", "that's right", "sounds good", "ok", "okay", "sure", "right"]
        print(f"📋 Brief Confirmatory Response: {brief_confirmatory}")
        
        if brief_confirmatory and progress_info["next_question"] and not progress_info.get("is_complete", False):
            print("✅ SHOULD USE: Structured next question from progress_info")
            print(f"🎯 Next Question: {progress_info['next_question'][:200]}...")
            
            if "management team" in progress_info['next_question'].lower():
                print("✅ SUCCESS: Next question is about management team")
            else:
                print("❌ PROBLEM: Next question is NOT about management team")
        else:
            print("❌ PROBLEM: Will use LLM generation instead of structured question")
            
    except Exception as e:
        print(f"❌ ERROR in flow analysis: {e}")

if __name__ == "__main__":
    debug_netflix_flow()