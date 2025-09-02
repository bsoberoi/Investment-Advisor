#!/usr/bin/env python3
"""
Investment Advisor Multi-Agent System - Main CLI Entry Point

This module provides the command-line interface for the Investment Advisor system,
allowing users to analyze stocks, view recommendations, and manage the system.
"""

import argparse
import sys
import os
from datetime import datetime
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.settings import settings
from config.logging_config import setup_logging, get_logger
from graphs.execution import GraphExecutor

# Import version information
try:
    from __version__ import get_version, get_build_info, format_version_info
except ImportError:
    def get_version():
        return "unknown"
    
    def get_build_info():
        return {"version": "unknown", "build_date": "unknown", "author": "unknown"}
    
    def format_version_info():
        return "Investment Advisor Multi-Agent System\nVersion: unknown"

# Setup logging
setup_logging()
logger = get_logger(__name__)

def analyze_stock(symbol: str, company_name: str = None):
    """Analyze a stock using the multi-agent system."""
    try:
        print(f"🚀 Starting investment analysis for {symbol}...")
        logger.info(f"Starting investment analysis for {symbol}...")
        
        if company_name:
            print(f"📋 Company: {company_name}")
            logger.info(f"Company: {company_name}")
            print("")
            logger.info("")
        
        # Initialize and execute the investment graph
        print("🔍 Initializing multi-agent system...")
        logger.info("Initializing multi-agent system...")
        executor = GraphExecutor()
        
        print("⚡ Executing analysis workflow...")
        logger.info("Executing analysis workflow...")
        results = executor.run_analysis(symbol, company_name)
        
        if results:
            print("✅ Analysis completed successfully!")
            print(f"⏱️  Execution time: {results.get('execution_time', 0):.2f} seconds")
            print("")
            logger.info("Analysis completed successfully!")
            logger.info(f"Execution time: {results.get('execution_time', 0):.2f} seconds")
            logger.info("")
            
            # Display generated files
            print("📁 Generated output files:")
            logger.info("Generated output files:")
            for file_type, filepath in results.get('output_files', {}).items():
                if os.path.exists(filepath):
                    print(f"   📄 {file_type.title()}: {filepath}")
                    logger.info(f"   {file_type.title()}: {filepath}")
            print("")
            logger.info("")
            
            return results
        else:
            print("❌ Analysis failed!")
            logger.error("Analysis failed!")
            return None
            
    except KeyboardInterrupt:
        print("\n⚠️  Analysis interrupted by user")
        logger.warning("Analysis interrupted by user")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        logger.error(f"Unexpected error: {e}")
        return None

def display_summary(results: dict, symbol: str):
    """Display a summary of the analysis results."""
    try:
        # Extract recommendation data
        recommendation_data = results.get('recommendation_data', {})
        recommendation = recommendation_data.get('recommendation', 'N/A')
        confidence = recommendation_data.get('confidence', 'N/A')
        target_price = recommendation_data.get('target_price', 'N/A')
        
        logger.info("INVESTMENT RECOMMENDATION")
        logger.info("=" * 50)
        logger.info(f"Recommendation: {recommendation}")
        logger.info(f"Confidence: {confidence}")
        logger.info(f"Target Price: {target_price}")
        logger.info("")
        
        # Extract company information
        financial_data = results.get('financial_data', {})
        company_info = financial_data.get('company_info', {})
        company_name = company_info.get('company_name', 'N/A')
        sector = company_info.get('sector', 'N/A')
        industry = company_info.get('industry', 'N/A')
        
        logger.info("COMPANY INFORMATION")
        logger.info("=" * 50)
        logger.info(f"Company: {company_name}")
        logger.info(f"Sector: {sector}")
        logger.info(f"Industry: {industry}")
        logger.info("")
        
        # Extract market data
        current_price_data = financial_data.get('current_price_data', {})
        current_price = current_price_data.get('current_price', 'N/A')
        market_cap = current_price_data.get('market_cap', 0)
        
        logger.info("CURRENT MARKET DATA")
        logger.info("=" * 50)
        logger.info(f"Current Price: ${current_price}")
        if market_cap and market_cap != 'N/A':
            logger.info(f"Market Cap: ${market_cap:,}")
        logger.info("")
        
        # Extract news sentiment
        news_data = results.get('news_data', {})
        analysis = news_data.get('analysis', {})
        sentiment = analysis.get('market_sentiment', 'N/A')
        
        logger.info("NEWS SENTIMENT")
        logger.info("=" * 50)
        logger.info(f"Market Sentiment: {sentiment}")
        logger.info("")
        
        logger.info("DETAILED RESULTS")
        logger.info("=" * 50)
        logger.info("For detailed analysis and recommendations, please check the generated markdown files.")
        logger.info("")
        
    except Exception as e:
        logger.error(f"Error displaying summary: {e}")

