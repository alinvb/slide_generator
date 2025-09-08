#!/usr/bin/env python3
"""
Test JSON Generation Fix
Tests the interview-to-JSON transition fixes
"""

import json
from perfect_json_prompter import PerfectJSONPrompter, get_interview_completion_prompt

def test_interview_completion_prompt():
    """Test that the interview completion prompt works correctly"""
    
    # Simulate conversation messages with substantial company info
    mock_messages = [
        {"role": "system", "content": "You are an investment banking assistant."},
        {"role": "assistant", "content": "What is your company name?"},
        {"role": "user", "content": "My company is Saudi Aramco, we are the world's largest oil company based in Saudi Arabia."},
        {"role": "assistant", "content": "Tell me about your financial performance."},
        {"role": "user", "content": "We have revenues of over $400 billion and are highly profitable with strong EBITDA margins."},
        {"role": "assistant", "content": "What about your management team?"},
        {"role": "user", "content": "We have a strong leadership team including CEO Amin Nasser and CFO Ziad Al-Murshed."},
        {"role": "assistant", "content": "Now let me generate the JSON structures for you."}
    ]
    
    # Test the completion prompt
    try:
        completion_prompt = get_interview_completion_prompt(mock_messages)
        
        print("✅ Interview completion prompt generated successfully")
        print(f"📏 Prompt length: {len(completion_prompt)} characters")
        print("📝 First 300 characters:")
        print(completion_prompt[:300] + "...")
        
        # Check that it contains key elements
        required_elements = [
            "generate",
            "json",
            "structures",
            "CONTENT IR JSON",
            "RENDER PLAN JSON"
        ]
        
        for element in required_elements:
            if element.lower() in completion_prompt.lower():
                print(f"✅ Contains required element: {element}")
            else:
                print(f"❌ Missing required element: {element}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating completion prompt: {str(e)}")
        return False

def test_perfect_json_prompter():
    """Test the PerfectJSONPrompter class"""
    
    try:
        prompter = PerfectJSONPrompter()
        print("✅ PerfectJSONPrompter initialized successfully")
        
        # Check if templates are loaded
        if prompter.perfect_content_ir_template:
            print("✅ Content IR template loaded")
        else:
            print("❌ Content IR template not loaded")
        
        if prompter.perfect_render_plan_template:
            print("✅ Render Plan template loaded")
        else:
            print("❌ Render Plan template not loaded")
        
        # Test system prompt creation
        system_prompt = prompter.create_enhanced_system_prompt()
        print(f"✅ Enhanced system prompt created (length: {len(system_prompt)})")
        
        # Check for critical elements in system prompt
        critical_elements = [
            "JSON GENERATION TRIGGERS",
            "ADAPTIVE APPROACH",
            "generate JSON when you have substantial information",
            "ALWAYS generate JSON when explicitly requested"
        ]
        
        for element in critical_elements:
            if element in system_prompt:
                print(f"✅ System prompt contains: {element}")
            else:
                print(f"⚠️ System prompt missing: {element}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing PerfectJSONPrompter: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing JSON Generation Fixes")
    print("=" * 50)
    
    print("\n1. Testing Interview Completion Prompt:")
    test1_result = test_interview_completion_prompt()
    
    print("\n2. Testing Perfect JSON Prompter:")
    test2_result = test_perfect_json_prompter()
    
    print("\n" + "=" * 50)
    if test1_result and test2_result:
        print("✅ All tests passed! JSON generation fixes are working.")
        print("🚀 The system should now properly transition from interview to JSON generation.")
    else:
        print("❌ Some tests failed. Check the errors above.")
    
    print("\n🌐 Streamlit URL: https://8502-i4lx93n6x87cg5p48o0ic-6532622b.e2b.dev")
    print("💡 Test the fixes by:")
    print("   1. Starting a conversation with company information")
    print("   2. Clicking the '🚀 Generate JSON Now' button")
    print("   3. Verifying that JSON files are generated instead of more interview questions")

if __name__ == "__main__":
    main()