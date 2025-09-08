#!/usr/bin/env python3
"""
Test the improve button functionality and validation feedback
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_validation_feedback_for_llm

def test_validation_feedback():
    """Test validation feedback generation for failing cases"""
    
    # Mock validation results that should trigger the improve button
    validation_results = {
        'overall_valid': False,  # Key: should be False to trigger feedback
        'valid_slides': 13,
        'invalid_slides': 1,
        'slide_validations': [
            {
                'slide_number': 2,
                'template': 'historical_financial_performance',
                'valid': False,
                'issues': [],
                'missing_fields': ['Missing Financial performance chart data'],
                'empty_fields': [],
                'warnings': []
            }
        ],
        'structure_validation': {
            'structure_issues': []
        }
    }
    
    print("🧪 Testing Improve Button Validation Feedback")
    print(f"📊 Input validation_results['overall_valid']: {validation_results['overall_valid']}")
    
    # Test the feedback generation
    feedback = create_validation_feedback_for_llm(validation_results)
    
    print(f"\n✅ Feedback Generated: {feedback is not None}")
    
    if feedback:
        print(f"📝 Feedback Length: {len(feedback)} characters")
        print(f"🔍 First 200 chars: {feedback[:200]}...")
        return True
    else:
        print("❌ No feedback generated - this would prevent the button from appearing!")
        return False

if __name__ == "__main__":
    test_validation_feedback()