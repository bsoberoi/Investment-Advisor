from typing import Dict, Any, TypedDict
from agents.analyst_agent import AnalystAgent
from config.logging_config import get_logger

logger = get_logger(__name__)

class AnalysisTaskState(TypedDict):
    """State for the analysis task."""
    symbol: str
    news_data: Dict[str, Any]
    financial_data: Dict[str, Any]
    analysis_data: Dict[str, Any]
    error: str

class AnalysisTask:
    """Task node for synthesizing news and financial data into comprehensive analysis."""
    
    def __init__(self):
        self.agent = AnalystAgent()
    
    def execute(self, state: AnalysisTaskState) -> AnalysisTaskState:
        """
        Execute the analysis synthesis task.
        
        Args:
            state: Current state containing news and financial data
            
        Returns:
            Updated state with analysis data
        """
        try:
            symbol = state.get('symbol')
            news_data = state.get('news_data', {})
            financial_data = state.get('financial_data', {})
            
            logger.info(f"Analysis Task: Starting execution for {symbol}")
            
            # Check if we have the required data
            if 'error' in news_data or 'error' in financial_data:
                error_msg = "Cannot perform analysis due to errors in previous tasks"
                logger.error(f"Analysis Task: Missing data for {symbol}")
                state['error'] = error_msg
                return state
            
            # Execute analyst agent
            analysis_data = self.agent.synthesize_analysis(symbol, news_data, financial_data)
            
            # Update state
            state['analysis_data'] = analysis_data
            
            if 'error' in analysis_data:
                state['error'] = analysis_data['error']
                logger.error(f"Analysis Task: Error for {symbol}: {analysis_data['error']}")
            else:
                logger.info(f"Analysis Task: Successfully completed for {symbol}")
            
            return state
            
        except Exception as e:
            error_msg = f"Analysis Task failed: {str(e)}"
            logger.error(f"Analysis Task: Exception for {state.get('symbol', 'unknown')}: {e}")
            state['error'] = error_msg
            return state
    
    def __call__(self, state: AnalysisTaskState) -> AnalysisTaskState:
        """Make the task callable for LangGraph."""
        return self.execute(state)
