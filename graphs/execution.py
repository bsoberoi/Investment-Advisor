from typing import Dict, Any, Optional
from datetime import datetime
import os
from graphs.investment_graph import InvestmentGraph
from config.settings import settings
from config.logging_config import get_logger

logger = get_logger(__name__)

class GraphExecutor:
    """Executor for running and monitoring LangGraph workflows."""
    
    def __init__(self):
        self.graph = InvestmentGraph()
        self.settings = settings
        
        # Ensure output directories exist
        self.settings.create_directories()
    
    def run_analysis(self, symbol: str, company_name: str = None) -> Dict[str, Any]:
        """
        Run complete investment analysis for a stock symbol.
        
        Args:
            symbol: Stock symbol to analyze
            company_name: Optional company name
            
        Returns:
            Analysis results and generated files
        """
        try:
            start_time = datetime.now()
            logger.info(f"Graph Executor: Starting analysis for {symbol}")
            
            # Execute the workflow
            results = self.graph.execute(symbol, company_name)
            
            # Generate output files
            output_files = self._generate_output_files(symbol, results)
            
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            
            logger.info(f"Graph Executor: Analysis completed for {symbol} in {execution_time:.2f} seconds")
            
            return {
                "symbol": symbol,
                "results": results,
                "output_files": output_files,
                "execution_time": execution_time,
                "timestamp": end_time.isoformat(),
                "success": "error" not in results or not results["error"]
            }
            
        except Exception as e:
            logger.error(f"Graph Executor: Analysis failed for {symbol}: {e}")
            return {
                "symbol": symbol,
                "error": f"Analysis execution failed: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "success": False
            }
    
    def _generate_output_files(self, symbol: str, results: Dict[str, Any]) -> Dict[str, str]:
        """
        Generate output files from analysis results.
        
        Args:
            symbol: Stock symbol
            results: Analysis results
            
        Returns:
            Dictionary of generated file paths
        """
        output_files = {}
        
        try:
            # Generate Analysis.md
            analysis_file = self._generate_analysis_file(symbol, results)
            if analysis_file:
                output_files['analysis'] = analysis_file
            
            # Generate Recommendation.md
            recommendation_file = self._generate_recommendation_file(symbol, results)
            if recommendation_file:
                output_files['recommendation'] = recommendation_file
                
        except Exception as e:
            logger.error(f"Graph Executor: Error generating output files for {symbol}: {e}")
        
        return output_files
    
    def _generate_analysis_file(self, symbol: str, results: Dict[str, Any]) -> Optional[str]:
        """Generate Analysis.md file."""
        try:
            if 'error' in results and results['error']:
                return None
            
            analysis_content = self._format_analysis_content(symbol, results)
            
            # Create filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{symbol}_Analysis_{timestamp}.md"
            filepath = os.path.join(self.settings.ANALYSIS_DIR, filename)
            
            # Write file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(analysis_content)
            
            logger.info(f"Graph Executor: Generated analysis file: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Graph Executor: Error generating analysis file for {symbol}: {e}")
            return None
    
    def _generate_recommendation_file(self, symbol: str, results: Dict[str, Any]) -> Optional[str]:
        """Generate Recommendation.md file."""
        try:
            if 'error' in results and results['error']:
                return None
            
            recommendation_content = self._format_recommendation_content(symbol, results)
            
            # Create filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{symbol}_Recommendation_{timestamp}.md"
            filepath = os.path.join(self.settings.RECOMMENDATION_DIR, filename)
            
            # Write file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(recommendation_content)
            
            logger.info(f"Graph Executor: Generated recommendation file: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Graph Executor: Error generating recommendation file for {symbol}: {e}")
            return None
    
    def _format_analysis_content(self, symbol: str, results: Dict[str, Any]) -> str:
        """Format content for Analysis.md file."""
        content = []
        content.append(f"# Investment Analysis Report: {symbol}")
        content.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        content.append("")
        
        # Company Information
        if 'financial_data' in results and 'company_info' in results['financial_data']:
            company_info = results['financial_data']['company_info']
            content.append("## Company Information")
            content.append(f"- **Company Name**: {company_info.get('company_name', 'N/A')}")
            content.append(f"- **Sector**: {company_info.get('sector', 'N/A')}")
            content.append(f"- **Industry**: {company_info.get('industry', 'N/A')}")
            content.append(f"- **Country**: {company_info.get('country', 'N/A')}")
            content.append("")
        
        # Current Market Data
        if 'financial_data' in results and 'current_price_data' in results['financial_data']:
            price_data = results['financial_data']['current_price_data']
            content.append("## Current Market Data")
            content.append(f"- **Current Price**: ${price_data.get('current_price', 'N/A')}")
            content.append(f"- **Market Cap**: ${price_data.get('market_cap', 'N/A'):,}" if price_data.get('market_cap') != 'N/A' else "- **Market Cap**: N/A")
            content.append(f"- **Volume**: {price_data.get('volume', 'N/A'):,}" if price_data.get('volume') != 'N/A' else "- **Volume**: N/A")
            content.append("")
        
        # News Analysis
        if 'news_data' in results and 'analysis' in results['news_data']:
            news_analysis = results['news_data']['analysis']
            content.append("## News and Market Sentiment")
            content.append(f"- **Market Sentiment**: {news_analysis.get('market_sentiment', 'N/A')}")
            content.append(f"- **Key Developments**:")
            for dev in news_analysis.get('key_developments', []):
                content.append(f"  - {dev}")
            content.append("")
        
        # Financial Analysis
        if 'financial_data' in results and 'analysis' in results['financial_data']:
            fin_analysis = results['financial_data']['analysis']
            content.append("## Financial Analysis")
            content.append(f"- **Financial Health**: {fin_analysis.get('health_assessment', 'N/A')}")
            content.append(f"- **Growth Trends**: {fin_analysis.get('growth_trends', 'N/A')}")
            content.append(f"- **Key Metrics**:")
            for metric in fin_analysis.get('financial_metrics', []):
                content.append(f"  - {metric}")
            content.append("")
        
        # Comprehensive Analysis
        if 'analysis_data' in results and 'comprehensive_analysis' in results['analysis_data']:
            comp_analysis = results['analysis_data']['comprehensive_analysis']
            content.append("## Comprehensive Analysis")
            
            if comp_analysis.get('executive_summary'):
                content.append("### Executive Summary")
                content.append(str(comp_analysis['executive_summary']))
                content.append("")
            
            if comp_analysis.get('key_insights'):
                content.append("### Key Insights")
                for insight in comp_analysis['key_insights']:
                    content.append(f"- {insight}")
                content.append("")
            
            # Fallback: include full LLM analysis text if present
            if comp_analysis.get('full_analysis'):
                content.append("### Full Analysis (LLM)")
                content.append(comp_analysis['full_analysis'])
                content.append("")
        
        # Fallbacks: include raw LLM outputs from earlier agents if sections were empty
        if ('news_data' in results and results['news_data'].get('analysis') and 
            results['news_data']['analysis'].get('llm_analysis')):
            content.append("## News Analysis (LLM)")
            content.append(results['news_data']['analysis']['llm_analysis'])
            content.append("")
        
        if ('financial_data' in results and results['financial_data'].get('analysis') and 
            results['financial_data']['analysis'].get('llm_analysis')):
            content.append("## Financial Analysis (LLM)")
            content.append(results['financial_data']['analysis']['llm_analysis'])
            content.append("")
        
        return "\n".join(content)
    
    def _format_recommendation_content(self, symbol: str, results: Dict[str, Any]) -> str:
        """Format content for Recommendation.md file."""
        content = []
        content.append(f"# Investment Recommendation: {symbol}")
        content.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        content.append("")
        
        # Main Recommendation
        if 'recommendation_data' in results and 'investment_recommendation' in results['recommendation_data']:
            rec_data = results['recommendation_data']['investment_recommendation']
            
            # Get current price from financial data
            current_price = "Not available"
            if 'financial_data' in results and 'current_price_data' in results['financial_data']:
                price_data = results['financial_data']['current_price_data']
                if 'current_price' in price_data and price_data['current_price'] != 'N/A':
                    current_price = f"${price_data['current_price']}"
            
            content.append("## Investment Recommendation")
            content.append(f"**RECOMMENDATION**: {rec_data.get('recommendation', 'HOLD')}")
            content.append(f"**Current Price**: {current_price}")
            content.append(f"**Confidence Level**: {rec_data.get('confidence_level', 'Medium')}")
            content.append(f"**Target Price**: {rec_data.get('target_price', 'Not specified')}")
            content.append(f"**Time Horizon**: {rec_data.get('time_horizon', 'Not specified')}")
            content.append("")
            
            # Reasoning
            if rec_data.get('reasoning') and rec_data['reasoning'].strip() and not rec_data['reasoning'].startswith("Section '") and not rec_data['reasoning'].startswith("Error extracting"):
                content.append("## Reasoning")
                content.append(rec_data['reasoning'])
                content.append("")
            
            # Risk Assessment
            if rec_data.get('risk_assessment') and rec_data['risk_assessment'].strip() and not rec_data['risk_assessment'].startswith("Section '") and not rec_data['risk_assessment'].startswith("Error extracting"):
                content.append("## Risk Assessment")
                content.append(rec_data['risk_assessment'])
                content.append("")
            
            # Investment Strategy
            if rec_data.get('investment_strategy') and rec_data['investment_strategy'].strip() and not rec_data['investment_strategy'].startswith("Section '") and not rec_data['investment_strategy'].startswith("Error extracting"):
                content.append("## Investment Strategy")
                content.append(rec_data['investment_strategy'])
                content.append("")
            
            # Monitoring Points
            if rec_data.get('monitoring_points') and rec_data['monitoring_points'].strip() and not rec_data['monitoring_points'].startswith("Section '") and not rec_data['monitoring_points'].startswith("Error extracting"):
                content.append("## Monitoring Points")
                content.append(rec_data['monitoring_points'])
                content.append("")
            
            # Key Factors
            if rec_data.get('key_factors') and rec_data['key_factors']:
                content.append("## Key Factors")
                for factor in rec_data['key_factors']:
                    content.append(f"- {factor}")
                content.append("")
            
            # Fallback: include full LLM recommendation text
            if rec_data.get('full_recommendation'):
                content.append("## Full Recommendation (LLM)")
                content.append(rec_data['full_recommendation'])
                content.append("")
        
        return "\n".join(content)
    
    def get_execution_status(self, symbol: str) -> Dict[str, Any]:
        """
        Get execution status for a specific symbol.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Execution status information
        """
        return self.graph.get_execution_summary(symbol)
