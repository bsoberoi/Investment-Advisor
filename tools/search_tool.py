try:
    # New package name
    from ddgs import DDGS
except ImportError:
    # Fallback to old name if present
    from duckduckgo_search import DDGS
from typing import List, Dict, Optional
from config.settings import settings
from config.logging_config import get_logger

logger = get_logger(__name__)

class SearchTool:
    """Tool for searching company news and information using DuckDuckGo."""
    
    def __init__(self):
        self.ddgs = DDGS()
        self.max_results = settings.DUCKDUCKGO_MAX_RESULTS
    
    def search_company_news(self, company_name: str, symbol: str) -> List[Dict[str, str]]:
        """
        Search for recent news about a company.
        
        Args:
            company_name: Name of the company
            symbol: Stock symbol
            
        Returns:
            List of news articles with title, link, and snippet
        """
        try:
            # Search for recent company news
            query = f"{company_name} {symbol} stock news latest"
            results = self.ddgs.text(query, max_results=self.max_results)
            
            news_articles = []
            for result in results:
                news_articles.append({
                    'title': result.get('title', ''),
                    'link': result.get('link', ''),
                    'snippet': result.get('body', ''),
                    'source': self._extract_source(result.get('link', ''))
                })
            
            logger.info(f"Found {len(news_articles)} news articles for {company_name} ({symbol})")
            return news_articles
            
        except Exception as e:
            logger.error(f"Error searching for company news: {e}")
            return []
    
    def search_company_info(self, company_name: str) -> Dict[str, str]:
        """
        Search for general company information.
        
        Args:
            company_name: Name of the company
            
        Returns:
            Dictionary with company information
        """
        try:
            query = f"{company_name} company overview business description"
            results = self.ddgs.text(query, max_results=3)
            
            if results:
                # Combine snippets for comprehensive info
                combined_info = " ".join([result.get('body', '') for result in results])
                return {
                    'overview': combined_info[:500] + "..." if len(combined_info) > 500 else combined_info,
                    'source': 'DuckDuckGo Search'
                }
            
            return {'overview': 'No company information found.', 'source': 'DuckDuckGo Search'}
            
        except Exception as e:
            logger.error(f"Error searching for company info: {e}")
            return {'overview': 'Error retrieving company information.', 'source': 'DuckDuckGo Search'}
    
    def _extract_source(self, url: str) -> str:
        """Extract domain name from URL as source."""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            return parsed.netloc
        except:
            return "Unknown"
