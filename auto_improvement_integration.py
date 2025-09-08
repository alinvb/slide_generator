#!/usr/bin/env python3
"""
Auto-Improvement Integration Module
Integrates the Enhanced Auto-Improvement System with the main Streamlit application
"""

import json
import streamlit as st
from typing import Dict, Any, Tuple, Optional, List
from enhanced_auto_improvement_system import (
    EnhancedAutoImprovementSystem,
    auto_improve_json_with_api_calls,
    ValidationResult,
    APICallResult
)


class AutoImprovementIntegrator:
    """
    Integration class that connects the enhanced auto-improvement system
    with the Streamlit application's existing infrastructure
    """
    
    def __init__(self):
        self.improvement_system = EnhancedAutoImprovementSystem()
        self.session_key_prefix = "auto_improve_"
        
    def initialize_session_state(self):
        """Initialize session state for auto-improvement functionality"""
        if f"{self.session_key_prefix}enabled" not in st.session_state:
            st.session_state[f"{self.session_key_prefix}enabled"] = False
        
        if f"{self.session_key_prefix}history" not in st.session_state:
            st.session_state[f"{self.session_key_prefix}history"] = []
        
        if f"{self.session_key_prefix}last_results" not in st.session_state:
            st.session_state[f"{self.session_key_prefix}last_results"] = None
            
        if f"{self.session_key_prefix}api_usage" not in st.session_state:
            st.session_state[f"{self.session_key_prefix}api_usage"] = {
                "total_calls": 0,
                "successful_calls": 0,
                "total_tokens": 0,
                "total_time": 0.0
            }

    def get_api_credentials(self) -> Tuple[str, str, str]:
        """Get API credentials from session state"""
        api_key = st.session_state.get('api_key', '')
        model = st.session_state.get('model', 'llama-3.1-sonar-large-128k-online')
        api_service = st.session_state.get('api_service', 'perplexity')
        
        return api_key, model, api_service

    def render_auto_improvement_controls(self):
        """Render auto-improvement controls in sidebar"""
        self.initialize_session_state()
        
        with st.sidebar:
            st.markdown("---")
            st.markdown("### 🔧 Auto-Improvement System")
            
            # Enable/disable toggle
            auto_improve_enabled = st.toggle(
                "Enable Auto-Improvement",
                value=st.session_state[f"{self.session_key_prefix}enabled"],
                help="Automatically improve JSON quality using API calls"
            )
            st.session_state[f"{self.session_key_prefix}enabled"] = auto_improve_enabled
            
            if auto_improve_enabled:
                # Configuration options
                st.markdown("#### Settings")
                
                target_score = st.slider(
                    "Target Quality Score",
                    min_value=0.8,
                    max_value=1.0,
                    value=0.95,
                    step=0.05,
                    help="Target quality score (0.8-1.0)"
                )
                
                max_iterations = st.selectbox(
                    "Max Improvement Iterations",
                    options=[3, 5, 7, 10],
                    index=1,
                    help="Maximum API calls for improvement"
                )
                
                # Update improvement system configuration
                self.improvement_system.target_score_threshold = target_score
                self.improvement_system.max_improvement_iterations = max_iterations
                
                # API usage statistics
                usage_stats = st.session_state[f"{self.session_key_prefix}api_usage"]
                
                if usage_stats["total_calls"] > 0:
                    st.markdown("#### API Usage Statistics")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Total Calls", usage_stats["total_calls"])
                        st.metric("Success Rate", f"{usage_stats['successful_calls']}/{usage_stats['total_calls']}")
                    
                    with col2:
                        st.metric("Total Tokens", f"{usage_stats['total_tokens']:,}")
                        st.metric("Avg Time", f"{usage_stats['total_time']/max(usage_stats['total_calls'], 1):.1f}s")

                # Manual improvement button
                if st.button("🔧 Improve Current JSON", help="Manually trigger improvement"):
                    if 'content_ir_json' in st.session_state and 'render_plan_json' in st.session_state:
                        self.manual_improvement_trigger()
                    else:
                        st.warning("Generate JSON first before improvement")

    def manual_improvement_trigger(self):
        """Manually trigger JSON improvement"""
        api_key, model, api_service = self.get_api_credentials()
        
        if not api_key:
            st.error("❌ Please set your API key first")
            return
        
        # Get current JSONs from session state
        content_ir = st.session_state.get('content_ir_json', {})
        render_plan = st.session_state.get('render_plan_json', {})
        
        if not content_ir and not render_plan:
            st.warning("No JSON data found to improve")
            return
        
        with st.spinner("🔧 Improving JSON quality..."):
            # Improve Content IR if available
            if content_ir:
                improved_content_ir, is_perfect_content, content_report = auto_improve_json_with_api_calls(
                    content_ir, "content_ir", api_key, model, api_service
                )
                st.session_state['content_ir_json'] = improved_content_ir
                
                if is_perfect_content:
                    st.success("✅ Content IR improved to target quality!")
                else:
                    st.warning("⚠️ Content IR partially improved - may need more iterations")
            
            # Improve Render Plan if available
            if render_plan:
                improved_render_plan, is_perfect_render, render_report = auto_improve_json_with_api_calls(
                    render_plan, "render_plan", api_key, model, api_service
                )
                st.session_state['render_plan_json'] = improved_render_plan
                
                if is_perfect_render:
                    st.success("✅ Render Plan improved to target quality!")
                else:
                    st.warning("⚠️ Render Plan partially improved - may need more iterations")
        
        st.rerun()

    def auto_improve_json_if_enabled(self, json_data: Dict[str, Any], json_type: str) -> Dict[str, Any]:
        """
        Automatically improve JSON if auto-improvement is enabled
        Returns improved JSON or original if disabled/failed
        """
        if not st.session_state.get(f"{self.session_key_prefix}enabled", False):
            return json_data
        
        api_key, model, api_service = self.get_api_credentials()
        
        if not api_key:
            st.warning("⚠️ Auto-improvement enabled but no API key provided")
            return json_data
        
        try:
            with st.spinner(f"🔧 Auto-improving {json_type}..."):
                improved_json, is_perfect, improvement_report = auto_improve_json_with_api_calls(
                    json_data, json_type, api_key, model, api_service
                )
                
                # Update session state statistics
                self._update_api_usage_stats(improvement_report)
                
                # Store improvement results
                improvement_result = {
                    "timestamp": st.session_state.get('current_time', 'Unknown'),
                    "json_type": json_type,
                    "original_json": json_data,
                    "improved_json": improved_json,
                    "is_perfect": is_perfect,
                    "report": improvement_report
                }
                
                st.session_state[f"{self.session_key_prefix}last_results"] = improvement_result
                
                # Add to history
                history = st.session_state[f"{self.session_key_prefix}history"]
                history.append(improvement_result)
                
                # Keep only last 10 improvement sessions
                if len(history) > 10:
                    history.pop(0)
                
                # Show improvement notification
                if is_perfect:
                    st.success(f"✅ {json_type.upper()} automatically improved to target quality!")
                else:
                    st.info(f"ℹ️ {json_type.upper()} partially improved (auto-improvement)")
                
                return improved_json
                
        except Exception as e:
            st.error(f"❌ Auto-improvement failed: {str(e)}")
            return json_data

    def _update_api_usage_stats(self, improvement_report: str):
        """Update API usage statistics from improvement report"""
        usage_stats = st.session_state[f"{self.session_key_prefix}api_usage"]
        
        # Parse improvement report for statistics
        # This is a simplified parser - could be enhanced
        try:
            lines = improvement_report.split('\n')
            for line in lines:
                if "API Calls Made:" in line:
                    calls = int(line.split(':')[1].strip())
                    usage_stats["total_calls"] += calls
                elif "Successful Calls:" in line:
                    success_part = line.split(':')[1].strip()
                    successful = int(success_part.split('/')[0])
                    usage_stats["successful_calls"] += successful
                elif "Total Tokens Used:" in line:
                    tokens_str = line.split(':')[1].strip().replace(',', '')
                    tokens = int(tokens_str)
                    usage_stats["total_tokens"] += tokens
                elif "Total Execution Time:" in line:
                    time_str = line.split(':')[1].strip().replace('s', '')
                    execution_time = float(time_str)
                    usage_stats["total_time"] += execution_time
        except:
            pass  # Ignore parsing errors

    def render_improvement_history(self):
        """Render improvement history in main area"""
        history = st.session_state.get(f"{self.session_key_prefix}history", [])
        
        if not history:
            return
        
        with st.expander("📊 Auto-Improvement History", expanded=False):
            for i, result in enumerate(reversed(history[-5:]), 1):  # Show last 5
                st.markdown(f"### Improvement Session {len(history) - i + 1}")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Type:** {result['json_type'].upper()}")
                    st.write(f"**Time:** {result['timestamp']}")
                
                with col2:
                    st.write(f"**Perfect:** {'✅ Yes' if result['is_perfect'] else '⚠️ Partial'}")
                
                with col3:
                    if st.button(f"View Report {len(history) - i + 1}", key=f"report_{len(history) - i + 1}"):
                        st.text_area(
                            "Improvement Report",
                            result['report'],
                            height=300,
                            key=f"report_text_{len(history) - i + 1}"
                        )
                
                st.markdown("---")

    def render_validation_status(self, json_data: Dict[str, Any], json_type: str):
        """Render current JSON validation status"""
        if not st.session_state.get(f"{self.session_key_prefix}enabled", False):
            return
        
        api_key, model, api_service = self.get_api_credentials()
        
        if not api_key:
            return
        
        if st.button(f"🔍 Validate {json_type.upper()}", help="Check current JSON quality"):
            with st.spinner(f"Validating {json_type}..."):
                try:
                    validation_result = self.improvement_system.api_validate_json_structure(
                        json_data, json_type, api_key, model, api_service
                    )
                    
                    if validation_result.success:
                        feedback = json.loads(validation_result.response)
                        score = feedback.get('overall_score', 0.0)
                        
                        # Display validation results
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            score_color = "🟢" if score >= 0.9 else "🟡" if score >= 0.7 else "🔴"
                            st.metric("Quality Score", f"{score_color} {score:.3f}")
                        
                        with col2:
                            is_valid = feedback.get('is_valid', False)
                            st.metric("Status", "✅ Valid" if is_valid else "❌ Invalid")
                        
                        with col3:
                            issues_count = len(feedback.get('issues', []))
                            st.metric("Issues", issues_count)
                        
                        # Show detailed feedback
                        if feedback.get('issues'):
                            st.subheader("Issues Found")
                            for issue in feedback['issues'][:5]:
                                st.write(f"• {issue}")
                        
                        if feedback.get('suggestions'):
                            st.subheader("Suggestions")
                            for suggestion in feedback['suggestions'][:3]:
                                st.write(f"• {suggestion}")
                    
                    else:
                        st.error(f"Validation failed: {validation_result.error}")
                        
                except Exception as e:
                    st.error(f"Validation error: {str(e)}")

    def get_improvement_suggestions(self, json_data: Dict[str, Any], json_type: str) -> List[str]:
        """Get quick improvement suggestions without full API validation"""
        suggestions = []
        
        try:
            if json_type == "content_ir":
                # Check for common Content IR issues
                if "entities" not in json_data or not json_data.get("entities"):
                    suggestions.append("Add company entities information")
                
                if "management_team" in json_data:
                    mgmt = json_data["management_team"]
                    left_profiles = mgmt.get("left_column_profiles", [])
                    right_profiles = mgmt.get("right_column_profiles", [])
                    total_profiles = len(left_profiles) + len(right_profiles)
                    
                    if total_profiles < 2:
                        suggestions.append("Add more management team profiles (minimum 2)")
                    elif total_profiles > 6:
                        suggestions.append("Reduce management team profiles (maximum 6)")
                
                if "strategic_buyers" in json_data:
                    buyers = json_data["strategic_buyers"]
                    if len(buyers) < 3:
                        suggestions.append("Add more strategic buyers (minimum 3-5)")
                
                if "financial_buyers" in json_data:
                    buyers = json_data["financial_buyers"]
                    if len(buyers) < 3:
                        suggestions.append("Add more financial buyers (minimum 3-5)")
            
            elif json_type == "render_plan":
                # Check for common Render Plan issues
                if "slides" not in json_data or not json_data.get("slides"):
                    suggestions.append("Add slides array to render plan")
                
                slides = json_data.get("slides", [])
                for i, slide in enumerate(slides):
                    if "template" not in slide:
                        suggestions.append(f"Add template field to slide {i+1}")
                    if "data" not in slide:
                        suggestions.append(f"Add data object to slide {i+1}")
        
        except Exception:
            suggestions.append("JSON structure validation recommended")
        
        return suggestions


