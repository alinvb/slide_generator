#!/usr/bin/env python3
"""
Research Agent - Clean and Simple Investment Banking Research System
Replaces the complicated chatbot with a straightforward research approach.
"""

import streamlit as st
import json
import time
from typing import Dict, List, Tuple, Any

# Import existing functions from app.py
from app import (
    call_llm_api,
    _run_research,
    _current_company
)
from bulletproof_json_generator import generate_bulletproof_json

def init_research_agent():
    """Initialize the Research Agent system"""
    st.set_page_config(
        page_title="Research Agent - AI Investment Banking Research", 
        page_icon="🔬", 
        layout="wide"
    )
    
    # Initialize session state
    if 'research_results' not in st.session_state:
        st.session_state.research_results = {}
    if 'research_completed' not in st.session_state:
        st.session_state.research_completed = False
    if 'fact_check_results' not in st.session_state:
        st.session_state.fact_check_results = {}

def get_research_prompts() -> Dict[str, Dict[str, str]]:
    """
    Get research prompts for all 14 investment banking topics
    Based on RESEARCH_INSTRUCTIONS_AND_REQUIREMENTS.md
    """
    return {
        "business_overview": {
            "title": "Business Overview & Strategy", 
            "prompt": """Research comprehensive business overview for {company}:
            
REQUIRED INFORMATION:
- Company name and legal structure (Inc, Corp, LLC, etc.)
- Detailed business description and core operations  
- Industry classification and market positioning
- Founding year and key milestones
- Headquarters location and geographic presence
- Employee count and organizational structure
- Primary business model and revenue streams
- Strategic positioning and competitive advantages

RESEARCH INSTRUCTIONS:
Focus on factual, verifiable information about the company's core business operations, organizational structure, and strategic market position. Include specific details about business model, geographic footprint, and operational scale.

Provide sources with readable titles and links. Be comprehensive but concise.""",
            "required_fields": ["name", "business_description", "founding_year", "legal_structure", "core_operations", "target_markets"]
        },
        
        "product_service_footprint": {
            "title": "Product/Service Footprint",
            "prompt": """Research {company}'s product and service portfolio:

REQUIRED INFORMATION:
- Complete list of products/services with descriptions
- Geographic markets and operational coverage
- Distribution channels and go-to-market strategy  
- Customer segments and target demographics
- Pricing models and revenue streams by product/service
- Market share and competitive positioning by offering
- International presence and localization strategies

RESEARCH INSTRUCTIONS:
Document the full scope of offerings, geographic reach, and market penetration. Include specific details about how products/services are delivered to customers across different markets.

Focus on quantifiable metrics where available (number of markets, customer counts, geographic coverage percentages).""",
            "required_fields": ["products_services", "geographic_coverage", "target_customers", "distribution_channels"]
        },
        
        "historical_financial_performance": {
            "title": "Historical Financial Performance", 
            "prompt": """Research {company}'s financial performance and metrics:

REQUIRED INFORMATION:
- Revenue figures for last 3-5 years with growth rates
- EBITDA, operating margins, and profitability metrics
- Key financial ratios and performance indicators
- Revenue breakdown by segment/geography if available
- Cash flow metrics and working capital trends
- Debt levels, capital structure, and financing history
- Key performance drivers and seasonal patterns

RESEARCH INSTRUCTIONS:
Prioritize verified financial data from annual reports, SEC filings, or credible financial databases. Include specific numbers with dates and sources. Calculate growth rates and highlight trends.

For private companies, seek estimates from industry reports or credible financial news sources.""",
            "required_fields": ["revenue_3_5_years", "ebitda_margins", "growth_rates", "key_metrics"]
        },

        "management_team": {
            "title": "Management Team & Leadership",
            "prompt": """Research {company}'s executive leadership team:

REQUIRED INFORMATION:
- CEO: Full name, title, background, tenure, key achievements
- CFO: Full name, title, background, tenure, financial expertise  
- 4-6 additional senior executives with names, titles, backgrounds
- Board composition and key independent directors
- Leadership experience and track record
- Educational backgrounds and professional history
- Previous companies and relevant experience
- Any leadership changes or succession planning

RESEARCH INSTRUCTIONS:
Focus on current leadership team with verified names, exact titles, and detailed professional backgrounds. Include specific experience relevant to investment banking evaluation.

Prioritize executives directly involved in strategic and financial decision-making.""",
            "required_fields": ["ceo", "cfo", "senior_executives", "leadership_experience"]
        },

        "growth_strategy_projections": {
            "title": "Growth Strategy & Projections",
            "prompt": """Research {company}'s growth strategy and future outlook:

REQUIRED INFORMATION:
- Strategic growth initiatives and expansion plans
- Market expansion opportunities and geographic growth
- Product/service innovation and R&D investments
- Acquisition strategy and M&A pipeline
- Technology investments and digital transformation
- Revenue growth projections and targets
- Market trends driving growth opportunities
- Capital allocation strategy for growth

RESEARCH INSTRUCTIONS:
Focus on publicly announced strategic initiatives, confirmed expansion plans, and market opportunities. Include specific timelines, investment amounts, and projected outcomes where available.

Distinguish between confirmed plans and speculative opportunities.""",
            "required_fields": ["growth_initiatives", "expansion_plans", "market_opportunities", "projections"]
        },

        "competitive_positioning": {
            "title": "Competitive Positioning",
            "prompt": """Research {company}'s competitive landscape and positioning:

REQUIRED INFORMATION:  
- Top 5-7 direct competitors with names and descriptions
- Market share analysis and competitive advantages
- Differentiation factors and unique value propositions
- Competitive threats and market challenges
- Industry dynamics and market structure
- Competitive response strategies
- Barriers to entry and competitive moats
- Market leadership position and brand strength

RESEARCH INSTRUCTIONS:
Identify and analyze direct competitors operating in similar markets with comparable business models. Include specific market share data, competitive advantages, and differentiation factors.

Focus on competitors that would be relevant for investment banking evaluation and strategic assessment.""",
            "required_fields": ["competitors", "market_share", "competitive_advantages", "differentiation"]
        },

        "precedent_transactions": {
            "title": "Precedent Transactions",
            "prompt": """Research relevant M&A transactions for {company} valuation:

REQUIRED INFORMATION:
- 4-6 precedent transactions in same/similar industry
- Transaction details: target, acquirer, date, enterprise value
- Revenue/EBITDA multiples and valuation metrics
- Deal rationale and strategic fit factors
- Geographic relevance (prioritize SEA/APAC if applicable)
- Transaction premiums and control premiums
- Market conditions at time of transaction
- Deal structure and consideration type

RESEARCH INSTRUCTIONS:
Focus on transactions involving companies with similar business models, geographic footprint, and scale. Prioritize recent transactions (last 3-5 years) with disclosed financial terms.

Include specific valuation multiples and deal metrics where available.""",
            "required_fields": ["transactions", "valuation_multiples", "deal_metrics", "market_context"]
        },

        "strategic_buyers": {
            "title": "Strategic Buyers Analysis",
            "prompt": """Identify strategic buyers who could acquire {company}:

REQUIRED INFORMATION:
- 5-7 potential strategic acquirers with names and descriptions
- Strategic rationale for each buyer (synergies, market access, etc.)
- Financial capacity analysis (revenue, market cap, cash position)
- Previous acquisition history and M&A strategy
- Geographic and market overlap with target
- Synergy opportunities and value creation potential
- Competitive positioning and strategic fit
- Management and board receptiveness to M&A

RESEARCH INSTRUCTIONS:
Identify corporations with strategic interest, financial capacity (typically 5-10x target company revenue), and logical synergies. Focus on companies with active M&A programs and strategic fit.

Prioritize buyers with proven track record of successful acquisitions in relevant sectors.""",
            "required_fields": ["strategic_buyers", "acquisition_rationale", "financial_capacity", "synergies"]
        },

        "financial_buyers": {
            "title": "Financial Buyers Analysis", 
            "prompt": """Identify private equity firms suitable for {company}:

REQUIRED INFORMATION:
- 5-7 relevant PE firms with fund details and AUM
- Investment criteria and sector focus alignment
- Deal size capabilities and check size ranges
- Portfolio companies and relevant experience
- Geographic investment focus and local presence
- Investment strategy (growth, buyout, etc.)
- Recent transactions and sector activity
- Fund vintage and investment timeline

RESEARCH INSTRUCTIONS:
Focus on PE firms with sector expertise, appropriate deal size capabilities, and geographic alignment. Include specific fund details, investment criteria, and recent relevant transactions.

Prioritize firms with active investment programs and capital available for deployment.""",
            "required_fields": ["pe_firms", "investment_criteria", "fund_details", "sector_experience"]
        },

        "sea_conglomerates": {
            "title": "Southeast Asian Conglomerates",
            "prompt": """Research SEA conglomerates relevant for {company} acquisition:

REQUIRED INFORMATION:
- 5-6 major SEA conglomerates with acquisition capability
- Business portfolio and strategic interests alignment
- Financial capacity and acquisition track record
- Geographic presence and market knowledge
- Strategic rationale for acquiring target company
- Management approach to acquisitions and integration
- Local market advantages and synergies
- Regulatory and political considerations

RESEARCH INSTRUCTIONS:
Focus on large, diversified conglomerates with established presence in Southeast Asia, proven acquisition capabilities, and strategic interest in target's sector.

Prioritize conglomerates with strong financial position and active M&A programs.""",
            "required_fields": ["conglomerates", "acquisition_capacity", "strategic_fit", "regional_advantages"]
        },

        "margin_cost_resilience": {
            "title": "Margin & Cost Resilience",
            "prompt": """Research {company}'s margin structure and cost management:

REQUIRED INFORMATION:
- EBITDA margin trends and benchmarking vs peers
- Cost structure analysis (fixed vs variable costs)
- Operating leverage and scalability factors  
- Cost management initiatives and efficiency programs
- Margin sensitivity to volume/pricing changes
- Historical margin resilience during downturns
- Operational improvements and automation
- Supply chain efficiency and cost optimization

RESEARCH INSTRUCTIONS:
Analyze the company's ability to maintain margins during challenging periods and scale efficiently during growth. Include specific margin data, cost breakdowns, and efficiency initiatives.

Focus on operational metrics that demonstrate cost discipline and margin sustainability.""",
            "required_fields": ["margin_trends", "cost_structure", "efficiency_initiatives", "margin_resilience"]
        },

        "investor_considerations": {
            "title": "Investment Considerations",
            "prompt": """Research key investment considerations for {company}:

REQUIRED INFORMATION:
- Primary investment risks and mitigation strategies
- Regulatory and compliance considerations
- Market and industry risk factors
- ESG (Environmental, Social, Governance) factors
- Technology and disruption risks
- Key person dependencies and management risks
- Financial and operational risks
- Investment opportunities and upside potential

RESEARCH INSTRUCTIONS:
Provide balanced analysis of investment risks and opportunities. Include specific risk factors, likelihood assessments, and mitigation strategies.

Focus on factors most relevant to investment banking evaluation and buyer decision-making.""",
            "required_fields": ["investment_risks", "opportunities", "esg_factors", "risk_mitigation"]
        },

        "investor_process_overview": {
            "title": "Investment Process Overview", 
            "prompt": """Research investment process considerations for {company}:

REQUIRED INFORMATION:
- Due diligence requirements and process timeline
- Key due diligence focus areas and data room contents
- Regulatory approvals and clearance requirements
- Stakeholder management and approval processes
- Synergy realization timeline and integration planning
- Valuation methodology and deal structure considerations
- Closing conditions and execution risks
- Post-acquisition integration requirements

RESEARCH INSTRUCTIONS:
Outline the typical investment process, due diligence requirements, and execution considerations for transactions involving companies like the target.

Include specific timelines, regulatory requirements, and integration planning factors.""",
            "required_fields": ["due_diligence", "regulatory_approvals", "process_timeline", "integration_planning"]
        }
    }

