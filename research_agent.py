#!/usr/bin/env python3
"""
Research Agent - Clean and Simple Investment Banking Research System
Replaces the complicated chatbot with a straightforward research approach.
"""

import streamlit as st
from shared_functions import safe_get
import json
import time
from typing import Dict, List, Tuple, Any

# Import shared functions to avoid circular import
from shared_functions import call_llm_api, run_research, get_current_company
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

CONTEXT FROM PRIOR RESEARCH:
Use business overview and operational insights from Topic 1 to provide detailed analysis of {company}'s product/service portfolio and geographic footprint.

REQUIRED INFORMATION:
- Complete list of products/services with descriptions (building on business overview)
- Geographic markets and operational coverage (detailed expansion of headquarters/presence)
- Distribution channels and go-to-market strategy  
- Customer segments and target demographics
- Pricing models and revenue streams by product/service
- Market share and competitive positioning by offering
- International presence and localization strategies

RESEARCH INSTRUCTIONS:
Build upon business overview from Topic 1 to provide comprehensive product/service analysis. Document the full scope of offerings, geographic reach, and market penetration.

Focus on quantifiable metrics where available (number of markets, customer counts, geographic coverage percentages).""",
            "required_fields": ["products_services", "geographic_coverage", "target_customers", "distribution_channels"]
        },
        
        "historical_financial_performance": {
            "title": "Historical Financial Performance", 
            "prompt": """Research {company}'s financial performance and metrics:

CONTEXT FROM PRIOR RESEARCH:
Use business overview and product/service insights from Topics 1-2 to analyze financial performance across business segments and geographies.

REQUIRED INFORMATION:
- Revenue figures for last 3-5 years with growth rates
- EBITDA, operating margins, and profitability metrics
- Key financial ratios and performance indicators
- Revenue breakdown by segment/geography (from product footprint analysis)
- Cash flow metrics and working capital trends
- Debt levels, capital structure, and financing history
- Key performance drivers and seasonal patterns

RESEARCH INSTRUCTIONS:
Build on business model understanding from prior topics. Prioritize verified financial data from annual reports, regulatory filings (SEC, SEDAR, FCA, etc.), or credible financial databases. 

Analyze financial performance in context of product portfolio and geographic presence identified in Topics 1-2.""",
            "required_fields": ["revenue_3_5_years", "ebitda_margins", "growth_rates", "key_metrics"]
        },

        "management_team": {
            "title": "Management Team & Leadership",
            "prompt": """Research {company}'s executive leadership team:

CONTEXT FROM PRIOR RESEARCH:
Use business overview, product portfolio, and financial performance insights to assess management team's track record and relevant experience.

REQUIRED INFORMATION:
- CEO: Full name, title, background, tenure, key achievements (related to business growth)
- CFO: Full name, title, background, tenure, financial expertise (relevant to performance trends)
- 4-6 additional senior executives with names, titles, backgrounds
- Board composition and key independent directors
- Leadership experience and track record (relevant to business model and geography)
- Educational backgrounds and professional history
- Previous companies and relevant experience in similar sectors/markets
- Any leadership changes or succession planning

RESEARCH INSTRUCTIONS:
Assess leadership team's qualifications in context of {company}'s business model, geographic presence, and financial performance from prior research.

Focus on experience relevant to identified growth strategies and market challenges.""",
            "required_fields": ["ceo", "cfo", "senior_executives", "leadership_experience"]
        },

        "growth_strategy_projections": {
            "title": "Growth Strategy & Projections",
            "prompt": """Research {company}'s growth strategy and future outlook:

CONTEXT FROM PRIOR RESEARCH:
Use insights from business model, product portfolio, financial performance, and management assessment to analyze growth strategy and projections.

