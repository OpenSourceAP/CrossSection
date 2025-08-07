# ABOUTME: Calculates earnings announcement returns from CRSP daily returns minus market returns
# ABOUTME: Uses 3-day window around announcement dates from Compustat quarterly data
# 
# This script replicates Code/Predictors/ZZ2_AnnouncementReturn.do
# Run from pyCode/ directory: python3 Predictors/ZZ2_AnnouncementReturn.py
#
# Inputs:
#   - pyData/Intermediate/CCMLinkingTable.parquet (CRSP-Compustat crosswalk)
#   - pyData/Intermediate/m_QCompustat.parquet (quarterly earnings announcement dates)  
#   - pyData/Intermediate/dailyCRSP.parquet (daily stock returns)
#   - pyData/Intermediate/dailyFF.parquet (daily Fama-French factors)
#
# Outputs:
#   - pyData/Predictors/AnnouncementReturn.csv (permno, yyyymm, AnnouncementReturn)

import pandas as pd
import numpy as np

print("Starting AnnouncementReturn calculation...")

# DATA LOAD

# Prepare crosswalk CRSP-CS
print("Loading CCMLinkingTable...")
tempCW = pd.read_parquet('../pyData/Intermediate/CCMLinkingTable.parquet')
tempCW = tempCW[['gvkey', 'permno', 'timeLinkStart_d', 'timeLinkEnd_d']]

# Prepare earnings announcement dates
print("Loading m_QCompustat...")
tempAnnDats = pd.read_parquet('../pyData/Intermediate/m_QCompustat.parquet')
tempAnnDats = tempAnnDats[['gvkey', 'rdq']]
tempAnnDats = tempAnnDats.dropna(subset=['rdq'])
tempAnnDats = tempAnnDats.rename(columns={'rdq': 'time_ann_d'})
tempAnnDats = tempAnnDats.drop_duplicates()

print("Loading dailyCRSP...")
df = pd.read_parquet('../pyData/Intermediate/dailyCRSP.parquet')
df = df[['permno', 'time_d', 'ret']]

# Match announcement dates
# Add identifiers for merging
print("Merging with crosswalk...")
df = df.merge(tempCW, on='permno', how='left')

# Use only if data date is within the validity period of the link
temp = (df['timeLinkStart_d'] <= df['time_d']) & (df['time_d'] <= df['timeLinkEnd_d'])
print(f"Observations within link validity period: {temp.sum()} out of {len(df)}")
df = df[temp == True]
df = df.drop(columns=['timeLinkStart_d', 'timeLinkEnd_d'])

df = df.rename(columns={'time_d': 'time_ann_d'})
df['gvkey'] = pd.to_numeric(df['gvkey'], errors='coerce')
df = df.merge(tempAnnDats, on=['gvkey', 'time_ann_d'], how='left', indicator=True)
df['anndat'] = (df['_merge'] == 'both').astype(int)
df = df.drop(columns=['_merge', 'gvkey'])

# Merge market return
df = df.rename(columns={'time_ann_d': 'time_d'})
print("Merging with dailyFF...")
dailyFF = pd.read_parquet('../pyData/Intermediate/dailyFF.parquet')
dailyFF = dailyFF[['time_d', 'mktrf', 'rf']]
df = df.merge(dailyFF, on='time_d', how='inner')

# SIGNAL CONSTRUCTION
df['AnnouncementReturn'] = df['ret'] - (df['mktrf'] + df['rf'])

# Sort by permno and time_d to create business day sequence
df = df.sort_values(['permno', 'time_d'])
df['time_temp'] = df.groupby('permno').cumcount() + 1

# Set up panel structure for lead/lag operations
df = df.set_index(['permno', 'time_temp']).sort_index()

# Create announcement window logic
# time_temp indexes the business days for a particular permno (1,2,3,..)
# time_ann_d creates a window that starts two biz days before anndat
# and ends 1 day after anndat. The value of time_ann_d is the biz day
# of the anndat (unique for each announcement) but is na if outside the window.

