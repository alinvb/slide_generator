# Investment Banking Research Agent System

A comprehensive AI-powered investment banking research and presentation generation system with advanced Research Agent capabilities.

## 🚀 Key Features

### 🔬 Research Agent System
- **14 Sequential Research Topics**: Comprehensive investment banking analysis covering all critical areas
- **Global Company Compatibility**: Works with companies from any region without hardcoded limitations
- **Perplexity Integration**: Advanced web research using Sonar Pro models for real-time market data
- **Context-Aware Analysis**: Each research topic builds upon previous findings for coherent analysis

### 📊 Investment Banking Topics Covered
1. **Business Overview** - Company description, industry, and market position
2. **Product & Service Footprint** - Portfolio analysis and geographic presence  
3. **Historical Financial Performance** - Revenue, profitability, and growth trends
4. **Management Team** - Executive profiles and leadership assessment
5. **Growth Strategy & Projections** - Future plans and market opportunities
6. **Competitive Positioning** - Market analysis and competitive advantages
7. **Precedent Transactions** - Comparable deals and valuation benchmarks
8. **Valuation Overview** - Financial modeling and valuation methodologies
9. **Strategic Buyers** - Industry players and potential acquirers
10. **Financial Buyers** - Private equity and institutional investors
11. **Global Conglomerates** - Large-scale strategic acquirers
12. **Margin & Cost Resilience** - Operational efficiency analysis
13. **Investor Considerations** - Risk factors and investment thesis
14. **Investor Process Overview** - Deal structure and timeline

### 🎯 Core Capabilities
- **Automated JSON Generation**: Research data automatically converted to structured JSON formats
- **PowerPoint Creation**: Professional investment banking presentations with company branding
- **Brand Integration**: Custom company logos, fonts, and styling in presentations
- **Quality Validation**: Built-in JSON validation and auto-improvement systems
- **Error Recovery**: Robust error handling with fallback mechanisms

### 🛠️ Technical Architecture
- **Streamlit Interface**: 5-tab user interface (Research Agent, Brand, JSON Editor, Execute, Validator)
- **Claude & Perplexity APIs**: Multi-model AI integration for research and analysis
- **Vector Database Support**: Optional enhanced data storage and retrieval
- **Supervisor Daemon**: Production-ready service management

## 📋 System Requirements

### Dependencies
```bash
pip install -r requirements.txt
```

### Key Python Packages
- `streamlit` - Web interface framework
- `anthropic` - Claude API integration  
- `requests` - HTTP requests for Perplexity API
- `python-pptx` - PowerPoint generation
- `json` - Data structure handling
- `supervisor` - Process management

### API Keys Required
- **Claude API Key** (Anthropic)
- **Perplexity API Key** (for Research Agent functionality)

## 🚀 Quick Start

### 1. Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Configure supervisor (for production)
supervisord -c supervisord.conf
```

### 2. Launch Application
```bash
# Development mode
streamlit run app.py

# Production mode (with supervisor)
supervisorctl start streamlit
```

### 3. Usage Workflow
1. **Research Agent Tab**: Enter company name and start comprehensive research
2. **Brand Tab**: Configure company branding and presentation styling
3. **JSON Editor Tab**: Review and edit generated research data (auto-populated)
4. **Execute Tab**: Generate branded PowerPoint presentation
5. **Validator Tab**: Validate JSON structure and data quality

## 🏗️ File Structure

### Core Application Files
- `app.py` - Main Streamlit application with 5-tab interface
- `research_agent.py` - Research Agent system with 14 research topics
- `shared_functions.py` - Shared utilities and API wrappers

### Specialized Modules
- `bulletproof_json_generator.py` - Robust JSON generation with error handling
- `topic_based_slide_generator.py` - Intelligent slide generation based on covered topics
- `brand_extractor.py` - Company branding and logo extraction
- `slide_templates.py` - PowerPoint template definitions
- `adapters.py` - PowerPoint rendering and formatting
- `enhanced_auto_improvement_system.py` - JSON quality enhancement
- `vector_db.py` - Optional vector database integration

### Supporting Components
- `perfect_json_prompter.py` - JSON format optimization
- `validators.py` - Data validation and quality checks
- `enhanced_ai_analysis.py` - Advanced AI analysis capabilities
- `executive_search.py` - Management team research
- `json_data_fixer.py` - Automatic JSON error correction

## 🔧 Configuration

### Supervisor Configuration
Production deployment uses supervisor for process management:
```ini
[program:streamlit]
command=streamlit run app.py --server.port=8501 --server.address=0.0.0.0
directory=/path/to/webapp
autostart=true
autorestart=true
```

### Environment Variables
- `CLAUDE_API_KEY` - Anthropic Claude API key
- `PERPLEXITY_API_KEY` - Perplexity API key for research
- `STREAMLIT_PORT` - Port for Streamlit application (default: 8501)

## 🎯 Key Improvements in This Version

### ✅ Research Agent Enhancements
- Fixed infinite loop issues in research topic progression
- Implemented proper topic completion detection
- Added comprehensive error handling and recovery mechanisms
- Improved context building between research topics

### ✅ Global Compatibility
- Removed hardcoded company limitations (US/Europe focus removed)
- Enhanced geographic-adaptive analysis for any region
- Improved currency and market context handling

### ✅ Technical Robustness
- Fixed tuple AttributeError with comprehensive type checking
- Enhanced JSON generation reliability with multiple fallback mechanisms
- Improved API integration with current Perplexity model names
- Streamlined codebase with unnecessary file cleanup

### ✅ User Experience
- Enhanced notifications for JSON auto-population with clear next steps
- Improved tab navigation guidance for better workflow
- Cleaner interface without promotional clutter
- Better error messages and recovery instructions

## 📊 Performance Optimizations

### Research Agent Optimizations
- Efficient API call management to avoid rate limiting  
- Smart caching of research results between topics
- Optimized conversation context management
- Reduced redundant research calls through better topic detection

### JSON Processing Improvements
- Bulletproof JSON parsing with multiple extraction methods
- Automatic format correction and validation
- Enhanced error recovery with meaningful fallbacks
- Streamlined auto-improvement integration

## 🔍 Troubleshooting

### Common Issues
1. **Tuple AttributeError**: Fixed with comprehensive type checking and fallbacks
2. **Research Loop**: Resolved with improved topic completion detection  
3. **API Rate Limits**: Handled with exponential backoff and retry logic
4. **JSON Validation**: Enhanced with automatic correction and user guidance

### Support
- Check supervisor logs: `supervisorctl tail streamlit`
- Validate JSON in Editor tab before execution
- Use auto-improvement for JSON quality issues
- Review Research Agent progress in real-time

## 📈 Future Enhancements

### Planned Features
- Multi-language support for international markets
- Advanced financial modeling integration
- Enhanced competitor analysis capabilities
- Automated regulatory compliance checking
- Integration with financial data providers

### Scalability Improvements
- Database backend for research data persistence
- API rate limiting and queuing system
- Multi-user session management
- Cloud deployment optimization

---

**Version**: Research Agent v2.0  
**Last Updated**: September 2024  
**License**: Proprietary - Investment Banking Research System