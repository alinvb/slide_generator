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


def call_llm_api(messages: List[Dict], model: str = None, api_key: str = None, api_service: str = "perplexity", retry_count: int = 0, timeout: int = 60) -> str:
    """
    Shared LLM API call function with retry logic for timeouts
    Moved here to avoid circular import between app.py and research_agent.py
    
    Args:
        timeout: Custom timeout in seconds (default 60s, use 180s+ for comprehensive gap-filling)
    """
    if not api_key:
        api_key = st.session_state.get('api_key', '')
    if not model:
        model = st.session_state.get('model', 'sonar-pro')
    if not api_service:
        api_service = st.session_state.get('api_service', 'perplexity')
    
    if not api_key:
        print("❌ [ERROR] No API key configured - no fallback data allowed")
        raise ValueError("API key required - no fallback data allowed. Configure API key to proceed.")
    
    try:
        if api_service == "perplexity":
            return call_perplexity_api(messages, model, api_key, timeout)
        elif api_service == "claude":
            return call_claude_api(messages, model, api_key, timeout)
        else:
            return f"Error: Unknown API service: {api_service}"
    except Exception as e:
        error_str = str(e)
        # Retry logic for timeout errors
        if "timed out" in error_str.lower() and retry_count < 2:
            print(f"🔄 [RETRY] API timeout on attempt {retry_count + 1}, retrying...")
            import time
            time.sleep(2 ** retry_count)  # Exponential backoff: 1s, 2s, 4s
            return call_llm_api(messages, model, api_key, api_service, retry_count + 1, timeout)
        else:
            # No fallback - raise error to expose API issues
            print(f"❌ [ERROR] API issue after {retry_count + 1} attempts: {error_str}")
            raise Exception(f"API calls failed after {retry_count + 1} attempts: {error_str}. No fallback data allowed - fix API configuration.")


def call_perplexity_api(messages: List[Dict], model: str, api_key: str, timeout: int = 60) -> str:
    """Call Perplexity API with proper message formatting"""
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    # FIX: Ensure proper message alternation for Perplexity API
    formatted_messages = _format_messages_for_perplexity(messages)
    print(f"🔍 [PERPLEXITY] Formatted {len(messages)} → {len(formatted_messages)} messages")
    
    # Check if this is investment banking related (should use completion mode to avoid timeouts)
    message_content = ' '.join([msg.get('content', '') for msg in formatted_messages]).lower()
    is_investment_banking = any(keyword in message_content for keyword in [
        'investment banking', 'strategic buyers', 'financial buyers', 'netflix', 
        'comprehensive gap-filling', 'bulletproof', 'precedent transactions',
        'management team', 'valuation', 'investment'
    ])
    
    # Also check for large prompts
    is_large_prompt = any(len(msg.get('content', '')) > 5000 for msg in formatted_messages)
    
    if is_investment_banking or is_large_prompt:
        print(f"🔍 [PERPLEXITY] Investment banking/large prompt - using COMPLETION MODE (no search)")
        data = {
            'model': model,
            'messages': formatted_messages,
            'max_tokens': 4000,
            'temperature': 0.1
            # No search parameters to avoid timeouts
        }
    else:
        print(f"🔍 [PERPLEXITY] Regular prompt - using search mode")
        data = {
            'model': model,
            'messages': formatted_messages,
            'max_tokens': 4000,
            'temperature': 0.1,
            'return_citations': True,
            'return_images': False,
            'return_related_questions': False,
            'search_domain_filter': [],
            'search_recency_filter': "month"
        }
    
    print(f"🔍 [PERPLEXITY] Making API call with timeout: {timeout}s")
    
    try:
        response = requests.post(
            'https://api.perplexity.ai/chat/completions',
            headers=headers,
            json=data,
            timeout=timeout
        )
        print(f"✅ [PERPLEXITY] API call completed, status: {response.status_code}")
    except requests.exceptions.Timeout:
        print(f"❌ [PERPLEXITY] API call timed out after {timeout}s")
        raise Exception(f"Perplexity API timeout after {timeout}s - no fallback data allowed")
    except Exception as e:
        print(f"❌ [PERPLEXITY] API call failed: {e}")
        raise
    
    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content']
    else:
        raise Exception(f"Perplexity API error {response.status_code}: {response.text}")


