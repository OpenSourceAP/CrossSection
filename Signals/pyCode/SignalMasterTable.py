# ABOUTME: Creates the "backbone" used in most predictors.
# ABOUTME: Incorporates basic info from monthly CRSP and annual Compustat.
"""
Inputs:
    - monthlyCRSP.parquet
    - m_aCompustat.parquet
    - IBESCRSPLinkingTable.parquet (optional)
    - OPTIONMETRICSCRSPLinkingTable.parquet (optional)

Outputs:
    - SignalMasterTable.parquet

"""
import pandas as pd
import numpy as np
from pathlib import Path


print("Starting SignalMasterTable.py...")

# DATA LOAD
print("Loading monthly CRSP data...")

# Start with monthly CRSP
df = pd.read_parquet('../pyData/Intermediate/monthlyCRSP.parquet',
    columns=['permno', 'ticker', 'exchcd', 'shrcd', 'time_avail_m', 'mve_c', 'prc', 'ret', 'sicCRSP'])

print(f"Loaded monthlyCRSP: {df.shape[0]} rows, {df.shape[1]} columns")

# Screen on Stock market information: common stocks and major exchanges
# TBC: remove and use this filter as default in SignalDoc.csv
print("Filtering for common stocks and major exchanges...")

# keep if (shrcd == 10 | shrcd == 11 | shrcd == 12) & (exchcd == 1 | exchcd == 2 | exchcd == 3)
df = df[(df['shrcd'].isin([10, 11, 12])) & (df['exchcd'].isin([1, 2, 3]))].copy()

print(f"After filtering: {df.shape[0]} rows")

# Merge with Compustat monthly data
print("Merging with m_aCompustat...")
compustat_df = pd.read_parquet('../pyData/Intermediate/m_aCompustat.parquet',
    columns=['permno', 'time_avail_m', 'gvkey', 'sic'])

# Merge (left join to keep all CRSP observations)
df = df.merge(compustat_df, on=['permno', 'time_avail_m'], how='left')

print(f"After Compustat merge: {df.shape[0]} rows")

# rename sic sicCS
df = df.rename(columns={'sic': 'sicCS'})

# Standardize sicCS string format to match Stata (handle None -> empty string)
df['sicCS'] = df['sicCS'].fillna('')

# add some auxiliary vars and clean up
print("Adding auxiliary variables...")

# gen NYSE = exchcd == 1
df['NYSE'] = (df['exchcd'] == 1).astype(int)

# Fix data types to match Stata output
# TBC: clean this up
df['exchcd'] = df['exchcd'].astype('int8')
df['shrcd'] = df['shrcd'].astype('int8')
df['sicCRSP'] = df['sicCRSP'].astype('int16')
df['NYSE'] = df['NYSE'].astype('int8')

# Comprehensive string column cleanup to match Stata format (handle None -> empty string)
string_columns = ['ticker', 'sicCS']
for col in string_columns:
    if col in df.columns:
        df[col] = df[col].fillna('')

print(f"After adding auxiliary vars: {df.shape[0]} rows, {df.shape[1]} columns")

# === Optional Columns ===

# Add IBES ticker (if available)
print("Checking for IBES-CRSP linking table...")

IBESCRSPLink_path = Path("../pyData/Intermediate/IBESCRSPLinkingTable.parquet")
if IBESCRSPLink_path.exists():
    print("Adding IBES-CRSP link...")        
    ibes_link = pd.read_parquet(
        IBESCRSPLink_path, columns=["permno", "tickerIBES"]
    )
    df = df.merge(ibes_link, on=['permno'], how='left')

    # Standardize IBES ticker string format to match Stata (handle None -> empty string)
    if 'tickerIBES' in df.columns:
        df['tickerIBES'] = df['tickerIBES'].fillna('')

    print(f"After IBES link merge: {df.shape[0]} rows, {df.shape[1]} columns")
else:
    print("Not adding IBES-CRSP link. Some signals cannot be generated.")
    df['tickerIBES'] = ''

# Add OptionMetrics secid (if available)
print("Checking for OptionMetrics-CRSP linking table...")

OptionMetricsLink_path = Path(
    "../pyData/Intermediate/OPTIONMETRICSCRSPLinkingTable.parquet"
)
if OptionMetricsLink_path.exists():
    print("Adding OptionMetrics-CRSP link...")

    # Load raw linking data
    om_link = pd.read_parquet(OptionMetricsLink_path)

    # Convert daily link dates to monthly periods
    # Convert start date to first day of same month
    om_link['sdate_m'] = pd.to_datetime(om_link['sdate']).dt.to_period('M').dt.to_timestamp()

    # Convert end date to previous month (since monthly dates assume end of month)
    om_link["edate_m"] = (
        pd.to_datetime(om_link["edate"]).dt.to_period("M") - 1
    ).dt.to_timestamp()

    # Create temporary df with time_avail_m for merging
    temp_om = om_link.merge(
        df[['permno', 'time_avail_m']].drop_duplicates(),
        on=['permno'],
        how='inner'
    )

    # Filter for valid date ranges
    temp_om = temp_om[
        (temp_om['time_avail_m'] >= temp_om['sdate_m']) &
        (temp_om['time_avail_m'] <= temp_om['edate_m'])
    ]

    # Remove duplicates by keeping best score for each permno-month
    # Lower score indicates better match quality
    temp_om = temp_om.sort_values(['permno','time_avail_m','score']).groupby(['permno','time_avail_m']).first().reset_index()

    # Keep only needed columns and rename score to om_score
    temp_om = temp_om[['permno', 'time_avail_m', 'secid', 'score']].rename(columns={'score': 'om_score'})

    # Merge with main dataframe
    df = df.merge(temp_om[['permno', 'time_avail_m', 'secid']], on=["permno", "time_avail_m"], how="left")

    print(f"After OptionMetrics link merge: {df.shape[0]} rows, {df.shape[1]} columns")
else:
    print("Not adding OptionMetrics-CRSP link. Some signals cannot be generated.")
    df['secid'] = np.nan

# reinforce sort (equivalent to xtset permno time_avail_m)
df = df.sort_values(['permno', 'time_avail_m'])

# Reorder columns: ['permno', 'time_avail_m'] + everything else
main_cols = ['permno', 'time_avail_m']
other_cols = [col for col in df.columns if col not in main_cols]
df = df[main_cols + other_cols]

# SAVE
print("Saving SignalMasterTable...")

# Create output directory if it doesn't exist
output_dir = Path("../pyData/Intermediate/")
output_dir.mkdir(parents=True, exist_ok=True)

# Save as parquet (equivalent to Stata's save)
output_path = output_dir / "SignalMasterTable.parquet"
df.to_parquet(output_path, index=False)

print(f"SignalMasterTable saved to: {output_path}")
print(f"Final shape: {df.shape[0]} rows, {df.shape[1]} columns")
print(f"Head: {df.head()}")