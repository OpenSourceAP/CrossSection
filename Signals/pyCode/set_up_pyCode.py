#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run a shell command and handle errors."""
    print(f"Running: {description}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return False


def setup_dropbox_ignore():
    """Set .venv to be ignored by Dropbox using xattr"""
    print("Setting up Dropbox ignore for .venv...")
    
    venv_path = Path(".venv").absolute()
    cmd = f'xattr -w com.dropbox.ignored 1 "{venv_path}"'
    
    return run_command(cmd, "Setting Dropbox ignore attribute for .venv")


def create_virtual_environment():
    """Create Python virtual environment"""
    print("Creating Python virtual environment...")
    
    if not run_command("python3 -m venv .venv", "Creating virtual environment"):
        return False
    
    # Set Dropbox ignore immediately after creation
    setup_dropbox_ignore()
    
    return True


def install_packages():
    """Install required packages into virtual environment"""
    print("Installing Python packages...")
    
    # Try to install PostgreSQL dependencies first (macOS)
    print("Installing PostgreSQL dependencies...")
    run_command("brew install postgresql", "Installing PostgreSQL via Homebrew")
    
    activate_and_install = """
    source .venv/bin/activate && 
    pip install --upgrade pip && 
    pip install -r requirements.txt
    """
    
    return run_command(activate_and_install, "Installing packages")


def check_env_file():
    """Check if .env file exists and warn if not"""
    env_file = Path(".env")
    if not env_file.exists():
        print("WARNING: .env file not found!")
        print("Please create .env file with your WRDS credentials:")
        print("WRDS_USERNAME=your_username")
        print("WRDS_PASSWORD=your_password")
        print("You can copy .env.template and modify it.")
        return False
    else:
        print("✓ .env file found")
        return True


def main():
    """Main setup function"""
    print("Setting up pyCode environment...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("CLAUDE.md").exists():
        print("Error: Please run this script from the pyCode directory")
        sys.exit(1)
    
    # Check for .env file
    check_env_file()
    
    # Create virtual environment (this will also set Dropbox ignore)
    if not create_virtual_environment():
        print("Failed to create virtual environment")
        sys.exit(1)
    
    # Install packages
    if not install_packages():
        print("Failed to install packages")
        sys.exit(1)
    
    print("=" * 50)
    print("Setup complete!")
    print("Virtual environment created and ignored by Dropbox")


if __name__ == "__main__":
    main()