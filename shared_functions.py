#!/usr/bin/env python3
"""
shared_functions.py - Shared functions to avoid circular imports
Contains functions that both app.py and research_agent.py need to access
"""

# NUCLEAR TUPLE ERROR FIX: Global bulletproof get function
def safe_get(obj, key, default=None):
    """Bulletproof get function that handles any object type"""
    try:
        if hasattr(obj, 'get') and callable(getattr(obj, 'get')):
            return obj.get(key, default)
        elif isinstance(obj, dict):
            return obj.get(key, default)
        else:
            print(f"🚨 SAFE_GET: Object is {type(obj)}, not dict - returning default: {default}")
            return default
    except Exception as e:
        print(f"🚨 SAFE_GET ERROR: {str(e)}, returning default: {default}")
        return default

import streamlit as st
import requests
import json
from typing import Dict, List, Tuple, Any


def call_llm_api(messages: List[Dict], model: str = None, api_key: str = None, api_service: str = "perplexity", retry_count: int = 0) -> str:
    """
    Shared LLM API call function with retry logic for timeouts
    Moved here to avoid circular import between app.py and research_agent.py
    """
    if not api_key:
        api_key = st.session_state.get('api_key', '')
    if not model:
        model = st.session_state.get('model', 'sonar-pro')
    if not api_service:
        api_service = st.session_state.get('api_service', 'perplexity')
    
    if not api_key:
        return "Error: No API key provided"
    
    try:
        if api_service == "perplexity":
            return call_perplexity_api(messages, model, api_key)
        elif api_service == "claude":
            return call_claude_api(messages, model, api_key)
        else:
            return f"Error: Unknown API service: {api_service}"
    except Exception as e:
        error_str = str(e)
        # Retry logic for timeout errors
        if "timed out" in error_str.lower() and retry_count < 2:
            print(f"🔄 [RETRY] API timeout on attempt {retry_count + 1}, retrying...")
            import time
            time.sleep(2 ** retry_count)  # Exponential backoff: 1s, 2s, 4s
            return call_llm_api(messages, model, api_key, api_service, retry_count + 1)
        else:
            # If still failing after retries, provide fallback response instead of complete failure
            if "timed out" in error_str.lower():
                print(f"⚠️ [FALLBACK] API timeout after {retry_count + 1} attempts, using fallback data")
                return generate_fallback_response(messages)
            return f"Error calling {api_service} API: {error_str}"


def call_perplexity_api(messages: List[Dict], model: str, api_key: str) -> str:
    """Call Perplexity API"""
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'model': model,
        'messages': messages,
        'max_tokens': 4000,
        'temperature': 0.1,
        'return_citations': True,
        'return_images': False,
        'return_related_questions': False,
        'search_domain_filter': [],
        'search_recency_filter': "month"
    }
    
    response = requests.post(
        'https://api.perplexity.ai/chat/completions',
        headers=headers,
        json=data,
        timeout=60
    )
    
    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content']
    else:
        raise Exception(f"Perplexity API error {response.status_code}: {response.text}")


def call_claude_api(messages: List[Dict], model: str, api_key: str) -> str:
    """Call Claude API"""
    headers = {
        'x-api-key': api_key,
        'Content-Type': 'application/json',
        'anthropic-version': '2023-06-01'
    }
    
    # Convert messages format for Claude
    system_message = ""
    claude_messages = []
    
    for msg in messages:
        if msg['role'] == 'system':
            system_message = msg['content']
        else:
            claude_messages.append({
                'role': msg['role'],
                'content': msg['content']
            })
    
    data = {
        'model': model,
        'max_tokens': 4000,
        'temperature': 0.1,
        'messages': claude_messages
    }
    
    if system_message:
        data['system'] = system_message
    
    response = requests.post(
        'https://api.anthropic.com/v1/messages',
        headers=headers,
        json=data,
        timeout=60
    )
    
    if response.status_code == 200:
        result = response.json()
        return result['content'][0]['text']
    else:
        raise Exception(f"Claude API error {response.status_code}: {response.text}")


def run_research(query: str) -> str:
    """
    Shared research function 
    Moved here to avoid circular import between app.py and research_agent.py
    """
    # Use the shared call_llm_api function
    messages = [
        {"role": "system", "content": "You are a senior investment banking research analyst with 15+ years experience at Goldman Sachs and Morgan Stanley. You provide SPECIFIC, DETAILED, and FACTUAL research with exact numbers, dates, names, and citations. NEVER use generic placeholders - always research real data. Focus on providing investment-grade analysis suitable for M&A transactions and due diligence processes."},
        {"role": "user", "content": query}
    ]
    
    return call_llm_api(messages)


def generate_fallback_response(messages: List[Dict]) -> str:
    """
    Generate fallback response when API calls fail
    """
    user_content = ""
    for msg in messages:
        if msg['role'] == 'user':
            user_content = msg['content']
            break
    
    # Extract company name from the user content
    company_name = "the target company"
    if '{company}' in user_content:
        # Try to get company from session state
        company_name = st.session_state.get('company_name', st.session_state.get('current_company', 'the target company'))
    
    # Generate basic fallback response based on request type
    if "business overview" in user_content.lower():
        return f"""**Business Overview for {company_name}**:

{company_name} is a technology company operating in the data and analytics sector. The company provides cloud-based solutions and platforms for data processing and analysis. 

**Key Information**:
- Industry: Technology/Data Analytics
- Business Model: Software as a Service (SaaS)
- Market Position: Competitive player in data analytics space
- Geographic Presence: Multi-regional operations

*Note: This is fallback data due to API timeout. For detailed research, please retry the generation.*"""
    elif "financial" in user_content.lower():
        return f"""**Financial Analysis for {company_name}**:

**Revenue Trends**: Growing revenue base with strong recurring revenue model
**Profitability**: Working towards profitability with improving unit economics
**Funding**: Multiple funding rounds supporting growth initiatives

*Note: This is fallback data due to API timeout. For detailed research, please retry the generation.*"""
    else:
        return f"""**Research Analysis for {company_name}**:

Basic company information and industry analysis available. The company operates in the technology sector with focus on providing innovative solutions to enterprise customers.

*Note: This is fallback data due to API timeout. For detailed research, please retry the generation.*"""


def get_current_company() -> str:
    """
    Shared function to get current company context
    Moved here to avoid circular import between app.py and research_agent.py
    """
    return st.session_state.get('current_company', st.session_state.get('company_name', ''))