from typing import Dict, Any, TypedDict
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from tasks.news_task import NewsTask, NewsTaskState
from tasks.financials_task import FinancialsTask, FinancialsTaskState
from tasks.analysis_task import AnalysisTask, AnalysisTaskState
from tasks.recommendation_task import RecommendationTask, RecommendationTaskState
from config.logging_config import get_logger

logger = get_logger(__name__)

class InvestmentGraphState(TypedDict):
    """Complete state for the investment analysis workflow."""
    symbol: str
    company_name: str
    news_data: Dict[str, Any]
    financial_data: Dict[str, Any]
    analysis_data: Dict[str, Any]
    recommendation_data: Dict[str, Any]
    error: str
    execution_path: list

class InvestmentGraph:
    """LangGraph workflow for investment analysis."""
    
    def __init__(self):
        # Initialize memory before building workflow (used by compile)
        self.memory = MemorySaver()
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow."""
        
        # Create the workflow
        workflow = StateGraph(InvestmentGraphState)
        
        # Add nodes
        workflow.add_node("news_task", NewsTask())
        workflow.add_node("financials_task", FinancialsTask())
        workflow.add_node("analysis_task", AnalysisTask())
        workflow.add_node("recommendation_task", RecommendationTask())
        
        # Set entry point
        workflow.set_entry_point("news_task")
        
        # Add edges - sequential workflow
        workflow.add_edge("news_task", "financials_task")
        workflow.add_edge("financials_task", "analysis_task")
        workflow.add_edge("analysis_task", "recommendation_task")
        workflow.add_edge("recommendation_task", END)
        
        # Compile the workflow without checkpointer to avoid msgpack serialization issues
        return workflow.compile()
    
    def execute(self, symbol: str, company_name: str = None) -> Dict[str, Any]:
        """
        Execute the complete investment analysis workflow.
        
        Args:
            symbol: Stock symbol to analyze
            company_name: Optional company name (defaults to symbol)
            
        Returns:
            Complete analysis results
        """
        try:
            logger.info(f"Investment Graph: Starting workflow for {symbol}")
            
            # Initialize state
            initial_state = {
                "symbol": symbol,
                "company_name": company_name or symbol,
                "news_data": {},
                "financial_data": {},
                "analysis_data": {},
                "recommendation_data": {},
                "error": "",
                "execution_path": []
            }
            
            # Execute workflow and return final state
            config = {"configurable": {"thread_id": f"thread_{symbol}_{hash(symbol)}"}}
            final_state: Dict[str, Any] = self.workflow.invoke(initial_state, config)
            
            logger.info(f"Investment Graph: Workflow completed for {symbol}")
            
            return final_state
            
        except Exception as e:
            logger.error(f"Investment Graph: Workflow failed for {symbol}: {e}")
            return {
                "symbol": symbol,
                "error": f"Workflow execution failed: {str(e)}",
                "execution_path": []
            }
    
    def get_execution_summary(self, symbol: str) -> Dict[str, Any]:
        """
        Get execution summary for a specific symbol.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Execution summary
        """
        try:
            config = {"configurable": {"thread_id": f"thread_{symbol}_{hash(symbol)}"}}
            state = self.workflow.get_state(config)
            
            if state:
                return {
                    "symbol": symbol,
                    "completed_tasks": state.values[0].get("execution_path", []),
                    "has_error": bool(state.values[0].get("error")),
                    "error": state.values[0].get("error", ""),
                    "timestamp": state.values[0].get("timestamp", "")
                }
            else:
                return {
                    "symbol": symbol,
                    "status": "No execution found"
                }
                
        except Exception as e:
            logger.error(f"Investment Graph: Error getting execution summary for {symbol}: {e}")
            return {
                "symbol": symbol,
                "error": f"Failed to get execution summary: {str(e)}"
            }
