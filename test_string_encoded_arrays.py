#!/usr/bin/env python3
"""
Test script to verify string-encoded array parsing fix
"""

# Simulate the string-encoded arrays issue
raw_table_data = [
    "['Region', 'Market Segment', 'Major Assets/Products', 'Coverage Details']",
    "['United States', 'Finance, Tech, Services', 'LlamaCloud, LlamaParse, Framework', 'Enterprise deployments, Fortune 500 clients']",
    "['Europe', 'Consulting, Manufacturing', 'LlamaCloud, LlamaParse, Connectors', 'KPMG, industry leaders, RAG and AI workflow standardization']"
]

print("🧪 Testing string-encoded array parsing")
print(f"Raw data type: {type(raw_table_data[0])}")
print(f"Raw data sample: {raw_table_data[0]}")

# Test the parsing logic
import ast
table_data = []

try:
    parsed_table_data = []
    for item in raw_table_data:
        if item.startswith('[') and item.endswith(']'):
            parsed_row = ast.literal_eval(item)
            parsed_table_data.append(parsed_row)
    
    if parsed_table_data:
        table_data = parsed_table_data
        print(f"✅ Successfully parsed {len(table_data)} string-encoded rows")
        print(f"Parsed data type: {type(table_data[0])}")
        print(f"Parsed data sample: {table_data[0]}")
    else:
        raise ValueError("No valid rows parsed from string data")

except Exception as e:
    print(f"❌ Failed to parse string-encoded arrays: {e}")

print("\n🎯 Final table data:")
for i, row in enumerate(table_data):
    print(f"  Row {i}: {row}")