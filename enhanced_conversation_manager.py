#!/usr/bin/env python3

"""
Enhanced Conversation Manager for Aliya Investment Banking System
Integrates dynamic conversation flow, LangChain memory, and intent classification
while preserving all existing JSON generation and contextual follow-up logic
"""

import os
import re
import json
from collections import deque
from typing import Dict, List, Optional, Tuple, Any

# --- Optional dependencies with graceful fallback ---
try:
    from langchain.memory import ConversationBufferMemory
    _HAS_LANGCHAIN = True
except Exception:
    ConversationBufferMemory = None
    _HAS_LANGCHAIN = False

try:
    from transformers import pipeline
    _ZERO_SHOT = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    _HAS_TRANSFORMERS = True
except Exception:
    _ZERO_SHOT = None
    _HAS_TRANSFORMERS = False

class EnhancedConversationManager:
    """
    Enhanced conversation manager that prevents getting stuck and provides
    dynamic conversation flow while preserving all Aliya functionality
    """
    
    def __init__(self):
        self.intent_labels = [
            "answering_question",
            "rejecting_repetition", 
            "changing_topic",
            "skip_move_on",
            "chit_chat",
            "requesting_research",
            "providing_partial_info",
            "asking_clarification"
        ]
        
        # Topic completion hints for auto-detection
        self.topic_hints = {
            "business_overview": ["industry", "sector", "business", "model", "employees", "offices", "founded"],
            "product_service_footprint": ["product", "service", "customer", "client", "solution", "differentiation"],
            "historical_financial_performance": ["revenue", "sales", "ebitda", "margin", "growth", "profit"],
            "management_team": ["ceo", "cfo", "founder", "executive", "management", "background"],
            "growth_strategy_projections": ["growth", "strategy", "projection", "expansion", "plan", "target"],
            "competitive_positioning": ["competitor", "competition", "advantage", "market", "share", "position"],
            "precedent_transactions": ["transaction", "acquisition", "merger", "deal", "valuation", "multiple"],
            "valuation_overview": ["valuation", "dcf", "multiple", "comps", "precedent", "enterprise"],
            "strategic_buyers": ["buyer", "acquirer", "strategic", "synergy", "rationale", "capacity"],
            "financial_buyers": ["private", "equity", "pe", "fund", "investor", "criteria"],
            "sea_conglomerates": ["conglomerate", "asia", "sea", "singapore", "regional", "group"],
            "margin_cost_resilience": ["margin", "cost", "resilience", "scalable", "efficiency", "structure"],
            "investor_considerations": ["risk", "opportunity", "challenge", "threat", "mitigation", "upside"],
            "investor_process_overview": ["process", "timeline", "diligence", "documentation", "requirements"]
        }
    
    def init_session_state(self, session_state: Dict) -> None:
        """Initialize enhanced session state for dynamic conversation management"""
        
        if 'conversation_manager' not in session_state:
            session_state['conversation_manager'] = {
                'covered_topics': [False] * 14,  # Track completion of all 14 topics
                'current_topic_idx': 0,
                'assistant_questions': deque(maxlen=10),  # Recent AI questions to avoid repetition
                'intent_history': deque(maxlen=5),  # Recent user intents
                'topic_satisfaction_scores': [0] * 14,  # Satisfaction level per topic (0-1)
                'conversation_turns': 0,
                'last_research_topic': None,
                'partial_info_buffer': {}  # Store partial info per topic
            }
        
        # Initialize LangChain memory if available
        if _HAS_LANGCHAIN and 'lc_memory' not in session_state:
            try:
                session_state['lc_memory'] = ConversationBufferMemory(
                    return_messages=True,
                    memory_key="chat_history"
                )
            except Exception:
                session_state['lc_memory'] = deque(maxlen=20)
        elif 'lc_memory' not in session_state:
            session_state['lc_memory'] = deque(maxlen=20)
    
    def classify_user_intent(self, user_message: str) -> str:
        """Classify user intent using transformers or fallback to regex"""
        
        user_lower = user_message.lower().strip()
        
        # PRIORITY: Handle short confirmatory responses FIRST to prevent misclassification
        if user_lower in ["ok", "okay", "yes", "sure", "right", "correct", "sounds good", 
                         "that's right", "good", "fine", "alright", "yep", "yeah"]:
            return "answering_question"
        
        # Handle very short responses that are clearly not research requests
        if len(user_message.split()) <= 2 and not any(word in user_lower for word in 
                                                      ["research", "find", "look", "search"]):
            return "answering_question"
        
        # Primary: Use transformers zero-shot classification if available
        if _HAS_TRANSFORMERS and _ZERO_SHOT:
            try:
                result = _ZERO_SHOT(user_message, self.intent_labels)
                if result and 'labels' in result and len(result['labels']) > 0:
                    # Double-check: Don't trust transformers for obvious short responses
                    predicted_intent = result['labels'][0]
                    if predicted_intent == "requesting_research" and len(user_message.split()) <= 3:
                        if not any(word in user_lower for word in ["research", "find", "look", "search", "investigate"]):
                            print(f"⚠️ Overriding transformers research classification for short response: '{user_message}'")
                            return "answering_question"
                    return predicted_intent
            except Exception as e:
                print(f"⚠️ Intent classification failed: {e}")
        
        # Fallback: Regex-based intent detection
        if any(phrase in user_lower for phrase in [
            "research for me", "research this", "research it", "find information", "look up"
        ]):
            return "requesting_research"
        
        if any(phrase in user_lower for phrase in [
            "skip this", "move on", "next topic", "skip topic", "next question"
        ]):
            return "skip_move_on"
        
        if any(phrase in user_lower for phrase in [
            "let's talk about", "what about", "tell me about", "i want to discuss"
        ]):
            return "changing_topic"
        
        if any(phrase in user_lower for phrase in [
            "that's wrong", "not correct", "i disagree", "actually"
        ]):
            return "rejecting_repetition"
        
        if any(phrase in user_lower for phrase in [
            "what do you mean", "can you clarify", "explain", "i don't understand"
        ]):
            return "asking_clarification"
        
        # Check if user provided partial information
        if len(user_message.split()) > 3 and not user_message.endswith('?'):
            return "providing_partial_info"
        
        # Default to answering question
        return "answering_question"
    
    def assess_topic_satisfaction(self, topic_id: str, user_message: str) -> float:
        """Assess how well user response satisfies current topic (0.0 to 1.0)"""
        
        if topic_id not in self.topic_hints:
            return 0.5  # Default moderate satisfaction
        
        user_lower = user_message.lower()
        topic_keywords = self.topic_hints[topic_id]
        
        # Count keyword matches
        matches = sum(1 for keyword in topic_keywords if keyword in user_lower)
        satisfaction_score = min(matches / len(topic_keywords), 1.0)
        
        # Boost score for longer, detailed responses
        if len(user_message.split()) > 15:
            satisfaction_score = min(satisfaction_score + 0.2, 1.0)
        
        # Reduce score for very short responses
        if len(user_message.split()) < 5:
            satisfaction_score *= 0.6
        
        return satisfaction_score
    
    def already_asked_similar(self, question: str, session_state: Dict) -> bool:
        """Check if we already asked a similar question using n-gram similarity"""
        
        assistant_questions = session_state.get('conversation_manager', {}).get('assistant_questions', deque())
        
        if not assistant_questions:
            return False
        
        # Normalize question for comparison
        normalized_question = self._normalize_text(question)
        question_ngrams = set(self._get_ngrams(normalized_question, n=3))
        
        for prev_question in assistant_questions:
            prev_normalized = self._normalize_text(prev_question)
            prev_ngrams = set(self._get_ngrams(prev_normalized, n=3))
            
            # Calculate Jaccard similarity
            if question_ngrams and prev_ngrams:
                intersection = len(question_ngrams.intersection(prev_ngrams))
                union = len(question_ngrams.union(prev_ngrams))
                similarity = intersection / union if union > 0 else 0
                
                if similarity > 0.7:  # High similarity threshold
                    return True
        
        return False
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text for comparison (fixed bug from original code)"""
        # Fixed regex: was r"\[a-z0-9\]+" now r"[a-z0-9]+"
        return ' '.join(re.findall(r"[a-z0-9]+", text.lower()))
    
    def _get_ngrams(self, text: str, n: int = 3) -> List[str]:
        """Generate n-grams from text"""
        words = text.split()
        if len(words) < n:
            return [text]
        return [' '.join(words[i:i+n]) for i in range(len(words) - n + 1)]
    
    def should_advance_topic(self, session_state: Dict, user_intent: str, 
                           topic_id: str, user_message: str) -> bool:
        """Determine if we should advance to next topic"""
        
        cm = session_state.get('conversation_manager', {})
        current_idx = cm.get('current_topic_idx', 0)
        
        # Explicit skip request
        if user_intent == "skip_move_on":
            return True
        
        # Topic change request
        if user_intent == "changing_topic":
            return True
        
        # Auto-advance based on satisfaction
        satisfaction = self.assess_topic_satisfaction(topic_id, user_message)
        cm['topic_satisfaction_scores'][current_idx] = satisfaction
        
        if satisfaction >= 0.8:  # High satisfaction threshold
            return True
        
        return False
    
    def advance_to_next_topic(self, session_state: Dict) -> Optional[str]:
        """Mark current topic covered and advance to next uncovered topic"""
        
        cm = session_state['conversation_manager']
        current_idx = cm['current_topic_idx']
        
        # Mark current topic as covered
        cm['covered_topics'][current_idx] = True
        
        # Find next uncovered topic
        for i in range(current_idx + 1, 14):
            if not cm['covered_topics'][i]:
                cm['current_topic_idx'] = i
                return self._get_topic_id_by_index(i)
        
        # All topics covered
        return None
    
    def _get_topic_id_by_index(self, idx: int) -> str:
        """Map topic index to topic ID"""
        topic_map = [
            "business_overview", "product_service_footprint", "historical_financial_performance",
            "management_team", "growth_strategy_projections", "competitive_positioning",
            "precedent_transactions", "valuation_overview", "strategic_buyers",
            "financial_buyers", "sea_conglomerates", "margin_cost_resilience",
            "investor_considerations", "investor_process_overview"
        ]
        return topic_map[idx] if 0 <= idx < len(topic_map) else "business_overview"
    
    def add_assistant_question(self, question: str, session_state: Dict) -> None:
        """Add assistant question to history for duplicate detection"""
        cm = session_state.get('conversation_manager', {})
        if 'assistant_questions' not in cm:
            cm['assistant_questions'] = deque(maxlen=10)
        cm['assistant_questions'].append(question)
    
    def get_conversation_memory(self, session_state: Dict, max_turns: int = 5) -> str:
        """Extract recent conversation memory for context"""
        
        if _HAS_LANGCHAIN and hasattr(session_state.get('lc_memory'), 'chat_memory'):
            try:
                messages = session_state['lc_memory'].chat_memory.messages
                recent_messages = messages[-max_turns*2:] if messages else []
                
                transcript = []
                for msg in recent_messages:
                    role = "User" if hasattr(msg, 'content') and getattr(msg, 'type', None) == 'human' else "AI"
                    content = getattr(msg, 'content', str(msg))
                    transcript.append(f"{role}: {content[:200]}...")
                
                return "\n".join(transcript)
            except Exception:
                pass
        
        # Fallback to session messages
        messages = session_state.get('messages', [])
        recent_messages = messages[-max_turns*2:] if messages else []
        
        transcript = []
        for msg in recent_messages:
            role = "User" if msg.get('role') == 'user' else "AI"
            content = msg.get('content', '')[:200]
            transcript.append(f"{role}: {content}...")
        
        return "\n".join(transcript)
    
    def update_memory(self, role: str, content: str, session_state: Dict) -> None:
        """Update conversation memory with new message"""
        
        if _HAS_LANGCHAIN and hasattr(session_state.get('lc_memory'), 'chat_memory'):
            try:
                if role == 'user':
                    session_state['lc_memory'].chat_memory.add_user_message(content)
                else:
                    session_state['lc_memory'].chat_memory.add_ai_message(content)
            except Exception:
                # Fallback to deque
                if isinstance(session_state['lc_memory'], deque):
                    session_state['lc_memory'].append({'role': role, 'content': content})
        elif isinstance(session_state.get('lc_memory'), deque):
            session_state['lc_memory'].append({'role': role, 'content': content})
    
    def generate_bridge_response(self, from_topic: str, to_topic: str, 
                                session_state: Dict, call_llm_api) -> str:
        """Generate natural transition between topics"""
        
        memory = self.get_conversation_memory(session_state, max_turns=3)
        company_name = session_state.get('company_name', 'your company')
        
        bridge_prompt = f"""You are a senior investment banking advisor conducting a professional interview for {company_name}. 
        
        CONTEXT: You just finished discussing {from_topic.replace('_', ' ')} and are now transitioning to {to_topic.replace('_', ' ')}.
        
        RECENT CONVERSATION:
        {memory}
        
        Generate a natural, professional transition that:
        1. Briefly acknowledges the previous topic discussion
        2. Smoothly introduces the new topic 
        3. Maintains conversational flow
        4. Uses investment banking terminology appropriately
        
        Keep response to 2-3 sentences maximum."""
        
        try:
            bridge_messages = [
                {"role": "system", "content": bridge_prompt},
                {"role": "user", "content": f"Generate transition from {from_topic} to {to_topic}"}
            ]
            
            return call_llm_api(
                bridge_messages,
                session_state.get('model', 'claude-3-5-sonnet-20241022'),
                session_state['api_key'],
                session_state.get('api_service', 'claude')
            )
        except Exception as e:
            print(f"⚠️ Bridge generation failed: {e}")
            return f"Thank you for that information about {from_topic.replace('_', ' ')}. Now let's discuss {to_topic.replace('_', ' ')}."
    
    def get_coverage_progress(self, session_state: Dict) -> Dict[str, Any]:
        """Get current topic coverage progress"""
        
        cm = session_state.get('conversation_manager', {})
        covered = cm.get('covered_topics', [False] * 14)
        current_idx = cm.get('current_topic_idx', 0)
        satisfaction_scores = cm.get('topic_satisfaction_scores', [0] * 14)
        
        return {
            'covered_count': sum(covered),
            'total_topics': 14,
            'current_topic_idx': current_idx,
            'current_topic_id': self._get_topic_id_by_index(current_idx),
            'progress_percentage': sum(covered) / 14 * 100,
            'average_satisfaction': sum(satisfaction_scores) / len(satisfaction_scores),
            'is_complete': sum(covered) == 14
        }

# Global instance for easy access
enhanced_manager = EnhancedConversationManager()