print("Creating announcement windows...")
df['time_ann_d'] = np.nan
df['time_ann_d'] = np.where(df['anndat'] == 1, df.index.get_level_values('time_temp'), df['time_ann_d'])

# Handle forward looking indicators (f1.anndat == 1, f2.anndat == 1)
df_grouped = df.groupby('permno')
df['anndat_f1'] = df_grouped['anndat'].shift(-1).fillna(0)
df['anndat_f2'] = df_grouped['anndat'].shift(-2).fillna(0)

# Handle backward looking indicators (l1.anndat == 1)  
df['anndat_l1'] = df_grouped['anndat'].shift(1).fillna(0)

# Apply the window logic
df['time_ann_d'] = np.where(df['anndat_f1'] == 1, df.index.get_level_values('time_temp') + 1, df['time_ann_d'])
df['time_ann_d'] = np.where(df['anndat_f2'] == 1, df.index.get_level_values('time_temp') + 2, df['time_ann_d'])
df['time_ann_d'] = np.where(df['anndat_l1'] == 1, df.index.get_level_values('time_temp') - 1, df['time_ann_d'])

# Keep only observations within announcement windows
df = df.dropna(subset=['time_ann_d'])

# Reset index to get permno and time_temp as columns
df = df.reset_index()

# Sum up daily returns over the window and assign to maximum date in window
print("Collapsing by announcement windows...")
df = df.groupby(['permno', 'time_ann_d']).agg({
    'AnnouncementReturn': 'sum',
    'time_d': 'max'
}).reset_index()

# Convert the daily date to monthly date
df['time_avail_m'] = df['time_d'].dt.to_period('M')

# Fill in months with no earnings announcements with most recent announcement return at most six months ago
df = df[['permno', 'time_avail_m', 'AnnouncementReturn']]
df = df.dropna(subset=['time_avail_m'])

# Keep only the last observation per permno-month
df = df.sort_values(['permno', 'time_avail_m']).groupby(['permno', 'time_avail_m']).tail(1)

print("Filling missing months...")
# Create full panel and forward fill up to 6 months
df = df.set_index(['permno', 'time_avail_m']).sort_index()

# Fill missing periods for each permno
df_filled_list = []
for permno in df.index.get_level_values('permno').unique():
    permno_df = df.loc[permno].copy()
    
    # Reindex to fill all months between min and max
    full_range = pd.period_range(start=permno_df.index.min(), end=permno_df.index.max(), freq='M')
    permno_df = permno_df.reindex(full_range)
    
    # Forward fill up to 6 months
    temp = permno_df['AnnouncementReturn'].copy()
    
    # Sequential forward fill (mimicking Stata's behavior)
    for i in range(1, 7):  # fill up to 6 lags
        mask = permno_df['AnnouncementReturn'].isna()
        permno_df.loc[mask, 'AnnouncementReturn'] = temp.shift(i).loc[mask]
    
    # Add permno back as column
    permno_df['permno'] = permno
    df_filled_list.append(permno_df)

df = pd.concat(df_filled_list)
df = df.dropna(subset=['AnnouncementReturn'])
df = df.reset_index()

print(f"Columns after reset_index: {df.columns.tolist()}")
print(f"Index name after reset_index: {df.index.name}")

# Convert time_avail_m to yyyymm format (time_avail_m became 'index' after reset_index)
df['yyyymm'] = df['index'].dt.year * 100 + df['index'].dt.month
df = df[['permno', 'yyyymm', 'AnnouncementReturn']]
df = df.sort_values(['permno', 'yyyymm'])

print(f"Final dataset shape: {df.shape}")
print("Saving to pyData/Predictors/AnnouncementReturn.csv...")

# Save to CSV
df.to_csv('../pyData/Predictors/AnnouncementReturn.csv', index=False)

print("AnnouncementReturn calculation completed.")