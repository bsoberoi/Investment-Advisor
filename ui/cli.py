"""
Investment Advisor Multi-Agent System - CLI Interface

This module provides a command-line interface for the investment advisor system.
It's an alternative to the main.py entry point with additional CLI features.
"""

import click
import sys
import os
from datetime import datetime
from typing import Optional

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import settings
from config.logging_config import setup_logging
from graphs.execution import GraphExecutor

@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Investment Advisor Multi-Agent System - CLI Interface"""
    pass

@cli.command()
@click.argument('symbol', type=str)
@click.option('--company', '-c', help='Company name (optional)')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.option('--output-dir', '-o', help='Custom output directory')
def analyze(symbol: str, company: Optional[str], verbose: bool, output_dir: Optional[str]):
    """Analyze a stock symbol and generate investment recommendations."""
    
    # Set up logging
    logger = setup_logging()
    
    # Validate settings
    try:
        settings.validate()
    except ValueError as e:
        click.echo(f"Configuration Error: {e}", err=True)
        click.echo("Please ensure you have set GROQ_API_KEY in your .env file", err=True)
        sys.exit(1)
    
    # Override output directory if specified
    if output_dir:
        settings.OUTPUT_DIR = output_dir
        settings.ANALYSIS_DIR = os.path.join(output_dir, "analysis")
        settings.RECOMMENDATION_DIR = os.path.join(output_dir, "recommendations")
        settings.LOGS_DIR = os.path.join(output_dir, "logs")
        settings.create_directories()
    
    # Start analysis
    click.echo(f"🚀 Starting investment analysis for {symbol}...")
    if company:
        click.echo(f"📋 Company: {company}")
    click.echo()
    
    try:
        # Initialize executor
        executor = GraphExecutor()
        
        # Run analysis
        start_time = datetime.now()
        results = executor.run_analysis(symbol, company)
        end_time = datetime.now()
        
        # Display results
        if results.get('success', False):
            click.echo("✅ Analysis completed successfully!")
            click.echo(f"⏱️  Execution time: {(end_time - start_time).total_seconds():.2f} seconds")
            click.echo()
            
            # Display output files
            output_files = results.get('output_files', {})
            if output_files:
                click.echo("📁 Generated output files:")
                for file_type, filepath in output_files.items():
                    click.echo(f"   {file_type.title()}: {filepath}")
                click.echo()
            
            # Display summary
            display_analysis_summary_cli(results, verbose)
            
        else:
            click.echo("❌ Analysis failed!", err=True)
            error_msg = results.get('error', 'Unknown error')
            click.echo(f"Error: {error_msg}", err=True)
            sys.exit(1)
            
    except KeyboardInterrupt:
        click.echo("\n⚠️  Analysis interrupted by user", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}", err=True)
        if logger:
            logger.error(f"Unexpected error in analysis: {e}")
        sys.exit(1)

@cli.command()
@click.argument('symbol', type=str)
def status(symbol: str):
    """Check the status of an analysis for a stock symbol."""
    
    # Set up logging
    logger = setup_logging()
    
    try:
        click.echo(f"📊 Checking analysis status for {symbol}...")
        
        executor = GraphExecutor()
        status_info = executor.get_execution_status(symbol)
        
        if 'status' in status_info and status_info['status'] == 'No execution found':
            click.echo(f"❌ No analysis found for {symbol}")
            click.echo(f"Run 'investment-advisor analyze {symbol}' to start analysis")
        else:
            click.echo(f"✅ Analysis status for {symbol}:")
            click.echo(f"   Completed tasks: {', '.join(status_info.get('completed_tasks', []))}")
            click.echo(f"   Has error: {status_info.get('has_error', False)}")
            if status_info.get('error'):
                click.echo(f"   Error: {status_info['error']}")
            if status_info.get('timestamp'):
                click.echo(f"   Last updated: {status_info['timestamp']}")
                
    except Exception as e:
        click.echo(f"❌ Error checking status: {e}", err=True)
        if logger:
            logger.error(f"Error checking status: {e}")

@cli.command()
@click.option('--symbol', '-s', help='Filter by stock symbol')
@click.option('--type', '-t', type=click.Choice(['analysis', 'recommendation', 'all']), 
              default='all', help='Type of files to list')
@click.option('--limit', '-l', type=int, default=10, help='Maximum number of files to show')
def list_files(symbol: Optional[str], type: str, limit: int):
    """List generated analysis and recommendation files."""
    
    try:
        executor = GraphExecutor()
        
        if type in ['analysis', 'all']:
            click.echo("📋 Analysis Reports:")
            analysis_files = get_files_in_directory_cli(executor.settings.ANALYSIS_DIR, symbol, limit)
            if analysis_files:
                for file_info in analysis_files:
                    click.echo(f"   📄 {file_info['name']} - {file_info['time']}")
            else:
                click.echo("   No analysis reports found")
            click.echo()
        
        if type in ['recommendation', 'all']:
            click.echo("🎯 Investment Recommendations:")
            recommendation_files = get_files_in_directory_cli(executor.settings.RECOMMENDATION_DIR, symbol, limit)
            if recommendation_files:
                for file_info in recommendation_files:
                    click.echo(f"   📄 {file_info['name']} - {file_info['time']}")
            else:
                click.echo("   No recommendation reports found")
            click.echo()
                
    except Exception as e:
        click.echo(f"❌ Error listing files: {e}", err=True)

@cli.command()
@click.argument('filepath', type=str)
def view(filepath: str):
    """View the content of a generated file."""
    
    try:
        if not os.path.exists(filepath):
            click.echo(f"❌ File not found: {filepath}", err=True)
            sys.exit(1)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        click.echo(f"📄 File: {filepath}")
        click.echo("=" * 80)
        click.echo(content)
        
    except Exception as e:
        click.echo(f"❌ Error reading file: {e}", err=True)
        sys.exit(1)

@cli.command()
def config():
    """Show current configuration settings."""
    
    try:
        # Validate settings
        try:
            settings.validate()
            api_key_status = "✅ Configured"
        except ValueError:
            api_key_status = "❌ Not configured"
        
        click.echo("⚙️  Configuration Settings")
        click.echo("=" * 50)
        click.echo(f"Groq API Key: {api_key_status}")
        click.echo(f"Model: {settings.GROQ_MODEL}")
        click.echo(f"Temperature: {settings.GROQ_TEMPERATURE}")
        click.echo(f"Log Level: {settings.LOG_LEVEL}")
        click.echo()
        
        click.echo("📁 Output Directories")
        click.echo("=" * 50)
        click.echo(f"Analysis: {settings.ANALYSIS_DIR}")
        click.echo(f"Recommendations: {settings.RECOMMENDATION_DIR}")
        click.echo(f"Logs: {settings.LOGS_DIR}")
        click.echo()
        
        # Check if directories exist
        click.echo("📂 Directory Status")
        click.echo("=" * 50)
        for directory in [settings.ANALYSIS_DIR, settings.RECOMMENDATION_DIR, settings.LOGS_DIR]:
            if os.path.exists(directory):
                click.echo(f"✅ {directory}")
            else:
                click.echo(f"❌ {directory}")
                
    except Exception as e:
        click.echo(f"❌ Error displaying configuration: {e}", err=True)

def display_analysis_summary_cli(results: dict, verbose: bool):
    """Display analysis summary in CLI format."""
    try:
        # Get recommendation
        if 'recommendation_data' in results and 'investment_recommendation' in results['recommendation_data']:
            rec_data = results['recommendation_data']['investment_recommendation']
            recommendation = rec_data.get('recommendation', 'HOLD')
            confidence = rec_data.get('confidence_level', 'Medium')
            target_price = rec_data.get('target_price', 'Not specified')
            
            click.echo("🎯 INVESTMENT RECOMMENDATION")
            click.echo("=" * 50)
            click.echo(f"Recommendation: {recommendation}")
            click.echo(f"Confidence: {confidence}")
            click.echo(f"Target Price: {target_price}")
            click.echo()
        
        # Get company info
        if 'financial_data' in results and 'company_info' in results['financial_data']:
            company_info = results['financial_data']['company_info']
            company_name = company_info.get('company_name', 'N/A')
            sector = company_info.get('sector', 'N/A')
            industry = company_info.get('industry', 'N/A')
            
            click.echo("🏢 COMPANY INFORMATION")
            click.echo("=" * 50)
            click.echo(f"Company: {company_name}")
            click.echo(f"Sector: {sector}")
            click.echo(f"Industry: {industry}")
            click.echo()
        
        # Get current price
        if 'financial_data' in results and 'current_price_data' in results['financial_data']:
            price_data = results['financial_data']['current_price_data']
            current_price = price_data.get('current_price', 'N/A')
            market_cap = price_data.get('market_cap', 'N/A')
            
            click.echo("💰 CURRENT MARKET DATA")
            click.echo("=" * 50)
            click.echo(f"Current Price: ${current_price}")
            if market_cap != 'N/A':
                click.echo(f"Market Cap: ${market_cap:,}")
            click.echo()
        
        # Get news sentiment
        if 'news_data' in results and 'analysis' in results['news_data']:
            news_analysis = results['news_data']['analysis']
            sentiment = news_analysis.get('market_sentiment', 'N/A')
            
            click.echo("📰 NEWS SENTIMENT")
            click.echo("=" * 50)
            click.echo(f"Market Sentiment: {sentiment}")
            click.echo()
        
        if verbose:
            click.echo("📊 DETAILED RESULTS")
            click.echo("=" * 50)
            click.echo("For detailed analysis and recommendations, please check the generated markdown files.")
            click.echo()
            
    except Exception as e:
        click.echo(f"Error displaying summary: {e}")

def get_files_in_directory_cli(directory: str, symbol_filter: Optional[str] = None, limit: int = 10):
    """Get files in a specific directory for CLI display."""
    files = []
    
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            if filename.endswith('.md'):
                # Apply symbol filter if specified
                if symbol_filter and symbol_filter.upper() not in filename.upper():
                    continue
                
                filepath = os.path.join(directory, filename)
                files.append({
                    'name': filename,
                    'path': filepath,
                    'time': datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d %H:%M')
                })
    
    # Sort by modification time (newest first) and apply limit
    files.sort(key=lambda x: x['time'], reverse=True)
    return files[:limit]

if __name__ == "__main__":
    cli()
