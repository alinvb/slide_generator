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
        """Enhance AI prompt with relevant Vector DB data"""
        
        if not self.vector_db.is_initialized:
            st.warning("⚠️ Vector DB not initialized. Using base prompt without enhancement.")
            return base_prompt
        
        try:
            # Get relevant context based on prompt type
            if "healthcare" in base_prompt.lower() or "medical" in base_prompt.lower():
                context_docs = self.vector_db.get_healthcare_transactions()
                context_type = "healthcare_transactions"
            elif "valuation" in base_prompt.lower() or "comparable" in base_prompt.lower():
                if company_profile:
                    context_docs = self.vector_db.get_valuation_comparables(company_profile)
                    context_type = "valuation_comparables"
                else:
                    context_docs = self.vector_db.get_market_data("general", "global")
                    context_type = "market_data"
            elif "market" in base_prompt.lower() or "industry" in base_prompt.lower():
                # Extract sector and region from prompt
                sector = "general"
                region = "global"
                if "asia" in base_prompt.lower():
                    region = "Asia"
                if "healthcare" in base_prompt.lower():
                    sector = "healthcare"
                
                context_docs = self.vector_db.get_market_data(sector, region)
                context_type = "market_data"
            else:
                # General search
                context_docs = self.vector_db.search_precedent_transactions(base_prompt[:500])
                context_type = "general_search"
            
            if context_docs:
                # Format context for AI
                context = self.vector_db.format_context_for_ai(context_docs)
                
                # Create enhanced prompt
                enhanced_prompt = f"""
{base_prompt}

## ENHANCED CONTEXT FROM VECTOR DATABASE
The following information has been retrieved from our precedent transactions and market data database to enhance your analysis:

{context}

## INSTRUCTIONS
Please use this additional context to provide more accurate and informed analysis. When referencing precedent transactions or market data, cite the specific information from the context above. If the context doesn't contain relevant information for a specific aspect of your analysis, clearly state that and proceed with your best judgment based on general knowledge.
"""
                
                st.success(f"✅ Enhanced prompt with {len(context_docs)} relevant documents from Vector DB")
                return enhanced_prompt
            else:
                st.info("ℹ️ No relevant Vector DB data found. Using base prompt.")
                return base_prompt
                
        except Exception as e:
            st.error(f"❌ Error enhancing prompt with Vector DB data: {str(e)}")
            return base_prompt
    
    def create_general_valuation_prompt(self, company_name: str, sector: str, region: str = "Asia") -> str:
        """Create a general valuation prompt with Vector DB context"""
        
        base_prompt = f"""
You are a senior M&A analyst. Your task is to produce a **highly accurate, well-structured comparable transaction analysis** for {company_name} in the {sector} sector based in {region} — **using only the information provided in the context below**.  
Do NOT invent or assume any data not explicitly present in the context.

## COMPANY PROFILE
- Company: {company_name}
- Sector: {sector}
- Region: {region}

## Step 1 – Select Comparables
Identify **relevant M&A transactions** from the context that are most comparable to {company_name}.  

### Relevance hierarchy (most to least important):
1. **Sector/Sub-sector Match** – Same or closely related industry
2. **Geography** –  
   - Priority 1: {region}  
   - Priority 2: Similar regions  
   - Priority 3: Other regions with relevant sector data
3. **Scale & Financial Size** – Similar revenue, EBITDA, or employee count
4. **Business Model** – Similar positioning and service mix
5. **Transaction Type** – Control (>50% stake) is more directly comparable than minority stakes
6. **Timing** – More recent transactions are generally more relevant

## Step 2 – Present Comparable Transactions
List the transactions in a **table ordered by Date (most recent first)** with relevant columns based on available data.

## Step 3 – Analysis
Provide:
1. **Key insights** from the precedent transactions
2. **Market trends** observed in the data
3. **Regional considerations** and differences
4. **Strategic implications** for {company_name}

## Output Format:
1. **Comparable Transactions Table** – ordered by most recent date
2. **Written Analysis** – covering key insights and trends
3. **Strategic Summary** – actionable insights and recommendations

**Important:**  
- Use only data from the provided context — no external sources, no assumptions.
- Focus on actionable insights and market intelligence.
"""
        
        # Enhance with Vector DB data
        return self.enhance_prompt_with_vector_data(base_prompt, "general_valuation", {
            'sector': sector,
            'region': region
        })
    
    def create_market_analysis_prompt(self, sector: str, region: str, focus_areas: List[str]) -> str:
        """Create a market analysis prompt with Vector DB context"""
        
        focus_text = "\n".join([f"- {area}" for area in focus_areas])
        
        base_prompt = f"""
You are a senior market analyst specializing in {sector} sector analysis. Provide a comprehensive market analysis for {region} using the context provided below.

## ANALYSIS REQUIREMENTS
Focus on the following areas:
{focus_text}

## ANALYSIS STRUCTURE
1. **Market Overview** - Size, growth, key drivers
2. **Competitive Landscape** - Major players, market share, positioning
3. **Regulatory Environment** - Key regulations, compliance requirements
4. **Market Trends** - Current and emerging trends
5. **Growth Opportunities** - Untapped markets, expansion potential
6. **Risk Factors** - Market risks, challenges, uncertainties
7. **Investment Climate** - M&A activity, investment trends
8. **Regional Variations** - Differences across sub-regions
9. **Future Outlook** - 3-5 year projections
10. **Strategic Recommendations** - Actionable insights

## OUTPUT FORMAT
Provide a structured analysis with clear sections, bullet points for key insights, and specific data points where available from the context.

**Important:** Use only information from the provided context. If specific data is not available, clearly state this limitation.
"""
        
        return self.enhance_prompt_with_vector_data(base_prompt, "market_analysis")
    
    def get_analysis_suggestions(self, prompt: str) -> List[str]:
        """Get suggestions for improving analysis based on Vector DB capabilities"""
        suggestions = []
        
        if not self.vector_db.is_initialized:
            suggestions.append("🔗 Initialize Vector DB to access precedent transactions and market data")
            return suggestions
        
        # Analyze prompt and suggest enhancements
        prompt_lower = prompt.lower()
        
        if "valuation" in prompt_lower or "comparable" in prompt_lower:
            suggestions.append("📊 Use Vector DB to find relevant precedent transactions for accurate multiples")
            suggestions.append("🌍 Access regional valuation data for geographic adjustments")
        
        if "healthcare" in prompt_lower or "medical" in prompt_lower:
            suggestions.append("🏥 Leverage healthcare-specific precedent transactions from Vector DB")
            suggestions.append("💊 Access medical sector market data and trends")
        
        if "technology" in prompt_lower or "software" in prompt_lower:
            suggestions.append("💻 Access technology sector precedent transactions and market data")
            suggestions.append("🚀 Use tech industry trends and valuation multiples")
        
        if "financial" in prompt_lower or "fintech" in prompt_lower:
            suggestions.append("🏦 Access financial services precedent transactions")
            suggestions.append("💰 Use financial sector market data and regulatory insights")
        
        if "market" in prompt_lower or "industry" in prompt_lower:
            suggestions.append("📈 Use Vector DB market data for industry insights and trends")
            suggestions.append("🎯 Access competitive landscape and market positioning data")
        
        if "asia" in prompt_lower or "hong kong" in prompt_lower:
            suggestions.append("🇭🇰 Access Asia-Pacific specific market data and transactions")
            suggestions.append("🌏 Use regional precedent transactions for local market insights")
        
        return suggestions

# Global instance
enhanced_ai_analysis = EnhancedAIAnalysis()

def get_enhanced_ai_analysis() -> EnhancedAIAnalysis:
    """Get the global enhanced AI analysis instance"""
    return enhanced_ai_analysis
