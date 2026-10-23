# ABOUTME: Environment and folder checks shared by master.py and crsp_only.py.
"""
Inputs: .env in the current directory (WRDS credentials), ../pyData folder tree.
Outputs: none; creates missing pyData and Logs folders on request.
How to run: imported by the orchestrators, which run from Signals/pyCode/.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

PYDATA_FOLDERS = [
    "../pyData",
    "../pyData/temp",
    "../pyData/Prep",
    "../pyData/Intermediate",
    "../pyData/Predictors",
    "../pyData/Placebos",
    "../Logs",
]


def require_pycode_cwd():
    """Stop unless the current directory is Signals/pyCode, which the scripts assume."""
    current_dir = Path.cwd()
    if current_dir.name != "pyCode":
        print("ERROR: Please run this script from the pyCode directory")
        print(f"Current directory: {current_dir}")
        return False
    return True


def check_env_file():
    """Check for the required .env file with WRDS credentials"""
    env_file = Path(".env")
    if not env_file.exists():
        print("ERROR: .env file not found")
        print("Create .env with your WRDS credentials, for example:")
        print('WRDS_USERNAME="your_username"')
        print('WRDS_PASSWORD="your_password"')
        print("You can copy dotenv.template and modify it.")
        return False

    print("✓ .env file found")
    return True


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


def check_folder_structure():
    """Verify required data and log folders exist"""
    print("Checking folder structure...")

    missing_folders = [folder for folder in PYDATA_FOLDERS if not Path(folder).exists()]

    if missing_folders:
        print(f"Folder(s) missing and will be created: {missing_folders}")
        return False

    print("✓ All required folders exist")
    return True


def create_folder_structure():
    """Create the pyData and Logs folder structure"""
    for folder in PYDATA_FOLDERS:
        Path(folder).mkdir(parents=True, exist_ok=True)
        print(f"Created: {folder}")


def run_settings():
    """Create missing folders and verify directory structure"""
    print("Running folder setup and verification...")

    if not check_folder_structure():
        print("Creating missing folders...")
        create_folder_structure()

    print("✓ Setup complete")
