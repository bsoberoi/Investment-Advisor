import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()

# Import version information
try:
    from __version__ import get_version, get_build_info
except ImportError:
    # Fallback if version file is not available
    def get_version():
        return "unknown"
    
    def get_build_info():
        return {
            "version": "unknown",
            "build_date": "unknown",
            "author": "unknown",
            "description": "unknown",
            "license": "unknown",
            "url": "unknown"
        }

class Settings:
    """Global configuration settings for the Investment Advisor system."""
    
    # Version Information
    VERSION: str = get_version()
    BUILD_INFO: dict = get_build_info()
    
    # Groq Configuration
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    GROQ_TEMPERATURE: float = float(os.getenv("GROQ_TEMPERATURE", "0.1"))
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Output Configuration
    OUTPUT_DIR: str = "outputs"
    ANALYSIS_DIR: str = os.path.join(OUTPUT_DIR, "analysis")
    RECOMMENDATION_DIR: str = os.path.join(OUTPUT_DIR, "recommendations")
    LOGS_DIR: str = os.path.join(OUTPUT_DIR, "logs")
    
    # API Configuration
    YAHOO_FINANCE_TIMEOUT: int = 30
    DUCKDUCKGO_MAX_RESULTS: int = 5
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required settings are configured."""
        if not cls.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is required. Please set it in your .env file.")
        return True
    
    @classmethod
    def create_directories(cls):
        """Create necessary output directories."""
        for directory in [cls.OUTPUT_DIR, cls.ANALYSIS_DIR, cls.RECOMMENDATION_DIR, cls.LOGS_DIR]:
            os.makedirs(directory, exist_ok=True)

# Global settings instance
settings = Settings()
