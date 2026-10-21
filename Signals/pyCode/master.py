"""
ABOUTME: Master orchestrator that runs the complete data processing pipeline
ABOUTME: Executes data downloads (01_DownloadData.py) then predictor creation (02_CreatePredictors.py)
Inputs: WRDS credentials from .env file, existing folder structure,
    cached Google Drive login if PATCH_OPTIONM_IV (see gdrive_login.R)
Outputs: Complete pipeline execution with data in pyData/ folders
How to run: python master.py (from pyCode/ directory)
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv

from config import PATCH_OPTIONM_IV


def check_environment():
    """Verify WRDS credentials are available in environment"""
    print("Checking environment setup...")

    if not check_env_file():
        return False

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


def check_env_file():
    """Check for the required .env file with WRDS credentials"""
    env_file = Path(".env")
    if not env_file.exists():
        print("ERROR: .env file not found")
        print("Create .env with your WRDS credentials, for example:")
        print('WRDS_USERNAME="your_username"')
        print('WRDS_PASSWORD="your_password"')
        print("You can copy .env.template and modify it.")
        return False

    print("✓ .env file found")
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
        print(f"Folder(s) missing and will be created: {missing_folders}")
        return False

    print("✓ Folder structure verified")
    return True


def run_settings():
    """Create missing folders and verify directory structure"""
    print("Running folder setup and verification...")

    if not check_folder_structure():
        print("Creating missing folders...")
        create_folder_structure()

    print("✓ Setup complete")


def check_prep_csv_files():
    """Ensure required prep CSVs exist or confirm with the user before proceeding."""
    expected_files = [
        "../pyData/Prep/bali_hovak_imp_vol.csv",
        "../pyData/Prep/corwin_schultz_spread.csv",
        "../pyData/Prep/hf_monthly.csv",
        "../pyData/Prep/OptionMetricsVolSurf.csv",
        "../pyData/Prep/OptionMetricsVolume.csv",
        "../pyData/Prep/OptionMetricsXZZ.csv",
        "../pyData/Prep/tr_13f.csv"
    ]

    missing_files = [str(Path(path)) for path in expected_files if not Path(path).exists()]

    if not missing_files:
        print("✓ All expected prep CSV files found")
        return True

    print("WARNING: Missing expected prep CSV files:")
    for path in missing_files:
        print(f"  - {path}")

    response = input("Proceed without these files? (y/N): ").strip().lower()
    if response not in {"y", "yes"}:
        print("Aborting at user request. Populate the missing prep files and rerun.")
        return False

    print("Continuing despite missing prep files.")
    return True


def check_optionm_patch_login():
    """If PATCH_OPTIONM_IV, check the Google Drive login used by the 7 patched signals."""
    if not PATCH_OPTIONM_IV:
        return True

    # Same client options as utils/gdrive_download.R, so the cached token matches
    r_check = (
        "suppressPackageStartupMessages(library(googledrive)); "
        "options(gargle_oauth_client_type = 'web'); "
        "invisible(tryCatch(drive_auth(scopes = 'drive.readonly', email = TRUE), "
        "error = function(e) NULL)); "
        "quit(status = if (drive_has_token()) 0 else 1)"
    )
    if shutil.which("Rscript") is None:
        problem = "Rscript not found on PATH"
    else:
        result = subprocess.run(["Rscript", "-e", r_check], capture_output=True, check=False)
        problem = None if result.returncode == 0 else "no googledrive package or no cached Google login"

    if problem is None:
        print("✓ Google Drive login found for the OptionMetrics 2023 patch")
        return True

    print(f"WARNING: PATCH_OPTIONM_IV is True but {problem}.")
    print("  CPVolSpread, dCPVolSpread, dVolCall, dVolPut, skew1, SmileSlope and")
    print("  RIVolSpread will fail. See https://github.com/OpenSourceAP/CrossSection/issues/156")
    print('  To fix: from Signals/pyCode/, start R and run source("gdrive_login.R")')

    response = input("Proceed without these 7 signals? (y/N): ").strip().lower()
    if response not in {"y", "yes"}:
        print("Aborting at user request. Log in to Google Drive and rerun.")
        return False

    print("Continuing without the Google Drive login.")
    return True


def create_folder_structure():
    """Create the folder structure matching ../Code/settings.do"""
    folders = [
        "../pyData",
        "../pyData/temp",
        "../pyData/Prep",
        "../pyData/Intermediate",
        "../pyData/Predictors",
        "../pyData/Placebos",
        "../Logs",
    ]

    for folder in folders:
        Path(folder).mkdir(parents=True, exist_ok=True)
        print(f"Created: {folder}")


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

    # Confirm prep CSV availability with the user
    if not check_prep_csv_files():
        sys.exit(1)

    # Confirm the Google Drive login for the OptionMetrics 2023 patch
    if not check_optionm_patch_login():
        sys.exit(1)

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
