#!/usr/bin/env python3
"""
Test the research request loop issue on Topic 3
"""

import sys
sys.path.append('/home/user/webapp')
from app import analyze_conversation_progress

def test_research_loop_issue():
    """Test the exact scenario causing the research loop"""
    
    # Simulate the conversation that leads to the research loop
    messages = [
        {"role": "assistant", "content": "What is your company name and give me a brief overview of what your business does?"},
        {"role": "user", "content": "databricks"},
        {"role": "assistant", "content": "Databricks research response..."},
        {"role": "user", "content": "ok"},
        {"role": "assistant", "content": "Now let's discuss your product/service footprint. What are your main offerings?"},
        {"role": "user", "content": "research this yourself"},
        {"role": "assistant", "content": "Product research response..."},
        {"role": "user", "content": "ok"},
        {"role": "assistant", "content": "Let's analyze your historical financial performance. Can you provide your revenue, EBITDA, margins, and key financial metrics for the last 3-5 years?"},
        {"role": "user", "content": "research this yourself"},
        # After this, system should research financial data and move to Topic 4, but it's looping
    ]
    
    result = analyze_conversation_progress(messages)
    
    print(f"Current Issue:")
    print(f"Next Topic: {result.get('next_topic')}")
    print(f"Should be: management_team (Topic 4)")
    print(f"Problem: System keeps asking financial performance question instead of progressing")
    
    if result.get('next_topic') == 'historical_financial_performance':
        return 'CONFIRMED_BUG'
    elif result.get('next_topic') == 'management_team':
        return 'WORKS_CORRECTLY'
    else:
        return f"UNEXPECTED_{result.get('next_topic')}"

if __name__ == "__main__":
    print("🔍 TESTING RESEARCH REQUEST LOOP ISSUE")
    status = test_research_loop_issue()
    print(f"Status: {status}")