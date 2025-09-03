#%%
import os
os.chdir(os.path.abspath(os.path.dirname(__file__)))
os.chdir("..")
os.listdir()


"""
ABOUTME: Option Volume Data from OptionMetrics - Python translation of OptionMetricsVolume.R
ABOUTME: Downloads option volume data from OptionMetrics and aggregates by month
"""

import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
import time
from datetime import datetime

print("=" * 60, flush=True)
print("📊 ZH1_OptionVolume.py - OptionMetrics Volume Data", flush=True)
print("=" * 60, flush=True)

# Debug mode - set to True to limit to 1000 rows per year for testing
debug_mode = False  # Set to False for production

if debug_mode:
    querylimit = '1000'
    print("DEBUG MODE: Limiting to 1000 rows per year", flush=True)
else:
    querylimit = 'all'
    print("PRODUCTION MODE: Downloading all data", flush=True)

# Environment setup
load_dotenv()

# Create output directory
path_dl_me = '../pyData/Prep/'
os.makedirs(path_dl_me, exist_ok=True)

# Create SQLAlchemy engine for database connection
print("Connecting to WRDS...", flush=True)
engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

# Get list of OptionMetrics tables
print("Getting list of OptionMetrics tables...", flush=True)
# Hardcode years for now due to information_schema query issue
# Years available in OptionMetrics typically from 1996 onwards
yearlist = [str(year) for year in range(1996, 2025)]
print(f"Processing years: {yearlist[:3]}...{yearlist[-3:]}", flush=True)

# Loop over years and download data
volmany = []

for i, year in enumerate(yearlist):
    print(f"\n[{i+1}/{len(yearlist)}] Processing Volume for Year: {year}", flush=True)
    tic = time.time()
    
    # Build query matching R script logic
    # From R script: "options expiring in the 30 trading days beginning five days after the trade date"
    # exdate - date >= 5 and exdate - date <= 5+30*(30.5/20)
    query = f"""
    SELECT secid, date, exdate, volume
    FROM optionm.opprcd{year}
    WHERE cp_flag != 'NaN' 
    AND exdate - date >= 5 
    AND exdate - date <= {5 + 30 * (30.5/20)}
    """
    
    if querylimit != 'all':
        query += f" LIMIT {querylimit}"
    
    try:
        temp = pd.read_sql_query(query, engine)
        volmany.append(temp)
        print(f"  Retrieved {len(temp):,} records in {time.time() - tic:.2f} seconds", flush=True)
    except Exception as e:
        print(f"  Error processing year {year}: {e}", flush=True)
        continue

# Disconnect from WRDS
engine.dispose()
print("\nDisconnected from WRDS", flush=True)

# Bind all years together
print("\nCombining all years...", flush=True)
volall = pd.concat(volmany, ignore_index=True)
print(f"Total records: {len(volall):,}", flush=True)

# # Save to CSV
# output_file = os.path.join(path_dl_me, 'OptionMetricsVolume.csv')
# print(f"\nSaving to {output_file}...", flush=True)
# volall.to_csv(output_file, index=False)
# print(f"Saved {len(volall):,} records to {output_file}", flush=True)

# print("\n✅ OptionMetrics Volume data download completed successfully!", flush=True)

#%%

volall.head()