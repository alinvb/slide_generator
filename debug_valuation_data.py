"""
Debug valuation data extraction issue
"""

import streamlit as st
from bulletproof_json_generator_clean import CleanBulletproofJSONGenerator

def debug_valuation_data():
    """Debug why valuation data is empty"""
    
    if not hasattr(st, 'session_state'):
        st.session_state = {}
    
    st.session_state['api_key'] = 'your_api_key_here'  # Replace with your actual API key
    st.session_state['model'] = 'sonar-pro'
    
    print("🔍 DEBUGGING VALUATION DATA")
    
    generator = CleanBulletproofJSONGenerator()
    
    # Test chunk 2 which should contain valuation data
    extracted_data = {'competitors_mentioned': [], 'company_name': 'Netflix'}
    
    chunk_result = generator._generate_competitive_valuation_chunk(
        company_name="Netflix",
        industry="Streaming",
        extracted_data=extracted_data,
        llm_api_call=None
    )
    
    print(f"Chunk result keys: {list(chunk_result.keys()) if chunk_result else 'None'}")
    
    if 'valuation_data' in chunk_result:
        valuation_raw = chunk_result['valuation_data']
        print(f"Raw valuation data type: {type(valuation_raw)}")
        print(f"Raw valuation data: {valuation_raw}")
        
        # Check what the slide extraction expects
        if isinstance(valuation_raw, dict):
            # Convert to list format that slide renderer expects
            valuation_list = []
            for method, data in valuation_raw.items():
                if isinstance(data, dict):
                    valuation_list.append({
                        "method": method,
                        "low": data.get('low', 'N/A'),
                        "high": data.get('high', 'N/A'),
                        "mean": data.get('mean', 'N/A')
                    })
            print(f"Converted valuation list: {valuation_list}")
        
    else:
        print("❌ No valuation_data in chunk result")

if __name__ == "__main__":
    debug_valuation_data()
