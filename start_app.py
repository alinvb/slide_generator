#!/usr/bin/env python3
"""
Startup script to properly configure Streamlit before launching the app.
This bypasses the Unicode issues in Streamlit's metrics system.
"""
import os
import sys

# CRITICAL: Set environment variables FIRST
os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
os.environ['STREAMLIT_GLOBAL_DEVELOPMENT_MODE'] = 'false'
os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
os.environ['STREAMLIT_LOGGER_LEVEL'] = 'error'

# Patch sys.modules BEFORE any streamlit imports
import types
class DummyInstallation:
    def __init__(self):
        self.installation_id_v3 = "dummy-safe-id"
    @classmethod 
    def instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls()
        return cls._instance

def dummy_gather_metrics(*args, **kwargs):
    return {}

def dummy_metric_func(*args, **kwargs):
    return None

# Create and register dummy module BEFORE streamlit loads
dummy_metrics = types.ModuleType('streamlit.runtime.metrics_util')
dummy_metrics.Installation = DummyInstallation
dummy_metrics.gather_metrics = dummy_gather_metrics
dummy_metrics.track_config_option_usage = dummy_metric_func
dummy_metrics.track_cache_usage = dummy_metric_func

sys.modules['streamlit.runtime.metrics_util'] = dummy_metrics

print("🔧 Metrics patch applied successfully before Streamlit import")

# Now safely import and run the main app
try:
    # Import the actual app module
    import app
    print("✅ App imported successfully with Unicode crash protection")
except Exception as e:
    print(f"❌ Error importing app: {e}")
    sys.exit(1)