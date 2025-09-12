# Investment Banking Research App Configuration
# This file provides secure API key configuration as a fallback when sidebar input fails

import os
from pathlib import Path

# Load environment variables from .env file if it exists
env_file = Path(__file__).parent / '.env'
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value

# PERPLEXITY API KEY CONFIGURATION
# Set your Perplexity API key here as a fallback when sidebar input doesn't work
# SECURITY: API key should be set via environment variable for production
# For development, you can uncomment and set the API key below:
# PERPLEXITY_API_KEY = "your-api-key-here"
PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY', '')

# Export as environment variable for the session
if PERPLEXITY_API_KEY:
    os.environ['PERPLEXITY_API_KEY'] = PERPLEXITY_API_KEY
    print(f"✅ [CONFIG] Perplexity API key configured: {len(PERPLEXITY_API_KEY)} characters")

# Default model settings
DEFAULT_MODEL = "sonar-pro"
DEFAULT_SERVICE = "perplexity"

# Function to get working API key with multiple fallbacks
def get_working_api_key():
    """Get API key from multiple sources with priority order"""
    
    # Priority 1: Environment variable set by this config
    api_key = os.getenv('PERPLEXITY_API_KEY')
    if api_key and len(api_key.strip()) > 0:
        print(f"✅ [CONFIG] Using environment API key: {len(api_key)} chars")
        return api_key.strip()
    
    # Priority 2: Direct config constant
    if PERPLEXITY_API_KEY and len(PERPLEXITY_API_KEY.strip()) > 0:
        print(f"✅ [CONFIG] Using config API key: {len(PERPLEXITY_API_KEY)} chars") 
        return PERPLEXITY_API_KEY.strip()
    
    # Priority 3: None found
    print("🚨 [CONFIG] No API key found in config or environment")
    return None

def get_default_settings():
    """Get default API settings"""
    return {
        'api_key': get_working_api_key(),
        'model': DEFAULT_MODEL,
        'service': DEFAULT_SERVICE
    }

# Test the configuration
if __name__ == "__main__":
    settings = get_default_settings()
    print(f"🔍 [CONFIG_TEST] API Key: {'*' * len(settings['api_key']) if settings['api_key'] else 'None'}")
    print(f"🔍 [CONFIG_TEST] Model: {settings['model']}")
    print(f"🔍 [CONFIG_TEST] Service: {settings['service']}")