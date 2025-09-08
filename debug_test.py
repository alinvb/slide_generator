#!/usr/bin/env python3

# Debug the test case
test_response = "Based on our conversation, I'll now generate the Content IR and Render Plan JSONs. Here's the detailed content: " + "x" * 500

print(f"Response: '{test_response[:100]}...'")
print(f"Length: {len(test_response)}")
print(f"Contains 'content_ir': {'content_ir' in test_response.lower()}")
print(f"Contains 'render_plan': {'render_plan' in test_response.lower()}")
print(f"Has both keywords: {'content_ir' in test_response.lower() and 'render_plan' in test_response.lower()}")
print(f"Contains braces: {'{' in test_response and '}' in test_response}")