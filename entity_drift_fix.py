# Quick fix for NVIDIA entity drift issue
# Add this to your chat input handler in app.py around line 6465

# ENHANCED ENTITY CAPTURE - Add before the existing router logic
def _enhanced_entity_capture(user_text: str):
    """Enhanced entity capture with better pattern matching"""
    text = user_text.strip()
    
    # Handle direct company name statements
    if len(text.split()) <= 3:  # Short responses likely to be company names
        # Known major companies (add more as needed)
        major_companies = ['nvidia', 'apple', 'microsoft', 'google', 'amazon', 'tesla', 'meta']
        if text.lower() in major_companies:
            _set_entity_profile(text.upper(), aliases=[text.lower(), text.title(), text.upper()])
            st.session_state['company_name'] = text.upper()
            print(f"🏢 [ENHANCED CAPTURE] Locked entity: {text.upper()}")
            return True
    
    # Handle "My company is X" or "The company is X" patterns
    patterns = [
        r"(?:my )?company (?:is )?(.+)",
        r"(?:the )?company name is (.+)",
        r"we are (.+)",
        r"it'?s (.+)",
    ]
    
    for pattern in patterns:
        import re
        match = re.search(pattern, text.lower())
        if match:
            company_name = match.group(1).strip()
            _set_entity_profile(company_name.title())
            st.session_state['company_name'] = company_name.title()
            print(f"🏢 [ENHANCED CAPTURE] Extracted entity: {company_name.title()}")
            return True
    
    return False

# Call this BEFORE the existing router:
# _enhanced_entity_capture(prompt)  # Add this line in your chat handler
