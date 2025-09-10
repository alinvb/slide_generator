"""
Sequential Topic Manager for Investment Banking Pitch Deck Interview
Manages topic-by-topic flow and ensures sequential progression through all topics.
"""
import streamlit as st


class SequentialTopicManager:
    """Manages sequential topic flow for investment banking pitch deck interviews"""
    
    def __init__(self):
        self.topics = [
            {'id': 'business_overview', 'name': 'Business Overview', 'description': 'Company background and core business model'},
            {'id': 'market_analysis', 'name': 'Market Analysis', 'description': 'Market size, trends, and dynamics'},
            {'id': 'competitive_positioning', 'name': 'Competitive Positioning', 'description': 'Competitive landscape and differentiation'},
            {'id': 'financial_performance', 'name': 'Financial Performance', 'description': 'Historical and current financial metrics'},
            {'id': 'growth_strategy', 'name': 'Growth Strategy', 'description': 'Future growth plans and initiatives'},
            {'id': 'management_team', 'name': 'Management Team', 'description': 'Key executives and leadership'},
            {'id': 'valuation', 'name': 'Valuation', 'description': 'Company valuation and metrics'},
            {'id': 'strategic_buyers', 'name': 'Strategic Buyers', 'description': 'Potential strategic acquirers'},
            {'id': 'financial_buyers', 'name': 'Financial Buyers', 'description': 'Private equity and financial buyers'},
            {'id': 'transaction_rationale', 'name': 'Transaction Rationale', 'description': 'Strategic rationale for transaction'},
            {'id': 'synergies', 'name': 'Synergies', 'description': 'Revenue and cost synergies'},
            {'id': 'risks_mitigants', 'name': 'Risks & Mitigants', 'description': 'Key risks and mitigation strategies'},
            {'id': 'timeline', 'name': 'Timeline', 'description': 'Transaction timeline and milestones'},
            {'id': 'next_steps', 'name': 'Next Steps', 'description': 'Immediate action items'}
        ]
        
        # Initialize session state for topic management
        if 'current_topic_index' not in st.session_state:
            st.session_state.current_topic_index = 0
        if 'topic_data' not in st.session_state:
            st.session_state.topic_data = {}
        if 'company_name' not in st.session_state:
            st.session_state.company_name = None
    
    def get_current_topic(self):
        """Get the current topic object"""
        if st.session_state.current_topic_index < len(self.topics):
            return self.topics[st.session_state.current_topic_index]
        return None
    
    def start_topic(self, topic_obj):
        """Start a new topic and return the initial prompt"""
        topic_name = topic_obj['name']
        topic_desc = topic_obj['description']
        company_name = st.session_state.get('company_name', 'the company')
        
        return f"""Let's start with **{topic_name}** for {company_name}.

{topic_desc}

I'll research this topic for you. Please tell me what specific aspects you'd like me to focus on, or say "research this" and I'll gather comprehensive information about {company_name}'s {topic_name.lower()}.

You can also say "next topic" when you're satisfied with the information to move forward."""
    
    def ask_topic_completion(self, topic_obj):
        """Ask if the current topic is complete"""
        topic_name = topic_obj['name']
        return f"""Are you satisfied with the {topic_name.lower()} information we've gathered?

You can:
- Ask for more specific details about any aspect
- Say "research more about [specific area]" for additional information  
- Say "next topic" to move to the next section
- Say "skip this topic" to move forward without additional research

What would you like to do next?"""
    
    def check_skip_request(self, user_message):
        """Check if user wants to skip the current topic"""
        skip_phrases = [
            'skip this topic', 'skip topic', 'skip this', 'skip slide',
            'next topic', 'move to next', 'next section', 'continue',
            'go to next', 'proceed to next'
        ]
        
        user_lower = user_message.lower().strip()
        return any(phrase in user_lower for phrase in skip_phrases)
    
    def skip_current_topic(self, topic_obj):
        """Skip the current topic and move to next"""
        # Move to next topic
        st.session_state.current_topic_index += 1
        
        # Get next topic
        next_topic = self.get_current_topic()
        
        if next_topic:
            return f"""✅ Skipped **{topic_obj['name']}**.

{self.start_topic(next_topic)}"""
        else:
            return """✅ All topics completed! 

I have all the information needed to create your investment banking pitch deck. The presentation will include comprehensive analysis across all key areas."""
    
    def save_topic_data(self, topic_id, data):
        """Save data for a specific topic"""
        if 'topic_data' not in st.session_state:
            st.session_state.topic_data = {}
        st.session_state.topic_data[topic_id] = data
    
    def is_interview_complete(self):
        """Check if all topics have been completed"""
        return st.session_state.current_topic_index >= len(self.topics)
    
    def generate_research_instruction(self, topic_obj, user_prompt):
        """Generate research instruction for the current topic"""
        company_name = st.session_state.get('company_name', 'the company')
        topic_name = topic_obj['name']
        
        instruction = f"""Research {company_name}'s {topic_name.lower()} focusing on:

{topic_obj['description']}

User's specific request: {user_prompt}

Please provide comprehensive, factual information suitable for an investment banking pitch deck."""
        
        return instruction
    
    def verify_factual_accuracy(self, topic_id, user_input):
        """Verify factual accuracy of user input for known companies"""
        # Check for suspicious patterns that might indicate fictional data
        suspicious_patterns = [
            # Celebrity names that shouldn't be company executives
            'elon musk', 'jeff bezos', 'bill gates', 'mark zuckerberg',
            'warren buffett', 'steve jobs', 'tim cook',
            # Fictional characters
            'tony stark', 'bruce wayne', 'clark kent', 'peter parker',
            # Unrealistic financial data
            'trillion revenue', 'billion employees', 'thousand% growth'
        ]
        
        user_lower = user_input.lower()
        
        for pattern in suspicious_patterns:
            if pattern in user_lower:
                return f"""⚠️ **Fact Check Required**

I notice some information that seems unusual or potentially inaccurate. For investment banking presentations, we need verified, factual data.

Could you please:
1. Double-check this information for accuracy
2. Provide verified sources if possible  
3. Or let me research this topic to ensure we have correct data

Would you like me to research this topic instead to get accurate information?"""
        
        return None  # No issues detected


# Create global instance
sequential_topic_manager = SequentialTopicManager()