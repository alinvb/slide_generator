"""
Unicode Crash Prevention Patch for Streamlit
Prevents UnicodeDecodeError in various Streamlit functions
"""
import logging

# Safe patching approach that doesn't break if modules don't exist
try:
    # Try to patch metrics if it exists - try different module paths
    try:
        from streamlit.runtime.metrics import _get_machine_id_v3
    except ImportError:
        from streamlit.runtime.metrics_util import _get_machine_id_v3
    
    def patched_get_machine_id_v3():
        """
        Patched version of _get_machine_id_v3 that handles Unicode errors gracefully
        """
        try:
            # Try the original function
            return _get_machine_id_v3()
        except UnicodeDecodeError as e:
            logging.warning(f"Unicode error in _get_machine_id_v3, using fallback: {e}")
            return "streamlit-fallback-machine-id"
        except Exception as e:
            logging.warning(f"Error in _get_machine_id_v3, using fallback: {e}")
            return "streamlit-fallback-machine-id"

    # Apply the patch - try both possible modules
    try:
        import streamlit.runtime.metrics
        streamlit.runtime.metrics._get_machine_id_v3 = patched_get_machine_id_v3
    except (ImportError, AttributeError):
        import streamlit.runtime.metrics_util
        streamlit.runtime.metrics_util._get_machine_id_v3 = patched_get_machine_id_v3
    print("✅ Streamlit Unicode crash patch applied successfully")
    
except ImportError:
    # Module doesn't exist, no patching needed
    print("ℹ️ Streamlit metrics module not found - no patching needed")
    
except Exception as e:
    print(f"⚠️ Could not apply Streamlit patch (non-critical): {e}")

# Additional Unicode safety measures
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'