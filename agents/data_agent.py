from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
from typing import Dict, List, Any
from tools.finance_tools import FinanceTools
from config.settings import settings
from config.logging_config import get_logger

logger = get_logger(__name__)

class DataAgent:
    """Agent responsible for gathering financial data and statements."""
    
    def __init__(self):
        self.llm = ChatGroq(
            model=settings.GROQ_MODEL,
            temperature=settings.GROQ_TEMPERATURE,
            groq_api_key=settings.GROQ_API_KEY
        )
        self.finance_tools = FinanceTools()
        
        self.system_prompt = """You are a Financial Data Research Agent specializing in analyzing company financials.
Your role is to gather, validate, and interpret financial data to support investment analysis.

Key responsibilities:
1. Fetch comprehensive financial data from reliable sources
2. Analyze financial statements and key metrics
3. Identify trends and patterns in financial performance
4. Provide insights on financial health and stability

Always provide accurate, data-driven analysis and highlight any data quality issues."""
    
    def gather_financial_data(self, symbol: str) -> Dict[str, Any]:
        """
        Gather comprehensive financial data for a company.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Dictionary containing financial data and analysis
        """
        try:
            logger.info(f"Data Agent: Starting financial data gathering for {symbol}")
            
            # Gather all financial data
            current_price_data = self.finance_tools.get_current_stock_price(symbol)
            company_info = self.finance_tools.get_company_info(symbol)
            income_statements = self.finance_tools.get_income_statements(symbol)
            balance_sheet = self.finance_tools.get_balance_sheet(symbol)
            
            # Analyze the gathered data
            analysis = self._analyze_financial_data(
                symbol, current_price_data, company_info, income_statements, balance_sheet
            )
            
            logger.info(f"Data Agent: Completed financial data gathering for {symbol}")
            
            return {
                'symbol': symbol,
                'current_price_data': current_price_data,
                'company_info': company_info,
                'income_statements': income_statements,
                'balance_sheet': balance_sheet,
                'analysis': analysis,
                'timestamp': analysis.get('timestamp', ''),
                'agent': 'DataAgent'
            }
            
        except Exception as e:
            logger.error(f"Data Agent: Error gathering financial data for {symbol}: {e}")
            return {
                'symbol': symbol,
                'error': f"Failed to gather financial data: {str(e)}",
                'agent': 'DataAgent'
            }
    
    def _analyze_financial_data(self, symbol: str, current_price_data: Dict, 
                               company_info: Dict, income_statements: Dict, 
                               balance_sheet: Dict) -> Dict[str, Any]:
        """
        Analyze gathered financial data using LLM.
        
        Args:
            symbol: Stock symbol
            current_price_data: Current stock price and market data
            company_info: Company information
            income_statements: Income statement data
            balance_sheet: Balance sheet data
            
        Returns:
            Financial analysis results
        """
        try:
            # Prepare financial summary for LLM analysis
            financial_summary = self._prepare_financial_summary(
                current_price_data, income_statements, balance_sheet
            )
            
            prompt = f"""
Analyze the following financial data for {symbol}:

Company Information:
- Name: {company_info.get('company_name', 'N/A')}
- Sector: {company_info.get('sector', 'N/A')}
- Industry: {company_info.get('industry', 'N/A')}

Current Market Data:
{self._format_market_data(current_price_data)}

Financial Summary:
{financial_summary}

Please provide:
1. Key financial metrics and their interpretation
2. Financial health assessment
3. Growth trends and patterns
4. Risk factors and concerns
5. Strengths and opportunities

Format your response as a structured financial analysis.
"""
            
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            
            return {
                'financial_metrics': self._extract_metrics(response.content),
                'health_assessment': self._assess_financial_health(income_statements, balance_sheet),
                'growth_trends': self._analyze_growth_trends(income_statements),
                'risk_factors': self._identify_risk_factors(current_price_data, income_statements),
                'strengths': self._identify_strengths(income_statements, balance_sheet),
                'timestamp': self._get_timestamp(),
                'llm_analysis': response.content
            }
            
        except Exception as e:
            logger.error(f"Data Agent: Error analyzing financial data for {symbol}: {e}")
            return {
                'error': f"Failed to analyze financial data: {str(e)}",
                'timestamp': self._get_timestamp()
            }
    
    def _prepare_financial_summary(self, current_price_data: Dict, 
                                  income_statements: Dict, balance_sheet: Dict) -> str:
        """Prepare a summary of key financial data."""
        summary_parts = []
        
        # Current price summary
        if 'current_price' in current_price_data and current_price_data['current_price'] != 'N/A':
            summary_parts.append(f"Current Price: ${current_price_data['current_price']}")
        
        # Market cap
        if 'market_cap' in current_price_data and current_price_data['market_cap'] != 'N/A':
            summary_parts.append(f"Market Cap: ${current_price_data['market_cap']:,}")
        
        # Income statement summary
        if 'income_statements' in income_statements:
            for period, data in list(income_statements['income_statements'].items())[:2]:  # Last 2 periods
                if 'Total Revenue' in data:
                    summary_parts.append(f"{period} Revenue: ${data['Total Revenue']:,}")
                if 'Net Income' in data:
                    summary_parts.append(f"{period} Net Income: ${data['Net Income']:,}")
        
        # Balance sheet summary
        if 'balance_sheet' in balance_sheet:
            for period, data in list(balance_sheet['balance_sheet'].items())[:2]:  # Last 2 periods
                if 'Total Assets' in data:
                    summary_parts.append(f"{period} Total Assets: ${data['Total Assets']:,}")
                if 'Total Liabilities Net Minority Interest' in data:
                    summary_parts.append(f"{period} Total Liabilities: ${data['Total Liabilities Net Minority Interest']:,}")
        
        return "\n".join(summary_parts) if summary_parts else "Limited financial data available"
    
    def _format_market_data(self, current_price_data: Dict) -> str:
        """Format market data for display."""
        if 'error' in current_price_data:
            return f"Error: {current_price_data['error']}"
        
        parts = []
        if current_price_data.get('current_price') != 'N/A':
            parts.append(f"Current Price: ${current_price_data['current_price']}")
        if current_price_data.get('previous_close') != 'N/A':
            parts.append(f"Previous Close: ${current_price_data['previous_close']}")
        if current_price_data.get('volume') != 'N/A':
            parts.append(f"Volume: {current_price_data['volume']:,}")
        
        return "\n".join(parts) if parts else "Market data unavailable"
    
    def _extract_metrics(self, llm_response: str) -> List[str]:
        """Extract key financial metrics from LLM response."""
        try:
            lines = llm_response.split('\n')
            metrics = []
            
            for line in lines:
                line = line.strip()
                if line.startswith(('-', '•', '*', '1.', '2.', '3.')):
                    metrics.append(line.lstrip('-•*1234567890. '))
                elif line and len(line) > 20 and not line.startswith('#'):
                    metrics.append(line)
            
            return metrics[:5]  # Return top 5 metrics
        except:
            return [llm_response[:200] + "..." if len(llm_response) > 200 else llm_response]
    
    def _assess_financial_health(self, income_statements: Dict, balance_sheet: Dict) -> str:
        """Assess overall financial health."""
        try:
            if 'income_statements' in income_statements and income_statements['income_statements']:
                # Check if company is profitable
                latest_income = list(income_statements['income_statements'].values())[0]
                if 'Net Income' in latest_income and latest_income['Net Income'] > 0:
                    return "Healthy - Profitable"
                elif 'Net Income' in latest_income and latest_income['Net Income'] < 0:
                    return "Concerning - Loss-making"
            
            return "Moderate - Limited data available"
        except:
            return "Unknown - Data analysis failed"
    
    def _analyze_growth_trends(self, income_statements: Dict) -> str:
        """Analyze growth trends from income statements."""
        try:
            if 'income_statements' in income_statements and len(income_statements['income_statements']) >= 2:
                periods = list(income_statements['income_statements'].keys())
                if len(periods) >= 2:
                    recent = income_statements['income_statements'][periods[0]]
                    previous = income_statements['income_statements'][periods[1]]
                    
                    if 'Total Revenue' in recent and 'Total Revenue' in previous:
                        if recent['Total Revenue'] > previous['Total Revenue']:
                            return "Growing - Revenue increasing"
                        else:
                            return "Declining - Revenue decreasing"
            
            return "Stable - Insufficient data for trend analysis"
        except:
            return "Unknown - Trend analysis failed"
    
    def _identify_risk_factors(self, current_price_data: Dict, income_statements: Dict) -> List[str]:
        """Identify potential risk factors."""
        risks = []
        
        # Check for data errors
        if 'error' in current_price_data:
            risks.append("Data retrieval issues")
        
        # Check for negative net income
        if 'income_statements' in income_statements:
            for period, data in income_statements['income_statements'].items():
                if 'Net Income' in data and data['Net Income'] < 0:
                    risks.append(f"Loss-making in {period}")
        
        return risks[:3] if risks else ["No significant risks identified"]
    
    def _identify_strengths(self, income_statements: Dict, balance_sheet: Dict) -> List[str]:
        """Identify company strengths."""
        strengths = []
        
        # Check for profitability
        if 'income_statements' in income_statements:
            for period, data in income_statements['income_statements'].items():
                if 'Net Income' in data and data['Net Income'] > 0:
                    strengths.append(f"Profitable in {period}")
        
        # Check for revenue growth
        if 'income_statements' in income_statements and len(income_statements['income_statements']) >= 2:
            periods = list(income_statements['income_statements'].keys())
            if len(periods) >= 2:
                recent = income_statements['income_statements'][periods[0]]
                previous = income_statements['income_statements'][periods[1]]
                if 'Total Revenue' in recent and 'Total Revenue' in previous:
                    if recent['Total Revenue'] > previous['Total Revenue']:
                        strengths.append("Revenue growth")
        
        return strengths[:3] if strengths else ["Limited strength indicators available"]
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()
