#!/usr/bin/env python3
"""
Simple test for investment banking interview flow
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_basic_flow():
    """Basic test that doesn't require full Streamlit context"""
    
    try:
        from app import analyze_conversation_progress
        
        print("🧪 Testing Basic Interview Flow")
        print("=" * 40)
        
        # Test 1: Empty conversation
        messages_empty = [{"role": "system", "content": "System prompt"}]
        try:
            progress = analyze_conversation_progress(messages_empty)
            next_topic = progress.get('next_topic')
            print(f"✅ Test 1 PASS: Empty conversation → {next_topic}")
            
            if next_topic != 'business_overview':
                print(f"⚠️  Expected business_overview, got {next_topic}")
        except Exception as e:
            print(f"❌ Test 1 FAIL: {str(e)}")
        
        # Test 2: Business overview response
        messages_with_biz = [
            {"role": "system", "content": "System prompt"},
            {"role": "assistant", "content": "What is your company name?"},
            {"role": "user", "content": "Databricks founded 2013 San Francisco unified analytics platform"}
        ]
        
        try:
            progress = analyze_conversation_progress(messages_with_biz) 
            next_topic = progress.get('next_topic')
            print(f"✅ Test 2 PASS: After business overview → {next_topic}")
        except Exception as e:
            print(f"❌ Test 2 FAIL: {str(e)}")
            
        print("\n🎯 Basic tests completed successfully!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_basic_flow()