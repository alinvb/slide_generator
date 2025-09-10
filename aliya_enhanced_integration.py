#!/usr/bin/env python3

"""
Aliya Enhanced Integration Layer
Integrates dynamic conversation improvements with existing Aliya system
Preserves ALL JSON generation logic while preventing getting stuck
"""

import streamlit as st
from collections import deque
from enhanced_conversation_manager import enhanced_manager
from typing import Dict, Optional, Tuple, Any

def integrate_enhanced_conversation_into_aliya():
    """
    Integration function that enhances the existing Aliya system with:
    1. Dynamic topic tracking and coverage
    2. Intent classification to prevent getting stuck  
    3. LangChain memory for better context
    4. Anti-repetition system
    5. Auto-advance when topics are satisfied
    
    This preserves ALL existing functionality while adding improvements
    """
    
    # Initialize enhanced conversation state
    enhanced_manager.init_session_state(st.session_state)
    
    def enhanced_chat_input_handler(prompt: str, analyze_conversation_progress_func, 
                                  call_llm_api_func) -> Dict[str, Any]:
        """
        Enhanced version of the chat input handler that integrates with existing Aliya logic
        Returns decision on how to proceed while preserving all existing functionality
        """
        
        # Update conversation memory
        enhanced_manager.update_memory('user', prompt, st.session_state)
        
        # Classify user intent
        user_intent = enhanced_manager.classify_user_intent(prompt)
        st.session_state['conversation_manager']['intent_history'].append(user_intent)
        
        print(f"🧠 [ENHANCED] User intent detected: {user_intent}")
        
        # Get current progress using existing function
        progress_info = analyze_conversation_progress_func(st.session_state.messages)
        current_topic = progress_info.get('current_topic', 'business_overview')
        
        # Check topic satisfaction
        satisfaction = enhanced_manager.assess_topic_satisfaction(current_topic, prompt)
        current_idx = st.session_state['conversation_manager']['current_topic_idx']
        st.session_state['conversation_manager']['topic_satisfaction_scores'][current_idx] = satisfaction
        
        print(f"📊 [ENHANCED] Topic satisfaction for {current_topic}: {satisfaction:.2f}")
        
        # Determine action based on intent and satisfaction
        action_decision = {
            'action': 'continue_normal_flow',  # Default: use existing Aliya logic
            'should_advance': False,
            'intent': user_intent,
            'satisfaction': satisfaction,
            'bridge_message': None,
            'prevent_repetition': False
        }
        
        # Handle research requests (preserve existing research flow)
        if user_intent == "requesting_research":
            action_decision['action'] = 'trigger_research'
            print(f"🔍 [ENHANCED] Research request - using existing research flow")
            return action_decision
        
        # Handle skip/advance requests
        if user_intent in ["skip_move_on", "changing_topic"]:
            if enhanced_manager.should_advance_topic(st.session_state, user_intent, current_topic, prompt):
                # Get current topic before advancing
                from_topic = current_topic
                
                # Advance to next topic
                next_topic = enhanced_manager.advance_to_next_topic(st.session_state)
                
                if next_topic:
                    # Generate bridge message for smooth transition
                    bridge_message = enhanced_manager.generate_bridge_response(
                        from_topic, next_topic, st.session_state, call_llm_api_func
                    )
                    
                    action_decision.update({
                        'action': 'advance_topic',
                        'should_advance': True,
                        'next_topic': next_topic,
                        'bridge_message': bridge_message
                    })
                    
                    print(f"🎯 [ENHANCED] Advancing from {from_topic} to {next_topic}")
                else:
                    # All topics covered - trigger JSON generation
                    action_decision['action'] = 'trigger_json_generation'
                    print(f"🎉 [ENHANCED] All topics covered - ready for JSON generation")
        
        # Auto-advance based on high satisfaction
        elif satisfaction >= 0.8 and user_intent == "answering_question":
            # User provided comprehensive answer - consider auto-advance
            cm = st.session_state['conversation_manager']
            turns_on_topic = cm.get('conversation_turns', 0) - current_idx * 3  # Estimate
            
            if turns_on_topic >= 2:  # Ensure minimum interaction per topic
                from_topic = current_topic
                next_topic = enhanced_manager.advance_to_next_topic(st.session_state)
                
                if next_topic:
                    bridge_message = f"Excellent information on {from_topic.replace('_', ' ')}! " + \
                                   enhanced_manager.generate_bridge_response(
                                       from_topic, next_topic, st.session_state, call_llm_api_func
                                   )
                    
                    action_decision.update({
                        'action': 'auto_advance_topic',
                        'should_advance': True,
                        'next_topic': next_topic,
                        'bridge_message': bridge_message,
                        'reason': 'high_satisfaction'
                    })
                    
                    print(f"🚀 [ENHANCED] Auto-advancing due to high satisfaction: {satisfaction:.2f}")
        
        # Check for repetition prevention
        # This will be used by the existing Aliya logic to avoid asking similar questions
        action_decision['prevent_repetition'] = True  # Always enable this check
        
        # Update conversation turn counter
        st.session_state['conversation_manager']['conversation_turns'] += 1
        
        return action_decision
    
    def check_question_repetition(question: str) -> bool:
        """Check if we're about to ask a similar question (integrates with existing flow)"""
        return enhanced_manager.already_asked_similar(question, st.session_state)
    
    def add_assistant_message_to_memory(message: str) -> None:
        """Add assistant message to enhanced memory system"""
        enhanced_manager.update_memory('assistant', message, st.session_state)
        enhanced_manager.add_assistant_question(message, st.session_state)
    
    def get_conversation_context_for_llm(max_turns: int = 5) -> str:
        """Get rich conversation context for LLM calls"""
        return enhanced_manager.get_conversation_memory(st.session_state, max_turns)
    
    def get_enhanced_progress_info() -> Dict[str, Any]:
        """Get enhanced progress information that includes satisfaction and coverage"""
        return enhanced_manager.get_coverage_progress(st.session_state)
    
    def should_trigger_contextual_followup(topic: str, user_response: str, 
                                         existing_followup_result: Dict) -> bool:
        """
        Enhanced decision for contextual follow-ups that considers:
        1. Existing Aliya contextual logic (preserved)
        2. Topic satisfaction scores
        3. User intent patterns
        4. Conversation history
        """
        
        # Always respect existing Aliya contextual follow-up logic first
        if existing_followup_result.get('needs_more_info', False):
            return True
        
        # Additional enhancement: check satisfaction patterns
        cm = st.session_state.get('conversation_manager', {})
        current_idx = cm.get('current_topic_idx', 0)
        satisfaction = cm.get('topic_satisfaction_scores', [0] * 14)[current_idx]
        
        # If satisfaction is low, suggest follow-up even if existing logic doesn't require it
        if satisfaction < 0.4:
            recent_intents = list(cm.get('intent_history', deque()))[-3:]
            
            # If user has been providing short or unclear answers, suggest follow-up
            if recent_intents.count('providing_partial_info') >= 2:
                return True
        
        return False
    
    def enhance_llm_system_prompt(base_prompt: str, topic: str) -> str:
        """Enhance LLM system prompts with conversation memory and context"""
        
        memory_context = get_conversation_context_for_llm(max_turns=3)
        progress_info = get_enhanced_progress_info()
        
        enhanced_prompt = f"""{base_prompt}
        
ENHANCED CONTEXT:
- Current Topic Progress: {progress_info['covered_count']}/14 topics covered
- Topic Satisfaction: {progress_info['average_satisfaction']:.1%}
- Current Topic: {topic.replace('_', ' ')} (Topic {progress_info['current_topic_idx'] + 1})

RECENT CONVERSATION MEMORY:
{memory_context}

INSTRUCTIONS:
- Build on previous conversation context naturally
- Avoid repeating similar questions from memory
- If user provided partial information, ask for specific missing components
- Maintain professional investment banking tone
- Consider conversation flow when formulating responses"""
        
        return enhanced_prompt
    
    # Return integration functions for use in main app
    return {
        'enhanced_chat_handler': enhanced_chat_input_handler,
        'check_repetition': check_question_repetition,
        'add_to_memory': add_assistant_message_to_memory,
        'get_context': get_conversation_context_for_llm,
        'get_progress': get_enhanced_progress_info,
        'should_followup': should_trigger_contextual_followup,
        'enhance_prompt': enhance_llm_system_prompt
    }

