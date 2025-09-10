# Add this to your streamlit app for downloads
import streamlit as st
import os

def create_download_section():
    """Add download section to the streamlit app"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("## 📥 Downloads")
    
    # Check if files exist
    files_to_download = {
        "Complete System (ZIP)": "aliya_enhanced_system.zip",
        "Main App File": "download_app.py", 
        "Entity Fix Patch": "entity_drift_fix.py",
        "README": "README_DOWNLOAD.md"
    }
    
    for name, filename in files_to_download.items():
        if os.path.exists(filename):
            with open(filename, "rb") as file:
                st.sidebar.download_button(
                    label=f"📥 {name}",
                    data=file.read(),
                    file_name=filename,
                    mime="application/octet-stream"
                )
        else:
            st.sidebar.text(f"❌ {name} not found")

# Add this function call to your main app
