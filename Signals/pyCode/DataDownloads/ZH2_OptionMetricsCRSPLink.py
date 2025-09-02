# %%

# ABOUTME: ZL_CRSPOPTIONMETRICS.py makes pyData/Intermediate/OPTIONMETRICSCRSPLinkingTable.parquet with columns permno, time_avail_m, secid, score, sdate_m, edate_m, volume
# ABOUTME: the extra columns are for record keeping
"""
Usage:
    python3 DataDownloads/ZH2_OptionMetricsCRSPLink.py

Outputs:
    - pyData/Intermediate/OPTIONMETRICSCRSPLinkingTable.parquet

Currently, even though the option volume data isn't actually helping with deduplication, we're keeping it around for clarity in case it's useful later (2025-09-02)
"""

import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import MAX_ROWS_DL
from utils.column_standardizer_yaml import standardize_columns

load_dotenv()


# %% load data

print("Processing CRSP-OptionMetrics data...")

engine = create_engine(
    f"postgresql://{os.getenv('WRDS_USERNAME')}:{os.getenv('WRDS_PASSWORD')}@wrds-pgdata.wharton.upenn.edu:9737/wrds"
)

# Query WRDS database for OptionMetrics linking data
QUERY = """
SELECT secid, sdate, edate, permno, score
FROM wrdsapps_link_crsp_optionm.opcrsphist as a
WHERE permno is not null
"""

# Read from WRDS database
omlink0 = pd.read_sql_query(QUERY, engine)
print(f"Loaded {len(omlink0)} OptionMetrics linking records from WRDS")

engine.dispose()

# load CRSP monthly data
crspm = pd.read_parquet("../pyData/Intermediate/monthlyCRSP.parquet", columns=['permno', 'time_avail_m'])

# load option volume data
opvold = pd.read_parquet("../pyData/Intermediate/OptionMetricsVolume.parquet", columns=['secid', 'date','volume'])

# %% Convert link dates to monthly
omlink = omlink0.copy()

# start date -> same month
omlink['sdate_m'] = pd.to_datetime(omlink['sdate']).dt.to_period('M').dt.to_timestamp()

# end date -> previous month (since monthly dates assume end of the month)
omlink["edate_m"] = (
    pd.to_datetime(omlink["edate"]).dt.to_period("M") - 1
).dt.to_timestamp()

omlink.drop(columns=['sdate', 'edate'], inplace=True)

# %% Convert option volume data to monthly

opvold['time_avail_m'] = opvold['date'].dt.to_period('M').dt.to_timestamp()
opvolm = opvold.groupby(['secid','time_avail_m'])['volume'].sum().reset_index()


# %% join data

# full join
df0 = omlink.merge(crspm, on=['permno'], how='outer').query(
    "secid.notna()" # keep if a link exists
).query(
    "time_avail_m >= sdate_m & time_avail_m <= edate_m" # keep if link date is valid
).merge(opvolm, on=['secid','time_avail_m'], how='left')

print(f'joined om-crsp link, crspm, and option volume data: {len(df0)} rows')

#%% remove duplicates

# first keep the lowest score
# (comparing old data based on Code/PrepScripts/oclink_to_csv.sas with new data, lowest score is the best)
df = df0.sort_values(['permno','time_avail_m','score']).groupby(['permno','time_avail_m']).first().reset_index()
print(f'removed duplicates by score: {len(df)} rows')

# then keep highest volume 
# (this actually doesn't make any difference right now)
df = df.sort_values(['permno','time_avail_m','volume'], ascending=[True, True, False]).groupby(['permno','time_avail_m']).first().reset_index()
print(f'removed duplicates by volume: {len(df)} rows')

#%% standardize columns
df = standardize_columns(df, "OPTIONMETRICSCRSPLinkingTable")

#%%
# save
df.to_parquet("../pyData/Intermediate/OPTIONMETRICSCRSPLinkingTable.parquet", index=False)

print(f"OptionMetrics linking data saved with {len(df)} records")