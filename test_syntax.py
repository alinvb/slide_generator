def test_dict():
    return {
        "historical_financial_performance": {
            "title": "Historical Financial Performance", 
            "prompt": """📊 DETAILED FINANCIAL PERFORMANCE ANALYSIS for {company}:

CONTEXT FROM PRIOR RESEARCH:
Use business model and operational insights from Topics 1-2 to analyze financial trends across segments and geographies.

🚨 MANDATORY REQUIREMENTS - PROVIDE ACTUAL FINANCIAL DATA:
Research and provide SPECIFIC financial metrics:

**REVENUE ANALYSIS (3-5 Years)**:
✅ **Annual Revenue**: Exact revenue figures for last 3-5 years (in millions USD)
✅ **Revenue Growth**: Year-over-year growth rates for each period
✅ **Revenue Breakdown**: By business segment, geography, or product line (%)
✅ **Revenue Mix**: Recurring vs. one-time revenue breakdown
✅ **Key Revenue Drivers**: Specific factors driving revenue growth

**PROFITABILITY METRICS**:
✅ **Gross Profit/Margin**: Gross profit dollars and margins by year
✅ **EBITDA**: Actual EBITDA figures and margins for each year
✅ **Operating Income**: Operating profit and operating margins
✅ **Net Income**: Net profit figures and net margins
✅ **Margin Trends**: Analysis of margin expansion/compression

**CASH FLOW & BALANCE SHEET**:
✅ **Operating Cash Flow**: Cash from operations for each year
✅ **Free Cash Flow**: FCF calculation and conversion rates
✅ **Working Capital**: Working capital trends and efficiency
✅ **Debt Levels**: Total debt, debt-to-equity ratios
✅ **Cash Position**: Cash and equivalents on balance sheet

**KEY PERFORMANCE INDICATORS**:
✅ **Unit Economics**: Customer acquisition cost, lifetime value, etc.
✅ **Operational Metrics**: Key business metrics specific to industry
✅ **Financial Ratios**: ROE, ROA, asset turnover, etc.
✅ **Benchmarking**: Performance vs. industry averages

**CAPITAL STRUCTURE & FINANCING**:
✅ **Funding History**: Funding rounds, amounts, dates, investors
✅ **Capital Efficiency**: Revenue per employee, capital intensity
✅ **Seasonal Patterns**: Quarterly trends and seasonality factors

RESEARCH INSTRUCTIONS:
Provide investment banking-grade financial analysis with specific numbers, ratios, and trends. Focus on verified data from regulatory filings, audited statements, or credible databases.""",
            "required_fields": ["annual_revenue_usd_m", "revenue_growth_rates", "ebitda_figures", "operating_margins", "cash_flow_metrics", "debt_levels", "key_financial_ratios", "funding_history", "unit_economics"]
        },

        "management_team": {
            "title": "Management Team & Leadership",
            "prompt": """👥 COMPREHENSIVE LEADERSHIP TEAM ANALYSIS for {company}:

CONTEXT FROM PRIOR RESEARCH:
Use business model, financial performance, and growth strategy insights to assess management capabilities.""",
            "required_fields": ["management_profiles", "experience", "track_record"]
        }
    }

if __name__ == "__main__":
    print("Testing dictionary structure...")
    result = test_dict()
    print("Success - no syntax errors!")