def show_enhanced_progress_sidebar():
    """Enhanced sidebar showing topic coverage, satisfaction, and conversation insights"""
    
    progress_info = enhanced_manager.get_coverage_progress(st.session_state)
    cm = st.session_state.get('conversation_manager', {})
    
    st.sidebar.markdown("### 🎯 Enhanced Topic Progress")
    
    # Progress bar
    st.sidebar.progress(progress_info['progress_percentage'] / 100)
    st.sidebar.caption(f"{progress_info['covered_count']}/14 topics completed")
    
    # Current topic highlight
    st.sidebar.markdown(f"**Current Topic:** {progress_info['current_topic_id'].replace('_', ' ').title()}")
    
    # Satisfaction metrics
    avg_satisfaction = progress_info['average_satisfaction']
    satisfaction_color = "🟢" if avg_satisfaction >= 0.7 else "🟡" if avg_satisfaction >= 0.4 else "🔴"
    st.sidebar.markdown(f"**Quality Score:** {satisfaction_color} {avg_satisfaction:.1%}")
    
    # Recent intents
    recent_intents = list(cm.get('intent_history', deque()))[-3:]
    if recent_intents:
        st.sidebar.markdown("**Recent Intents:**")
        for intent in recent_intents:
            st.sidebar.caption(f"• {intent.replace('_', ' ').title()}")
    
    # Conversation insights
    conversation_turns = cm.get('conversation_turns', 0)
    st.sidebar.markdown(f"**Conversation Turns:** {conversation_turns}")
    
    # Topic breakdown
    with st.sidebar.expander("📊 Topic Details"):
        covered = cm.get('covered_topics', [False] * 14)
        satisfaction_scores = cm.get('topic_satisfaction_scores', [0] * 14)
        
        topic_names = [
            "Business Overview", "Product/Service Footprint", "Financial Performance",
            "Management Team", "Growth Strategy", "Competitive Positioning",
            "Precedent Transactions", "Valuation Overview", "Strategic Buyers",
            "Financial Buyers", "SEA Conglomerates", "Margin Resilience",
            "Investor Considerations", "Investment Process"
        ]
        
        for i, (name, is_covered, satisfaction) in enumerate(zip(topic_names, covered, satisfaction_scores)):
            status = "✅" if is_covered else "⏳" if i == progress_info['current_topic_idx'] else "⭕"
            quality = f"{satisfaction:.0%}" if satisfaction > 0 else "N/A"
            st.caption(f"{status} {name} ({quality})")

# Example usage and integration points for main app
if __name__ == "__main__":
    print("🚀 Enhanced Conversation Manager Ready for Aliya Integration!")
    print("=" * 60)
    print("✅ Dynamic topic tracking and coverage")
    print("✅ LangChain memory integration with fallback")
    print("✅ Intent classification (transformers + regex fallback)")
    print("✅ Anti-repetition system using n-gram similarity")
    print("✅ Auto-advance based on topic satisfaction")
    print("✅ Natural transition generation between topics")
    print("✅ Enhanced progress tracking and insights")
    print("✅ Preserves ALL existing JSON generation logic")
    print("✅ Contextual follow-up enhancement")
    print("\n🎯 Ready to integrate into main app.py!")