def call_claude_api(messages: List[Dict], model: str, api_key: str, timeout: int = 60) -> str:
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
        timeout=timeout
    )
    
    if response.status_code == 200:
        result = response.json()
        return result['content'][0]['text']
    else:
        raise Exception(f"Claude API error {response.status_code}: {response.text}")


def run_research(query: str, timeout: int = None) -> str:
    """
    Shared research function with configurable timeout
    Moved here to avoid circular import between app.py and research_agent.py
    
    Args:
        query: Research query to execute
        timeout: Custom timeout in seconds (default: 60s, use 120s+ for complex buyers research)
    """
    # Detect if this is buyers research that needs longer timeout
    if timeout is None:
        is_buyers_research = any(keyword in query.lower() for keyword in [
            'strategic buyers', 'financial buyers', 'private equity', 'strategic acquirer'
        ])
        timeout = 120 if is_buyers_research else 60
        if is_buyers_research:
            print(f"🔍 [TIMEOUT] Detected buyers research - using extended timeout: {timeout}s")
    
    # Use the shared call_llm_api function
    messages = [
        {"role": "system", "content": "You are a senior investment banking research analyst with 15+ years experience at Goldman Sachs and Morgan Stanley. You provide SPECIFIC, DETAILED, and FACTUAL research with exact numbers, dates, names, and citations. NEVER use generic placeholders - always research real data. Focus on providing investment-grade analysis suitable for M&A transactions and due diligence processes."},
        {"role": "user", "content": query}
    ]
    
    return call_llm_api(messages, timeout=timeout)


def generate_fallback_response(messages: List[Dict]) -> str:
    """
    NO FALLBACK DATA - Raise error to expose gaps in data sourcing
    """
    print("❌ [ERROR] Fallback response generator removed - no hard-coded data allowed")
    raise ValueError("Fallback response generator removed. System must use actual API calls or research data. No hard-coded fallbacks allowed.")
def get_current_company() -> str:
    """
    Shared function to get current company context
    Moved here to avoid circular import between app.py and research_agent.py
    """
    return st.session_state.get('current_company', st.session_state.get('company_name', ''))


def _format_messages_for_perplexity(messages: List[Dict]) -> List[Dict]:
    """
    Format messages to ensure proper user/assistant alternation for Perplexity API
    Perplexity requires: (optional) system message(s), then alternating user/assistant messages
    """
    if not messages:
        return []
    
    formatted_messages = []
    system_messages = []
    other_messages = []
    
    # Separate system messages from others
    for msg in messages:
        if msg.get('role') == 'system':
            system_messages.append(msg)
        else:
            other_messages.append(msg)
    
    # Add system messages first (if any)
    formatted_messages.extend(system_messages)
    
    # If we only have one non-system message, ensure it's a user message
    if len(other_messages) == 1:
        msg = other_messages[0]
        if msg.get('role') != 'user':
            # Convert single message to user message
            formatted_messages.append({
                'role': 'user',
                'content': msg.get('content', '')
            })
        else:
            formatted_messages.append(msg)
        return formatted_messages
    
    # For multiple messages, ensure alternation starting with user
    if not other_messages:
        return formatted_messages
    
    # If we have multiple messages, combine them into a single user message to avoid alternation issues
    if len(other_messages) > 1:
        # Combine all non-system messages into one user message
        combined_content = ""
        for i, msg in enumerate(other_messages):
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            if i == 0:
                combined_content = content
            else:
                combined_content += f"\n\n{content}"
        
        formatted_messages.append({
            'role': 'user', 
            'content': combined_content
        })
    
    return formatted_messages