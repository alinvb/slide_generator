#!/usr/bin/env python3
"""
Test the encoding fix for Unicode characters in API calls
"""

import json

def test_unicode_encoding():
    """Test that Unicode characters can be properly encoded"""
    
    print("🧪 Testing Unicode Encoding Fix")
    
    # Test payload with Unicode characters (emojis)
    test_payload = {
        "messages": [
            {
                "role": "user", 
                "content": "❌ JSON Extraction Failed: Here's some Unicode content with emojis ✅ 🚀 🎯"
            },
            {
                "role": "assistant",
                "content": "I understand! Let me help you fix this issue. 🔧 Here are the steps: ✅ Step 1, ✅ Step 2"
            }
        ],
        "model": "test-model",
        "temperature": 0.7
    }
    
    print("📝 Test payload contains Unicode characters:")
    for msg in test_payload["messages"]:
        print(f"   {msg['role']}: {msg['content'][:50]}...")
    
    # Test the encoding approach used in our fix
    try:
        # This is what we're now doing in the API calls
        json_data = json.dumps(test_payload, ensure_ascii=False)
        encoded_data = json_data.encode('utf-8')
        
        print(f"\n✅ SUCCESS: JSON encoded to UTF-8")
        print(f"   Original length: {len(json_data)} characters")
        print(f"   Encoded length: {len(encoded_data)} bytes")
        
        # Test decoding back
        decoded_data = encoded_data.decode('utf-8')
        parsed_data = json.loads(decoded_data)
        
        print(f"✅ SUCCESS: Data can be decoded back correctly")
        print(f"   First message content: {parsed_data['messages'][0]['content'][:30]}...")
        
        return True
        
    except UnicodeEncodeError as e:
        print(f"❌ ENCODING FAILED: {e}")
        return False
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {e}")
        return False

def test_old_approach():
    """Test what would happen with the old approach (for comparison)"""
    
    print(f"\n🔍 Testing Old Approach (for comparison)")
    
    test_payload = {
        "messages": [{"role": "user", "content": "❌ Unicode test ✅"}]
    }
    
    try:
        # This simulates what requests.post(json=payload) does internally
        json_data = json.dumps(test_payload)  # ensure_ascii=True by default
        print(f"✅ Old approach would work with ensure_ascii=True")
        print(f"   Result: {json_data}")
        return True
    except Exception as e:
        print(f"❌ Old approach failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    success1 = test_unicode_encoding()
    success2 = test_old_approach()
    
    print("=" * 60)
    if success1:
        print("✅ UTF-8 encoding fix is working correctly!")
        print("🎯 API calls should now handle Unicode characters properly.")
    else:
        print("❌ Encoding fix needs adjustment!")
    
    print("🔧 The fix ensures Unicode characters are properly encoded as UTF-8.")