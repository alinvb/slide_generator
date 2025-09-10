# Quick fix for NVIDIA entity drift issue
# Add this to your chat input handler in app.py around line 6465

# ENHANCED ENTITY CAPTURE - Add before the existing router logic
def _enhanced_entity_capture(user_text: str):
    """Enhanced entity capture with better pattern matching"""
    text = user_text.strip()
    
    # Handle direct company name statements
    if len(text.split()) <= 3:  # Short responses likely to be company names
        # Generic company detection - works for ANY company worldwide
        import re
        
        # Check for company-like patterns (proper noun, common suffixes, etc.)
        is_company_like = (
            text[0].isupper() or  # Starts with capital (proper noun)
            any(suffix in text.lower() for suffix in ['inc', 'corp', 'ltd', 'llc', 'ag', 'sa', 'gmbh', 'co']) or
            re.match(r'^[A-Z]{2,}$', text) or  # All caps (like NVIDIA, IBM)
            len(text) >= 2 and text.isalpha()  # Basic alphabetic company name
        )
        
        if is_company_like:
            # Use appropriate capitalization
            entity_name = text.upper() if len(text) <= 5 and text.isalpha() else text.title()
            _set_entity_profile(entity_name, aliases=[text.lower(), text.title(), text.upper()])
            st.session_state['company_name'] = entity_name
            print(f"🏢 [ENHANCED CAPTURE] Locked entity: {entity_name}")
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
