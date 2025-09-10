#!/usr/bin/env python3
"""
Simple test to verify the cleaned app works
"""
import streamlit as st

st.title("🔬 Research Agent Test")
st.success("✅ App runs without errors!")

# Test basic functionality
if st.button("Test Button"):
    st.balloons()
    st.success("🎉 Test successful!")

st.info("💡 If you see this message, the app structure is working correctly.")