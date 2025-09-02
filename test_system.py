#!/usr/bin/env python3
"""
Investment Advisor System - Component Test Script

This script tests all major components of the Investment Advisor system
to ensure they are properly installed and configured.
"""

import sys
import os
from datetime import datetime
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.settings import settings
from config.logging_config import setup_logging, get_logger

def test_imports():
    """Test that all required modules can be imported."""
    logger.info("Testing imports...")
    
    try:
        # Test config imports
        from config.settings import settings
        logger.info("OK Config settings imported successfully")
        
        from config.logging_config import setup_logging, get_logger
        logger.info("OK Logging config imported successfully")
        
        # Test tool imports
        from tools.search_tool import SearchTool
        logger.info("OK Search tool imported successfully")
        
        from tools.finance_tools import FinanceTools
        logger.info("OK Finance tools imported successfully")
        
        # Test agent imports
        from agents.news_agent import NewsAgent
        logger.info("OK News agent imported successfully")
        
        from agents.data_agent import DataAgent
        logger.info("OK Data agent imported successfully")
        
        from agents.analyst_agent import AnalystAgent
        logger.info("OK Analyst agent imported successfully")
        
        from agents.financial_expert_agent import FinancialExpertAgent
        logger.info("OK Financial expert agent imported successfully")
        
        # Test task imports
        from tasks.news_task import NewsTask
        logger.info("OK News task imported successfully")
        
        from tasks.financials_task import FinancialsTask
        logger.info("OK Financials task imported successfully")
        
        from tasks.analysis_task import AnalysisTask
        logger.info("OK Analysis task imported successfully")
        
        from tasks.recommendation_task import RecommendationTask
        logger.info("OK Recommendation task imported successfully")
        
        # Test graph imports
        from graphs.investment_graph import InvestmentGraph
        logger.info("OK Investment graph imported successfully")
        
        from graphs.execution import GraphExecutor
        logger.info("OK Graph executor imported successfully")
        
        logger.info("All imports successful!")
        return True
        
    except ImportError as e:
        logger.error(f"Import error: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during imports: {e}")
        return False

def test_directory_structure():
    """Test that all required directories exist."""
    logger.info("\nTesting directory structure...")
    
    required_dirs = [
        "agents",
        "tasks", 
        "tools",
        "graphs",
        "config",
        "ui",
        "outputs",
        "outputs/analysis",
        "outputs/recommendations",
        "outputs/logs"
    ]
    
    all_exist = True
    for directory in required_dirs:
        if os.path.exists(directory):
            logger.info(f"OK {directory}/")
        else:
            logger.error(f"Missing {directory}/")
            all_exist = False
    
    return all_exist

def test_file_creation():
    """Test that files can be created in output directories."""
    logger.info("\nTesting file creation...")
    
    try:
        # Test analysis directory
        test_file = Path(settings.ANALYSIS_DIR) / "test_file.txt"
        test_file.write_text("Test content")
        
        if test_file.exists():
            logger.info("OK Test file created successfully")
            test_file.unlink()  # Clean up
            logger.info("OK Test file cleaned up")
        else:
            logger.error("Test file creation failed")
            return False
            
        return True
        
    except Exception as e:
        logger.error(f"File creation test failed: {e}")
        return False

def test_configuration():
    """Test configuration settings."""
    logger.info("\nTesting configuration...")
    
    try:
        # Test that output directories can be created
        os.makedirs(settings.ANALYSIS_DIR, exist_ok=True)
        os.makedirs(settings.RECOMMENDATION_DIR, exist_ok=True)
        os.makedirs(settings.LOGS_DIR, exist_ok=True)
        
        logger.info("OK Output directories created")
        
        # Test settings access
        logger.info(f"   Model: {getattr(settings, 'GROQ_MODEL', 'N/A')}")
        logger.info(f"   Temperature: {getattr(settings, 'GROQ_TEMPERATURE', 'N/A')}")
        logger.info(f"   Log Level: {settings.LOG_LEVEL}")
        
        return True
        
    except Exception as e:
        logger.error(f"Configuration test failed: {e}")
        return False

def test_logging():
    """Test logging functionality."""
    logger.info("\nTesting logging setup...")
    
    try:
        # Test that we can log messages
        test_logger = get_logger("test_logger")
        test_logger.info("This is a test log message")
        test_logger.warning("This is a test warning")
        test_logger.error("This is a test error")
        
        logger.info("OK Logging setup successful")
        
        # Test that log file was created
        log_files = list(Path(settings.LOGS_DIR).glob("*.log"))
        if log_files:
            logger.info("OK Logger test successful")
            return True
        else:
            logger.error("No log files found")
            return False
            
    except Exception as e:
        logger.error(f"Logging test failed: {e}")
        return False

def main():
    """Run all tests."""
    # Reconfigure stdout/stderr to handle Unicode on Windows
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8', errors='ignore')
        sys.stderr.reconfigure(encoding='utf-8', errors='ignore')

    # Setup logging
    setup_logging()
    global logger
    logger = get_logger(__name__)
    
    logger.info("Investment Advisor System - Component Test")
    logger.info("=" * 50)
    logger.info(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("")
    
    # Define tests
    tests = [
        ("Import Test", test_imports),
        ("Directory Structure", test_directory_structure),
        ("File Creation", test_file_creation),
        ("Configuration", test_configuration),
        ("Logging", test_logging)
    ]
    
    # Run tests
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"Running {test_name}...")
        if test_func():
            passed += 1
        logger.info("")
    
    # Print summary
    logger.info("Test Summary")
    logger.info("=" * 50)
    
    for test_name, test_func in tests:
        status = "PASS" if test_func() else "FAIL"
        logger.info(f"{test_name}: {status}")
    
    logger.info(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("All tests passed! The system is ready for use.")
        logger.info("\nNext steps:")
        logger.info("1. Set your GROQ_API_KEY in a .env file")
        logger.info("2. Run: python main.py analyze AAPL")
        logger.info("3. Or start the UI: streamlit run ui/app.py")
        return True
    else:
        logger.error(f"{total - passed} tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
