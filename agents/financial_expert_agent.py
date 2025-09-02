from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
from typing import Dict, List, Any
from config.settings import settings
from config.logging_config import get_logger

logger = get_logger(__name__)

class FinancialExpertAgent:
    """Agent responsible for generating final investment recommendations."""
    
    def __init__(self):
        self.llm = ChatGroq(
            model=settings.GROQ_MODEL,
            temperature=settings.GROQ_TEMPERATURE,
            groq_api_key=settings.GROQ_API_KEY
        )
        
        self.system_prompt = """You are a Senior Financial Expert and Investment Advisor with decades of experience.
Your role is to provide final investment recommendations based on comprehensive analysis.

Key responsibilities:
1. Evaluate all available information to make informed recommendations
2. Provide clear Buy/Hold/Sell recommendations with confidence levels
3. Explain the reasoning behind recommendations in simple terms
4. Highlight key risks and opportunities
5. Suggest investment strategies and time horizons

Always provide balanced, evidence-based recommendations and acknowledge uncertainty."""
    
    def generate_recommendation(self, symbol: str, news_data: Dict, 
                              financial_data: Dict, analysis_data: Dict) -> Dict[str, Any]:
        """
        Generate final investment recommendation based on all gathered data.
        
        Args:
            symbol: Stock symbol
            news_data: Data from News Agent
            financial_data: Data from Data Agent
            analysis_data: Data from Analyst Agent
            
        Returns:
            Investment recommendation results
        """
        try:
            logger.info(f"Financial Expert Agent: Starting recommendation generation for {symbol}")
            
            # Generate comprehensive recommendation
            recommendation = self._create_investment_recommendation(
                symbol, news_data, financial_data, analysis_data
            )
            
            logger.info(f"Financial Expert Agent: Completed recommendation for {symbol}")
            
            return {
                'symbol': symbol,
                'investment_recommendation': recommendation,
                'timestamp': recommendation.get('timestamp', ''),
                'agent': 'FinancialExpertAgent'
            }
            
        except Exception as e:
            logger.error(f"Financial Expert Agent: Error generating recommendation for {symbol}: {e}")
            return {
                'symbol': symbol,
                'error': f"Failed to generate recommendation: {str(e)}",
                'agent': 'FinancialExpertAgent'
            }
    
    def _create_investment_recommendation(self, symbol: str, news_data: Dict, 
                                        financial_data: Dict, analysis_data: Dict) -> Dict[str, Any]:
        """
        Create comprehensive investment recommendation using LLM.
        
        Args:
            symbol: Stock symbol
            news_data: News agent data
            financial_data: Financial data agent data
            analysis_data: Analyst agent data
            
        Returns:
            Investment recommendation results
        """
        try:
            # Prepare comprehensive context for LLM
            context = self._prepare_recommendation_context(
                symbol, news_data, financial_data, analysis_data
            )
            
            prompt = f"""
Based on the comprehensive analysis of {symbol}, provide a final investment recommendation.

{context}

Please provide a structured investment recommendation covering:

1. **RECOMMENDATION: BUY/HOLD/SELL**
   - Clear recommendation with confidence level (High/Medium/Low)
   - Target price range (if applicable)
   - Investment time horizon

2. **Reasoning**
   - Key factors supporting the recommendation
   - Primary drivers of the decision
   - How news and financial data align

3. **Risk Assessment**
   - Primary risks to the recommendation
   - Risk mitigation strategies
   - What could change the recommendation

4. **Investment Strategy**
   - Suggested entry/exit points
   - Position sizing considerations
   - Portfolio fit and diversification

5. **Monitoring Points**
   - Key metrics to watch
   - Events that could impact the recommendation
   - Review timeline

6. **Alternative Scenarios**
   - Bull case outcome
   - Bear case outcome
   - Base case expectations

Format your response as a professional investment recommendation.
"""
            
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            
            return {
                'recommendation': self._extract_recommendation(response.content),
                'reasoning': self._extract_section(response.content, 'Reasoning'),
                'risk_assessment': self._extract_section(response.content, 'Risk Assessment'),
                'investment_strategy': self._extract_section(response.content, 'Investment Strategy'),
                'monitoring_points': self._extract_section(response.content, 'Monitoring Points'),
                'alternative_scenarios': self._extract_section(response.content, 'Alternative Scenarios'),
                'confidence_level': self._extract_confidence_level(response.content),
                'target_price': self._extract_target_price(response.content),
                'time_horizon': self._extract_time_horizon(response.content),
                'key_factors': self._extract_key_factors(response.content),
                'timestamp': self._get_timestamp(),
                'full_recommendation': response.content
            }
            
        except Exception as e:
            logger.error(f"Financial Expert Agent: Error creating recommendation for {symbol}: {e}")
            return {
                'error': f"Failed to create recommendation: {str(e)}",
                'timestamp': self._get_timestamp()
            }
    
    def _prepare_recommendation_context(self, symbol: str, news_data: Dict, 
                                      financial_data: Dict, analysis_data: Dict) -> str:
        """Prepare comprehensive context for recommendation generation."""
        context_parts = []
        
        # Company overview
        if 'company_info' in financial_data:
            company_info = financial_data['company_info']
            context_parts.append(f"COMPANY: {company_info.get('company_name', 'N/A')} ({symbol})")
            context_parts.append(f"SECTOR: {company_info.get('sector', 'N/A')}")
            context_parts.append(f"INDUSTRY: {company_info.get('industry', 'N/A')}")
        
        # Current market data
        if 'current_price_data' in financial_data:
            price_data = financial_data['current_price_data']
            if 'current_price' in price_data and price_data['current_price'] != 'N/A':
                context_parts.append(f"CURRENT PRICE: ${price_data['current_price']}")
            if 'market_cap' in price_data and price_data['market_cap'] != 'N/A':
                context_parts.append(f"MARKET CAP: ${price_data['market_cap']:,}")
        
        # News sentiment
        if 'analysis' in news_data:
            news_analysis = news_data['analysis']
            context_parts.append(f"NEWS SENTIMENT: {news_analysis.get('market_sentiment', 'N/A')}")
            if 'key_developments' in news_analysis:
                context_parts.append(f"KEY DEVELOPMENTS: {', '.join(news_analysis['key_developments'][:3])}")
        
        # Financial health
        if 'analysis' in financial_data:
            fin_analysis = financial_data['analysis']
            context_parts.append(f"FINANCIAL HEALTH: {fin_analysis.get('health_assessment', 'N/A')}")
            context_parts.append(f"GROWTH TRENDS: {fin_analysis.get('growth_trends', 'N/A')}")
        
        # Comprehensive analysis
        if 'comprehensive_analysis' in analysis_data:
            comp_analysis = analysis_data['comprehensive_analysis']
            if 'executive_summary' in comp_analysis:
                context_parts.append(f"EXECUTIVE SUMMARY: {comp_analysis['executive_summary'][:200]}...")
            if 'key_insights' in comp_analysis:
                context_parts.append(f"KEY INSIGHTS: {', '.join(comp_analysis['key_insights'][:3])}")
        
        return "\n".join(context_parts)
    
    def _extract_recommendation(self, content: str) -> str:
        """Extract the main recommendation (BUY/HOLD/SELL)."""
        try:
            lines = content.split('\n')
            
            # Look for the actual recommendation in the LLM response
            # Skip template text and look for the real recommendation
            for line in lines:
                line_lower = line.lower().strip()
                
                # Skip template lines
                if 'buy/hold/sell' in line_lower or 'recommendation:' in line_lower and 'buy/hold/sell' in line_lower:
                    continue
                
                # Look for actual recommendation statements
                if any(phrase in line_lower for phrase in [
                    'we recommend a buy', 'recommend a buy', 'recommendation: buy',
                    'we recommend a sell', 'recommend a sell', 'recommendation: sell', 
                    'we recommend a hold', 'recommend a hold', 'recommendation: hold'
                ]):
                    if 'buy' in line_lower:
                        return "BUY"
                    elif 'sell' in line_lower:
                        return "SELL"
                    elif 'hold' in line_lower:
                        return "HOLD"
                
                # Look for bold recommendation statements
                if '**' in line and any(word in line_lower for word in ['buy', 'sell', 'hold']):
                    if 'buy' in line_lower and 'sell' not in line_lower and 'hold' not in line_lower:
                        return "BUY"
                    elif 'sell' in line_lower and 'buy' not in line_lower and 'hold' not in line_lower:
                        return "SELL"
                    elif 'hold' in line_lower and 'buy' not in line_lower and 'sell' not in line_lower:
                        return "HOLD"
            
            # Fallback: look for the most specific recommendation
            content_lower = content.lower()
            if 'we recommend a buy' in content_lower or 'recommend a buy' in content_lower:
                return "BUY"
            elif 'we recommend a sell' in content_lower or 'recommend a sell' in content_lower:
                return "SELL"
            elif 'we recommend a hold' in content_lower or 'recommend a hold' in content_lower:
                return "HOLD"
            
            # Final fallback: look for any clear recommendation
            if 'buy' in content_lower and 'sell' not in content_lower and 'hold' not in content_lower:
                return "BUY"
            elif 'sell' in content_lower and 'buy' not in content_lower and 'hold' not in content_lower:
                return "SELL"
            elif 'hold' in content_lower and 'buy' not in content_lower and 'sell' not in content_lower:
                return "HOLD"
            
            return "HOLD"  # Default to HOLD if unclear
        except:
            return "HOLD"
    
    def _extract_confidence_level(self, content: str) -> str:
        """Extract confidence level from the recommendation."""
        try:
            content_lower = content.lower()
            
            if 'high confidence' in content_lower or 'high confidence level' in content_lower:
                return "High"
            elif 'medium confidence' in content_lower or 'medium confidence level' in content_lower:
                return "Medium"
            elif 'low confidence' in content_lower or 'low confidence level' in content_lower:
                return "Low"
            else:
                # Look for confidence indicators
                if any(phrase in content_lower for phrase in ['very confident', 'strong conviction']):
                    return "High"
                elif any(phrase in content_lower for phrase in ['moderate confidence', 'some confidence']):
                    return "Medium"
                else:
                    return "Medium"  # Default
        except:
            return "Medium"
    
    def _extract_target_price(self, content: str) -> str:
        """Extract target price from the recommendation."""
        try:
            import re
            # Look for price patterns like $150, $150-200, etc.
            price_patterns = re.findall(r'\$\d+(?:\.\d+)?(?:\s*-\s*\$\d+(?:\.\d+)?)?', content)
            if price_patterns:
                return price_patterns[0]
            
            # Look for "target price" mentions
            lines = content.split('\n')
            for line in lines:
                if 'target' in line.lower() and 'price' in line.lower():
                    price_match = re.search(r'\$\d+(?:\.\d+)?(?:\s*-\s*\$\d+(?:\.\d+)?)?', line)
                    if price_match:
                        return price_match.group()
            
            return "Not specified"
        except:
            return "Not specified"
    
    def _extract_time_horizon(self, content: str) -> str:
        """Extract investment time horizon from the recommendation."""
        try:
            content_lower = content.lower()
            
            if any(phrase in content_lower for phrase in ['short term', 'short-term', '3-6 months', '6 months']):
                return "Short-term (3-6 months)"
            elif any(phrase in content_lower for phrase in ['medium term', 'medium-term', '6-12 months', '1 year']):
                return "Medium-term (6-12 months)"
            elif any(phrase in content_lower for phrase in ['long term', 'long-term', '1+ years', '2+ years']):
                return "Long-term (1+ years)"
            else:
                return "Not specified"
        except:
            return "Not specified"
    
    def _extract_key_factors(self, content: str) -> List[str]:
        """Extract key factors supporting the recommendation."""
        try:
            lines = content.split('\n')
            factors = []
            
            for line in lines:
                line = line.strip()
                line_lower = line.lower()
                
                # Skip template text and malformed lines
                if any(template in line_lower for template in [
                    'buy/hold/sell', 'recommendation:', 'target price range:', 
                    'investment time horizon:', 'reasoning', 'risk assessment',
                    'investment strategy', 'monitoring points', 'alternative scenarios'
                ]):
                    continue
                
                # Skip lines with template formatting issues
                if line.endswith('**') or line.startswith('**') and ':' in line:
                    continue
                
                # Extract actual factors
                if (line.startswith(('-', '•', '*', '→', '▶')) and len(line) > 10):
                    factor = line.lstrip('-•*→▶ ').strip()
                    if factor and not any(template in factor.lower() for template in ['buy/hold/sell', 'recommendation:']):
                        factors.append(factor)
                elif (line.startswith(('Key', 'Primary', 'Main', 'Factor')) and len(line) > 20):
                    if not any(template in line_lower for template in ['buy/hold/sell', 'recommendation:']):
                        factors.append(line)
                elif (line.endswith('.') and len(line) > 30 and 
                      any(keyword in line_lower for keyword in ['key', 'primary', 'main', 'factor'])):
                    if not any(template in line_lower for template in ['buy/hold/sell', 'recommendation:']):
                        factors.append(line)
            
            return factors[:5] if factors else []
        except:
            return []
    
    def _extract_section(self, content: str, section_name: str) -> str:
        """Extract a specific section from the LLM response."""
        try:
            lines = content.split('\n')
            section_content = []
            in_section = False
            
            for line in lines:
                # Check if this line starts a new section
                if section_name.lower() in line.lower() and ('#' in line or line.strip().endswith(':')):
                    in_section = True
                    continue
                elif in_section and line.strip() and (line.startswith('#') or 
                      any(other_section in line.lower() for other_section in 
                          ['recommendation', 'reasoning', 'risk assessment', 'investment strategy', 
                           'monitoring points', 'alternative scenarios'])):
                    break
                elif in_section:
                    section_content.append(line)
            
            # Return the section content if found, otherwise return empty string to avoid "not found" messages
            return '\n'.join(section_content).strip() if section_content else ""
        except:
            return ""
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()
