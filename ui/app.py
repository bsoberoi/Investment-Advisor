"""
Investment Advisor Multi-Agent System - Streamlit Web Application

This module provides a web-based interface for the investment advisor system.
It allows users to analyze stocks and view results through a modern web UI.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import settings
from config.logging_config import setup_logging
from graphs.execution import GraphExecutor

# Page configuration
st.set_page_config(
    page_title="Investment Advisor AI",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main Streamlit application."""
    
    # Initialize logging
    logger = setup_logging()
    
    # Sidebar
    st.sidebar.title("📈 Investment Advisor AI")
    st.sidebar.markdown("---")
    
    # Navigation
    page = st.sidebar.selectbox(
        "Navigation",
        ["🏠 Home", "🔍 Analyze Stock", "📊 Results", "⚙️ Settings"]
    )
    
    # Main content
    if page == "🏠 Home":
        show_home_page()
    elif page == "🔍 Analyze Stock":
        show_analyze_page()
    elif page == "📊 Results":
        show_results_page()
    elif page == "⚙️ Settings":
        show_settings_page()

def show_home_page():
    """Display the home page."""
    st.title("🚀 Investment Advisor Multi-Agent System")
    st.markdown("---")
    
    # Introduction
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## Welcome to the Future of Investment Analysis
        
        Our AI-powered system leverages multiple specialized agents to provide comprehensive 
        investment insights and recommendations. Using advanced LangGraph orchestration, 
        we analyze stocks through multiple lenses:
        
        - **📰 News Agent**: Gathers and analyzes company news and market sentiment
        - **📊 Data Agent**: Retrieves financial data and statements
        - **🧠 Analyst Agent**: Synthesizes information into comprehensive analysis
        - **💼 Financial Expert Agent**: Generates actionable investment recommendations
        
        ### Key Features
        - 🔍 **Automated Research**: Gather company news and financial data automatically
        - 🧠 **AI-Powered Analysis**: Synthesize information into actionable insights
        - 📋 **Structured Outputs**: Generate detailed analysis and recommendation reports
        - ⚡ **Fast Execution**: Complete analysis in under 1 minute
        """)
    
    with col2:
        st.info("""
        **Quick Start**
        
        1. Go to "🔍 Analyze Stock"
        2. Enter a stock symbol (e.g., AAPL, MSFT)
        3. Click "Analyze" to start
        4. View results in "📊 Results"
        """)
    
    # Recent activity
    st.markdown("---")
    st.subheader("📈 Recent Activity")
    
    # Check for recent output files
    try:
        recent_files = get_recent_files()
        if recent_files:
            for file_info in recent_files[:5]:  # Show last 5
                st.text(f"📄 {file_info['name']} - {file_info['time']}")
        else:
            st.info("No recent analyses found. Start by analyzing a stock!")
    except Exception as e:
        st.warning(f"Could not load recent files: {e}")

def show_analyze_page():
    """Display the stock analysis page."""
    st.title("🔍 Analyze Stock")
    st.markdown("---")
    
    # Input form
    with st.form("analysis_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            symbol = st.text_input(
                "Stock Symbol",
                placeholder="e.g., AAPL, MSFT, GOOGL",
                help="Enter the stock symbol you want to analyze"
            )
        
        with col2:
            company_name = st.text_input(
                "Company Name (Optional)",
                placeholder="e.g., Apple Inc.",
                help="Optional: Provide the full company name for better context"
            )
        
        # Analysis options
        st.markdown("### Analysis Options")
        col3, col4 = st.columns(2)
        
        with col3:
            verbose_output = st.checkbox("Verbose Output", value=False)
        
        with col4:
            auto_refresh = st.checkbox("Auto-refresh Results", value=True)
        
        # Submit button
        submitted = st.form_submit_button("🚀 Start Analysis", type="primary")
    
    # Handle form submission
    if submitted:
        if not symbol:
            st.error("Please enter a stock symbol")
            return
        
        # Validate symbol format
        symbol = symbol.upper().strip()
        if not symbol.replace('.', '').replace('-', '').isalnum():
            st.error("Invalid stock symbol format")
            return
        
        # Start analysis
        run_analysis(symbol, company_name, verbose_output, auto_refresh)

def run_analysis(symbol: str, company_name: str = None, verbose: bool = False, auto_refresh: bool = True):
    """Run the investment analysis."""
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Initialize executor
        status_text.text("Initializing analysis system...")
        progress_bar.progress(10)
        
        executor = GraphExecutor()
        progress_bar.progress(20)
        
        # Run analysis
        status_text.text(f"Starting analysis for {symbol}...")
        progress_bar.progress(30)
        
        start_time = datetime.now()
        results = executor.run_analysis(symbol, company_name)
        end_time = datetime.now()
        
        progress_bar.progress(90)
        status_text.text("Generating output files...")
        
        # Display results
        if results.get('success', False):
            progress_bar.progress(100)
            status_text.text("✅ Analysis completed successfully!")
            
            # Success message
            st.success(f"Analysis completed for {symbol} in {(end_time - start_time).total_seconds():.2f} seconds!")
            
            # Display results
            display_analysis_results(results, verbose)
            
            # Auto-refresh if enabled
            if auto_refresh:
                st.info("Results will auto-refresh. Check the '📊 Results' page for detailed outputs.")
                st.rerun()
                
        else:
            progress_bar.progress(100)
            status_text.text("❌ Analysis failed!")
            st.error(f"Analysis failed: {results.get('error', 'Unknown error')}")
            
    except Exception as e:
        progress_bar.progress(100)
        status_text.text("❌ Analysis failed!")
        st.error(f"Unexpected error: {e}")

def display_analysis_results(results: dict, verbose: bool):
    """Display analysis results in the UI."""
    
    # Create tabs for different result sections
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Recommendation", "🏢 Company Info", "📊 Financial Data", "📰 News Analysis"])
    
    with tab1:
        if 'recommendation_data' in results and 'investment_recommendation' in results['recommendation_data']:
            rec_data = results['recommendation_data']['investment_recommendation']
            
            # Main recommendation
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Recommendation", rec_data.get('recommendation', 'HOLD'))
            with col2:
                st.metric("Confidence", rec_data.get('confidence_level', 'Medium'))
            with col3:
                st.metric("Target Price", rec_data.get('target_price', 'Not specified'))
            
            # Detailed recommendation
            if verbose and 'full_recommendation' in rec_data:
                st.markdown("### Detailed Recommendation")
                st.text_area("Full Analysis", rec_data['full_recommendation'], height=300)
        else:
            st.warning("No recommendation data available")
    
    with tab2:
        if 'financial_data' in results and 'company_info' in results['financial_data']:
            company_info = results['financial_data']['company_info']
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### Company Details")
                st.write(f"**Name**: {company_info.get('company_name', 'N/A')}")
                st.write(f"**Sector**: {company_info.get('sector', 'N/A')}")
                st.write(f"**Industry**: {company_info.get('industry', 'N/A')}")
                st.write(f"**Country**: {company_info.get('country', 'N/A')}")
            
            with col2:
                st.markdown("### Business Summary")
                business_summary = company_info.get('business_summary', 'No summary available')
                st.text_area("Summary", business_summary, height=150)
        else:
            st.warning("No company information available")
    
    with tab3:
        if 'financial_data' in results and 'current_price_data' in results['financial_data']:
            price_data = results['financial_data']['current_price_data']
            
            # Market metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Current Price", f"${price_data.get('current_price', 'N/A')}")
            with col2:
                st.metric("Market Cap", f"${price_data.get('market_cap', 'N/A'):,}" if price_data.get('market_cap') != 'N/A' else 'N/A')
            with col3:
                st.metric("Volume", f"{price_data.get('volume', 'N/A'):,}" if price_data.get('volume') != 'N/A' else 'N/A')
            
            # Financial analysis
            if 'analysis' in results['financial_data']:
                fin_analysis = results['financial_data']['analysis']
                st.markdown("### Financial Analysis")
                st.write(f"**Health**: {fin_analysis.get('health_assessment', 'N/A')}")
                st.write(f"**Growth Trends**: {fin_analysis.get('growth_trends', 'N/A')}")
        else:
            st.warning("No financial data available")
    
    with tab4:
        if 'news_data' in results and 'analysis' in results['news_data']:
            news_analysis = results['news_data']['analysis']
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### Market Sentiment")
                sentiment = news_analysis.get('market_sentiment', 'N/A')
                if sentiment == 'Positive':
                    st.success(f"Sentiment: {sentiment}")
                elif sentiment == 'Negative':
                    st.error(f"Sentiment: {sentiment}")
                else:
                    st.info(f"Sentiment: {sentiment}")
            
            with col2:
                st.markdown("### Key Developments")
                developments = news_analysis.get('key_developments', [])
                if developments:
                    for dev in developments:
                        st.write(f"• {dev}")
                else:
                    st.write("No key developments identified")
        else:
            st.warning("No news analysis available")

def show_results_page():
    """Display the results page."""
    st.title("📊 Analysis Results")
    st.markdown("---")
    
    # File browser
    st.subheader("📁 Generated Files")
    
    try:
        # Analysis files
        st.markdown("### 📋 Analysis Reports")
        analysis_files = get_files_in_directory(settings.ANALYSIS_DIR)
        if analysis_files:
            for file_info in analysis_files:
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(f"📄 {file_info['name']}")
                with col2:
                    st.write(f"📅 {file_info['time']}")
                with col3:
                    if st.button(f"View {file_info['name']}", key=f"view_analysis_{file_info['name']}"):
                        display_file_content(file_info['path'])
        else:
            st.info("No analysis reports found")
        
        # Recommendation files
        st.markdown("### 🎯 Investment Recommendations")
        recommendation_files = get_files_in_directory(settings.RECOMMENDATION_DIR)
        if recommendation_files:
            for file_info in recommendation_files:
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(f"📄 {file_info['name']}")
                with col2:
                    st.write(f"📅 {file_info['time']}")
                with col3:
                    if st.button(f"View {file_info['name']}", key=f"view_rec_{file_info['name']}"):
                        display_file_content(file_info['path'])
        else:
            st.info("No recommendation reports found")
            
    except Exception as e:
        st.error(f"Error loading results: {e}")

def show_settings_page():
    """Display the settings page."""
    st.title("⚙️ Settings")
    st.markdown("---")
    
    st.markdown("### Configuration")
    
    # API Key status
    api_key = settings.GROQ_API_KEY
    if api_key:
        st.success("✅ Groq API Key is configured")
        st.info(f"Model: {settings.GROQ_MODEL}")
        st.info(f"Temperature: {settings.GROQ_TEMPERATURE}")
    else:
        st.error("❌ Groq API Key is not configured")
        st.info("Please set GROQ_API_KEY in your .env file")
    
    # Output directories
    st.markdown("### Output Directories")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Analysis**: {settings.ANALYSIS_DIR}")
        st.write(f"**Recommendations**: {settings.RECOMMENDATION_DIR}")
    
    with col2:
        st.write(f"**Logs**: {settings.LOGS_DIR}")
        st.write(f"**Log Level**: {settings.LOG_LEVEL}")
    
    # System info
    st.markdown("### System Information")
    st.write(f"**Python Version**: {sys.version}")
    st.write(f"**Working Directory**: {os.getcwd()}")

def get_recent_files():
    """Get recent output files."""
    files = []
    
    # Check analysis directory
    if os.path.exists(settings.ANALYSIS_DIR):
        for filename in os.listdir(settings.ANALYSIS_DIR):
            if filename.endswith('.md'):
                filepath = os.path.join(settings.ANALYSIS_DIR, filename)
                files.append({
                    'name': filename,
                    'path': filepath,
                    'time': datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d %H:%M')
                })
    
    # Check recommendation directory
    if os.path.exists(settings.RECOMMENDATION_DIR):
        for filename in os.listdir(settings.RECOMMENDATION_DIR):
            if filename.endswith('.md'):
                filepath = os.path.join(settings.RECOMMENDATION_DIR, filename)
                files.append({
                    'name': filename,
                    'path': filepath,
                    'time': datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d %H:%M')
                })
    
    # Sort by modification time (newest first)
    files.sort(key=lambda x: x['time'], reverse=True)
    return files

def get_files_in_directory(directory: str):
    """Get files in a specific directory."""
    files = []
    
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            if filename.endswith('.md'):
                filepath = os.path.join(directory, filename)
                files.append({
                    'name': filename,
                    'path': filepath,
                    'time': datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d %H:%M')
                })
    
    # Sort by modification time (newest first)
    files.sort(key=lambda x: x['time'], reverse=True)
    return files

def display_file_content(filepath: str):
    """Display the content of a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        st.markdown("### File Content")
        st.text_area("Content", content, height=400)
        
        # Download button
        st.download_button(
            label="📥 Download File",
            data=content,
            file_name=os.path.basename(filepath),
            mime="text/markdown"
        )
        
    except Exception as e:
        st.error(f"Error reading file: {e}")

if __name__ == "__main__":
    main()
