"""
Test the fixed gap filling that uses chunked approach
"""

import streamlit as st
from bulletproof_json_generator_clean import generate_clean_bulletproof_json

def test_fixed_gap_filling():
    """Test the fixed gap filling that should not return None"""
    
    # Setup session state
    if not hasattr(st, 'session_state'):
        st.session_state = {}
    
    st.session_state['api_key'] = 'your_api_key_here'  # Replace with your actual API key
    st.session_state['model'] = 'sonar-pro'
    
    print("🔍 TESTING FIXED GAP FILLING")
    
    # Test with the actual main function
    test_messages = [
        {"role": "user", "content": "Generate investment banking analysis for Netflix including strategic buyers, financial buyers, management team, precedent transactions, and valuation data."}
    ]
    
    required_slides = [
        "business_overview",
        "strategic_buyers", 
        "financial_buyers",
        "precedent_transactions",
        "management_team"
    ]
    
    try:
        response = generate_clean_bulletproof_json(
            messages=test_messages,
            required_slides=required_slides,
            llm_api_call=None  # Will use session state
        )
        
        if "Gap filling returned None" in response:
            print("❌ STILL FAILING: Gap filling returns None")
            return False
        elif "CLEAN Bulletproof JSON Generation Completed Successfully!" in response:
            print("✅ SUCCESS: Gap filling works correctly")
            print(f"Response preview: {response[:200]}...")
            return True
        else:
            print(f"❌ UNEXPECTED RESPONSE: {response[:200]}...")
            return False
    
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_fixed_gap_filling()
    if success:
        print("\n🎉 GAP FILLING FIXED!")
        print("The app should now work correctly without None errors!")
    else:
        print("\n❌ Gap filling still has issues...")
