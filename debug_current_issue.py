#!/usr/bin/env python3
"""
Debug the current research loop issue on Topic 3
"""

import sys
sys.path.append('/home/user/webapp')
from app import analyze_conversation_progress

def test_current_issue():
    """Test the exact scenario from user report"""
    
    print("🚨 DEBUGGING CURRENT ISSUE")
    print("User Report: Topic 3 financial performance stuck in loop")
    print("=" * 60)
    
    # Exact conversation from user report
    messages = [
        {"role": "assistant", "content": "Now let's discuss your product/service footprint. What are your main offerings?"},
        {"role": "user", "content": "research this yourself"},
        {"role": "assistant", "content": "Product research response..."},
        {"role": "user", "content": "ok"},
        {"role": "assistant", "content": "Let's analyze your historical financial performance. Can you provide your revenue, EBITDA, margins, and key financial metrics for the last 3-5 years?"},
        {"role": "user", "content": "research this yourself"},
        # After this, system should research financial data and move to Topic 4 (management_team)
        # But it's repeating the same financial question
    ]
    
    print("📊 ANALYZING CONVERSATION STATE...")
    result = analyze_conversation_progress(messages)
    
    print(f"Next Topic: {result.get('next_topic')}")
    print(f"Next Question: {result.get('next_question', '')[:100]}...")
    
    # What should happen
    if result.get('next_topic') == 'management_team':
        print("✅ WORKING: Should progress to management team")
        return True
    elif result.get('next_topic') == 'historical_financial_performance':
        print("❌ BUG CONFIRMED: Still stuck on financial performance")
        print("   Topic 3 is not being marked as complete after research request")
        return False
    else:
        print(f"⚠️  UNEXPECTED: Got {result.get('next_topic')}")
        return False

if __name__ == "__main__":
    test_current_issue()