def research_all_topics(company_name: str, user_info: str = "") -> Dict[str, Any]:
    """
    Research all 14 topics comprehensively for the specified company
    """
    research_prompts = get_research_prompts()
    results = {}
    
    st.info(f"🔬 Starting comprehensive research for {company_name}...")
    
    # Create progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    total_topics = len(research_prompts)
    
    for i, (topic_id, topic_config) in enumerate(research_prompts.items()):
        # Update progress
        progress = (i + 1) / total_topics
        progress_bar.progress(progress)
        status_text.text(f"Researching {topic_config['title']} ({i+1}/{total_topics})")
        
        # Format prompt with company name
        formatted_prompt = topic_config['prompt'].format(company=company_name)
        
        # Add user information context if provided
        if user_info and user_info.strip():
            formatted_prompt += f"\n\nUSER PROVIDED INFORMATION:\n{user_info}\n\nNote: Fact-check the user information and alert if any facts are incorrect. Use correct information in your research."
        
        try:
            # Use existing research system
            st.session_state['current_company'] = company_name
            research_result = _run_research(formatted_prompt)
            
            results[topic_id] = {
                'title': topic_config['title'],
                'content': research_result,
                'required_fields': topic_config['required_fields'],
                'status': 'completed'
            }
            
            # Brief pause to show progress 
            time.sleep(0.5)
            
        except Exception as e:
            st.error(f"Error researching {topic_config['title']}: {e}")
            results[topic_id] = {
                'title': topic_config['title'], 
                'content': f"Research failed: {str(e)}",
                'required_fields': topic_config['required_fields'],
                'status': 'error'
            }
    
    progress_bar.progress(1.0)
    status_text.text("✅ Research completed!")
    
    return results

