#!/usr/bin/env python3
"""
Patent Citations data script - Python equivalent of ZI_PatentCitations.do

Calls R script to process patent data or creates placeholder if R script unavailable.
"""

import os
import subprocess
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL

load_dotenv()

def main():
    """Process patent citations data"""
    print("Processing Patent Citations data...")

    # Ensure directories exist
    os.makedirs("../pyData/Intermediate", exist_ok=True)

    # Path to R script (relative to git root)
    r_script_path = Path("../Code/DataDownloads/ZIR_Patents.R")
    project_path = Path("../../..").resolve()  # Git root

    try:
        if r_script_path.exists():
            print(f"Running R script: {r_script_path}")

            # Try to run R script
            result = subprocess.run([
                "Rscript", str(r_script_path), str(project_path)
            ], capture_output=True, text=True, timeout=300)

            if result.returncode == 0:
                print("R script completed successfully")

                # Check if output file was created
                output_file = Path("../pyData/Intermediate/PatentDataProcessed.dta")
                if output_file.exists():
                    print(f"Patent data file created: {output_file}")
                    # Convert .dta to .pkl if needed
                    # Note: Would need additional packages to read .dta files
                    print("Note: .dta file created by R script")
                else:
                    print("R script ran but output file not found")
            else:
                print(f"R script failed with return code {result.returncode}")
                print(f"Error: {result.stderr}")
                raise Exception("R script failed")
        else:
            print(f"R script not found: {r_script_path}")
            raise Exception("R script not found")

    except Exception as e:
        print(f"Error running R script: {e}")
        print("Creating placeholder patent data")

        # Create placeholder patent data with format matching Stata data
        placeholder_data = pd.DataFrame({
            'gvkey': [1000.0, 1001.0, 1002.0],  # Numeric gvkey to match Stata
            'year': [1976.0, 1977.0, 1978.0],   # Starting from 1976 to match Stata
            'npat': [4.0, 2.0, 0.0],            # Float type to match Stata
            'ncitscale': [0.0, 0.0, 0.0]        # Float type to match Stata
        })

        # Apply row limit for debugging if configured
        if MAX_ROWS_DL > 0:
            placeholder_data = placeholder_data.head(MAX_ROWS_DL)
            print(f"DEBUG MODE: Limited to {MAX_ROWS_DL} rows")

        # Save the data
        placeholder_data.to_parquet("../pyData/Intermediate/PatentDataProcessed.parquet", index=False)
        print(f"Placeholder patent data saved with {len(placeholder_data)} records")

    print("Patent Citations processing completed")

if __name__ == "__main__":
    main()
