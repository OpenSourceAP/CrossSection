"""
ABOUTME: Creates SignalMasterTable.parquet then executes all predictor scripts in alphabetical order
ABOUTME: Tracks execution results, timeouts, and errors with detailed logging

Inputs:
  - SignalMasterTable.py (creates SignalMasterTable.parquet)
  - All .py files in Predictors/ directory

Outputs:
  - ../pyData/Intermediate/SignalMasterTable.parquet
  - ../pyData/Predictors/*.csv (one per predictor script)
  - ../Logs/02_CreatePredictorsFlags.csv (execution tracking)
  - ../Logs/02_CreatePredictors_console.txt (detailed console output)

Usage:
  python 02_CreatePredictors.py
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
    """Initialize error tracking and console logging"""
    log_dir = Path("../Logs")
    log_dir.mkdir(exist_ok=True)
    
    # Create error tracking DataFrame for execution monitoring
    error_log = pd.DataFrame(columns=['SignalFile', 'SignalTime', 'lastRun', 'ReturnCode'])
    
    # Initialize console log list for detailed txt output
    console_log = []
    console_log.append(f"Create Predictors Log - Started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    console_log.append("=" * 80)
    
    return error_log, console_log

def execute_signalmaster_table(console_log):
    """Create the master signal table required by all predictor scripts"""
    script_name = "SignalMasterTable.py"
    start_msg = f"\n🔄 Creating Signal Master Table: {script_name}"
    separator = "=" * 60
    
    print(start_msg)
    print(separator)
    
    # Add to console log
    console_log.append(f"\n{start_msg}")
    console_log.append(separator)
    
    start_time = time.time()
    return_code = 0
    script_output = []
    
    try:
        # Execute SignalMasterTable.py
        result = subprocess.run(
            [sys.executable, script_name],
            cwd=".",
            capture_output=True,
            text=True,
            timeout=SCRIPT_TIMEOUT_MINUTES * 60
        )
        
        # Capture output
        if result.stdout:
            script_output.extend(result.stdout.splitlines())
            print(result.stdout)
        if result.stderr:
            script_output.extend(result.stderr.splitlines())
            print(result.stderr)
        
        return_code = result.returncode
        
        if return_code == 0:
            success_msg = f"✅ Completed: {script_name}"
            print(separator)
            print(success_msg)
            
            console_log.extend(script_output)
            console_log.append(separator)
            console_log.append(success_msg)
        else:
            raise subprocess.CalledProcessError(return_code, [sys.executable, script_name])
            
    except subprocess.TimeoutExpired:
        return_code = -9
        timeout_msg = f"⏱️ TIMEOUT in {script_name}: Script exceeded {SCRIPT_TIMEOUT_MINUTES} minutes"
        print(separator)
        print(timeout_msg)
        
        console_log.extend(script_output)
        console_log.append(separator)
        console_log.append(timeout_msg)
        
    except subprocess.CalledProcessError as e:
        return_code = e.returncode
        error_msg = f"❌ ERROR in {script_name}: Return code {e.returncode}"
        print(separator)
        print(error_msg)
        
        console_log.extend(script_output)
        console_log.append(separator)
        console_log.append(error_msg)
        
    except Exception as e:
        return_code = 1
        error_msg = f"💥 UNEXPECTED ERROR in {script_name}: {e}"
        print(separator)
        print(error_msg)
        
        console_log.extend(script_output)
        console_log.append(separator)
        console_log.append(error_msg)
    
    # Calculate execution time
    execution_time = time.time() - start_time
    time_msg = f"Execution time: {execution_time:.2f} seconds"
    console_log.append(time_msg)
    
    return return_code, execution_time, console_log

def find_predictor_scripts():
    """Locate all Python predictor scripts to execute"""
    predictors_dir = Path("Predictors")
    
    if not predictors_dir.exists():
        print(f"ERROR: {predictors_dir} directory not found")
        return []
    
    # Find all .py files, excluding __pycache__ and system files
    py_files = []
    for file in predictors_dir.glob("*.py"):
        if not file.name.startswith("__"):
            py_files.append(file.name)
    
    # Sort alphabetically for consistent execution order
    py_files.sort(key=str.lower)
    
    print(f"Found {len(py_files)} predictor scripts:")
    for file in py_files:
        print(f"  - {file}")
    
    return py_files

def execute_predictor_script(script_name, error_log, console_log):
    """Run individual predictor script with timeout and error tracking"""
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
        # Execute the script in the Predictors directory
        script_path = Path("Predictors") / script_name
        
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
    
    # Record execution results for monitoring
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    new_row = pd.DataFrame({
        'SignalFile': [script_name],
        'SignalTime': [execution_time],
        'lastRun': [current_time],
        'ReturnCode': [return_code]
    })
    
    error_log = pd.concat([error_log, new_row], ignore_index=True)
    
    return error_log, return_code, console_log

def save_error_log(error_log, console_log):
    """Write execution logs to CSV and text files"""
    csv_path = Path("../Logs/02_CreatePredictorsFlags.csv")
    txt_path = Path("../Logs/02_CreatePredictors_console.txt")
    
    # Save to CSV
    error_log.to_csv(csv_path, index=False)
    
    # Save detailed console output to txt file
    with open(txt_path, 'w') as f:
        f.write('\n'.join(console_log))
        f.write(f"\n\nLog completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
  
    print(f"\nLog files saved:")
    print(f"  CSV: {csv_path}")
    print(f"  TXT: {txt_path}")

def main():
    """Execute signal table creation then all predictor scripts"""
    print("=" * 60)
    print("Create Predictors Script - Python equivalent of 02_CreatePredictors.do")
    print("=" * 60)
    
    # Setup logging
    error_log, console_log = setup_logging()
    
    # Step 1: Create the master signal table used by all predictors
    print("\nStep 1: Creating Signal Master Table...")
    signalmaster_code, signalmaster_time, console_log = execute_signalmaster_table(console_log)
    
    if signalmaster_code != 0:
        print("❌ ERROR: SignalMasterTable.py failed. Cannot proceed with predictor creation.")
        # Still save the error log
        save_error_log(error_log, console_log)
        return
    
    # Step 2: Find all predictor scripts
    print("\nStep 2: Finding predictor scripts...")
    predictor_scripts = find_predictor_scripts()
    
    if not predictor_scripts:
        print("No predictor scripts found in Predictors/")
        save_error_log(error_log, console_log)
        return
    
    # Step 3: Execute each predictor script sequentially with error tracking
    print(f"\nStep 3: Executing {len(predictor_scripts)} predictor scripts...")
    
    failed_scripts = []
    
    for script in predictor_scripts:
        error_log, return_code, console_log = execute_predictor_script(script, error_log, console_log)
        
        if return_code != 0:
            failed_scripts.append(script)
        
        # Save execution log after each script for monitoring
        save_error_log(error_log, console_log)
    
    # Generate final execution summary and report
    print("\n" + "=" * 60)
    print("PREDICTOR CREATION SUMMARY")
    print("=" * 60)
    
    total_scripts = len(predictor_scripts)
    successful_scripts = total_scripts - len(failed_scripts)
    
    print(f"Total scripts: {total_scripts}")
    print(f"Successful: {successful_scripts}")
    print(f"Failed: {len(failed_scripts)}")
    
    if failed_scripts:
        print("\nThe following signal scripts did not complete successfully:")
        for script in failed_scripts:
            print(f"  ✗ {script}")
        print(f"\nCheck {Path('../Logs/02_CreatePredictorsFlags.csv').absolute()} for details")
    else:
        print("\n✓ All predictor scripts completed successfully!")
    
    print("=" * 60)

if __name__ == "__main__":
    main()