def fact_check_user_info(user_info: str, company_name: str) -> Dict[str, Any]:
    """
    Fact-check user provided information against known facts about the company
    """
    if not user_info or not user_info.strip():
        return {'has_info': False, 'fact_check': 'No user information provided'}
    
    fact_check_prompt = f"""
    Fact-check the following user-provided information about {company_name}:
    
    USER INFORMATION:
    {user_info}
    
    Please verify each claim and respond with:
    1. VERIFIED FACTS: List what is correct
    2. INCORRECT FACTS: List what is wrong with corrections  
    3. MISSING CONTEXT: List what needs additional context
    4. OVERALL ASSESSMENT: Brief summary of accuracy
    
    Be specific about what is right or wrong and provide corrections.
    """
    
    try:
        messages = [
            {"role": "system", "content": "You are a precise fact-checker. Verify claims about companies using reliable sources."},
            {"role": "user", "content": fact_check_prompt}
        ]
        
        response = call_llm_api(messages, 
                              st.session_state.get('model', 'llama-3.1-sonar-large-128k-online'),
                              st.session_state.get('api_key'), 
                              st.session_state.get('api_service', 'perplexity'))
        
        return {
            'has_info': True,
            'fact_check': response or "Fact-check completed",
            'original_info': user_info
        }
        
    except Exception as e:
        return {
            'has_info': True,
            'fact_check': f"Fact-check failed: {str(e)}",
            'original_info': user_info
        }

