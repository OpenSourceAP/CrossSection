"""
ABOUTME: Master orchestrator that runs the complete data processing pipeline
ABOUTME: Executes data downloads (01_DownloadData.py) then predictor creation (02_CreatePredictors.py)
Inputs: WRDS credentials from .env file, existing folder structure
Outputs: Complete pipeline execution with data in pyData/ folders
How to run: python master.py (from pyCode/ directory)
"""

import os
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv


def check_environment():
    """Verify WRDS credentials are available in environment"""
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
    """Verify required data and log folders exist"""
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
    """Create missing folders and verify directory structure"""
    print("Running folder setup and verification...")

    if not check_folder_structure():
        print("Creating missing folders...")
        # Import and run folder creation
        from set_up_pyCode import create_folder_structure  # pylint: disable=import-outside-toplevel
        create_folder_structure()

    print("✓ Setup complete")


def main():
    """Execute complete data processing pipeline"""
    print("=" * 60)
    print("Python Data Processing Pipeline - Master Orchestrator")
    print("=" * 60)

    # Check if we're in the right directory (should end with pyCode)
    current_dir = Path.cwd()
    if current_dir.name != "pyCode":
        print("ERROR: Please run this script from the pyCode directory")
        print(f"Current directory: {current_dir}")
        sys.exit(1)

    # Verify WRDS credentials and environment setup
    if not check_environment():
        sys.exit(1)

    # Create required folders and verify structure
    run_settings()

    # Enable CSV output for data files
    os.environ["SAVE_CSV"] = "1"

    print("\nRunning main processing steps...")

    # Execute all data download scripts sequentially
    print("\n1. Running data downloads...")
    try:
        # Use subprocess.run without capture_output for real-time streaming
        result = subprocess.run([sys.executable, "-u", "01_DownloadData.py"],
                              check=True)
        print("✓ Data downloads completed")
    except subprocess.CalledProcessError as e:
        print(f"ERROR in data downloads: {e}")
        sys.exit(1)

    # Generate predictor signals from downloaded data
    print("\n2. Creating predictors...")
    try:
        # Use subprocess.run without capture_output for real-time streaming
        result = subprocess.run([sys.executable, "-u", "02_CreatePredictors.py"],
                              check=True)
        print("✓ Predictor creation completed")
    except subprocess.CalledProcessError as e:
        print(f"ERROR in predictor creation: {e}")
        sys.exit(1)

    # Generate placebos
    print("\n3. Creating placebos...")
    try:
        # Use subprocess.run without capture_output for real-time streaming
        result = subprocess.run([sys.executable, "-u", "03_CreatePlacebos.py"],
                              check=True)
        print("✓ Placebo creation completed")
    except subprocess.CalledProcessError as e:
        print(f"ERROR in placebo creation: {e}")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("Master script completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()