#!/usr/bin/env python3
"""
Debug exactly where AI content is appearing
"""

from bulletproof_json_generator_clean import generate_clean_bulletproof_json
import json

def debug_ai_content():
    """Find exactly where AI content appears"""
    
    # Mock messages about Rolex
    test_messages = [
        {"role": "user", "content": "Let's analyze Rolex"},
        {"role": "assistant", "content": "I'd be happy to help with Rolex analysis"}
    ]
    
    # Mock LLM API call function
    def mock_llm_call(messages):
        return """
        {
            "company_name": "Rolex",
            "business_description_detailed": "Swiss luxury watchmaker", 
            "industry": "Luxury Watches"
        }
        """
    
    required_slides = ["business_overview"]
    
    print("🔍 Debugging AI Content Source...")
    
    try:
        response, content_ir, render_plan = generate_clean_bulletproof_json(
            test_messages,
            required_slides, 
            mock_llm_call,
            company_name="Rolex"
        )
        
        print(f"\n📄 FULL RESPONSE:")
        print(response)
        print(f"\n" + "="*60)
        
        # Check each line for AI content
        lines_with_ai = []
        for i, line in enumerate(response.split('\n')):
            if 'AI' in line or 'ai' in line.lower():
                lines_with_ai.append((i+1, line))
        
        if lines_with_ai:
            print(f"\n🔍 LINES CONTAINING 'AI':")
            for line_num, line in lines_with_ai:
                print(f"Line {line_num}: {line}")
        
        # Also check content_ir
        content_ir_str = str(content_ir)
        if 'AI' in content_ir_str or 'ai' in content_ir_str.lower():
            print(f"\n🔍 CONTENT_IR CONTAINS AI:")
            for key, value in content_ir.items():
                value_str = str(value)
                if 'AI' in value_str or 'ai' in value_str.lower():
                    print(f"Key '{key}' contains AI: {value_str[:200]}...")
        
        return True
            
    except Exception as e:
        print(f"❌ Debug failed: {e}")
        return False

if __name__ == "__main__":
    debug_ai_content()