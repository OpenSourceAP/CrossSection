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
import threading
import pandas as pd
from pathlib import Path
from datetime import datetime
from config import SCRIPT_TIMEOUT_MINUTES

def setup_logging():
    """Setup logging equivalent to Stata log files"""
    log_dir = Path("../Logs")
    log_dir.mkdir(exist_ok=True)
    
    # Create error tracking DataFrame (equivalent to 01_DownloadDataFlags.dta)
    error_log = pd.DataFrame(columns=['DataFile', 'DataTime', 'ReturnCode', 'Message'])
    
    # Initialize console log list for detailed txt output
    console_log = []
    console_log.append(f"Data Download Log - Started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    console_log.append("=" * 80)
    
    return error_log, console_log

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

def execute_script(script_name, error_log, console_log):
    """Execute a single download script and track results with configurable timeout"""
    start_msg = f"\n🔄 Starting: {script_name}"
    separator = "=" * 60
    
    print(start_msg)
    print(separator)
    
    # Add to console log
    console_log.append(f"\n{start_msg}")
    console_log.append(separator)
    
    start_time = time.time()
    return_code = 0
    script_output = []
    process = None
    timer = None
    timed_out = False
    
    def timeout_handler():
        """Handle timeout by terminating the process"""
        nonlocal timed_out
        timed_out = True
        if process and process.poll() is None:
            process.terminate()
            # Give it 2 seconds to terminate gracefully, then kill
            threading.Timer(2.0, lambda: process.kill() if process.poll() is None else None).start()
    
    try:
        # Execute the script in the DataDownloads directory
        script_path = Path("DataDownloads") / script_name
        
        # Use Popen for real-time output streaming and capture
        process = subprocess.Popen(
            [sys.executable, str(script_path)],
            cwd=".",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Set up configurable timeout (convert minutes to seconds)
        timeout_seconds = SCRIPT_TIMEOUT_MINUTES * 60
        timer = threading.Timer(timeout_seconds, timeout_handler)
        timer.start()
        
        # Stream output in real-time and capture for logging
        for line in process.stdout:
            if timed_out:
                break
            print(line, end='', flush=True)
            script_output.append(line.rstrip())
        
        # Cancel timer if process completed normally
        if timer:
            timer.cancel()
        
        # Wait for completion and check return code
        process.wait()
        
        if timed_out:
            return_code = -9  # SIGKILL return code
            timeout_msg = f"⏱️ TIMEOUT in {script_name}: Script exceeded {SCRIPT_TIMEOUT_MINUTES} minutes"
            print(separator)
            print(timeout_msg)
            
            # Add timeout details to console log
            console_log.extend(script_output)
            console_log.append(separator)
            console_log.append(timeout_msg)
            console_log.append(f"Script was terminated due to {SCRIPT_TIMEOUT_MINUTES}-minute timeout")
            
        elif process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, [sys.executable, str(script_path)])
        else:
            success_msg = f"✅ Completed: {script_name}"
            print(separator)
            print(success_msg)
            
            # Add success to console log
            console_log.extend(script_output)
            console_log.append(separator)
            console_log.append(success_msg)
        
    except subprocess.CalledProcessError as e:
        return_code = e.returncode
        error_msg = f"❌ ERROR in {script_name}: Return code {e.returncode}"
        print(separator)
        print(error_msg)
        
        # Add error details to console log
        console_log.extend(script_output)
        console_log.append(separator)
        console_log.append(error_msg)
        console_log.append(f"Error details: Script failed with return code {e.returncode}")
    
    except Exception as e:
        return_code = 1
        error_msg = f"💥 UNEXPECTED ERROR in {script_name}: {e}"
        print(separator)
        print(error_msg)
        
        # Add exception details to console log
        console_log.extend(script_output)
        console_log.append(separator)
        console_log.append(error_msg)
        console_log.append(f"Exception details: {str(e)}")
        console_log.append(f"Exception type: {type(e).__name__}")
    
    finally:
        # Clean up timer and process
        if timer:
            timer.cancel()
        if process and process.poll() is None:
            process.terminate()
    
    # Calculate execution time
    execution_time = time.time() - start_time
    time_msg = f"Execution time: {execution_time:.2f} seconds"
    console_log.append(time_msg)
    
    # Log results (equivalent to Stata's error tracking)
    if timed_out:
        message = "Processing timeout"
    elif return_code == 0:
        message = "Processing successful"
    else:
        message = "Processing error"
    
    new_row = pd.DataFrame({
        'DataFile': [script_name],
        'DataTime': [execution_time],
        'ReturnCode': [return_code],
        'Message': [message]
    })
    
    error_log = pd.concat([error_log, new_row], ignore_index=True)
    
    return error_log, return_code, console_log

def save_error_log(error_log, console_log):
    """Save error log to files (equivalent to Stata's save and export)"""
    csv_path = Path("../Logs/01_DownloadDataFlags.csv")
    txt_path = Path("../Logs/01_DownloadData_console.txt")
    
    # Save to CSV
    error_log.to_csv(csv_path, index=False)
    
    # Save detailed console output to txt file
    with open(txt_path, 'w') as f:
        f.write('\n'.join(console_log))
        f.write(f"\n\nLog completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
  
    print(f"\nLog files saved:")
    print(f"  CSV: {csv_path}")
    print(f"  TXT: {txt_path}")

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
    error_log, console_log = setup_logging()
    
    # Find all download scripts
    download_scripts = find_download_scripts()
    
    if not download_scripts:
        print("No download scripts found in DataDownloads/")
        return
    
    # Execute each script (equivalent to Stata's forvalues loop)
    print(f"\nExecuting {len(download_scripts)} download scripts...")
    
    failed_scripts = []
    
    for script in download_scripts:
        error_log, return_code, console_log = execute_script(script, error_log, console_log)
        
        if return_code != 0:
            failed_scripts.append(script)
        
        # Save error log after each script (like Stata does)
        save_error_log(error_log, console_log)
    
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