REQUIRED INFORMATION:
- Strategic growth initiatives and expansion plans (building on product/geographic footprint)
- Market expansion opportunities and geographic growth (aligned with current presence)
- Product/service innovation and R&D investments
- Acquisition strategy and M&A pipeline (related to business model)
- Technology investments and digital transformation
- Revenue growth projections and targets (building on historical performance)
- Market trends driving growth opportunities
- Capital allocation strategy for growth (informed by financial position)

RESEARCH INSTRUCTIONS:
Analyze growth strategy in context of current business position, financial capacity, and management capabilities from prior research.

Focus on growth initiatives that leverage existing geographic presence and product strengths.""",
            "required_fields": ["growth_initiatives", "expansion_plans", "market_opportunities", "projections"]
        },

        "competitive_positioning": {
            "title": "Competitive Positioning",
            "prompt": """Research {company}'s competitive landscape and positioning:

CONTEXT FROM PRIOR RESEARCH:
Use business model, product portfolio, geographic presence, financial performance, and growth strategy insights to assess competitive position.

REQUIRED INFORMATION:  
- Top 5-7 direct competitors with names and descriptions (in same markets/geographies)
- Market share analysis and competitive advantages (relative to business model)
- Differentiation factors and unique value propositions (based on product analysis)
- Competitive threats and market challenges (relevant to growth strategy)
- Industry dynamics and market structure (in key geographies)
- Competitive response strategies
- Barriers to entry and competitive moats (based on business strengths)
- Market leadership position and brand strength

RESEARCH INSTRUCTIONS:
Assess competitive position using comprehensive business understanding from prior research. Identify competitors operating in similar markets with comparable business models and geographic presence.

Focus on competitive dynamics most relevant to growth strategy and financial performance.""",
            "required_fields": ["competitors", "market_share", "competitive_advantages", "differentiation"]
        },

        "precedent_transactions": {
            "title": "Precedent Transactions",
            "prompt": """Research relevant M&A transactions for {company} valuation:

CONTEXT FROM PRIOR RESEARCH:
Use all previous research findings about {company}'s business model, geography, financial performance, and competitive positioning to identify the most relevant precedent transactions.

