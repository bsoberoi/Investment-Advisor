from typing import Dict, Any, TypedDict
from agents.financial_expert_agent import FinancialExpertAgent
from config.logging_config import get_logger

logger = get_logger(__name__)

class RecommendationTaskState(TypedDict):
    """State for the recommendation task."""
    symbol: str
    news_data: Dict[str, Any]
    financial_data: Dict[str, Any]
    analysis_data: Dict[str, Any]
    recommendation_data: Dict[str, Any]
    error: str

class RecommendationTask:
    """Task node for generating final investment recommendations."""
    
    def __init__(self):
        self.agent = FinancialExpertAgent()
    
    def execute(self, state: RecommendationTaskState) -> RecommendationTaskState:
        """
        Execute the recommendation generation task.
        
        Args:
            state: Current state containing all gathered data
            
        Returns:
            Updated state with recommendation data
        """
        try:
            symbol = state.get('symbol')
            news_data = state.get('news_data', {})
            financial_data = state.get('financial_data', {})
            analysis_data = state.get('analysis_data', {})
            
            logger.info(f"Recommendation Task: Starting execution for {symbol}")
            
            # Check if we have the required data
            if any('error' in data for data in [news_data, financial_data, analysis_data]):
                error_msg = "Cannot generate recommendation due to errors in previous tasks"
                logger.error(f"Recommendation Task: Missing data for {symbol}")
                state['error'] = error_msg
                return state
            
            # Execute financial expert agent
            recommendation_data = self.agent.generate_recommendation(
                symbol, news_data, financial_data, analysis_data
            )
            
            # Update state
            state['recommendation_data'] = recommendation_data
            
            if 'error' in recommendation_data:
                state['error'] = recommendation_data['error']
                logger.error(f"Recommendation Task: Error for {symbol}: {recommendation_data['error']}")
            else:
                logger.info(f"Recommendation Task: Successfully completed for {symbol}")
            
            return state
            
        except Exception as e:
            error_msg = f"Recommendation Task failed: {str(e)}"
            logger.error(f"Recommendation Task: Exception for {state.get('symbol', 'unknown')}: {e}")
            state['error'] = error_msg
            return state
    
    def __call__(self, state: RecommendationTaskState) -> RecommendationTaskState:
        """Make the task callable for LangGraph."""
        return self.execute(state)
