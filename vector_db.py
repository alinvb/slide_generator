"""
Vector DB Module for Enhanced AI Analysis
Handles Cassandra Vector Database operations for retrieving precedent transactions
and market data to enhance AI responses.
"""

import os
from typing import List, Dict, Optional, Any
import streamlit as st

# Optional vector database support
try:
    import cassio
    from cassio.vector import VectorTable
    CASSIO_AVAILABLE = True
except ImportError:
    CASSIO_AVAILABLE = False
    print("⚠️ Vector Database (cassio) not available - using mock data")

class VectorDBManager:
    """Manages Vector Database operations for enhanced AI analysis"""
    
    def __init__(self):
        self.vector_table = None
        self.is_initialized = False
        self.mock_data_enabled = True  # Enable mock data for testing
        
    def initialize(self, database_id: str, token: str, keyspace: str = 'default_keyspace', table_name: str = 'ma10'):
        """Initialize connection to Cassandra Vector Database"""
        if not CASSIO_AVAILABLE:
            print("⚠️ Cassio not available - using mock mode")
            self.is_initialized = True
            return True
            
        try:
            # Set environment variables
            os.environ["PERPLEXITY_API_KEY"] = "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"
            
            # Initialize cassio
            cassio.init(
                database_id=database_id,
                token=token
            )
            
            # Create vector store (we'll need to set up embedding model later)
            # For now, we'll create a placeholder that can be configured
            self.database_id = database_id
            self.token = token
            self.keyspace = keyspace
            self.table_name = table_name
            
            st.success(f"✅ Vector DB initialized successfully!")
            st.info(f"Database: {database_id[:8]}... | Keyspace: {keyspace} | Table: {table_name}")
            
            self.is_initialized = True
            return True
            
        except Exception as e:
            st.error(f"❌ Failed to initialize Vector DB: {str(e)}")
            self.is_initialized = False
            return False
    
    def setup_vector_table(self, dimension: int = 384):
        """Set up the vector table for operations"""
        try:
            if not self.is_initialized:
                st.error("❌ Vector DB not initialized. Please initialize first.")
                return False
            
            # Create vector table using cassio
            self.vector_table = VectorTable(
                table=self.table_name,
                keyspace=self.keyspace,
                vector_dimension=dimension
            )
            
            st.success("✅ Vector table configured successfully!")
            return True
            
        except Exception as e:
            st.error(f"❌ Failed to setup vector table: {str(e)}")
            return False
    
    def search_precedent_transactions(self, query: str, k: int = 50) -> List[Dict[str, Any]]:
        """Search for precedent transactions using vector similarity"""
        try:
            # For now, return mock data if vector table isn't configured or if mock is enabled
            if not self.vector_table or self.mock_data_enabled:
                st.info("⚠️ Using mock data for precedent transactions")
                return self._get_mock_transactions(query, k)
            
            # TODO: Implement actual vector search when embeddings are available
            # This would require an embedding model to convert the query to a vector
            # and then search the vector table
            
            st.success(f"✅ Retrieved mock precedent transactions")
            return self._get_mock_transactions(query, k)
            
        except Exception as e:
            st.error(f"❌ Search failed: {str(e)}")
            return []
    
    def get_precedent_transactions(self, company_name: str, company_overview: str, sector: str, region: str = "Global", revenue_range: str = None, ebitda_range: str = None) -> List[Dict[str, Any]]:
        """Get precedent transactions for any company type based on dynamic company context"""
        
        # Create multiple query variations to maximize data retrieval
        queries = self._generate_transaction_queries(company_name, company_overview, sector, region, revenue_range, ebitda_range)
        
        all_results = []
        for query in queries:
            results = self.search_precedent_transactions(query)
            all_results.extend(results)
        
        # Deduplicate results based on content similarity
        return self._deduplicate_results(all_results)
    
    def _generate_transaction_queries(self, company_name: str, company_overview: str, sector: str, region: str, revenue_range: str = None, ebitda_range: str = None) -> List[str]:
        """Generate multiple query variations for comprehensive data retrieval"""
        queries = []
        
        # Query 1: Sector-focused with geography
        query1 = f"""
        Return precedent transactions involving companies in the {sector} sector in {region} or globally.
        Focus on extracting the following for each transaction:

        - Target company name
        - Acquirer name  
        - Announcement or completion date
        - Country / Geography
        - Deal value (US$m)
        - Revenue and EBITDA (if available)
        - Historical revenue growth (if available)
        - EBITDA margin (if available)
        - EV/Revenue and EV/EBITDA multiples
        - Sector/subsector details
        - Transaction rationale (e.g., market entry, synergies, roll-up strategy)

        Prioritize transactions most comparable to: {company_name} - {company_overview[:200]}...
        {f'Revenue range: {revenue_range}' if revenue_range else ''}
        {f'EBITDA range: {ebitda_range}' if ebitda_range else ''}
        """
        queries.append(query1)
        
        # Query 2: Business model focused
        query2 = f"""
        Find M&A transactions involving companies with similar business models to {company_name}.
        Company description: {company_overview[:300]}...
        
        Search for transactions in {sector} and related sectors, focusing on:
        - Companies with similar operational models
        - Similar target markets and customer segments
        - Comparable revenue streams and business structures
        - Geographic presence in {region} or similar markets
        
        Extract: deal multiples, transaction rationale, strategic considerations, and financial metrics.
        """
        queries.append(query2)
        
        # Query 3: Regional and size-based
        if revenue_range or ebitda_range:
            query3 = f"""
            Search for precedent transactions in {region} and globally for companies in {sector} with:
            {f'- Revenue range: {revenue_range}' if revenue_range else ''}
            {f'- EBITDA range: {ebitda_range}' if ebitda_range else ''}
            - Similar to {company_name}: {company_overview[:200]}...
            
            Focus on control transactions (>50% stake) from the last 5 years.
            Extract deal multiples, geographic premiums/discounts, and strategic rationale.
            """
            queries.append(query3)
        
        # Query 4: Strategic rationale focused
        query4 = f"""
        Find transactions where the strategic rationale would be similar for acquiring {company_name}.
        Target profile: {sector} company - {company_overview[:250]}...
        
        Look for deals involving:
        - Market consolidation plays
        - Geographic expansion strategies  
        - Operational synergy opportunities
        - Technology or capability acquisitions
        - Roll-up strategies in similar sectors
        
        Geographic focus: {region} and comparable markets.
        """
        queries.append(query4)
        
        return queries
    
    def get_market_data(self, company_name: str, company_overview: str, sector: str, region: str) -> List[Dict[str, Any]]:
        """Get market data for specific company context, sector and region"""
        
        # Generate multiple market analysis queries
        queries = self._generate_market_queries(company_name, company_overview, sector, region)
        
        all_results = []
        for query in queries:
            results = self.search_precedent_transactions(query)
            all_results.extend(results)
        
        return self._deduplicate_results(all_results)
    
    def _generate_market_queries(self, company_name: str, company_overview: str, sector: str, region: str) -> List[str]:
        """Generate multiple market analysis queries"""
        queries = []
        
        # Query 1: Comprehensive market analysis
        query1 = f"""
        Return comprehensive market data and analysis for the {sector} sector in {region} including:
        - Market size and growth rates
        - Key market trends and dynamics
        - Regulatory environment and compliance requirements
        - Competitive landscape and major players
        - Valuation multiples by region and subsector
        - Recent M&A activity and transaction trends
        - Growth drivers and market challenges
        - Investment climate and capital availability
        
        Context: Analysis for {company_name} - {company_overview[:200]}...
        """
        queries.append(query1)
        
        # Query 2: Competitive positioning analysis
        query2 = f"""
        Analyze competitive positioning and market dynamics relevant to {company_name}.
        Company profile: {company_overview[:300]}...
        
        Focus on:
        - Key competitors in {sector} within {region}
        - Market share dynamics and competitive advantages
        - Barriers to entry and competitive moats
        - Pricing trends and margin pressures
        - Customer behavior and market preferences
        - Technology disruption and innovation trends
        """
        queries.append(query2)
        
        # Query 3: Investment and M&A landscape
        query3 = f"""
        Analyze the investment and M&A landscape for {sector} companies in {region}.
        
        Target company context: {company_name} - {company_overview[:200]}...
        
        Include:
        - Recent M&A transaction activity and trends
        - Strategic buyer interest and acquisition criteria
        - Private equity and financial buyer activity
        - Valuation trends and multiple expansion/compression
        - Deal rationales and strategic themes
        - Market consolidation dynamics
        """
        queries.append(query3)
        
        return queries
    
    def get_valuation_comparables(self, company_name: str, company_overview: str, company_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get valuation comparables based on comprehensive company profile"""
        # Extract key metrics for comparison
        revenue = company_profile.get('revenue', 0)
        ebitda = company_profile.get('ebitda', 0)
        sector = company_profile.get('sector', 'general')
        region = company_profile.get('region', 'global')
        
        # Generate multiple valuation queries
        queries = self._generate_valuation_queries(company_name, company_overview, revenue, ebitda, sector, region)
        
        all_results = []
        for query in queries:
            results = self.search_precedent_transactions(query)
            all_results.extend(results)
        
        return self._deduplicate_results(all_results)
    
    def _generate_valuation_queries(self, company_name: str, company_overview: str, revenue: float, ebitda: float, sector: str, region: str) -> List[str]:
        """Generate multiple valuation-focused queries"""
        queries = []
        
        # Query 1: Financial metrics based
        if revenue > 0 and ebitda > 0:
            query1 = f"""
            Find precedent transactions for companies in {sector} sector with:
            - Revenue range: ${revenue * 0.5:.1f}M - ${revenue * 2.0:.1f}M
            - EBITDA range: ${ebitda * 0.5:.1f}M - ${ebitda * 2.0:.1f}M
            - Geography: {region} (priority) or similar regions
            - Transaction type: Control transactions (>50% stake)
            - Recent transactions (last 5 years preferred)
            
            Target company context: {company_name} - {company_overview[:200]}...
            
            Focus on extracting:
            - Deal multiples (EV/Revenue, EV/EBITDA, P/E)
            - Transaction rationale and strategic premium
            - Regional valuation differences and adjustments
            - Market conditions at time of transaction
            """
            queries.append(query1)
        
        # Query 2: Comparable business model focus
        query2 = f"""
        Find valuation benchmarks for companies with similar business models to {company_name}.
        
        Company description: {company_overview[:300]}...
        Sector: {sector} | Region: {region}
        
        Search for:
        - Companies with similar operational characteristics
        - Comparable customer bases and market positioning
        - Similar revenue models and margin profiles
        - Geographic overlap or comparable market dynamics
        
        Extract: trading multiples, transaction multiples, and valuation methodologies.
        """
        queries.append(query2)
        
        # Query 3: Regional and sector-specific multiples
        query3 = f"""
        Analyze valuation multiples and benchmarks for {sector} companies in {region}.
        
        Reference company: {company_name} - {company_overview[:200]}...
        
        Focus on:
        - Sector-specific valuation multiples and trends
        - Regional valuation premiums and discounts
        - Market cycle impacts on valuations
        - Strategic vs financial buyer pricing differences
        - Recent transaction multiple trends
        - Comparable public company trading multiples
        """
        queries.append(query3)
        
        return queries
    
    def format_context_for_ai(self, retrieved_docs: List[Dict[str, Any]], context_type: str = "general") -> str:
        """Format retrieved documents into context for AI analysis with enhanced structure"""
        if not retrieved_docs:
            return "No relevant precedent transactions or market data found in the database."
        
        # Combine document contents with enhanced formatting
        context_parts = []
        context_parts.append(f"=== VECTOR DATABASE CONTEXT ({context_type.upper()}) ===")
        context_parts.append(f"Retrieved {len(retrieved_docs)} relevant documents for enhanced analysis.\n")
        
        for i, doc in enumerate(retrieved_docs[:25]):  # Increased limit to 25 for better context
            content = doc.get('content', '')
            metadata = doc.get('metadata', {})
            score = doc.get('score', 0.0)
            
            # Enhanced formatting with metadata
            doc_header = f"📊 Document {i+1} (Relevance Score: {score:.3f})"
            if metadata:
                metadata_info = " | ".join([f"{k}: {v}" for k, v in metadata.items() if v])
                if metadata_info:
                    doc_header += f" | {metadata_info}"
            
            context_parts.append(f"{doc_header}:\n{content}")
        
        context_parts.append("\n=== END VECTOR DATABASE CONTEXT ===")
        return "\n\n---\n\n".join(context_parts)
    
    def _deduplicate_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate results based on content similarity"""
        if not results:
            return results
        
        unique_results = []
        seen_content = set()
        
        for result in results:
            content = result.get('content', '')
            # Simple deduplication based on first 100 characters
            content_key = content[:100].lower().strip()
            
            if content_key not in seen_content:
                seen_content.add(content_key)
                unique_results.append(result)
        
        # Sort by relevance score (highest first)
        unique_results.sort(key=lambda x: x.get('score', 0.0), reverse=True)
        return unique_results[:30]  # Limit to top 30 unique results
    
    def _get_mock_transactions(self, query: str, k: int = 50) -> List[Dict[str, Any]]:
        """Return mock precedent transaction data for testing with more diverse examples"""
        mock_transactions = [
            {
                'content': 'Healthcare Services: KKR acquisition of WebMD Health Services for $2.8B, expanding digital health platform capabilities. EV/Revenue: 4.2x, EV/EBITDA: 12.1x. Strategic rationale focused on telehealth and digital patient engagement.',
                'metadata': {'sector': 'healthcare', 'region': 'north_america', 'year': 2023, 'deal_type': 'strategic_acquisition'},
                'score': 0.95
            },
            {
                'content': 'Technology Services: Microsoft acquisition of Nuance Communications for $19.7B, enhancing AI-powered healthcare solutions. EV/Revenue: 8.7x. Strategic focus on cloud-based healthcare AI and voice recognition technology.',
                'metadata': {'sector': 'technology', 'region': 'global', 'year': 2022, 'deal_type': 'strategic_acquisition'},
                'score': 0.92
            },
            {
                'content': 'Financial Services: Blackstone acquisition of Simply Business (UK SME insurance) for $1.2B. EV/Revenue: 6.8x, EV/EBITDA: 15.2x. Roll-up strategy targeting digital insurance platforms in European markets.',
                'metadata': {'sector': 'financial_services', 'region': 'europe', 'year': 2024, 'deal_type': 'pe_buyout'},
                'score': 0.90
            },
            {
                'content': 'Consumer Services: TPG acquisition of Life Time Fitness for $4.0B. EV/Revenue: 2.1x, EV/EBITDA: 9.8x. Strategic thesis around premium fitness and wellness experiences with membership-based recurring revenue model.',
                'metadata': {'sector': 'consumer_services', 'region': 'north_america', 'year': 2023, 'deal_type': 'pe_buyout'},
                'score': 0.88
            },
            {
                'content': 'Healthcare: Teladoc Health acquisition of Livongo for $18.5B, creating integrated virtual care platform. EV/Revenue: 24.1x at announcement. Focus on chronic disease management and telehealth convergence.',
                'metadata': {'sector': 'healthcare', 'region': 'global', 'year': 2021, 'deal_type': 'strategic_merger'},
                'score': 0.85
            },
            {
                'content': 'Business Services: Salesforce acquisition of Slack for $27.7B, expanding collaboration and productivity suite. EV/Revenue: 26.8x. Strategic rationale around workplace transformation and customer relationship integration.',
                'metadata': {'sector': 'technology', 'region': 'global', 'year': 2021, 'deal_type': 'strategic_acquisition'},
                'score': 0.83
            },
            {
                'content': 'Asia-Pacific Healthcare: IHH Healthcare acquisition of Fortis Healthcare (India) stake for $1.1B. EV/Revenue: 3.2x, EV/EBITDA: 11.4x. Geographic expansion strategy targeting emerging healthcare markets.',
                'metadata': {'sector': 'healthcare', 'region': 'asia_pacific', 'year': 2023, 'deal_type': 'strategic_acquisition'},
                'score': 0.81
            }
        ]
        
        # Filter based on query content for better relevance
        query_lower = query.lower()
        filtered_results = []
        
        # Priority scoring based on query keywords
        for transaction in mock_transactions:
            content_lower = transaction['content'].lower()
            metadata = transaction.get('metadata', {})
            
            # Calculate relevance boost based on query matching
            relevance_boost = 0.0
            
            # Check for sector match
            for sector_keyword in ['healthcare', 'technology', 'financial', 'consumer', 'business']:
                if sector_keyword in query_lower and sector_keyword in content_lower:
                    relevance_boost += 0.1
            
            # Check for region match  
            for region_keyword in ['asia', 'europe', 'america', 'global']:
                if region_keyword in query_lower and region_keyword in content_lower:
                    relevance_boost += 0.05
            
            # Adjust score
            transaction['score'] = min(0.99, transaction['score'] + relevance_boost)
            
            filtered_results.append(transaction)
            if len(filtered_results) >= min(k, 7):  # Limit to max 7 mock results
                break
        
        return filtered_results

    def get_status(self) -> Dict[str, Any]:
        """Get current status of Vector DB connection"""
        return {
            'is_initialized': self.is_initialized,
            'has_vector_table': self.vector_table is not None,
            'mock_data_enabled': getattr(self, 'mock_data_enabled', True),
            'database_id': getattr(self, 'database_id', None),
            'keyspace': getattr(self, 'keyspace', None),
            'table_name': getattr(self, 'table_name', None)
        }

# Global instance
vector_db_manager = VectorDBManager()

def get_vector_db_manager() -> VectorDBManager:
    """Get the global Vector DB manager instance"""
    return vector_db_manager
