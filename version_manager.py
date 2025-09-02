#!/usr/bin/env python3
"""
Version management utility for Investment Advisor system.

This script provides utilities for managing versions, creating release tags,
and displaying version information.
"""

import argparse
import subprocess
import sys
import os
from datetime import datetime
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from __version__ import get_version, get_build_info, get_version_history, VERSION_HISTORY
except ImportError:
    print("❌ Error: __version__.py not found. Please ensure it exists in the project root.")
    sys.exit(1)

def show_version():
    """Display current version information."""
    print("📋 Investment Advisor Multi-Agent System - Version Information")
    print("=" * 60)
    
    build_info = get_build_info()
    print(f"Current Version: {build_info['version']}")
    print(f"Build Date: {build_info['build_date']}")
    print(f"Author: {build_info['author']}")
    print(f"License: {build_info['license']}")
    print(f"Description: {build_info['description']}")
    print(f"URL: {build_info['url']}")
    
    print("\n📚 Version History:")
    print("-" * 40)
    for version, info in VERSION_HISTORY.items():
        print(f"\n{version} ({info['date']}):")
        for change in info['changes']:
            print(f"  • {change}")

def create_release_tag(version):
    """Create a git tag for the release."""
    try:
        # Check if git is available
        subprocess.run(['git', '--version'], check=True, capture_output=True)
        
        # Check if we're in a git repository
        subprocess.run(['git', 'status'], check=True, capture_output=True)
        
        # Create the tag
        tag_message = f"Release version {version}"
        subprocess.run(['git', 'tag', '-a', f'v{version}', '-m', tag_message], check=True)
        print(f"✅ Created git tag v{version}")
        
        # Ask if user wants to push the tag
        push = input("Do you want to push the tag to remote? (y/N): ").lower().strip()
        if push in ['y', 'yes']:
            subprocess.run(['git', 'push', 'origin', f'v{version}'], check=True)
            print(f"✅ Pushed tag v{version} to remote")
        else:
            print("ℹ️  Tag created locally. Use 'git push origin v{version}' to push to remote.")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating tag: {e}")
        if "not a git repository" in str(e):
            print("💡 Tip: Initialize git repository with 'git init' first")
        return False
    except FileNotFoundError:
        print("❌ Error: Git not found. Please install Git to use tagging features.")
        return False
    return True

def list_tags():
    """List all git tags."""
    try:
        result = subprocess.run(['git', 'tag', '-l'], check=True, capture_output=True, text=True)
        tags = result.stdout.strip().split('\n') if result.stdout.strip() else []
        
        if tags:
            print("🏷️  Git Tags:")
            print("-" * 20)
            for tag in sorted(tags):
                print(f"  {tag}")
        else:
            print("ℹ️  No git tags found. Create one with: python version_manager.py --tag <version>")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error listing tags: {e}")
    except FileNotFoundError:
        print("❌ Error: Git not found. Please install Git to use tagging features.")

def check_git_status():
    """Check git repository status."""
    try:
        # Check if we're in a git repository
        subprocess.run(['git', 'status'], check=True, capture_output=True)
        
        # Get current branch
        result = subprocess.run(['git', 'branch', '--show-current'], check=True, capture_output=True, text=True)
        current_branch = result.stdout.strip()
        
        # Get last commit
        result = subprocess.run(['git', 'log', '-1', '--oneline'], check=True, capture_output=True, text=True)
        last_commit = result.stdout.strip()
        
        print("🔍 Git Repository Status:")
        print("-" * 30)
        print(f"Current Branch: {current_branch}")
        print(f"Last Commit: {last_commit}")
        
        # Check for uncommitted changes
        result = subprocess.run(['git', 'status', '--porcelain'], check=True, capture_output=True, text=True)
        if result.stdout.strip():
            print("⚠️  Warning: You have uncommitted changes")
            print("Consider committing changes before creating a release tag")
        else:
            print("✅ Working directory is clean")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error checking git status: {e}")
        if "not a git repository" in str(e):
            print("💡 Tip: Initialize git repository with 'git init' first")
    except FileNotFoundError:
        print("❌ Error: Git not found. Please install Git to use git features.")

def update_version_file(new_version, build_date=None):
    """Update the version in __version__.py file."""
    if not build_date:
        build_date = datetime.now().strftime("%Y-%m-%d")
    
    version_file = Path("__version__.py")
    if not version_file.exists():
        print("❌ Error: __version__.py not found")
        return False
    
    try:
        # Read current content
        with open(version_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update version
        content = content.replace(f'__version__ = "{get_version()}"', f'__version__ = "{new_version}"')
        content = content.replace(f'__build__ = "{get_build_info()["build_date"]}"', f'__build__ = "{build_date}"')
        
        # Parse version tuple
        version_parts = new_version.split('.')
        version_tuple = f"({', '.join(version_parts)})"
        content = content.replace(f'__version_info__ = {get_version().replace(".", ", ")}', f'__version_info__ = {version_tuple}')
        
        # Write updated content
        with open(version_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Updated __version__.py to version {new_version}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating version file: {e}")
        return False

def main():
    """Main entry point for version manager."""
    parser = argparse.ArgumentParser(
        description="Version management utility for Investment Advisor system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python version_manager.py --show                    # Show current version info
  python version_manager.py --tag 1.0.0              # Create git tag for version 1.0.0
  python version_manager.py --list-tags              # List all git tags
  python version_manager.py --git-status             # Check git repository status
  python version_manager.py --update-version 1.1.0   # Update version in __version__.py
        """
    )
    
    parser.add_argument('--show', action='store_true', help='Show current version information')
    parser.add_argument('--tag', type=str, help='Create git tag for specified version')
    parser.add_argument('--list-tags', action='store_true', help='List all git tags')
    parser.add_argument('--git-status', action='store_true', help='Check git repository status')
    parser.add_argument('--update-version', type=str, help='Update version in __version__.py')
    
    args = parser.parse_args()
    
    if args.show:
        show_version()
    elif args.tag:
        print(f"🏷️  Creating release tag for version {args.tag}...")
        create_release_tag(args.tag)
    elif args.list_tags:
        list_tags()
    elif args.git_status:
        check_git_status()
    elif args.update_version:
        print(f"📝 Updating version to {args.update_version}...")
        update_version_file(args.update_version)
    else:
        # Default: show version information
        show_version()

if __name__ == "__main__":
    main()
