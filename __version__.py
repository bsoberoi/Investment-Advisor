"""
Version information for Investment Advisor Multi-Agent System.
"""

__version__ = "1.0.0"
__version_info__ = (1, 0, 0)
__build__ = "2025-09-01"
__author__ = "Investment Advisor Team"
__email__ = "team@investment-advisor.com"
__description__ = "AI-powered investment advisory system with multi-agent architecture"
__license__ = "MIT"
__url__ = "https://github.com/bsoberoi/investment-advisor"

# Version history
VERSION_HISTORY = {
    "1.0.0": {
        "date": "2025-09-01",
        "changes": [
            "Initial release",
            "Multi-agent architecture with LangGraph",
            "GROQ LLM integration",
            "Yahoo Finance data integration",
            "DuckDuckGo news search",
            "Streamlit web interface",
            "CLI interface",
            "Comprehensive analysis and recommendation generation",
            "Technical documentation and system diagrams",
            "JPG diagram generation for documentation"
        ]
    }
}

def get_version():
    """Get the current version string."""
    return __version__

def get_version_info():
    """Get the version as a tuple."""
    return __version_info__

def get_build_info():
    """Get build information."""
    return {
        "version": __version__,
        "build_date": __build__,
        "author": __author__,
        "description": __description__,
        "license": __license__,
        "url": __url__
    }

def get_version_history():
    """Get complete version history."""
    return VERSION_HISTORY

def format_version_info():
    """Format version information for display."""
    build_info = get_build_info()
    return f"""
Investment Advisor Multi-Agent System
Version: {build_info['version']}
Build Date: {build_info['build_date']}
Author: {build_info['author']}
License: {build_info['license']}
Description: {build_info['description']}
URL: {build_info['url']}
"""
