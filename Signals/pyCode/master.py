#!/usr/bin/env python3
"""
Master file for pyCode - Python equivalent of master.do

This script mimics the functionality of ../Code/master.do
"""

import os
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv


def check_environment():
    """Check that required environment variables are set"""
    print("Checking environment setup...")

    # Load environment variables
    load_dotenv()

    # Check WRDS credentials
    wrds_user = os.getenv("WRDS_USERNAME")
    wrds_pass = os.getenv("WRDS_PASSWORD")

    if not wrds_user or not wrds_pass:
        print("ERROR: WRDS credentials not set")
        print("Please set WRDS_USERNAME and WRDS_PASSWORD in .env file")
        return False

    print("✓ WRDS credentials found")
    return True


def check_folder_structure():
    """Check that required folders exist"""
    print("Checking folder structure...")

    required_folders = [
        "../pyData",
        "../pyData/Intermediate",
        "../pyData/Predictors",
        "../pyData/Placebos",
        "../pyData/temp",
        "../pyData/Prep",
        "../Logs"
    ]

    missing_folders = []
    for folder in required_folders:
        if not Path(folder).exists():
            missing_folders.append(folder)

    if missing_folders:
        print(f"ERROR: Missing folders: {missing_folders}")
        print("Please run set_up_pyCode.py first to create folder structure")
        return False

    print("✓ Folder structure verified")
    return True


def run_settings():
    """Run setup equivalent to settings.do - folder creation and checks"""
    print("Running setup (equivalent to settings.do)...")

    if not check_folder_structure():
        print("Creating missing folders...")
        # Import and run folder creation
        from set_up_pyCode import create_folder_structure  # pylint: disable=import-outside-toplevel
        create_folder_structure()

    print("✓ Setup complete")


def main():
    """Main execution function mimicking master.do"""
    print("=" * 60)
    print("Python Master Script - pyCode equivalent of master.do")
    print("=" * 60)

    # Check if we're in the right directory
    if not Path("CLAUDE.md").exists():
        print("ERROR: Please run this script from the pyCode directory")
        sys.exit(1)

    # Check environment setup (equivalent to checking globals in master.do)
    if not check_environment():
        sys.exit(1)

    # Run settings equivalent
    run_settings()

    # Set CSV output option (equivalent to global save_csv 1)
    os.environ["SAVE_CSV"] = "1"

    print("\nRunning main processing steps...")

    # Download data (equivalent to do "$pathCode/01_DownloadData.do")
    print("\n1. Running data downloads...")
    try:
        # Use subprocess.run without capture_output for real-time streaming
        result = subprocess.run([sys.executable, "-u", "01_DownloadData.py"],
                              check=True)
        print("✓ Data downloads completed")
    except subprocess.CalledProcessError as e:
        print(f"ERROR in data downloads: {e}")
        sys.exit(1)

    # TODO: Create predictors (equivalent to do "$pathCode/02_CreatePredictors.do")
    # print("\n2. Creating predictors...")

    # TODO: Create placebos (equivalent to do "$pathCode/03_CreatePlacebos.do")
    # print("\n3. Creating placebos...")

    print("\n" + "=" * 60)
    print("Master script completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()