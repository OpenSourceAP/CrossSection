# ABOUTME: 02_CreatePredictors.py - orchestrates predictor signal creation, direct translation from 02_CreatePredictors.do
# ABOUTME: Line-by-line translation preserving exact Stata logic and execution order

import pandas as pd
import numpy as np
import subprocess
import time
import sys
from pathlib import Path
from datetime import datetime
import glob
import os

def main():
    """
    Create Predictors
    Direct translation from 02_CreatePredictors.do
    """
    
    print("Starting 02_CreatePredictors.py...")
    
    # Create logs directory
    logs_dir = Path("../Logs")
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    # Log file for signal creation
    # clear
    # gen SignalFile = ""
    # gen double SignalTime = .
    # gen lastRun = ""
    # gen ReturnCode = .
    # save "$pathLogs/02_CreatePredictorsFlags", replace
    flags_data = []  # Will accumulate results
    
    # Create Signal Master Table with some meta data
    # do "$pathCode/SignalMasterTable.do"
    print("Creating Signal Master Table...")
    try:
        result = subprocess.run([sys.executable, "SignalMasterTable.py"], 
                              capture_output=True, text=True, timeout=600)
        if result.returncode != 0:
            print(f"Warning: SignalMasterTable.py failed with return code {result.returncode}")
            if result.stderr:
                print(f"Error: {result.stderr}")
        else:
            print("SignalMasterTable.py completed successfully")
    except subprocess.TimeoutExpired:
        print("Error: SignalMasterTable.py timed out")
    except Exception as e:
        print(f"Error running SignalMasterTable.py: {e}")
    
    # Look-up signal scripts 
    # filelist, pat("*.py") nor directory("$pathCodePredictors")
    # gen filenameLower = strlower(filename)
    # sort filenameLower
    # save "$pathLogs/tempFilenames", replace
    
    predictors_dir = Path("Predictors")
    if not predictors_dir.exists():
        print(f"Error: Predictors directory not found: {predictors_dir}")
        return
    
    # Find all .py files in Predictors directory
    py_files = list(predictors_dir.glob("*.py"))
    py_files = [f.name for f in py_files]  # Get just the filenames
    py_files.sort(key=str.lower)  # Sort case-insensitive like Stata strlower
    
    print(f"Found {len(py_files)} predictor scripts")
    for f in py_files:
        print(f"  {f}")
    
    # Loop over all signal scripts
    # local obs = _N
    # forvalues i=1/`obs' {
    obs = len(py_files)
    for i, filename in enumerate(py_files, 1):
        print(f"\n=== Processing {i}/{obs}: {filename} ===")
        
        # timer clear 1
        # timer on 1 
        start_time = time.time()
        
        # capture noisily do "$pathCodePredictors/`file'"
        script_path = predictors_dir / filename
        return_code = 0
        
        try:
            # Run the predictor script
            result = subprocess.run([sys.executable, str(script_path)], 
                                  capture_output=True, text=True, timeout=1800)  # 30 min timeout
            return_code = result.returncode
            
            if return_code == 0:
                print(f"✓ {filename} completed successfully")
                if result.stdout:
                    print("Output:")
                    for line in result.stdout.strip().split('\n'):
                        print(f"  {line}")
            else:
                print(f"✗ {filename} failed with return code {return_code}")
                if result.stderr:
                    print("Error output:")
                    for line in result.stderr.strip().split('\n'):
                        print(f"  {line}")
                if result.stdout:
                    print("Standard output:")
                    for line in result.stdout.strip().split('\n'):
                        print(f"  {line}")
                        
        except subprocess.TimeoutExpired:
            print(f"✗ {filename} timed out after 30 minutes")
            return_code = 124  # Standard timeout return code
        except Exception as e:
            print(f"✗ {filename} failed with exception: {e}")
            return_code = 1
        
        # timer off 1
        end_time = time.time()
        signal_time = end_time - start_time
        
        # gen SignalFile = "`file'"
        # gen SignalTime = r(t1)
        # gen lastRun = "$S_DATE $S_TIME"
        # gen ReturnCode = _rc
        last_run = datetime.now().strftime("%d %b %Y %H:%M:%S")
        
        flags_data.append({
            'SignalFile': filename,
            'SignalTime': signal_time,
            'lastRun': last_run,
            'ReturnCode': return_code
        })
        
        # append using "$pathLogs/02_CreatePredictorsFlags"
        # save "$pathLogs/02_CreatePredictorsFlags", replace
        # export delimited using "$pathLogs/02_CreatePredictorsFlags.csv", replace 
        
        # Save intermediate results after each script
        flags_df = pd.DataFrame(flags_data)
        flags_df.to_csv(logs_dir / "02_CreatePredictorsFlags.csv", index=False)
        
        print(f"Time: {signal_time:.2f} seconds")
    
    # di("The following signal scripts did not complete successfully")
    # li if ReturnCode !=0
    print("\n" + "="*60)
    print("FINAL SUMMARY")
    print("="*60)
    
    flags_df = pd.DataFrame(flags_data)
    failed_scripts = flags_df[flags_df['ReturnCode'] != 0]
    
    if len(failed_scripts) == 0:
        print("✓ All signal scripts completed successfully!")
    else:
        print("The following signal scripts did not complete successfully:")
        for _, row in failed_scripts.iterrows():
            print(f"  {row['SignalFile']} (return code: {row['ReturnCode']})")
    
    # Save final results
    flags_df.to_csv(logs_dir / "02_CreatePredictorsFlags.csv", index=False)
    
    print(f"\nProcessed {len(py_files)} scripts")
    print(f"Successful: {len(flags_df[flags_df['ReturnCode'] == 0])}")
    print(f"Failed: {len(failed_scripts)}")
    print(f"Total time: {sum(flags_df['SignalTime']):.2f} seconds")
    print(f"\nFlags saved to: {logs_dir / '02_CreatePredictorsFlags.csv'}")
    
    print("02_CreatePredictors.py completed")

if __name__ == "__main__":
    main()