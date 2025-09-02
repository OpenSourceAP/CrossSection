#%%
import os
os.chdir(os.path.abspath(os.path.dirname(__file__)))
os.chdir("..")
os.listdir()

#%%

#!/usr/bin/env python3
"""
CRSP-OptionMetrics data script - Python equivalent of ZL_CRSPOPTIONMETRICS.do

Processes OptionMetrics data from preprocessed file.
"""

import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL
from utils.column_standardizer_yaml import standardize_columns

load_dotenv()


"""Process CRSP-OptionMetrics data"""
print("Processing CRSP-OptionMetrics data...")

# Ensure directories exist
os.makedirs("../pyData/Intermediate", exist_ok=True)

# Check for oclink.csv in Prep folder
om_path = Path("../pyData/Prep/oclink.csv")


# Read the OptionMetrics linking file
om_data = pd.read_csv(om_path)
print(f"Loaded {len(om_data)} OptionMetrics linking records")

# Keep only records with score <= 6 (good matches)
if 'SCORE' in om_data.columns:
    om_data = om_data[om_data['SCORE'] <= 6]
    print(f"After filtering for score <= 6: {len(om_data)} records")

# Rename columns to match expected output
column_mapping = {
    'PERMNO': 'permno',
    'SCORE': 'om_score'
}
om_data = om_data.rename(columns=column_mapping)

# Keep only required columns
required_cols = ['secid', 'permno', 'om_score']
available_cols = [col for col in required_cols if col in om_data.columns]
om_data = om_data[available_cols]

# Keep best match (lowest score) per permno
if 'om_score' in om_data.columns and 'permno' in om_data.columns:
    om_data = om_data.sort_values('om_score').groupby('permno').first().reset_index()

# Standardize columns to match DTA file
om_data = standardize_columns(om_data, "OPTIONMETRICSCRSPLinkingTable")

# Save processed data
om_data.to_parquet("../pyData/Intermediate/OPTIONMETRICSCRSPLinkingTable.parquet", index=False)

print(f"OptionMetrics linking data saved with {len(om_data)} records")
print(f"Unique permnos: {om_data['permno'].nunique()}")

print("CRSP-OptionMetrics processing completed")

