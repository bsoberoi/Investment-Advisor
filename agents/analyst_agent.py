from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
from typing import Dict, List, Any
from config.settings import settings
from config.logging_config import get_logger

logger = get_logger(__name__)

class AnalystAgent:
    """Agent responsible for synthesizing news and financial data into comprehensive analysis."""
    
    def __init__(self):
        self.llm = ChatGroq(
            model=settings.GROQ_MODEL,
            temperature=settings.GROQ_TEMPERATURE,
            groq_api_key=settings.GROQ_API_KEY
        )
        
        self.system_prompt = """You are a Senior Financial Analyst specializing in comprehensive investment analysis.
Your role is to synthesize information from multiple sources to provide holistic investment insights.

Key responsibilities:
1. Integrate news, financial data, and market context
2. Identify correlations between news events and financial performance
3. Assess overall company positioning and market outlook
4. Provide balanced analysis considering multiple factors
5. Highlight key insights and potential catalysts

Always provide evidence-based analysis and acknowledge data limitations."""
    
    def synthesize_analysis(self, symbol: str, news_data: Dict, financial_data: Dict) -> Dict[str, Any]:
        """
        Synthesize news and financial data into comprehensive analysis.
        
        Args:
            symbol: Stock symbol
            news_data: Data from News Agent
            financial_data: Data from Data Agent
            
        Returns:
            Comprehensive analysis results
        """
        try:
            logger.info(f"Analyst Agent: Starting synthesis for {symbol}")
            
            # Prepare comprehensive analysis
            analysis = self._create_comprehensive_analysis(symbol, news_data, financial_data)
            
            logger.info(f"Analyst Agent: Completed synthesis for {symbol}")
            
            return {
                'symbol': symbol,
                'comprehensive_analysis': analysis,
                'timestamp': analysis.get('timestamp', ''),
                'agent': 'AnalystAgent'
            }
            
        except Exception as e:
            logger.error(f"Analyst Agent: Error synthesizing analysis for {symbol}: {e}")
            return {
                'symbol': symbol,
                'error': f"Failed to synthesize analysis: {str(e)}",
                'agent': 'AnalystAgent'
            }
    
    def _create_comprehensive_analysis(self, symbol: str, news_data: Dict, 
                                     financial_data: Dict) -> Dict[str, Any]:
        """
        Create comprehensive analysis using LLM.
        
        Args:
            symbol: Stock symbol
            news_data: News agent data
            financial_data: Financial data agent data
            
        Returns:
            Comprehensive analysis results
        """
        try:
            # Prepare context for LLM analysis
            context = self._prepare_analysis_context(news_data, financial_data)
            
            prompt = f"""
Create a comprehensive investment analysis for {symbol} based on the following information:

{context}

Please provide a structured analysis covering:

1. **Executive Summary**
   - Key highlights and overall assessment

2. **Company Overview**
   - Business model and market position
   - Sector and industry context

3. **Financial Analysis**
   - Key financial metrics and trends
   - Financial health assessment
   - Growth prospects and challenges

4. **News and Market Sentiment**
   - Recent developments and their impact
   - Market sentiment analysis
   - Key catalysts to watch

5. **Risk Assessment**
   - Primary risk factors
   - Market and company-specific risks
   - Risk mitigation factors

6. **Investment Thesis**
   - Bull case arguments
   - Bear case arguments
   - Neutral considerations

7. **Conclusion**
   - Overall investment outlook
   - Key factors driving the recommendation

Format your response as a professional investment analysis report.
"""
            
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            
            return {
                'executive_summary': self._extract_section(response.content, 'Executive Summary'),
                'company_overview': self._extract_section(response.content, 'Company Overview'),
                'financial_analysis': self._extract_section(response.content, 'Financial Analysis'),
                'news_sentiment': self._extract_section(response.content, 'News and Market Sentiment'),
                'risk_assessment': self._extract_section(response.content, 'Risk Assessment'),
                'investment_thesis': self._extract_section(response.content, 'Investment Thesis'),
                'conclusion': self._extract_section(response.content, 'Conclusion'),
                'key_insights': self._extract_key_insights(response.content),
                'correlation_analysis': self._analyze_correlations(news_data, financial_data),
                'timestamp': self._get_timestamp(),
                'full_analysis': response.content
            }
            
        except Exception as e:
            logger.error(f"Analyst Agent: Error creating comprehensive analysis for {symbol}: {e}")
            return {
                'error': f"Failed to create comprehensive analysis: {str(e)}",
                'timestamp': self._get_timestamp()
            }
    
    def _prepare_analysis_context(self, news_data: Dict, financial_data: Dict) -> str:
        """Prepare context information for LLM analysis."""
        context_parts = []
        
        # News context
        if 'analysis' in news_data:
            news_analysis = news_data['analysis']
            context_parts.append("NEWS AND MARKET CONTEXT:")
            context_parts.append(f"- Market Sentiment: {news_analysis.get('market_sentiment', 'N/A')}")
            context_parts.append(f"- Key Developments: {', '.join(news_analysis.get('key_developments', ['None']))}")
            if 'news_highlights' in news_analysis:
                context_parts.append(f"- News Highlights: {', '.join(news_analysis['news_highlights'][:3])}")
        
        # Financial context
        if 'analysis' in financial_data:
            fin_analysis = financial_data['analysis']
            context_parts.append("\nFINANCIAL CONTEXT:")
            context_parts.append(f"- Financial Health: {fin_analysis.get('health_assessment', 'N/A')}")
            context_parts.append(f"- Growth Trends: {fin_analysis.get('growth_trends', 'N/A')}")
            if 'financial_metrics' in fin_analysis:
                context_parts.append(f"- Key Metrics: {', '.join(fin_analysis['financial_metrics'][:3])}")
        
        # Company info
        if 'company_info' in financial_data:
            company_info = financial_data['company_info']
            context_parts.append(f"\nCOMPANY INFORMATION:")
            context_parts.append(f"- Company: {company_info.get('company_name', 'N/A')}")
            context_parts.append(f"- Sector: {company_info.get('sector', 'N/A')}")
            context_parts.append(f"- Industry: {company_info.get('industry', 'N/A')}")
        
        return "\n".join(context_parts)
    
    def _extract_section(self, content: str, section_name: str) -> str:
        """Extract a specific section from the LLM response."""
        try:
            lines = content.split('\n')
            section_content = []
            in_section = False
            
            for line in lines:
                if section_name.lower() in line.lower() and ('#' in line or line.strip().endswith(':')):
                    in_section = True
                    continue
                elif in_section and line.strip() and (line.startswith('#') or 
                      any(other_section in line.lower() for other_section in 
                          ['executive summary', 'company overview', 'financial analysis', 
                           'news and market sentiment', 'risk assessment', 'investment thesis', 'conclusion'])):
                    break
                elif in_section:
                    section_content.append(line)
            
            # Return the section content if found, otherwise return empty string to avoid "not found" messages
            return '\n'.join(section_content).strip() if section_content else ""
        except:
            return ""
    
    def _extract_key_insights(self, content: str) -> List[str]:
        """Extract key insights from the analysis."""
        try:
            lines = content.split('\n')
            insights = []
            
            # Look for key insights in various formats
            for line in lines:
                line = line.strip()
                if (line.startswith(('-', '•', '*', '→', '▶')) and len(line) > 10):
                    insights.append(line.lstrip('-•*→▶ '))
                elif (line.startswith(('Key', 'Important', 'Critical', 'Notable')) and len(line) > 20):
                    insights.append(line)
                elif (line.endswith('.') and len(line) > 30 and 
                      any(keyword in line.lower() for keyword in ['key', 'important', 'critical', 'notable'])):
                    insights.append(line)
            
            return insights[:5] if insights else ["Key insights analysis completed"]
        except:
            return ["Key insights extraction completed"]
    
    def _analyze_correlations(self, news_data: Dict, financial_data: Dict) -> Dict[str, Any]:
        """Analyze correlations between news and financial data."""
        correlations = {}
        
        try:
            # News sentiment vs financial health
            if 'analysis' in news_data and 'analysis' in financial_data:
                news_sentiment = news_data['analysis'].get('market_sentiment', 'Neutral')
                financial_health = financial_data['analysis'].get('health_assessment', 'Unknown')
                
                correlations['sentiment_health_alignment'] = self._assess_alignment(
                    news_sentiment, financial_health
                )
            
            # News developments vs financial trends
            if 'analysis' in news_data and 'analysis' in financial_data:
                growth_trends = financial_data['analysis'].get('growth_trends', 'Unknown')
                key_developments = news_data['analysis'].get('key_developments', [])
                
                correlations['developments_trends_alignment'] = self._assess_developments_trends_alignment(
                    key_developments, growth_trends
                )
            
            return correlations
            
        except Exception as e:
            logger.error(f"Error analyzing correlations: {e}")
            return {'error': f"Correlation analysis failed: {str(e)}"}
    
    def _assess_alignment(self, sentiment: str, health: str) -> str:
        """Assess alignment between news sentiment and financial health."""
        if sentiment == "Positive" and "Healthy" in health:
            return "Strong alignment - Positive news supports strong fundamentals"
        elif sentiment == "Negative" and "Concerning" in health:
            return "Strong alignment - Negative news aligns with weak fundamentals"
        elif sentiment == "Positive" and "Concerning" in health:
            return "Divergence - Positive news despite weak fundamentals"
        elif sentiment == "Negative" and "Healthy" in health:
            return "Divergence - Negative news despite strong fundamentals"
        else:
            return "Mixed alignment - Inconclusive correlation"
    
    def _assess_developments_trends_alignment(self, developments: List[str], trends: str) -> str:
        """Assess alignment between news developments and financial trends."""
        if not developments:
            return "No developments to correlate"
        
        # Simple keyword-based correlation
        positive_dev_keywords = ['growth', 'expansion', 'profit', 'success', 'positive']
        negative_dev_keywords = ['decline', 'loss', 'risk', 'concern', 'negative']
        
        positive_count = sum(1 for dev in developments 
                           if any(keyword in dev.lower() for keyword in positive_dev_keywords))
        negative_count = sum(1 for dev in developments 
                           if any(keyword in dev.lower() for keyword in negative_dev_keywords))
        
        if "Growing" in trends and positive_count > negative_count:
            return "Strong alignment - Positive developments support growth trends"
        elif "Declining" in trends and negative_count > positive_count:
            return "Strong alignment - Negative developments align with declining trends"
        elif "Growing" in trends and negative_count > positive_count:
            return "Divergence - Negative developments despite growth trends"
        elif "Declining" in trends and positive_count > negative_count:
            return "Divergence - Positive developments despite declining trends"
        else:
            return "Mixed alignment - Inconclusive correlation"
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()
