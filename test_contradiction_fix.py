#!/usr/bin/env python3
"""
Test the contradiction detection functionality
"""

# Mock streamlit session state for testing
class MockSessionState:
    def __init__(self):
        self.data = {}
    
    def get(self, key, default=None):
        return self.data.get(key, default)
    
    def __getitem__(self, key):
        return self.data[key]
    
    def __setitem__(self, key, value):
        self.data[key] = value

# Mock streamlit module
class MockST:
    def __init__(self):
        self.session_state = MockSessionState()

import sys
sys.modules['streamlit'] = MockST()

# Now import the functions we need to test
from app import _is_fact_query, _is_contradictory_statement, _current_company

# Set up test scenario
import streamlit as st
st.session_state['current_company'] = 'NVIDIA'
st.session_state['company_name'] = 'NVIDIA'

def test_contradiction_detection():
    """Test various contradiction scenarios"""
    
    print("🧪 Testing Contradiction Detection")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        ("NVIDIA is a garbage disposal company", True),
        ("nvidia is a waste management company", True), 
        ("NVIDIA is a technology company", False),
        ("What does NVIDIA do?", False),
        ("research this for me", False),
        ("Apple is a restaurant chain", True),
    ]
    
    for text, expected in test_cases:
        print(f"\nTesting: '{text}'")
        print(f"Current company: '{_current_company()}'")
        
        is_contradiction = _is_contradictory_statement(text)
        is_fact_query = _is_fact_query(text)
        
        print(f"Contradiction detected: {is_contradiction}")
        print(f"Fact query detected: {is_fact_query}")
        print(f"Expected contradiction: {expected}")
        print(f"✅ PASS" if is_contradiction == expected else f"❌ FAIL - Expected {expected}, got {is_contradiction}")

if __name__ == "__main__":
    test_contradiction_detection()