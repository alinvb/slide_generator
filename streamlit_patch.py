"""
Patch to disable Streamlit metrics completely to prevent UnicodeDecodeError crashes
"""
import sys
import os

# Set environment variables to disable metrics
os.environ.setdefault('STREAMLIT_BROWSER_GATHER_USAGE_STATS', 'false')
os.environ.setdefault('STREAMLIT_GLOBAL_DEVELOPMENT_MODE', 'false')

def patch_streamlit_metrics():
    """Completely replace the problematic metrics module"""
    print("🔧 Applying Streamlit metrics patch to prevent UnicodeDecodeError...")
    
    # Create a dummy metrics_util module
    class DummyInstallation:
        def __init__(self):
            self.installation_id_v3 = "dummy-id-safe"
            
        @classmethod 
        def instance(cls):
            if not hasattr(cls, '_instance'):
                cls._instance = cls()
            return cls._instance
    
    # Create dummy module with all required functions
    import types
    dummy_metrics = types.ModuleType('streamlit.runtime.metrics_util')
    dummy_metrics.Installation = DummyInstallation
    
    # Add missing functions that Streamlit expects
    def dummy_gather_metrics():
        """Dummy function to replace gather_metrics - returns callable"""
        def inner(*args, **kwargs):
            return {}
        return inner
    
    def dummy_metric_func(*args, **kwargs):
        """Generic dummy function for any other metrics functions"""
        return None
    
    dummy_metrics.gather_metrics = dummy_gather_metrics
    dummy_metrics.track_config_option_usage = dummy_metric_func
    dummy_metrics.track_cache_usage = dummy_metric_func
    
    # Register in sys.modules BEFORE streamlit imports it
    sys.modules['streamlit.runtime.metrics_util'] = dummy_metrics
    print("✅ Metrics patch applied successfully")

# Apply patch immediately when this module is imported
patch_streamlit_metrics()