"""
Enhanced AI Analysis Module
Integrates Vector DB data with LLM calls for more informed and accurate responses.
"""

import streamlit as st
from typing import List, Dict, Any, Optional
from vector_db import get_vector_db_manager

class EnhancedAIAnalysis:
    """Enhanced AI analysis with Vector DB integration"""
    
    def __init__(self):
        self.vector_db = get_vector_db_manager()
    
    def enhance_prompt_with_vector_data(self, base_prompt: str, context_type: str = "general", 
                                      company_profile: Optional[Dict[str, Any]] = None) -> str:
        """Enhance AI prompt with relevant Vector DB data using dynamic company context"""
        
        if not self.vector_db.is_initialized:
            st.warning("⚠️ Vector DB not initialized. Using base prompt without enhancement.")
            return base_prompt
        
        try:
            # Extract company context from the prompt or company profile
            company_context = self._extract_company_context(base_prompt, company_profile)
            
            # Determine the type of enhancement needed
            context_docs = []
            
            # Check for buyer analysis sections (strategic/financial buyers)
            if any(keyword in base_prompt.lower() for keyword in ["strategic buyer", "financial buyer", "buyer analysis", "potential acquirer"]):
                # Get comprehensive data for buyer analysis
                context_docs.extend(self._get_buyer_analysis_context(company_context))
                context_type = "buyer_analysis"
                
            elif "valuation" in base_prompt.lower() or "comparable" in base_prompt.lower():
                if company_context["name"] and company_context["overview"]:
                    context_docs = self.vector_db.get_valuation_comparables(
                        company_context["name"], 
                        company_context["overview"],
                        company_context["profile"]
                    )
                    context_type = "valuation_comparables"
                else:
                    context_docs = self.vector_db.search_precedent_transactions(base_prompt[:500])
                    context_type = "general_valuation"
                    
            elif "market" in base_prompt.lower() or "industry" in base_prompt.lower():
                if company_context["name"] and company_context["overview"]:
                    context_docs = self.vector_db.get_market_data(
                        company_context["name"],
                        company_context["overview"],
                        company_context["sector"],
                        company_context["region"]
                    )
                    context_type = "market_analysis"
                else:
                    context_docs = self.vector_db.search_precedent_transactions(base_prompt[:500])
                    context_type = "general_market"
                    
            elif "precedent" in base_prompt.lower() or "transaction" in base_prompt.lower():
                if company_context["name"] and company_context["overview"]:
                    context_docs = self.vector_db.get_precedent_transactions(
                        company_context["name"],
                        company_context["overview"],
                        company_context["sector"],
                        company_context["region"]
                    )
                    context_type = "precedent_transactions"
                else:
                    context_docs = self.vector_db.search_precedent_transactions(base_prompt[:500])
                    context_type = "general_transactions"
                    
            else:
                # General enhancement
                context_docs = self.vector_db.search_precedent_transactions(base_prompt[:500])
                context_type = "general_search"
            
            if context_docs:
                # Format context for AI with enhanced structure
                context = self.vector_db.format_context_for_ai(context_docs, context_type)
                
                # Create enhanced prompt with buyer-specific instructions
                enhanced_prompt = self._create_enhanced_prompt(base_prompt, context, context_type, company_context)
                
                st.success(f"✅ Enhanced prompt with {len(context_docs)} relevant documents from Vector DB ({context_type})")
                return enhanced_prompt
            else:
                st.info("ℹ️ No relevant Vector DB data found. Using base prompt.")
                return base_prompt
                
        except Exception as e:
            st.error(f"❌ Error enhancing prompt with Vector DB data: {str(e)}")
            return base_prompt
    
    def create_general_valuation_prompt(self, company_name: str, company_overview: str, sector: str, region: str = "Global") -> str:
        """Create a general valuation prompt with Vector DB context using dynamic company information"""
        
        base_prompt = f"""
You are a senior M&A analyst. Your task is to produce a **highly accurate, well-structured comparable transaction analysis** for {company_name} in the {sector} sector based in {region} — **using only the information provided in the context below**.  
Do NOT invent or assume any data not explicitly present in the context.

## TARGET COMPANY PROFILE
- Company: {company_name}
- Business Overview: {company_overview[:300]}...
- Sector: {sector}
- Region: {region}

## Step 1 – Select Comparables
Identify **relevant M&A transactions** from the context that are most comparable to {company_name}.  

### Relevance hierarchy (most to least important):
1. **Sector/Sub-sector Match** – Same or closely related industry to {sector}
2. **Business Model Similarity** – Similar operational characteristics to described business model
3. **Geography** –  
   - Priority 1: {region}  
   - Priority 2: Similar regions or markets 
   - Priority 3: Other regions with relevant sector data
4. **Scale & Financial Size** – Similar revenue, EBITDA, or operational scale
5. **Transaction Type** – Control (>50% stake) is more directly comparable than minority stakes
6. **Timing** – More recent transactions are generally more relevant (last 5 years preferred)

## Step 2 – Present Comparable Transactions
List the transactions in a **table ordered by Date (most recent first)** with relevant columns based on available data.
Include: Target, Acquirer, Date, Deal Value, EV/Revenue, EV/EBITDA, Strategic Rationale

## Step 3 – Analysis
Provide:
1. **Key insights** from the precedent transactions most relevant to {company_name}
2. **Market trends** observed in the data for {sector} sector
3. **Regional considerations** and valuation differences for {region}
4. **Strategic implications** and buyer interest patterns for similar companies
5. **Valuation range** and methodology recommendations

## Output Format:
1. **Comparable Transactions Table** – ordered by most recent date
2. **Written Analysis** – covering key insights and trends
3. **Strategic Summary** – actionable insights and recommendations for {company_name}

**Important:**  
- Use only data from the provided context — no external sources, no assumptions.
- Reference specific transactions when making points about valuation multiples or strategic themes.
- Focus on actionable insights and market intelligence relevant to {company_name}.
"""
        
        # Enhance with Vector DB data using company context
        return self.enhance_prompt_with_vector_data(base_prompt, "general_valuation", {
            'name': company_name,
            'overview': company_overview,
            'sector': sector,
            'region': region
        })
    
    def create_market_analysis_prompt(self, company_name: str, company_overview: str, sector: str, region: str, focus_areas: List[str]) -> str:
        """Create a market analysis prompt with Vector DB context using dynamic company information"""
        
        focus_text = "\n".join([f"- {area}" for area in focus_areas])
        
        base_prompt = f"""
You are a senior market analyst specializing in {sector} sector analysis. Provide a comprehensive market analysis for {region} with specific relevance to {company_name}, using the context provided below.

## TARGET COMPANY CONTEXT
- Company: {company_name}
- Business Overview: {company_overview[:300]}...
- Sector: {sector}
- Region: {region}

## ANALYSIS REQUIREMENTS
Focus on the following areas with specific relevance to the target company:
{focus_text}

## ANALYSIS STRUCTURE
1. **Market Overview** - Size, growth, key drivers relevant to {company_name}'s business model
2. **Competitive Landscape** - Major players, market positioning, competitive threats and opportunities
3. **Regulatory Environment** - Key regulations, compliance requirements affecting similar businesses
4. **Market Trends** - Current and emerging trends impacting the sector and business model
5. **Growth Opportunities** - Market expansion potential, untapped segments relevant to the company
6. **Risk Factors** - Market risks, challenges, and uncertainties for similar business models
7. **Investment Climate** - M&A activity, investor interest, and transaction trends in the sector
8. **Regional Dynamics** - Geographic considerations and market variations in {region}
9. **Strategic Buyer Interest** - Types of acquirers active in this market and their motivations
10. **Future Outlook** - 3-5 year projections and strategic implications for {company_name}

## OUTPUT FORMAT
Provide a structured analysis with:
- Clear sections with specific relevance to {company_name}
- Bullet points for key insights backed by context data
- Specific transaction examples and market data where available
- Strategic implications for companies with similar business models

**Important:** Use only information from the provided Vector DB context. Reference specific transactions or market data when making analytical points. If specific data is not available, clearly state this limitation.
"""
        
        return self.enhance_prompt_with_vector_data(base_prompt, "market_analysis", {
            'name': company_name,
            'overview': company_overview,
            'sector': sector,
            'region': region
        })
    
    def _extract_company_context(self, prompt: str, company_profile: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Extract company context from prompt and profile for dynamic queries"""
        context = {
            "name": "",
            "overview": "",
            "sector": "general",
            "region": "global",
            "profile": {}
        }
        
        if company_profile:
            context["name"] = company_profile.get("name", "")
            context["overview"] = company_profile.get("overview", "")
            context["sector"] = company_profile.get("sector", "general")
            context["region"] = company_profile.get("region", "global")
            context["profile"] = company_profile
        
        # Try to extract from prompt if not in profile
        if not context["name"] or not context["overview"]:
            # Simple extraction patterns (can be enhanced)
            lines = prompt.split('\n')
            for line in lines:
                if "company:" in line.lower() or "company name:" in line.lower():
                    context["name"] = line.split(':')[-1].strip()
                elif "sector:" in line.lower():
                    context["sector"] = line.split(':')[-1].strip()
                elif "region:" in line.lower() or "geography:" in line.lower():
                    context["region"] = line.split(':')[-1].strip()
        
        return context
    
    def _get_buyer_analysis_context(self, company_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get comprehensive context for buyer analysis sections"""
        all_context = []
        
        # Get precedent transactions for strategic buyer analysis
        if company_context["name"] and company_context["overview"]:
            precedent_docs = self.vector_db.get_precedent_transactions(
                company_context["name"],
                company_context["overview"],
                company_context["sector"],
                company_context["region"]
            )
            all_context.extend(precedent_docs)
            
            # Get market data for buyer landscape analysis
            market_docs = self.vector_db.get_market_data(
                company_context["name"],
                company_context["overview"],
                company_context["sector"],
                company_context["region"]
            )
            all_context.extend(market_docs)
            
            # Get valuation comparables for pricing context
            valuation_docs = self.vector_db.get_valuation_comparables(
                company_context["name"],
                company_context["overview"],
                company_context["profile"]
            )
            all_context.extend(valuation_docs)
        
        return self.vector_db._deduplicate_results(all_context)
    
    def _create_enhanced_prompt(self, base_prompt: str, context: str, context_type: str, company_context: Dict[str, Any]) -> str:
        """Create enhanced prompt with buyer-specific instructions"""
        
        # Special instructions for buyer analysis
        buyer_instructions = ""
        if context_type == "buyer_analysis":
            buyer_instructions = f"""

## BUYER ANALYSIS SPECIFIC INSTRUCTIONS
When analyzing potential buyers for {company_context.get('name', 'the target company')}, use the Vector DB context to:

**For Strategic Buyers:**
- Reference specific precedent transactions showing strategic rationales
- Identify acquirers who have been active in {company_context.get('sector', 'the sector')}
- Highlight synergy opportunities based on similar transactions
- Use market data to support strategic buyer motivations
- Reference geographic expansion patterns from the transaction data

**For Financial Buyers:**
- Reference valuation multiples from comparable transactions  
- Identify PE/financial buyer transaction patterns in the sector
- Use market data to support return thesis and exit strategies
- Reference operational improvement opportunities from similar deals
- Highlight recurring revenue or cash flow characteristics that appeal to financial buyers

**Evidence-Based Analysis:**
- Cite specific transactions, companies, and deal rationales from the Vector DB context
- Reference actual buyer names and their strategic moves in the market
- Use real valuation multiples and transaction structures from the data
- Ground all buyer fit assessments in factual precedent transaction evidence
"""
        
        enhanced_prompt = f"""
{base_prompt}

## ENHANCED CONTEXT FROM VECTOR DATABASE
The following information has been retrieved from our precedent transactions and market data database to enhance your analysis:

{context}{buyer_instructions}

## GENERAL INSTRUCTIONS
Please use this additional context to provide more accurate and informed analysis. When referencing precedent transactions or market data, cite the specific information from the context above. If the context doesn't contain relevant information for a specific aspect of your analysis, clearly state that and proceed with your best judgment based on general knowledge.

**Key Requirements:**
- Always reference specific transactions, companies, or data points from the Vector DB context when available
- Use actual deal rationales and strategic themes from the precedent transactions
- Ground valuation assessments in real transaction multiples from the context
- Cite geographic and sector-specific trends from the market data
- Be explicit when information is not available in the context vs. when it is supported by the data
"""
        
        return enhanced_prompt
    
    def get_analysis_suggestions(self, prompt: str, company_context: Optional[Dict[str, Any]] = None) -> List[str]:
        """Get suggestions for improving analysis based on Vector DB capabilities and company context"""
        suggestions = []
        
        if not self.vector_db.is_initialized:
            suggestions.append("🔗 Initialize Vector DB to access precedent transactions and market data")
            return suggestions
        
        # Analyze prompt and suggest enhancements
        prompt_lower = prompt.lower()
        
        # Company-specific suggestions
        if company_context and company_context.get("name"):
            company_name = company_context["name"]
            sector = company_context.get("sector", "your sector")
            suggestions.append(f"🎯 Use {company_name}-specific transaction patterns and buyer interests from Vector DB")
            suggestions.append(f"📈 Access {sector} sector trends and competitive landscape data")
        
        # Analysis-type specific suggestions
        if "strategic buyer" in prompt_lower or "financial buyer" in prompt_lower:
            suggestions.append("🔍 Leverage Vector DB for buyer identification and strategic rationale analysis")
            suggestions.append("💼 Use precedent transactions to identify active acquirers in the sector")
        
        if "valuation" in prompt_lower or "comparable" in prompt_lower:
            suggestions.append("📊 Use Vector DB to find relevant precedent transactions for accurate multiples")
            suggestions.append("🌍 Access regional valuation data for geographic adjustments")
        
        if "market" in prompt_lower or "industry" in prompt_lower:
            suggestions.append("📈 Use Vector DB market data for industry insights and trends")
            suggestions.append("🎯 Access competitive landscape and market positioning data")
        
        # Sector-specific suggestions based on common sectors
        sector_keywords = {
            "healthcare": "🏥 Leverage healthcare-specific precedent transactions and regulatory trends",
            "technology": "💻 Access technology sector transaction patterns and innovation trends", 
            "financial": "🏦 Use financial services transaction data and regulatory insights",
            "consumer": "🛍️ Access consumer sector transaction trends and market dynamics",
            "industrial": "🏭 Use industrial sector M&A patterns and operational synergy themes"
        }
        
        for sector, suggestion in sector_keywords.items():
            if sector in prompt_lower:
                suggestions.append(suggestion)
                break
        
        # Geographic suggestions
        if any(region in prompt_lower for region in ["asia", "europe", "america", "global"]):
            suggestions.append("🌏 Access region-specific transaction multiples and market dynamics")
            suggestions.append("🏛️ Use regional regulatory and competitive landscape insights")
        
        return suggestions

    def create_buyer_analysis_prompt(self, company_name: str, company_overview: str, sector: str, region: str, analysis_type: str = "both") -> str:
        """Create specialized buyer analysis prompt with comprehensive Vector DB integration"""
        
        base_prompt = f"""
You are a senior M&A advisor specializing in buyer analysis. Your task is to identify and analyze potential acquirers for {company_name} using the comprehensive market intelligence provided in the Vector DB context below.

## TARGET COMPANY PROFILE
- Company: {company_name}
- Business Overview: {company_overview}
- Sector: {sector}
- Region: {region}

## BUYER ANALYSIS REQUIREMENTS

{'### STRATEGIC BUYERS' if analysis_type in ['strategic', 'both'] else ''}
{'''Identify potential strategic acquirers who would have compelling rationales for acquiring this business. For each strategic buyer:

1. **Buyer Identification**: Name specific companies based on precedent transaction patterns
2. **Strategic Rationale**: Explain the strategic logic using examples from similar transactions
3. **Synergy Opportunities**: Detail operational, revenue, and cost synergies based on transaction precedents
4. **Geographic Fit**: Assess regional expansion motivations using market data
5. **Acquisition History**: Reference their M&A track record in this or adjacent sectors
6. **Strategic Fit Score**: Rate fit as High (8-10), Medium (5-7), or Low (1-4) with evidence''' if analysis_type in ['strategic', 'both'] else ''}

{'### FINANCIAL BUYERS' if analysis_type in ['financial', 'both'] else ''}
{'''Identify potential financial buyers (PE firms, growth equity) who would be interested in this investment. For each financial buyer:

1. **Buyer Identification**: Name specific PE firms based on their sector focus and transaction history
2. **Investment Thesis**: Explain the financial buyer appeal using comparable transaction rationales
3. **Value Creation Strategy**: Detail operational improvements and growth strategies based on precedent deals
4. **Return Profile**: Assess return potential using relevant transaction multiples and exit strategies
5. **Portfolio Fit**: Explain how this fits their existing portfolio or sector expertise
6. **Financial Fit Score**: Rate fit as High (8-10), Medium (5-7), or Low (1-4) with supporting data''' if analysis_type in ['financial', 'both'] else ''}

## ANALYSIS FRAMEWORK

Use the Vector DB context to provide evidence-based analysis:
- **Reference Specific Transactions**: Cite actual deals that support your buyer identification
- **Use Real Acquirer Names**: Name companies that have been active in similar transactions  
- **Ground Valuations**: Reference actual multiples and deal structures from the data
- **Support Strategic Logic**: Use transaction rationales and market trends from the context
- **Prioritize by Evidence**: Rank buyers based on strength of supporting precedent transaction evidence

## OUTPUT FORMAT

1. **Executive Summary** - Key buyer themes and market dynamics
2. **Strategic Buyer Analysis** - Detailed analysis of top strategic candidates
3. **Financial Buyer Analysis** - Detailed analysis of top financial buyer candidates  
4. **Market Intelligence** - Key insights from precedent transactions and market data
5. **Competitive Dynamics** - Expected buyer competition and process implications

**Critical Requirement**: All buyer identifications and strategic rationales must be grounded in specific evidence from the Vector DB context. Do not speculate beyond what is supported by the precedent transaction and market data provided.
"""
        
        return self.enhance_prompt_with_vector_data(base_prompt, "buyer_analysis", {
            'name': company_name,
            'overview': company_overview,
            'sector': sector,
            'region': region
        })

# Global instance
enhanced_ai_analysis = EnhancedAIAnalysis()

def get_enhanced_ai_analysis() -> EnhancedAIAnalysis:
    """Get the global enhanced AI analysis instance"""
    return enhanced_ai_analysis