# Global integrator instance
auto_improvement_integrator = AutoImprovementIntegrator()


def integrate_auto_improvement_with_app():
    """
    Main integration function to add auto-improvement to the Streamlit app
    Call this function in your main app to enable auto-improvement features
    """
    # Render controls in sidebar
    auto_improvement_integrator.render_auto_improvement_controls()
    
    # Render history in main area if there's data
    auto_improvement_integrator.render_improvement_history()


def auto_improve_if_enabled(json_data: Dict[str, Any], json_type: str) -> Dict[str, Any]:
    """
    Wrapper function for easy integration with existing JSON generation flow
    """
    return auto_improvement_integrator.auto_improve_json_if_enabled(json_data, json_type)


def render_json_validation_status(json_data: Dict[str, Any], json_type: str):
    """
    Wrapper function to render validation status for any JSON
    """
    auto_improvement_integrator.render_validation_status(json_data, json_type)


def get_quick_suggestions(json_data: Dict[str, Any], json_type: str) -> List[str]:
    """
    Get quick improvement suggestions without API calls
    """
    return auto_improvement_integrator.get_improvement_suggestions(json_data, json_type)


if __name__ == "__main__":
    # Test the integration module
    print("Testing Auto-Improvement Integration...")
    
    # Initialize integrator
    integrator = AutoImprovementIntegrator()
    
    # Test suggestions
    test_json = {"entities": {"company": {"name": "Test"}}}
    suggestions = integrator.get_improvement_suggestions(test_json, "content_ir")
    
    print(f"Sample suggestions: {suggestions}")
    print("✅ Auto-Improvement Integration ready!")