def display_research_results(results: Dict[str, Any]) -> None:
    """
    Display research results in a clean, organized format
    """
    st.markdown("## 📊 Research Results")
    
    # Create tabs for each topic
    topic_tabs = st.tabs([results[topic]['title'] for topic in results.keys()])
    
    for i, (topic_id, topic_data) in enumerate(results.items()):
        with topic_tabs[i]:
            st.markdown(f"### {topic_data['title']}")
            
            # Show status
            if topic_data['status'] == 'completed':
                st.success("✅ Research completed")
            else:
                st.error("❌ Research failed")
            
            # Show content
            st.markdown("**Research Results:**")
            st.markdown(topic_data['content'])
            
            # Show required fields that should be covered
            with st.expander(f"📋 Required fields for {topic_data['title']}"):
                for field in topic_data['required_fields']:
                    st.write(f"• {field}")

def create_edit_interface(results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create interface for users to edit/modify research results
    """
    st.markdown("## ✏️ Review & Edit Results")
    st.markdown("Review the research results below. You can edit any section before generating the final JSON.")
    
    edited_results = {}
    
    for topic_id, topic_data in results.items():
        st.markdown(f"### {topic_data['title']}")
        
        # Create text area for editing
        edited_content = st.text_area(
            f"Edit {topic_data['title']} content:",
            value=topic_data['content'],
            height=200,
            key=f"edit_{topic_id}"
        )
        
        edited_results[topic_id] = {
            **topic_data,
            'content': edited_content
        }
        
        st.markdown("---")
    
    return edited_results

def main():
    """Main Research Agent interface"""
    init_research_agent()
    
    st.title("🔬 Research Agent")
    st.markdown("**AI-Powered Investment Banking Research System**")
    st.markdown("Enter a company name and let the AI research all 14 investment banking topics comprehensively.")
    
    # Highlight Sonar Pro capabilities
    st.info("🌐 **Powered by Perplexity Sonar Pro** - Real-time web research with citations for comprehensive, up-to-date market analysis")
    
    # Sidebar for API configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # LLM Service Selection - Match main app interface
        llm_service = st.radio(
            "LLM Service",
            ["🔍 Perplexity (Recommended)", "🧠 Claude (Anthropic)"],
            help="Perplexity includes Sonar Pro for enhanced web research capabilities"
        )
        
        if llm_service.startswith("🔍"):
            api_service = "perplexity"
            # Perplexity models with Sonar Pro
            model_options = [
                "llama-3.1-sonar-large-128k-online",
                "llama-3.1-sonar-small-128k-online", 
                "llama-3.1-sonar-huge-128k-online"
            ]
            selected_model = st.selectbox("Model", model_options, index=0)
            
            api_key = st.text_input(
                "Perplexity API Key",
                type="password",
                help="Enter your Perplexity API key (includes Sonar Pro web access)"
            )
            
            st.info("🌐 **Sonar Pro Web Access**: Real-time web research with citations and current data")
            
        else:  # Claude
            api_service = "claude"
            model_options = [
                "claude-3-5-sonnet-20241022",
                "claude-3-sonnet-20240229", 
                "claude-3-haiku-20240307"
            ]
            selected_model = st.selectbox("Model", model_options, index=0)
            
            api_key = st.text_input(
                "Claude API Key",
                type="password",
                help="Enter your Anthropic Claude API key"
            )
        
        st.session_state['api_service'] = api_service
        st.session_state['api_key'] = api_key
        st.session_state['model'] = selected_model
        
        st.session_state['model'] = model
    
    # Main interface
    if not api_key:
        st.error("⚠️ Please enter your API key in the sidebar to start research")
        return
    
    # Company input section
    st.markdown("## 🏢 Company Information")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        company_name = st.text_input(
            "Company Name *", 
            placeholder="e.g., Netflix, Apple, Microsoft",
            help="Enter the company name you want to research"
        )
    
    with col2:
        user_info = st.text_area(
            "Additional Information (Optional)",
            placeholder="Enter any information you already have about the company...\n\nExample:\n- Founded in 1997\n- Streaming service company\n- Headquarters in Los Gatos, CA",
            height=100,
            help="Provide any information you have. The AI will fact-check it and use correct information."
        )
    
    # Research button
    if st.button("🚀 Start Comprehensive Research", type="primary", disabled=not company_name):
        if not company_name.strip():
            st.error("Please enter a company name")
            return
        
        # Fact-check user info if provided
        if user_info and user_info.strip():
            st.markdown("### 🔍 Fact-Checking User Information")
            with st.spinner("Fact-checking provided information..."):
                fact_check_results = fact_check_user_info(user_info, company_name)
                st.session_state.fact_check_results = fact_check_results
            
            if fact_check_results.get('has_info'):
                st.markdown("**Fact-Check Results:**")
                st.markdown(fact_check_results['fact_check'])
                st.markdown("---")
        
        # Start comprehensive research
        with st.spinner("Researching all topics... This may take 3-5 minutes."):
            research_results = research_all_topics(company_name, user_info)
            st.session_state.research_results = research_results
            st.session_state.research_completed = True
            st.session_state.company_name = company_name
        
        st.success("✅ Research completed!")
        st.rerun()
    
    # Display results if research is completed
    if st.session_state.research_completed and st.session_state.research_results:
        display_research_results(st.session_state.research_results)
        
        # User satisfaction check
        st.markdown("## 🎯 Review Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ Results Look Good - Generate JSON", type="primary"):
                st.markdown("### 🔄 Generating Investment Banking JSON...")
                
                # Use existing JSON generation system
                with st.spinner("Generating comprehensive JSON files..."):
                    try:
                        # Convert research results to conversation format for existing system
                        conversation_messages = [
                            {"role": "system", "content": "Investment banking research data"}
                        ]
                        
                        for topic_id, topic_data in st.session_state.research_results.items():
                            conversation_messages.append({
                                "role": "assistant",
                                "content": f"{topic_data['title']}: {topic_data['content']}"
                            })
                        
                        # All 14 slides for comprehensive pitch deck
                        required_slides = [
                            "business_overview",
                            "product_service_footprint", 
                            "historical_financial_performance",
                            "management_team",
                            "growth_strategy_projections",
                            "competitive_positioning",
                            "valuation_overview",
                            "precedent_transactions",
                            "strategic_buyers",
                            "financial_buyers", 
                            "sea_conglomerates",
                            "margin_cost_resilience",
                            "investor_considerations",
                            "investor_process_overview"
                        ]
                        
                        # Generate JSON using existing bulletproof system
                        def llm_wrapper(messages, model=None, api_key=None, api_service=None):
                            return call_llm_api(
                                messages, 
                                st.session_state.get('model'),
                                st.session_state.get('api_key'),
                                st.session_state.get('api_service')
                            )
                        
                        response, content_ir, render_plan = generate_bulletproof_json(
                            conversation_messages,
                            required_slides,
                            llm_wrapper
                        )
                        
                        if content_ir and render_plan:
                            st.success("✅ JSON Generation Successful!")
                            
                            # Store in session state
                            st.session_state['content_ir_json'] = content_ir
                            st.session_state['render_plan_json'] = render_plan
                            st.session_state['files_ready'] = True
                            
                            # Show summary
                            st.info(f"Generated {len(render_plan.get('slides', []))} slides with comprehensive content")
                            
                            # Download buttons
                            st.download_button(
                                "📥 Download Content IR JSON",
                                data=json.dumps(content_ir, indent=2),
                                file_name=f"{st.session_state.company_name}_content_ir.json",
                                mime="application/json"
                            )
                            
                            st.download_button(
                                "📥 Download Render Plan JSON", 
                                data=json.dumps(render_plan, indent=2),
                                file_name=f"{st.session_state.company_name}_render_plan.json",
                                mime="application/json"
                            )
                            
                            # Show JSON preview
                            with st.expander("📋 JSON Preview"):
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.subheader("Content IR Keys")
                                    for key in content_ir.keys():
                                        st.write(f"• {key}")
                                with col2:
                                    st.subheader("Render Plan Slides")
                                    for slide in render_plan.get('slides', []):
                                        st.write(f"• {slide.get('template', 'unknown')}")
                        else:
                            st.error("JSON Generation failed - no valid content returned")
                            
                    except Exception as e:
                        st.error(f"Error generating JSON: {e}")
                        st.exception(e)
        
        with col2:
            if st.button("✏️ Edit Results Before JSON Generation"):
                st.session_state.edit_mode = True
                st.rerun()
    
    # Edit mode
    if st.session_state.get('edit_mode', False) and st.session_state.research_results:
        st.markdown("---")
        edited_results = create_edit_interface(st.session_state.research_results)
        
        if st.button("💾 Save Changes & Generate JSON", type="primary"):
            st.session_state.research_results = edited_results
            st.session_state.edit_mode = False
            st.success("✅ Changes saved! Click 'Results Look Good' to generate JSON.")
            st.rerun()

if __name__ == "__main__":
    main()