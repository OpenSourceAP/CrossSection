# ABOUTME: Main script to generate all placebo signals by running individual placebo scripts
# ABOUTME: Inputs: All data from pyData/Intermediate/; Outputs: CSV files in pyData/Placebos/

import os
import sys
import glob
import subprocess
import time
import pandas as pd
from datetime import datetime

def main():
    print("Starting 03_CreatePlacebos.py")
    
    # Get all Python files in Placebos directory
    placebo_dir = "Placebos/"
    pattern = os.path.join(placebo_dir, "*.py")
    placebo_files = glob.glob(pattern)
    
    # Sort alphabetically (same as Stata)
    placebo_files.sort()
    
    print(f"Found {len(placebo_files)} placebo scripts to run")
    
    # Initialize results tracking
    results = []
    
    # Run each placebo script
    for i, script_path in enumerate(placebo_files, 1):
        script_name = os.path.basename(script_path)
        print(f"[{i}/{len(placebo_files)}] Running {script_name}")
        
        start_time = time.time()
        
        try:
            # Run the script
            result = subprocess.run([
                sys.executable, script_path
            ], 
            capture_output=True, 
            text=True,
            cwd=os.getcwd(),
            timeout=1800  # 30 minute timeout per script
            )
            
            end_time = time.time()
            runtime = end_time - start_time
            
            # Record results
            results.append({
                'SignalFile': script_name,
                'SignalTime': runtime,
                'lastRun': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'ReturnCode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr
            })
            
            if result.returncode == 0:
                print(f"  ✅ Completed successfully in {runtime:.1f}s")
            else:
                print(f"  ❌ Failed with return code {result.returncode}")
                if result.stderr:
                    print(f"  Error: {result.stderr[:200]}...")
                    
        except subprocess.TimeoutExpired:
            print(f"  ⏰ Timed out after 30 minutes")
            results.append({
                'SignalFile': script_name,
                'SignalTime': 1800,
                'lastRun': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'ReturnCode': -1,
                'stdout': '',
                'stderr': 'Process timed out'
            })
        except Exception as e:
            print(f"  ❌ Exception: {e}")
            results.append({
                'SignalFile': script_name,
                'SignalTime': 0,
                'lastRun': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'ReturnCode': -2,
                'stdout': '',
                'stderr': str(e)
            })
    
    # Save results
    results_df = pd.DataFrame(results)
    log_path = "../Logs/03_CreatePlacebosFlags.csv"
    results_df.to_csv(log_path, index=False)
    print(f"\nResults saved to {log_path}")
    
    # Summary
    successful = len([r for r in results if r['ReturnCode'] == 0])
    failed = len([r for r in results if r['ReturnCode'] != 0])
    total_time = sum(r['SignalTime'] for r in results)
    
    print(f"\n=== SUMMARY ===")
    print(f"Total scripts: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Total runtime: {total_time:.1f} seconds ({total_time/60:.1f} minutes)")
    
    if failed > 0:
        print(f"\nThe following signal scripts did not complete successfully:")
        for result in results:
            if result['ReturnCode'] != 0:
                print(f"  - {result['SignalFile']} (code: {result['ReturnCode']})")
    
    print("03_CreatePlacebos.py completed")
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())