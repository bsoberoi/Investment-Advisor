import logging
import os
from datetime import datetime
from config.settings import settings

def setup_logging():
    """Configure logging for the Investment Advisor system."""
    
    # Create logs directory if it doesn't exist
    os.makedirs(settings.LOGS_DIR, exist_ok=True)
    
    # Generate log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = os.path.join(settings.LOGS_DIR, f"investment_advisor_{timestamp}.log")
    
    # Configure logging - ONLY to file, no console output
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            # Removed console output: logging.StreamHandler()
        ]
    )
    
    # Set specific logger levels
    logging.getLogger("yfinance").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    
    return logging.getLogger(__name__)

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a specific module."""
    return logging.getLogger(name)
