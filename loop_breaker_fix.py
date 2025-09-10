#!/usr/bin/env python3
"""
Additional fix for the specific loop issue where the system asks the same question repeatedly
even after user provides information (correct or incorrect).
"""

# This would be integrated into app.py, but testing the logic here first

def _user_provided_company_info(text: str) -> bool:
    """
    Detect if user provided any information about their company, even if incorrect.
    This should trigger fact-checking or acceptance, not repetition of the same question.
    """
    text_lower = text.lower().strip()
    
    # Patterns that indicate user is providing company information
    company_info_patterns = [
        "is a ",
        "is an ", 
        "we are a",
        "we are an",
        "company is",
        "business is", 
        "firm is",
        "my company",
        "our company",
        "we do",
        "we make",
        "we provide",
        "we offer"
    ]
    
    for pattern in company_info_patterns:
        if pattern in text_lower:
            return True
    
    # Also check if text contains company name + description
    if any(word in text_lower for word in ["company", "business", "firm", "corporation"]):
        if any(word in text_lower for word in ["is", "does", "makes", "provides", "offers"]):
            return True
    
    return False

def test_company_info_detection():
    """Test the company info detection"""
    
    test_cases = [
        ("NVIDIA is a garbage disposal company", True),
        ("We are a tech company", True), 
        ("My company makes software", True),
        ("Our business provides AI services", True),
        ("The firm is located in California", True),
        ("What do you mean?", False),
        ("I don't know", False),
        ("Can you research this?", False),
        ("research this for me", False),
        ("next topic", False)
    ]
    
    print("Testing Company Info Detection")
    print("=" * 40)
    
    for text, expected in test_cases:
        result = _user_provided_company_info(text)
        status = "✅" if result == expected else "❌"
        print(f"{status} '{text}' -> {result} (expected {expected})")

if __name__ == "__main__":
    test_company_info_detection()