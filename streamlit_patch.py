"""
Unicode Crash Prevention Patch for Streamlit
Prevents UnicodeDecodeError in _get_machine_id_v3 function
"""
import streamlit as st
from streamlit.runtime.metrics import _get_machine_id_v3
import logging

def patched_get_machine_id_v3():
    """
    Patched version of _get_machine_id_v3 that handles Unicode errors gracefully
    """
    try:
        # Try the original function
        return _get_machine_id_v3()
    except UnicodeDecodeError as e:
        logging.warning(f"Unicode error in _get_machine_id_v3, using fallback: {e}")
        # Return a safe fallback machine ID
        return "streamlit-fallback-machine-id"
    except Exception as e:
        logging.warning(f"Error in _get_machine_id_v3, using fallback: {e}")
        return "streamlit-fallback-machine-id"

# Apply the patch
try:
    import streamlit.runtime.metrics
    streamlit.runtime.metrics._get_machine_id_v3 = patched_get_machine_id_v3
    print("✅ Streamlit Unicode crash patch applied successfully")
except Exception as e:
    print(f"⚠️ Could not apply Streamlit patch: {e}")