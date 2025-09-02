from typing import Dict, Any, TypedDict
from agents.data_agent import DataAgent
from config.logging_config import get_logger

logger = get_logger(__name__)

class FinancialsTaskState(TypedDict):
    """State for the financials task."""
    symbol: str
    financial_data: Dict[str, Any]
    error: str

class FinancialsTask:
    """Task node for gathering financial data and statements."""
    
    def __init__(self):
        self.agent = DataAgent()
    
    def execute(self, state: FinancialsTaskState) -> FinancialsTaskState:
        """
        Execute the financial data gathering task.
        
        Args:
            state: Current state containing symbol
            
        Returns:
            Updated state with financial data
        """
        try:
            symbol = state.get('symbol')
            
            logger.info(f"Financials Task: Starting execution for {symbol}")
            
            # Execute data agent
            financial_data = self.agent.gather_financial_data(symbol)
            
            # Update state
            state['financial_data'] = financial_data
            
            if 'error' in financial_data:
                state['error'] = financial_data['error']
                logger.error(f"Financials Task: Error for {symbol}: {financial_data['error']}")
            else:
                logger.info(f"Financials Task: Successfully completed for {symbol}")
            
            return state
            
        except Exception as e:
            error_msg = f"Financials Task failed: {str(e)}"
            logger.error(f"Financials Task: Exception for {state.get('symbol', 'unknown')}: {e}")
            state['error'] = error_msg
            return state
    
    def __call__(self, state: FinancialsTaskState) -> FinancialsTaskState:
        """Make the task callable for LangGraph."""
        return self.execute(state)
