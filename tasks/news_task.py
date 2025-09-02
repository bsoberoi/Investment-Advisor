from typing import Dict, Any, TypedDict
from agents.news_agent import NewsAgent
from config.logging_config import get_logger

logger = get_logger(__name__)

class NewsTaskState(TypedDict):
    """State for the news task."""
    symbol: str
    company_name: str
    news_data: Dict[str, Any]
    error: str

class NewsTask:
    """Task node for gathering company news and information."""
    
    def __init__(self):
        self.agent = NewsAgent()
    
    def execute(self, state: NewsTaskState) -> NewsTaskState:
        """
        Execute the news gathering task.
        
        Args:
            state: Current state containing symbol and company name
            
        Returns:
            Updated state with news data
        """
        try:
            symbol = state.get('symbol')
            company_name = state.get('company_name', symbol)
            
            logger.info(f"News Task: Starting execution for {symbol}")
            
            # Execute news agent
            news_data = self.agent.gather_company_news(symbol, company_name)
            
            # Update state
            state['news_data'] = news_data
            
            if 'error' in news_data:
                state['error'] = news_data['error']
                logger.error(f"News Task: Error for {symbol}: {news_data['error']}")
            else:
                logger.info(f"News Task: Successfully completed for {symbol}")
            
            return state
            
        except Exception as e:
            error_msg = f"News Task failed: {str(e)}"
            logger.error(f"News Task: Exception for {state.get('symbol', 'unknown')}: {e}")
            state['error'] = error_msg
            return state
    
    def __call__(self, state: NewsTaskState) -> NewsTaskState:
        """Make the task callable for LangGraph."""
        return self.execute(state)
