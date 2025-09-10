#!/usr/bin/env python3
"""
Simple HTTP server that bypasses Streamlit's problematic metrics system
by running the app logic directly without Streamlit's session management
"""
import sys
import os

# CRITICAL: Patch BEFORE any other imports
import sys
import types

# Create dummy metrics module BEFORE importing anything else
class DummyInstallation:
    def __init__(self):
        self.installation_id_v3 = "safe-dummy-id"
    @classmethod 
    def instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls()
        return cls._instance

def dummy_gather_metrics(*args, **kwargs):
    if args and callable(args[0]):
        return args[0]  # Return function unchanged if used as decorator without parentheses
    def decorator(func):
        return func
    return decorator

def dummy_func(*args, **kwargs):
    return None

# Create and register dummy module FIRST
dummy_metrics = types.ModuleType('streamlit.runtime.metrics_util')
dummy_metrics.Installation = DummyInstallation
dummy_metrics.gather_metrics = dummy_gather_metrics
dummy_metrics.track_config_option_usage = dummy_func
dummy_metrics.track_cache_usage = dummy_func
dummy_metrics._get_machine_id_v3 = lambda: "safe-machine-id"
sys.modules['streamlit.runtime.metrics_util'] = dummy_metrics

print("🔧 Pre-patched metrics system before Streamlit import")

# Now we can safely import Streamlit
import streamlit as st
from streamlit import cli as stcli
import subprocess

def run_app():
    """Run the app with maximum safety"""
    
    # Set safe environment
    os.environ.update({
        'STREAMLIT_BROWSER_GATHER_USAGE_STATS': 'false',
        'STREAMLIT_GLOBAL_DEVELOPMENT_MODE': 'false', 
        'STREAMLIT_SERVER_HEADLESS': 'true',
        'PYTHONIOENCODING': 'utf-8',
        'LC_ALL': 'C.UTF-8',
        'LANG': 'C.UTF-8'
    })
    
    # Run Streamlit with safe arguments
    sys.argv = [
        'streamlit', 'run', 'app.py',
        '--server.port=8504',
        '--server.address=0.0.0.0',
        '--server.headless=true',
        '--server.fileWatcherType=none',
        '--server.enableXsrfProtection=false',
        '--global.developmentMode=false',
        '--browser.gatherUsageStats=false'
    ]
    
    print("🚀 Starting safe Streamlit on port 8504...")
    stcli.main()

if __name__ == "__main__":
    run_app()