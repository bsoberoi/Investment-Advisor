#!/usr/bin/env python3
"""
Investment Advisor Multi-Agent System - Setup Script

This script sets up the environment, installs dependencies, and runs initial tests.
"""

import os
import sys
import subprocess
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.settings import settings
from config.logging_config import setup_logging, get_logger

def create_directories():
    """Create necessary directories for the project."""
    print("\n📁 Creating directories...")
    logger.info("\nCreating directories...")
    
    directories = [
        settings.OUTPUT_DIR,
        settings.ANALYSIS_DIR,
        settings.RECOMMENDATION_DIR,
        settings.LOGS_DIR,
        "agents",
        "tasks",
        "tools",
        "graphs",
        "config",
        "ui"
    ]
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"   ✅ {directory}/")
            logger.info(f"   OK {directory}/")
        except Exception as e:
            print(f"   ❌ {directory}/ (error)")
            logger.error(f"Error creating directories: {e}")
            return False
    
    return True

def create_env_file():
    """Create .env file template."""
    print("\n🔑 Creating environment file...")
    logger.info("\nCreating environment file...")

    env_content = """# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here

# Optional: Model Configuration
GROQ_MODEL=llama-3.1-8b-instant
GROQ_TEMPERATURE=0.1

# Optional: Logging Configuration
LOG_LEVEL=INFO
"""
    
    env_file = Path(".env")
    
    if not env_file.exists():
        try:
            with open(env_file, "w") as f:
                f.write(env_content)
            print("✅ .env file created")
            print("   ⚠️  Please edit .env and add your Groq API key")
            logger.info("OK .env file created")
            logger.info("   Please edit .env and add your Groq API key")
        except Exception as e:
            print(f"❌ Error creating .env file: {e}")
            logger.error(f"Error creating .env file: {e}")
            return False
    else:
        print("✅ .env file already exists")
        logger.info("OK .env file already exists")
    
    return True

def test_installation():
    """Test the system installation."""
    print("\n🧪 Testing installation...")
    logger.info("\nTesting installation...")
    
    try:
        # Run the test system script
        result = subprocess.run(
            [sys.executable, "test_system.py"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        if result.returncode == 0:
            print("✅ System test passed")
            logger.info("OK System test passed")
            return True
        else:
            print(f"❌ System test failed: {result.stderr}")
            logger.error(f"System test failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error running system test: {e}")
        logger.error(f"Error running system test: {e}")
        return False

def print_next_steps():
    """Print next steps for the user."""
    print("\n🎯 Next Steps")
    print("=" * 60)
    print("1. Edit .env file and add your Groq API key")
    print("2. Test the system: python test_system.py")
    print("3. Run CLI analysis: python main.py analyze AAPL")
    print("4. Run Streamlit UI: streamlit run ui/app.py")
    print()
    print("📚 Documentation:")
    print("   - README.md: Project overview and setup")
    print("   - main.py --help: CLI usage")
    print("   - ui/app.py: Web interface")
    print()
    
    logger.info("\nNext Steps")
    logger.info("=" * 60)
    logger.info("1. Edit .env file and add your Groq API key")
    logger.info("2. Test the system: python test_system.py")
    logger.info("3. Run CLI analysis: python main.py analyze AAPL")
    logger.info("4. Run Streamlit UI: streamlit run ui/app.py")
    logger.info("")
    logger.info("Documentation:")
    logger.info("   - README.md: Project overview and setup")
    logger.info("   - main.py --help: CLI usage")
    logger.info("   - ui/app.py: Web interface")
    logger.info("")

def main():
    """Main setup function."""
    # Setup logging
    setup_logging()
    global logger
    logger = get_logger(__name__)
    
    print("🚀 Investment Advisor Multi-Agent System - Setup")
    print("=" * 60)
    print()
    
    logger.info("Investment Advisor Multi-Agent System - Setup")
    logger.info("=" * 60)
    logger.info("")
    
    # Check Python version
    print("🐍 Checking Python version...")
    logger.info("Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        logger.error("Python 3.8 or higher is required")
        logger.info(f"   Current version: {sys.version}")
        return False
    else:
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
        logger.info(f"OK Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install dependencies
    print("\n📦 Installing dependencies...")
    logger.info("\nInstalling dependencies...")
    requirements_file = Path("requirements.txt")
    
    if not requirements_file.exists():
        print("❌ requirements.txt not found")
        logger.error("requirements.txt not found")
        return False
    
    try:
        print("   Installing packages from requirements.txt...")
        logger.info("   Installing packages from requirements.txt...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        if result.returncode == 0:
            print("✅ Dependencies installed successfully")
            logger.info("OK Dependencies installed successfully")
        else:
            print(f"❌ Failed to install dependencies: {result.stderr}")
            logger.error(f"Failed to install dependencies: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        logger.error(f"Error installing dependencies: {e}")
        return False
    
    # Create directories
    if not create_directories():
        return False
    
    # Create environment file
    if not create_env_file():
        return False
    
    # Test installation
    if not test_installation():
        return False
    
    # Print next steps
    print_next_steps()
    
    print("\n🎉 Setup completed successfully!")
    logger.info("\nSetup completed successfully!")
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n❌ Setup failed at dependency installation")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n❌ Setup failed at directory creation")
        sys.exit(1)
    except Exception as e:
        if "GROQ_API_KEY" in str(e):
            print("\n❌ Setup failed at environment file creation")
        elif "test_system.py" in str(e):
            print("\n❌ Setup failed at system test")
            print("   You may need to configure your API key first")
        else:
            print(f"\n❌ Setup failed: {e}")
        sys.exit(1)

