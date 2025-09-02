from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
from typing import Dict, List, Any
from tools.search_tool import SearchTool
from config.settings import settings
from config.logging_config import get_logger

logger = get_logger(__name__)

class NewsAgent:
    """Agent responsible for gathering company news and information."""
    
    def __init__(self):
        self.llm = ChatGroq(
            model=settings.GROQ_MODEL,
            temperature=settings.GROQ_TEMPERATURE,
            groq_api_key=settings.GROQ_API_KEY
        )
        self.search_tool = SearchTool()
        
        self.system_prompt = """You are a News & Information Research Agent specializing in financial markets.
Your role is to gather and synthesize relevant news and information about companies to support investment decisions.

Key responsibilities:
1. Search for recent news about companies
2. Identify important developments that could impact stock performance
3. Provide context and relevance of news items
4. Summarize key information in a structured format

Always provide factual, relevant information and avoid speculation."""
    
    def gather_company_news(self, symbol: str, company_name: str) -> Dict[str, Any]:
        """
        Gather comprehensive news and information about a company.
        
        Args:
            symbol: Stock symbol
            company_name: Company name
            
        Returns:
            Dictionary containing gathered news and information
        """
        try:
            logger.info(f"News Agent: Starting news gathering for {company_name} ({symbol})")
            
            # Search for company news
            news_articles = self.search_tool.search_company_news(company_name, symbol)
            
            # Search for company information
            company_info = self.search_tool.search_company_info(company_name)
            
            # Analyze and synthesize the gathered information
            analysis = self._analyze_news_and_info(symbol, company_name, news_articles, company_info)
            
            logger.info(f"News Agent: Completed news gathering for {company_name} ({symbol})")
            
            return {
                'symbol': symbol,
                'company_name': company_name,
                'news_articles': news_articles,
                'company_info': company_info,
                'analysis': analysis,
                'timestamp': analysis.get('timestamp', ''),
                'agent': 'NewsAgent'
            }
            
        except Exception as e:
            logger.error(f"News Agent: Error gathering news for {symbol}: {e}")
            return {
                'symbol': symbol,
                'company_name': company_name,
                'error': f"Failed to gather news: {str(e)}",
                'agent': 'NewsAgent'
            }
    
    def _analyze_news_and_info(self, symbol: str, company_name: str, 
                               news_articles: List[Dict], company_info: Dict) -> Dict[str, Any]:
        """
        Analyze gathered news and information using LLM.
        
        Args:
            symbol: Stock symbol
            company_name: Company name
            news_articles: List of news articles
            company_info: Company information
            
        Returns:
            Analysis results
        """
        try:
            # Prepare context for LLM analysis
            news_summary = "\n".join([
                f"- {article['title']}: {article['snippet']}" 
                for article in news_articles[:3]  # Top 3 most relevant
            ])
            
            company_overview = company_info.get('overview', 'No company information available.')
            
            prompt = f"""
Analyze the following information about {company_name} ({symbol}):

Company Overview:
{company_overview}

Recent News:
{news_summary}

Please provide:
1. Key news highlights and their potential impact
2. Company overview summary
3. Market sentiment indicators
4. Important developments to watch

Format your response as a structured analysis.
"""
            
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            
            return {
                'news_highlights': self._extract_highlights(response.content),
                'company_overview': company_overview,
                'market_sentiment': self._assess_sentiment(news_articles),
                'key_developments': self._identify_developments(news_articles),
                'timestamp': self._get_timestamp(),
                'llm_analysis': response.content
            }
            
        except Exception as e:
            logger.error(f"News Agent: Error analyzing news for {symbol}: {e}")
            return {
                'error': f"Failed to analyze news: {str(e)}",
                'timestamp': self._get_timestamp()
            }
    
    def _extract_highlights(self, llm_response: str) -> List[str]:
        """Extract key highlights from LLM response."""
        try:
            # Simple extraction - look for bullet points or numbered items
            lines = llm_response.split('\n')
            highlights = []
            
            for line in lines:
                line = line.strip()
                if line.startswith(('-', '•', '*', '1.', '2.', '3.')):
                    highlights.append(line.lstrip('-•*1234567890. '))
                elif line and len(line) > 20 and not line.startswith('#'):
                    highlights.append(line)
            
            return highlights[:5]  # Return top 5 highlights
        except:
            return [llm_response[:200] + "..." if len(llm_response) > 200 else llm_response]
    
    def _assess_sentiment(self, news_articles: List[Dict]) -> str:
        """Assess overall market sentiment based on news."""
        if not news_articles:
            return "Neutral"
        
        # Simple keyword-based sentiment analysis
        positive_keywords = ['positive', 'growth', 'profit', 'success', 'up', 'gain', 'strong']
        negative_keywords = ['negative', 'loss', 'decline', 'down', 'weak', 'risk', 'concern']
        
        positive_count = 0
        negative_count = 0
        
        for article in news_articles:
            text = (article.get('title', '') + ' ' + article.get('snippet', '')).lower()
            
            for keyword in positive_keywords:
                if keyword in text:
                    positive_count += 1
            
            for keyword in negative_keywords:
                if keyword in text:
                    negative_count += 1
        
        if positive_count > negative_count:
            return "Positive"
        elif negative_count > positive_count:
            return "Negative"
        else:
            return "Neutral"
    
    def _identify_developments(self, news_articles: List[Dict]) -> List[str]:
        """Identify key developments from news articles."""
        developments = []
        
        for article in news_articles[:3]:  # Top 3 articles
            title = article.get('title', '')
            if title and len(title) > 10:
                developments.append(title)
        
        return developments
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()
