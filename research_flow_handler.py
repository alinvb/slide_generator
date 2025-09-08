#!/usr/bin/env python3
"""
Research Flow Handler
Ensures proper research confirmation and user satisfaction checking
"""

import re
from typing import List, Dict, Any, Tuple

class ResearchFlowHandler:
    """
    Handles the research flow to ensure proper user confirmation and satisfaction checking
    """
    
    def __init__(self):
        self.research_indicators = [
            "research this", "research for me", "i don't know", "find information",
            "search for", "look up", "investigate", "research it"
        ]
        
        self.satisfaction_questions = [
            "Are you satisfied with this information, or would you like me to research something more specific?",
            "Is this research helpful, or should I investigate any particular aspect in more detail?", 
            "Does this research answer your needs, or would you like me to dig deeper into any specific area?",
            "Are you happy with this research, or should I look into something more particular?",
            "Is this sufficient, or would you like me to research any specific aspect in more depth?"
        ]
    
    def detect_research_request(self, user_message: str) -> bool:
        """
        Detect if user is requesting research
        """
        message_lower = user_message.lower().strip()
        
        # Direct research requests
        for indicator in self.research_indicators:
            if indicator in message_lower:
                return True
        
        # Short responses that might indicate lack of knowledge
        if len(message_lower.split()) <= 3 and any(word in message_lower for word in ["no", "not sure", "unsure", "dunno"]):
            return True
            
        return False
    
    def detect_research_response(self, ai_response: str) -> bool:
        """
        Detect if AI response contains research (vs direct question or JSON)
        """
        research_signals = [
            "based on", "according to", "research shows", "sources indicate",
            "here is", "here are", "[1]", "[2]", "[3]", "reports suggest",
            "available data", "industry analysis", "recent studies"
        ]
        
        response_lower = ai_response.lower()
        
        # Check for research indicators
        has_research_signals = any(signal in response_lower for signal in research_signals)
        
        # Check for reference citations
        has_citations = bool(re.search(r'\[\d+\]', ai_response))
        
        # Check if it's longer than typical interview question (research tends to be longer)
        is_substantial = len(ai_response) > 500
        
        return (has_research_signals or has_citations) and is_substantial
    
    def needs_satisfaction_check(self, conversation_messages: List[Dict[str, Any]]) -> Tuple[bool, str]:
        """
        Check if the conversation needs a satisfaction check after research
        """
        if len(conversation_messages) < 2:
            return False, ""
        
        # Get last AI response and user message
        last_ai_response = ""
        last_user_message = ""
        
        for msg in reversed(conversation_messages):
            if msg.get("role") == "assistant" and not last_ai_response:
                last_ai_response = msg.get("content", "")
            elif msg.get("role") == "user" and not last_user_message:
                last_user_message = msg.get("content", "")
            
            if last_ai_response and last_user_message:
                break
        
        # Check if last AI response was research
        if self.detect_research_response(last_ai_response):
            # Check if AI already asked satisfaction question
            satisfaction_asked = any(
                question.lower().replace("?", "") in last_ai_response.lower() 
                for question in self.satisfaction_questions
            )
            
            if not satisfaction_asked:
                # Need to add satisfaction check
                import random
                satisfaction_question = random.choice(self.satisfaction_questions)
                return True, satisfaction_question
        
        return False, ""
    
    def get_enhanced_research_prompt(self, original_prompt: str, topic: str) -> str:
        """
        Enhance the prompt to ensure satisfaction checking after research
        """
        
        research_enhancement = f"""

🔍 RESEARCH PROTOCOL FOR {topic.upper()}:
1. Provide comprehensive research on the requested topic
2. Include relevant sources and citations where possible  
3. MANDATORY: End your response with a satisfaction check question
4. Use one of these satisfaction questions:
   - "Are you satisfied with this information, or would you like me to research something more specific?"
   - "Is this research helpful, or should I investigate any particular aspect in more detail?"
   - "Does this research answer your needs, or would you like me to dig deeper into any specific area?"

⚠️ CRITICAL: You MUST ask for satisfaction confirmation after providing research. Do not proceed to the next topic without user confirmation."""

        return original_prompt + research_enhancement
    
    def create_satisfaction_follow_up(self, research_response: str) -> str:
        """
        Add satisfaction check to research response if missing
        """
        # Check if satisfaction question already present
        has_satisfaction = any(
            question.lower().replace("?", "") in research_response.lower() 
            for question in self.satisfaction_questions
        )
        
        if not has_satisfaction:
            import random
            satisfaction_question = random.choice(self.satisfaction_questions)
            return research_response + "\n\n" + satisfaction_question
        
        return research_response
    
    def should_proceed_to_next_topic(self, user_response: str) -> bool:
        """
        Check if user response indicates satisfaction and readiness to proceed
        """
        proceed_indicators = [
            "satisfied", "good", "proceed", "next", "continue", "ok", "okay", 
            "fine", "sufficient", "enough", "yes", "that's good", "looks good"
        ]
        
        response_lower = user_response.lower().strip()
        
        # Direct proceed indicators
        for indicator in proceed_indicators:
            if indicator in response_lower:
                return True
        
        # Short positive responses
        if response_lower in ["ok", "good", "yes", "sure", "right", "correct"]:
            return True
            
        return False


# Global instance for use in app
research_flow_handler = ResearchFlowHandler()


if __name__ == "__main__":
    # Test the research flow handler
    handler = ResearchFlowHandler()
    
    print("🧪 Testing Research Flow Handler")
    print("=" * 40)
    
    # Test research detection
    test_messages = [
        "research this for me",
        "I don't know about that", 
        "Can you find information?",
        "My company is TechCorp"
    ]
    
    for msg in test_messages:
        is_research = handler.detect_research_request(msg)
        print(f"'{msg}' -> Research request: {is_research}")
    
    print("\n✅ Research flow handler working!")