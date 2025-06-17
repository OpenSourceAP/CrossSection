#!/usr/bin/env python3
"""
Download Data script - Python equivalent of 01_DownloadData.do

This script finds all .py files in DataDownloads/ and executes them,
mimicking the Stata script's filelist and loop functionality.
"""

import os
import sys
import time
import subprocess
import pandas as pd
from pathlib import Path
from datetime import datetime

def setup_logging():
    """Setup logging equivalent to Stata log files"""
    log_dir = Path("../Logs")
    log_dir.mkdir(exist_ok=True)
    
    # Create error tracking DataFrame (equivalent to 01_DownloadDataFlags.dta)
    error_log = pd.DataFrame(columns=['DataFile', 'DataTime', 'ReturnCode', 'Message'])
    return error_log

def find_download_scripts():
    """Find all .py files in DataDownloads/ directory"""
    downloads_dir = Path("DataDownloads")
    
    if not downloads_dir.exists():
        print(f"ERROR: {downloads_dir} directory not found")
        return []
    
    # Find all .py files, excluding __pycache__ and system files
    py_files = []
    for file in downloads_dir.glob("*.py"):
        if not file.name.startswith("__"):
            py_files.append(file.name)
    
    # Sort alphabetically (like Stata's sort filename)
    py_files.sort()
    
    print(f"Found {len(py_files)} download scripts:")
    for file in py_files:
        print(f"  - {file}")
    
    return py_files

def execute_script(script_name, error_log):
    """Execute a single download script and track results"""
    print(f"\n🔄 Starting: {script_name}")
    print("=" * 60)
    
    start_time = time.time()
    return_code = 0
    
    try:
        # Execute the script in the DataDownloads directory
        script_path = Path("DataDownloads") / script_name
        
        # Use Popen for real-time output streaming
        process = subprocess.Popen(
            [sys.executable, str(script_path)],
            cwd=".",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Stream output in real-time
        for line in process.stdout:
            print(line, end='', flush=True)
        
        # Wait for completion and check return code
        process.wait()
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, [sys.executable, str(script_path)])
        
        print("=" * 60)
        print(f"✅ Completed: {script_name}")
        
    except subprocess.CalledProcessError as e:
        return_code = e.returncode
        print("=" * 60)
        print(f"❌ ERROR in {script_name}: Return code {e.returncode}")
    
    except Exception as e:
        return_code = 1
        print("=" * 60)
        print(f"💥 UNEXPECTED ERROR in {script_name}: {e}")
    
    # Calculate execution time
    execution_time = time.time() - start_time
    
    # Log results (equivalent to Stata's error tracking)
    message = "Processing successful" if return_code == 0 else "Processing error"
    
    new_row = pd.DataFrame({
        'DataFile': [script_name],
        'DataTime': [execution_time],
        'ReturnCode': [return_code],
        'Message': [message]
    })
    
    error_log = pd.concat([error_log, new_row], ignore_index=True)
    
    return error_log, return_code

def save_error_log(error_log):
    """Save error log to files (equivalent to Stata's save and export)"""
    log_path = Path("../Logs/01_DownloadDataFlags.csv")
    
    # Save to CSV
    error_log.to_csv(log_path, index=False)
    
    # Also save as pickle (Python equivalent of .dta)
    pickle_path = Path("../Logs/01_DownloadDataFlags.pkl")
    error_log.to_pickle(pickle_path)
    
    print(f"\nError log saved to: {log_path}")

def check_optional_files():
    """Check for optional preprocessed files (equivalent to Stata's confirm file checks)"""
    print("Checking for optional preprocessed files...")
    
    optional_files = [
        "../Data/Prep/iclink.csv",
        "../Data/Prep/OptionMetrics.csv", 
        "../Data/Prep/tr_13f.csv",
        "../Data/Prep/corwin_schultz_spread.csv"
    ]
    
    missing_files = []
    for file_path in optional_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("WARNING: Some optional files are missing:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        print("Some signals that depend on these files cannot be generated.")
        print("These files are created by code in ../PrepScripts/")
    else:
        print("✓ All optional preprocessed files found")

def main():
    """Main function mimicking 01_DownloadData.do logic"""
    print("=" * 60)
    print("Data Download Script - Python equivalent of 01_DownloadData.do")
    print("=" * 60)
    
    # Check for optional files
    check_optional_files()
    
    # Setup logging
    error_log = setup_logging()
    
    # Find all download scripts
    download_scripts = find_download_scripts()
    
    if not download_scripts:
        print("No download scripts found in DataDownloads/")
        return
    
    # Execute each script (equivalent to Stata's forvalues loop)
    print(f"\nExecuting {len(download_scripts)} download scripts...")
    
    failed_scripts = []
    
    for script in download_scripts:
        error_log, return_code = execute_script(script, error_log)
        
        if return_code != 0:
            failed_scripts.append(script)
        
        # Save error log after each script (like Stata does)
        save_error_log(error_log)
    
    # Final summary (equivalent to Stata's final checks)
    print("\n" + "=" * 60)
    print("DOWNLOAD SUMMARY")
    print("=" * 60)
    
    total_scripts = len(download_scripts)
    successful_scripts = total_scripts - len(failed_scripts)
    
    print(f"Total scripts: {total_scripts}")
    print(f"Successful: {successful_scripts}")
    print(f"Failed: {len(failed_scripts)}")
    
    if failed_scripts:
        print("\nThe following download scripts did not complete successfully:")
        for script in failed_scripts:
            print(f"  ✗ {script}")
        print(f"\nCheck {Path('../Logs/01_DownloadDataFlags.csv').absolute()} for details")
    else:
        print("\n✓ All download scripts completed successfully!")
    
    print("=" * 60)

if __name__ == "__main__":
    main()