#!/usr/bin/env python3
"""
Test precedent transactions validation to ensure only private M&A transactions are included
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from json_data_fixer import fix_precedent_transactions_data

def test_precedent_transactions_validation():
    """Test that invalid acquirer types are filtered out"""
    
    # Test data with both valid and invalid transactions
    test_data = {
        "transactions": [
            {
                "target": "Valid Corp",
                "acquirer": "Microsoft Corporation",  # VALID - real company
                "enterprise_value": 1000,
                "revenue": 100,
                "date": "2024-01-15"
            },
            {
                "target": "Invalid Corp 1",
                "acquirer": "Public Market",  # INVALID - should be filtered
                "enterprise_value": 500,
                "revenue": 50,
                "date": "2024-02-15"
            },
            {
                "target": "Invalid Corp 2", 
                "acquirer": "Series K",  # INVALID - should be filtered
                "enterprise_value": 200,
                "revenue": 25,
                "date": "2024-03-15"
            },
            {
                "target": "Valid Corp 2",
                "acquirer": "Amazon Web Services",  # VALID - real company
                "enterprise_value": 800,
                "revenue": 80,
                "date": "2024-04-15"
            },
            {
                "target": "Invalid Corp 3",
                "acquirer": "IPO",  # INVALID - should be filtered
                "enterprise_value": 300,
                "revenue": 30,
                "date": "2024-05-15"
            }
        ]
    }
    
    print("🧪 Testing Precedent Transactions Validation")
    print(f"📊 Input: {len(test_data['transactions'])} transactions")
    
    # Print input transactions
    for i, txn in enumerate(test_data['transactions']):
        print(f"  {i+1}. {txn['target']} <- {txn['acquirer']}")
    
    # Apply validation
    fixed_data = fix_precedent_transactions_data(test_data)
    
    print(f"\n✅ Output: {len(fixed_data['transactions'])} transactions")
    
    # Print output transactions
    for i, txn in enumerate(fixed_data['transactions']):
        print(f"  {i+1}. {txn['target']} <- {txn['acquirer']}")
    
    # Verify results
    valid_acquirers = [txn['acquirer'] for txn in fixed_data['transactions']]
    expected_valid = ['Microsoft Corporation', 'Amazon Web Services']
    
    print(f"\n🔍 Validation Results:")
    print(f"  Expected valid acquirers: {expected_valid}")
    print(f"  Actual valid acquirers: {valid_acquirers}")
    
    # Check if validation worked correctly
    success = (
        len(fixed_data['transactions']) == 2 and  # Only 2 valid transactions
        'Microsoft Corporation' in valid_acquirers and
        'Amazon Web Services' in valid_acquirers and
        'Public Market' not in valid_acquirers and
        'Series K' not in valid_acquirers and
        'IPO' not in valid_acquirers
    )
    
    if success:
        print("✅ PASS: Invalid acquirers were properly filtered!")
        return True
    else:
        print("❌ FAIL: Validation did not work correctly")
        return False

if __name__ == "__main__":
    test_precedent_transactions_validation()