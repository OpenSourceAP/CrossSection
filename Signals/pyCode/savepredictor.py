# ABOUTME: savepredictor.py - saves signal in a standardized way, direct translation from savepredictor.do
# ABOUTME: Line-by-line translation preserving exact Stata logic and execution order

import pandas as pd
import numpy as np
from pathlib import Path

def savepredictor(df, signal_name):
    """
    Saves signal in a standardized way
    Direct translation from savepredictor.do
    
    Args:
        df: DataFrame containing the signal data
        signal_name: Name of the signal column to save
    """
    
    print(f"saving {signal_name}")
    
    # preserve equivalent - work on copy
    df_work = df.copy()
    
    # clean up - drop if signal == .
    df_work = df_work[df_work[signal_name].notna()]
    
    # save csv, main output, need to change date from stata format
    # gen yyyymm = year(dofm(time_avail_m))*100 + month(dofm(time_avail_m))
    df_work['yyyymm'] = df_work['time_avail_m'].dt.year * 100 + df_work['time_avail_m'].dt.month
    
    # keep permno yyyymm signal
    # order permno yyyymm signal
    df_final = df_work[['permno', 'yyyymm', signal_name]].copy()
    
    # Create output directory if it doesn't exist
    output_dir = Path("../pyData/Predictors/")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # export delimited, replace
    output_path = output_dir / f"{signal_name}.csv"
    df_final.to_csv(output_path, index=False)
    
    print(f"Saved {signal_name} to {output_path}")

if __name__ == "__main__":
    # This is a utility module, not meant to be run directly
    print("savepredictor.py - utility module for saving predictor signals")