def check_status(symbol: str):
    """Check the status of a previous analysis."""
    try:
        print(f"📊 Checking analysis status for {symbol}...")
        logger.info(f"Checking analysis status for {symbol}...")
        
        # Check if analysis files exist
        analysis_dir = Path(settings.ANALYSIS_DIR)
        recommendation_dir = Path(settings.RECOMMENDATION_DIR)
        
        analysis_files = list(analysis_dir.glob(f"{symbol}_*"))
        recommendation_files = list(recommendation_dir.glob(f"{symbol}_*"))
        
        if not analysis_files and not recommendation_files:
            print(f"❌ No analysis found for {symbol}")
            print("Run 'python main.py analyze {symbol}' to start analysis")
            logger.info(f"No analysis found for {symbol}")
            logger.info("Run 'python main.py analyze {symbol}' to start analysis")
            return
        
        print(f"✅ Analysis status for {symbol}:")
        logger.info(f"Analysis status for {symbol}:")
        
        # Get the most recent files
        latest_analysis = max(analysis_files, key=lambda x: x.stat().st_mtime) if analysis_files else None
        latest_recommendation = max(recommendation_files, key=lambda x: x.stat().st_mtime) if recommendation_files else None
        
        status = {
            'completed_tasks': [],
            'has_error': False,
            'error': None,
            'timestamp': None
        }
        
        if latest_analysis:
            status['completed_tasks'].append('Analysis')
            status['timestamp'] = datetime.fromtimestamp(latest_analysis.stat().st_mtime)
        
        if latest_recommendation:
            status['completed_tasks'].append('Recommendation')
            status['timestamp'] = latest_recommendation.stat().st_mtime
        
        print(f"   📋 Completed tasks: {', '.join(status.get('completed_tasks', []))}")
        print(f"   ⚠️  Has error: {status.get('has_error', False)}")
        logger.info(f"   Completed tasks: {', '.join(status.get('completed_tasks', []))}")
        logger.info(f"   Has error: {status.get('has_error', False)}")
        
        if status.get('error'):
            print(f"   ❌ Error: {status['error']}")
            logger.info(f"   Error: {status['error']}")
        
        if status.get('timestamp'):
            print(f"   🕒 Last updated: {status['timestamp']}")
            logger.info(f"   Last updated: {status['timestamp']}")
            
    except Exception as e:
        print(f"❌ Error checking status: {e}")
        logger.error(f"Error checking status: {e}")

def show_version():
    """Display version information."""
    try:
        print("📋 Investment Advisor Multi-Agent System")
        print("=" * 50)
        print(format_version_info())
        print("🔗 For more information, visit: https://github.com/your-org/investment-advisor")
        print("📄 For changelog, see: CHANGELOG.md")
    except Exception as e:
        print(f"❌ Error displaying version: {e}")
        logger.error(f"Error displaying version: {e}")

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Investment Advisor Multi-Agent System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py analyze AAPL                    # Analyze Apple stock
  python main.py analyze AAPL "Apple Inc."      # Analyze with company name
  python main.py status AAPL                    # Check analysis status
  python main.py version                         # Show version information
  python main.py --help                         # Show this help message
        """
    )
    
    parser.add_argument(
        'command',
        choices=['analyze', 'status', 'version'],
        help='Command to execute'
    )
    
    parser.add_argument(
        'symbol',
        nargs='?',
        help='Stock symbol to analyze (e.g., AAPL) - not required for version command'
    )
    
    parser.add_argument(
        '--company-name',
        help='Company name (optional, for better context)'
    )
    
    args = parser.parse_args()
    
    # Validate settings
    try:
        settings.validate()
    except ValueError as e:
        logger.error(f"Configuration Error: {e}")
        logger.error("Please ensure you have set GROQ_API_KEY in your .env file.")
        sys.exit(1)
    
    # Execute command
    if args.command == 'analyze':
        if not args.symbol:
            print("❌ Error: Stock symbol is required for analyze command")
            sys.exit(1)
        results = analyze_stock(args.symbol, args.company_name)
        if results:
            display_summary(results, args.symbol)
    elif args.command == 'status':
        if not args.symbol:
            print("❌ Error: Stock symbol is required for status command")
            sys.exit(1)
        check_status(args.symbol)
    elif args.command == 'version':
        show_version()

if __name__ == "__main__":
    main()