REQUIRED INFORMATION:
- 4-6 precedent transactions in same/similar industry
- Transaction details: target, acquirer, date, enterprise value
- Revenue/EBITDA multiples and valuation metrics
- Deal rationale and strategic fit factors
- Geographic relevance (prioritize transactions in {company}'s target geography)
- Transaction premiums and control premiums
- Market conditions at time of transaction
- Deal structure and consideration type

RESEARCH INSTRUCTIONS:
Focus on transactions involving companies with similar business models, geographic footprint, and scale. Prioritize recent transactions (last 3-5 years) with disclosed financial terms.

Include specific valuation multiples and deal metrics where available.""",
            "required_fields": ["transactions", "valuation_multiples", "deal_metrics", "market_context"]
        },

        "valuation_overview": {
            "title": "Valuation Analysis",
            "prompt": """🔍 COMPREHENSIVE VALUATION ANALYSIS for {company}:

CONTEXT FROM PRIOR RESEARCH:
Use all previous research findings about {company}'s financial performance, growth strategy, competitive positioning, and market dynamics to inform valuation analysis.

You must provide THREE COMPLETE VALUATION METHODOLOGIES with actual calculations:

1. **DCF Analysis** (Provide full calculation):
   - Extract company's latest revenue from conversation history and prior research
   - Project 5-year revenue growth using stated/researched growth rates
   - Apply sector-appropriate EBITDA margins (research industry benchmarks)
   - Calculate FCF using typical tax rates, capex, and working capital assumptions
   - Apply terminal growth rate (2-3%) and appropriate WACC (8-12% based on risk profile)
   - **PROVIDE ENTERPRISE VALUE AND EQUITY VALUE ESTIMATES**

2. **Trading Multiples** (Calculate actual valuation):
   - Research current EV/Revenue multiples for public company peers in {company}'s sector
   - Research EV/EBITDA multiples for comparable companies
   - Apply median, 25th percentile, and 75th percentile multiples to company metrics
   - **PROVIDE VALUATION RANGE BASED ON MULTIPLE APPROACHES**

3. **Precedent Transactions** (Calculate transaction-based value):
   - Use precedent transactions researched in Topic 6
   - Extract transaction multiples (EV/Revenue, EV/EBITDA) from recent deals
   - Apply transaction multiples to company's financial metrics
   - **PROVIDE TRANSACTION-BASED VALUATION ESTIMATE**

**REQUIRED OUTPUT**: Three distinct valuation estimates with methodology details, assumptions, and final enterprise/equity values for {company}.
- Use sector-appropriate WACC (typically 8-12% for established companies, 10-15% for high-growth)
- Terminal growth: 2-4% (based on company maturity)
- **Calculate and provide specific enterprise value range**

**FINAL VALUATION RANGE**: Provide specific monetary amounts (in company's reporting currency) and methodology summary

RESEARCH INSTRUCTIONS:
Provide comprehensive valuation analysis using industry-standard methodologies. Include all assumptions, calculations, and final valuation ranges. This valuation will determine buyer affordability in subsequent topics.""",
            "required_fields": ["dcf_analysis", "trading_multiples", "precedent_multiples", "valuation_range"]
        },

        "strategic_buyers": {
            "title": "Strategic Buyers Analysis",
            "prompt": """Identify strategic buyers who could acquire {company}:

CONTEXT FROM PRIOR RESEARCH:
Use valuation analysis from Topic 7 to ensure buyers can afford the acquisition. Use geographic and business model insights from all prior research.

REQUIRED INFORMATION:
- 5-7 potential strategic acquirers with names and descriptions
- **AFFORDABILITY ANALYSIS**: Verify each buyer can afford {company}'s valuation range from Topic 7
- Strategic rationale for each buyer (synergies, market access, etc.)
- Financial capacity analysis (revenue, market cap, cash position vs. required acquisition cost)
- Previous acquisition history and M&A strategy
- Geographic and market overlap with target (prioritize buyers in {company}'s geography)
- Synergy opportunities and value creation potential
- Competitive positioning and strategic fit
- Management and board receptiveness to M&A

RESEARCH INSTRUCTIONS:
Identify corporations with strategic interest, financial capacity (typically 5-10x target company revenue), and logical synergies. **CRITICAL**: Use the valuation range from Topic 7 to verify each buyer can afford the acquisition.

Focus on companies with active M&A programs and strategic fit. Prioritize buyers operating in or targeting {company}'s geographic markets.""",
            "required_fields": ["strategic_buyers", "affordability_analysis", "acquisition_rationale", "financial_capacity", "synergies"]
        },

        "financial_buyers": {
            "title": "Financial Buyers Analysis", 
            "prompt": """⚠️ IMPORTANT: Identify PRIVATE EQUITY FIRMS suitable for {company}:

CONTEXT FROM PRIOR RESEARCH:
Use valuation analysis from Topic 7 and all business insights from prior research to identify suitable PE firms.

REQUIRED INFORMATION:
- 5-7 relevant PE firms with fund details and AUM
- **AFFORDABILITY ANALYSIS**: Verify each PE firm can afford {company}'s valuation range
- Investment criteria and sector focus alignment
- Deal size capabilities and check size ranges matching valuation
- Portfolio companies and relevant experience in {company}'s sector
- Geographic investment focus (prioritize firms active in {company}'s geography)
- Investment strategy (growth, buyout, etc.)
- Recent transactions and sector activity
- Fund vintage and investment timeline

RESEARCH INSTRUCTIONS:
Focus ONLY on Private Equity firms (NOT venture capital firms). Use valuation range from Topic 7 to ensure firms have appropriate fund size and deal capacity.

Focus on PE firms with sector expertise, appropriate deal size capabilities, and geographic alignment with {company}'s markets.""",
            "required_fields": ["pe_firms", "affordability_analysis", "investment_criteria", "fund_details", "sector_experience"]
        },

        "global_conglomerates": {
            "title": "Global Conglomerates",
            "prompt": """Research global conglomerates relevant for {company} acquisition:

CONTEXT FROM PRIOR RESEARCH:
Use {company}'s geographic presence and business model from prior research to identify relevant conglomerates. Use valuation analysis to verify affordability.

VECTOR DATABASE PRECEDENT TRANSACTIONS:
{vector_db_transactions}

REQUIRED INFORMATION:
- 5-6 major global conglomerates with acquisition capability
- **GEOGRAPHIC ALIGNMENT**: Focus on conglomerates operating in {company}'s target geography
- Business portfolio and strategic interests alignment
- **AFFORDABILITY ANALYSIS**: Financial capacity vs. {company}'s valuation range
- Previous acquisition track record in similar sectors (use vector DB data above)
- Strategic rationale for acquiring {company}
- Management approach to acquisitions and integration
- Local market advantages and synergies
- Regulatory and political considerations

RESEARCH INSTRUCTIONS:
Focus on large, diversified conglomerates with presence in {company}'s geographic markets. Prioritize conglomerates from the same region or with strong expansion interests in {company}'s geography.
IMPORTANT: Use the vector database transaction data above to identify conglomerates that have acquired similar companies and reference specific deals, valuations, and strategic rationales.

Use valuation range from Topic 7 to ensure conglomerates have financial capacity for acquisition.""",
            "required_fields": ["global_conglomerates", "geographic_alignment", "acquisition_capacity", "strategic_fit", "regional_advantages"]
        },

        "margin_cost_resilience": {
            "title": "Margin & Cost Resilience",
            "prompt": """Research {company}'s margin structure and cost management:

CONTEXT FROM PRIOR RESEARCH:
Use financial performance data, competitive positioning, and business model insights from all prior research to analyze margin sustainability.

REQUIRED INFORMATION:
- EBITDA margin trends and benchmarking vs peers (from competitive analysis)
- Cost structure analysis (fixed vs variable costs)
- Operating leverage and scalability factors  
- Cost management initiatives and efficiency programs
- Margin sensitivity to volume/pricing changes
- Historical margin resilience during downturns
- Operational improvements and automation
- Supply chain efficiency and cost optimization

RESEARCH INSTRUCTIONS:
Use prior financial performance and competitive analysis to assess margin sustainability. Analyze the company's ability to maintain margins during challenging periods and scale efficiently during growth.

Focus on operational metrics that demonstrate cost discipline and margin sustainability relative to competitors.""",
            "required_fields": ["margin_trends", "cost_structure", "efficiency_initiatives", "margin_resilience"]
        },

        "investor_considerations": {
            "title": "Investment Considerations",
            "prompt": """Research key investment considerations for {company}:

CONTEXT FROM PRIOR RESEARCH:
Synthesize insights from all prior research topics to identify key investment risks and opportunities based on business model, competitive position, management team, and growth strategy.

REQUIRED INFORMATION:
- Primary investment risks and mitigation strategies (based on business analysis)
- Regulatory and compliance considerations (geographic-specific)
- Market and industry risk factors (from competitive analysis)
- ESG (Environmental, Social, Governance) factors
- Technology and disruption risks (from competitive positioning)
- Key person dependencies and management risks (from leadership analysis)
- Financial and operational risks (from performance analysis)
- Investment opportunities and upside potential (from growth strategy)

RESEARCH INSTRUCTIONS:
Use all prior research to provide comprehensive risk-opportunity analysis. Include specific risk factors identified in business model, competitive threats, management dependencies, and market position.

Focus on factors most relevant to buyers identified in strategic/financial buyer analysis.""",
            "required_fields": ["investment_risks", "opportunities", "esg_factors", "risk_mitigation"]
        },

        "investor_process_overview": {
            "title": "Investment Process Overview", 
            "prompt": """Research investment process considerations for {company}:

CONTEXT FROM PRIOR RESEARCH:
Use valuation analysis, buyer identification, and risk assessment from all prior research to outline appropriate investment process and due diligence requirements.

REQUIRED INFORMATION:
- Due diligence requirements and process timeline (based on business complexity)
- Key due diligence focus areas and data room contents (tailored to identified risks)
- Regulatory approvals and clearance requirements (geography-specific)
- Stakeholder management and approval processes
- Synergy realization timeline and integration planning (based on buyer analysis)
- Valuation methodology and deal structure considerations (from Topic 7)
- Closing conditions and execution risks (based on risk analysis)
- Post-acquisition integration requirements (buyer-specific)

RESEARCH INSTRUCTIONS:
Use comprehensive business analysis and buyer profiles from prior research to outline tailored investment process. Consider geographic regulations, business complexity, and buyer-specific requirements.

Include specific timelines and requirements based on {company}'s sector, geography, and identified buyer profiles.""",
            "required_fields": ["due_diligence", "regulatory_approvals", "process_timeline", "integration_planning"]
        }
    }

def research_all_topics(company_name: str, user_info: str = "") -> Dict[str, Any]:
    """
    Research all 14 topics comprehensively for the specified company with sequential context building
    """
    research_prompts = get_research_prompts()
    results = {}
    accumulated_context = ""
    
    st.info(f"🔬 Starting comprehensive research for {company_name}...")
    
    # Create progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Correct topic order (14 topics total)
    topic_order = [
        "business_overview",
        "product_service_footprint", 
        "historical_financial_performance",
        "management_team",
        "growth_strategy_projections",
        "competitive_positioning",
        "precedent_transactions",
        "valuation_overview",  # Topic 7 - CRITICAL for buyer affordability
        "strategic_buyers",
        "financial_buyers",
        "global_conglomerates",  # Changed from sea_conglomerates
        "margin_cost_resilience",
        "investor_considerations",
        "investor_process_overview"
    ]
    
    total_topics = len(topic_order)
    
    for i, topic_id in enumerate(topic_order):
        if topic_id not in research_prompts:
            st.error(f"Missing prompt configuration for topic: {topic_id}")
            continue
            
        topic_config = research_prompts[topic_id]
        
        # Update progress
        progress = (i + 1) / total_topics
        progress_bar.progress(progress)
        status_text.text(f"Researching {topic_config['title']} (Topic {i+1}/{total_topics})")
        
        # Format prompt with company name and vector DB data if applicable
        vector_db_transactions = ""
        
        # Special handling for global_conglomerates topic - query vector DB for similar transactions
        if topic_id == "global_conglomerates":
            try:
                # Import and initialize vector DB
                from vector_db import VectorDBManager
                vector_db = VectorDBManager()
                
                # Check if vector DB credentials are available
                if st.safe_get(session_state, 'vector_db_id') and st.safe_get(session_state, 'vector_db_token'):
                    vector_db.initialize(
                        database_id=st.session_state['vector_db_id'],
                        token=st.session_state['vector_db_token']
                    )
                    
                    # Extract company details from previous research for better querying
                    company_overview = ""
                    sector = ""
                    region = ""
                    
                    # Try to extract context from previous research results
                    if 'business_overview' in results:
                        company_overview = results['business_overview'].get('content', '')[:500]
                    if 'competitive_positioning' in results:
                        sector_info = results['competitive_positioning'].get('content', '')
                        sector = sector_info[:200] if sector_info else "Technology"
                    if 'product_service_footprint' in results:
                        geo_info = results['product_service_footprint'].get('content', '')
                        region = geo_info[:200] if geo_info else "Global"
                    
                    # Query vector DB for precedent transactions
                    transactions = vector_db.get_precedent_transactions(
                        company_name=company_name,
                        company_overview=company_overview or f"Company: {company_name}",
                        sector=sector or "Technology",
                        region=region or "Global"
                    )
                    
                    if transactions:
                        vector_db_transactions = "SIMILAR TRANSACTION DATA FROM DATABASE:\n"
                        for i, tx in enumerate(transactions[:10]):  # Limit to top 10
                            vector_db_transactions += f"\n{i+1}. {tx}\n"
                        vector_db_transactions += "\nUse this transaction data to identify relevant conglomerates and their acquisition patterns.\n"
                    else:
                        vector_db_transactions = "No similar transactions found in vector database. Focus on general market research.\n"
                else:
                    vector_db_transactions = "Vector database not configured. Using general market research approach.\n"
                    
            except Exception as e:
                print(f"⚠️ Vector DB query failed for {topic_id}: {str(e)}")
                vector_db_transactions = "Vector database unavailable. Using general market research approach.\n"
        
        # Format prompt with company name and vector DB data
        formatted_prompt = topic_config['prompt'].format(
            company=company_name,
            vector_db_transactions=vector_db_transactions
        )
        
        # Add accumulated context from prior topics (except for Topic 1)
        if i > 0:
            formatted_prompt += f"\n\nCONTEXT FROM PRIOR RESEARCH TOPICS:\n{accumulated_context}\n\nUse this context to inform your research for {topic_config['title']}."
        
        # Add user information context if provided
        if user_info and user_info.strip():
            formatted_prompt += f"\n\nUSER PROVIDED INFORMATION:\n{user_info}\n\nNote: Fact-check the user information and alert if any facts are incorrect. Use correct information in your research."
        
        try:
            # Use existing research system
            st.session_state['current_company'] = company_name
            research_result = run_research(formatted_prompt)
            
            results[topic_id] = {
                'title': topic_config['title'],
                'content': research_result,
                'required_fields': topic_config['required_fields'],
                'status': 'completed',
                'topic_number': i + 1
            }
            
            # Add this topic's results to accumulated context for subsequent topics
            accumulated_context += f"\n\n{topic_config['title']}: {research_result[:500]}..."  # First 500 chars for context
            
            # Brief pause to show progress 
            time.sleep(0.5)
            
        except Exception as e:
            st.error(f"Error researching {topic_config['title']}: {e}")
            results[topic_id] = {
                'title': topic_config['title'], 
                'content': f"Research failed: {str(e)}",
                'required_fields': topic_config['required_fields'],
                'status': 'error',
                'topic_number': i + 1
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
                              st.safe_get(session_state, 'model', 'sonar-pro'),
                              st.safe_get(session_state, 'api_key'), 
                              st.safe_get(session_state, 'api_service', 'perplexity'))
        
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
                "sonar-pro",
                "sonar",
                "sonar-reasoning-pro",
                "sonar-reasoning",
                "sonar-deep-research"
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
            
            if safe_get(fact_check_results, 'has_info'):
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
                            "global_conglomerates",
                            "margin_cost_resilience",
                            "investor_considerations",
                            "investor_process_overview"
                        ]
                        
                        # Generate JSON using existing bulletproof system
                        def llm_wrapper(messages, model=None, api_key=None, api_service=None):
                            return call_llm_api(
                                messages, 
                                st.safe_get(session_state, 'model'),
                                st.safe_get(session_state, 'api_key'),
                                st.safe_get(session_state, 'api_service')
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
                            st.info(f"Generated {len(safe_get(render_plan, 'slides', []))} slides with comprehensive content")
                            
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
                                    for slide in safe_get(render_plan, 'slides', []):
                                        st.write(f"• {safe_get(slide, 'template', 'unknown')}")
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
    if st.safe_get(session_state, 'edit_mode', False) and st.session_state.research_results:
        st.markdown("---")
        edited_results = create_edit_interface(st.session_state.research_results)
        
        if st.button("💾 Save Changes & Generate JSON", type="primary"):
            st.session_state.research_results = edited_results
            st.session_state.edit_mode = False
            st.success("✅ Changes saved! Click 'Results Look Good' to generate JSON.")
            st.rerun()

if __name__ == "__main__":
    main()