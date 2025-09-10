#!/usr/bin/env python3
"""
Simple test of contradiction detection logic
"""

def _is_contradictory_statement_test(text: str, company: str) -> bool:
    """Test version of contradiction detection"""
    import re
    
    text_lower = text.lower()
    company_lower = company.lower() if company else ""
    
    print(f"🔍 [CONTRADICTION CHECK] Text: '{text}' | Company: '{company}'")
    
    # Pattern: "X is a Y company" where Y is obviously wrong
    wrong_industries = [
        'garbage disposal', 'waste management', 'plumbing', 'restaurant', 
        'fast food', 'clothing', 'retail', 'grocery', 'farming', 'agriculture'
    ]
    
    # Check if this looks like a contradictory statement about a known tech company
    if company_lower in ['nvidia', 'apple', 'google', 'microsoft', 'meta', 'tesla']:
        for industry in wrong_industries:
            if industry in text_lower and ('is a' in text_lower or 'is an' in text_lower):
                print(f"🚨 [CONTRADICTION DETECTED] {company} + {industry}")
                return True
    
    # Generic pattern: [Company Name] is a [Obviously Wrong Industry]
    if company and 'is a' in text_lower:
        # Check if the statement contradicts what we know about the company
        for industry in wrong_industries:
            if industry in text_lower:
                print(f"🚨 [CONTRADICTION DETECTED] Generic: {company} + {industry}")
                return True
    
    print(f"🔍 [CONTRADICTION CHECK] No contradiction detected")
    return False

def test_cases():
    """Run test cases"""
    
    print("🧪 Testing Contradiction Detection")
    print("=" * 50)
    
    # Test cases: (text, company, expected_contradiction)
    test_cases = [
        ("NVIDIA is a garbage disposal company", "NVIDIA", True),
        ("nvidia is a waste management company", "NVIDIA", True), 
        ("NVIDIA is a technology company", "NVIDIA", False),
        ("What does NVIDIA do?", "NVIDIA", False),
        ("research this for me", "NVIDIA", False),
        ("Apple is a restaurant chain", "Apple", True),
        ("Microsoft is a plumbing company", "Microsoft", True),
    ]
    
    for text, company, expected in test_cases:
        print(f"\n{'='*40}")
        result = _is_contradictory_statement_test(text, company)
        status = "✅ PASS" if result == expected else "❌ FAIL"
        print(f"{status} - Expected: {expected}, Got: {result}")

if __name__ == "__main__":
    test_cases()