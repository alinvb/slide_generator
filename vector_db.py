"""
Vector DB Module for Enhanced AI Analysis
Handles Cassandra Vector Database operations for retrieving precedent transactions
and market data to enhance AI responses.
"""

import os
import cassio
from typing import List, Dict, Optional, Any
from cassio.vector import Cassandra
import streamlit as st

class VectorDBManager:
    """Manages Vector Database operations for enhanced AI analysis"""
    
    def __init__(self):
        self.vectorstore = None
        self.retriever = None
        self.is_initialized = False
        
    def initialize(self, database_id: str, token: str, keyspace: str = 'default_keyspace', table_name: str = 'ma10'):
        """Initialize connection to Cassandra Vector Database"""
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
    
    def setup_embedding_model(self, embedding_model):
        """Set up the embedding model for vector operations"""
        try:
            if not self.is_initialized:
                st.error("❌ Vector DB not initialized. Please initialize first.")
                return False
            
            # Create vector store with embedding model
            self.vectorstore = Cassandra(
                embedding=embedding_model,
                keyspace=self.keyspace,
                table_name=self.table_name,
            )
            
            # Create retriever
            self.retriever = self.vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 50}  # Retrieve top 50 most similar documents
            )
            
            st.success("✅ Embedding model configured successfully!")
            return True
            
        except Exception as e:
            st.error(f"❌ Failed to setup embedding model: {str(e)}")
            return False
    
    def search_precedent_transactions(self, query: str, k: int = 50) -> List[Dict[str, Any]]:
        """Search for precedent transactions using vector similarity"""
        try:
            if not self.retriever:
                st.warning("⚠️ Retriever not configured. Please setup embedding model first.")
                return []
            
            # Execute search
            retrieved_docs = self.retriever.invoke(query)
            
            # Convert to structured format
            results = []
            for doc in retrieved_docs:
                results.append({
                    'content': doc.page_content,
                    'metadata': getattr(doc, 'metadata', {}),
                    'score': getattr(doc, 'score', 0.0)
                })
            
            st.success(f"✅ Retrieved {len(results)} precedent transactions")
            return results
            
        except Exception as e:
            st.error(f"❌ Search failed: {str(e)}")
            return []
    
    def get_healthcare_transactions(self, region: str = "Asia", sector: str = "healthcare") -> List[Dict[str, Any]]:
        """Get healthcare-specific precedent transactions"""
        query = f"""
        Return a list of precedent transactions involving healthcare clinics, private hospitals, medical groups, or outpatient care companies in {region}.
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
        - Sector/subsector (e.g., outpatient, primary care, diagnostics)
        - Rationale for the transaction (e.g., market entry, synergies, roll-up strategy)

        Prioritize transactions most comparable to a premium multi-clinic outpatient operator in Hong Kong with ~$6M EBITDA and ~10-15% margins.
        If possible, include transactions involving businesses in the same country or region with similar business models and patient volumes.
        """
        
        return self.search_precedent_transactions(query)
    
    def get_market_data(self, sector: str, region: str) -> List[Dict[str, Any]]:
        """Get market data for specific sector and region"""
        query = f"""
        Return market data and analysis for {sector} sector in {region} including:
        - Market size and growth rates
        - Key market trends
        - Regulatory environment
        - Competitive landscape
        - Valuation multiples by region
        - Recent M&A activity
        - Growth drivers and challenges
        """
        
        return self.search_precedent_transactions(query)
    
    def get_valuation_comparables(self, company_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get valuation comparables based on company profile"""
        # Extract key metrics for comparison
        revenue = company_profile.get('revenue', 0)
        ebitda = company_profile.get('ebitda', 0)
        sector = company_profile.get('sector', 'general')
        region = company_profile.get('region', 'global')
        
        query = f"""
        Find precedent transactions for companies in {sector} sector with:
        - Revenue range: ${revenue * 0.5}M - ${revenue * 2.0}M
        - EBITDA range: ${ebitda * 0.5}M - ${ebitda * 2.0}M
        - Geography: {region} (priority) or similar regions
        - Transaction type: Control transactions (>50% stake)
        - Recent transactions (last 5 years preferred)
        
        Focus on extracting:
        - Deal multiples (EV/Revenue, EV/EBITDA)
        - Transaction rationale
        - Strategic considerations
        - Regional valuation differences
        """
        
        return self.search_precedent_transactions(query)
    
    def format_context_for_ai(self, retrieved_docs: List[Dict[str, Any]]) -> str:
        """Format retrieved documents into context for AI analysis"""
        if not retrieved_docs:
            return "No relevant precedent transactions found in the database."
        
        # Combine document contents
        context_parts = []
        for i, doc in enumerate(retrieved_docs[:20]):  # Limit to top 20 for context
            content = doc.get('content', '')
            metadata = doc.get('metadata', {})
            score = doc.get('score', 0.0)
            
            context_parts.append(f"Document {i+1} (Relevance: {score:.3f}):\n{content}")
        
        return "\n\n---\n\n".join(context_parts)
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of Vector DB connection"""
        return {
            'is_initialized': self.is_initialized,
            'has_retriever': self.retriever is not None,
            'database_id': getattr(self, 'database_id', None),
            'keyspace': getattr(self, 'keyspace', None),
            'table_name': getattr(self, 'table_name', None)
        }

# Global instance
vector_db_manager = VectorDBManager()

def get_vector_db_manager() -> VectorDBManager:
    """Get the global Vector DB manager instance"""
    return vector_db_manager
