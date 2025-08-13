# ABOUTME: retConglomerate predictor - calculates conglomerate returns based on segment-weighted industry returns
# ABOUTME: Run: python3 pyCode/Predictors/retConglomerate.py

"""
retConglomerate Predictor - Conglomerate Return Calculation

This predictor calculates returns for conglomerate firms by:
1. Identifying conglomerates vs stand-alone companies using segment data
2. Calculating industry returns from stand-alone companies
3. Matching weighted industry returns to conglomerate companies based on their segment sales

Inputs:
- CCMLinkingTable.parquet (gvkey, permno, timeLink*)
- monthlyCRSP.parquet (permno, time_avail_m, ret)
- a_aCompustat.parquet (gvkey, permno, sale, fyear)
- CompustatSegments.parquet (gvkey, datadate, stype, sics1, sales)

Outputs:
- retConglomerate.csv (permno, yyyymm, retConglomerate)
"""

import pandas as pd
import numpy as np
import sys
import os

# Add utils directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from savepredictor import save_predictor
from stata_ineq import stata_ineq_pd

def main():
    print("Starting retConglomerate predictor (rewritten from scratch)...")
    
    # ------------------------------------------------------------
    # Load Data (following Stata code lines 1-25 exactly)
    # ------------------------------------------------------------
    
    # --- Prepare GVKEY-PERMNO crosswalk
    print("Loading CCMLinkingTable...")
    crosswalk = pd.read_parquet('../pyData/Intermediate/CCMLinkingTable.parquet',
                                columns=['gvkey', 'permno', 'timeLinkStart_d', 'timeLinkEnd_d'])
    print(f"Initial crosswalk shape: {crosswalk.shape}")
    
    # destring gvkey, replace
    crosswalk['gvkey'] = pd.to_numeric(crosswalk['gvkey'], errors='coerce')
    
    # save "$pathtemp/tempCW", replace  
    tempCW = crosswalk.copy()
    print(f"tempCW shape after destring: {tempCW.shape}")
    
    # --- Prepare monthly CRSP returns
    print("Loading monthlyCRSP...")
    crsp_df = pd.read_parquet('../pyData/Intermediate/monthlyCRSP.parquet',
                             columns=['permno', 'time_avail_m', 'ret'])
    print(f"Initial CRSP shape: {crsp_df.shape}")
    
    # keep permno time_avail_m ret (already done in loading)
    # save "$pathtemp/tempCRSP", replace
    tempCRSP = crsp_df.copy()
    print(f"tempCRSP shape: {tempCRSP.shape}")
    
    # --- Annual sales from CS
    print("Loading a_aCompustat...")
    compustat_annual = pd.read_parquet('../pyData/Intermediate/a_aCompustat.parquet',
                                       columns=['gvkey', 'permno', 'sale', 'fyear'])
    print(f"Initial compustat annual shape: {compustat_annual.shape}")
    
    # rename sale saleACS
    compustat_annual = compustat_annual.rename(columns={'sale': 'saleACS'})
    
    # drop if saleACS <0 | mi(saleACS)
    # Apply Trap #1: Stata's inequality behavior - use stata_ineq_pd for < comparison
    mask_keep = ~(stata_ineq_pd(compustat_annual['saleACS'], "<", 0) | compustat_annual['saleACS'].isna())
    compustat_annual = compustat_annual[mask_keep]
    
    # save "$pathtemp/tempCS", replace
    tempCS = compustat_annual.copy()
    print(f"tempCS shape after filtering: {tempCS.shape}")
    
    # --- Conglomerates from CS segment data
    print("Loading CompustatSegments...")
    segments_df = pd.read_parquet('../pyData/Intermediate/CompustatSegments.parquet',
                                 columns=['gvkey', 'datadate', 'stype', 'sics1', 'sales'])
    print(f"Initial segments shape: {segments_df.shape}")
    
    # keep if stype == "OPSEG" | stype == "BUSSEG"
    segments_df = segments_df[segments_df['stype'].isin(['OPSEG', 'BUSSEG'])]
    print(f"After stype filter: {segments_df.shape}")
    
    # drop if sales < 0 | mi(sales)
    # Apply Trap #1: Stata's inequality behavior
    mask_keep = ~(stata_ineq_pd(segments_df['sales'], "<", 0) | segments_df['sales'].isna())
    segments_df = segments_df[mask_keep]
    print(f"After sales filter: {segments_df.shape}")
    
    # tostring sics1, replace
    segments_df['sics1'] = segments_df['sics1'].astype(str)
    
    # ------------------------------------------------------------
    # Identify Conglomerates (following Stata code lines 27-46 exactly)
    # ------------------------------------------------------------
    print("Identifying conglomerates...")
    
    # gen sic2D = substr(sics1, 1,2)
    segments_df['sic2D'] = segments_df['sics1'].str[:2]
    
    # gcollapse (sum) sales, by(gvkey sic2D datadate)
    segments_agg = segments_df.groupby(['gvkey', 'sic2D', 'datadate'])['sales'].sum().reset_index()
    print(f"After collapse: {segments_agg.shape}")
    
    # gen fyear = yofd(datadate)
    segments_agg['fyear'] = pd.to_datetime(segments_agg['datadate']).dt.year
    
    # merge m:1 gvkey fyear using "$pathtemp/tempCS", keep(match) nogenerate
    segments_agg = pd.merge(segments_agg, tempCS, on=['gvkey', 'fyear'], how='inner')
    print(f"After merge with tempCS: {segments_agg.shape}")
    print(f"Columns after merge: {list(segments_agg.columns)}")
    
    # egen temptotalSales = total(sales), by(gvkey fyear)
    segments_agg['temptotalSales'] = segments_agg.groupby(['gvkey', 'fyear'])['sales'].transform('sum')
    
    # gen tempCSSegmentShare = sales/saleACS
    segments_agg['tempCSSegmentShare'] = segments_agg['sales'] / segments_agg['saleACS']
    
    # bys gvkey datadate: gen tempNInd = _N
    segments_agg['tempNInd'] = segments_agg.groupby(['gvkey', 'datadate']).transform('size')
    
    # tab tempNInd
    print(f"Industry count distribution:\\n{segments_agg['tempNInd'].value_counts().head()}")
    
    # Apply conglomerate classification logic exactly as Stata
    # gen Conglomerate = 0 if tempNInd == 1 & tempCSSegmentShare > .8
    # replace Conglomerate = 1 if tempNInd > 1 & tempCSSegmentShare > .8
    
    segments_agg['Conglomerate'] = np.nan
    
    # Stand-alone: tempNInd == 1 & tempCSSegmentShare > 0.8
    # Apply Trap #1: Use stata_ineq_pd for > comparison with missing values
    mask_standalone = (segments_agg['tempNInd'] == 1) & stata_ineq_pd(segments_agg['tempCSSegmentShare'], ">", 0.8)
    segments_agg.loc[mask_standalone, 'Conglomerate'] = 0
    
    # Conglomerate: tempNInd > 1 & tempCSSegmentShare > 0.8
    mask_conglomerate = (segments_agg['tempNInd'] > 1) & stata_ineq_pd(segments_agg['tempCSSegmentShare'], ">", 0.8)
    segments_agg.loc[mask_conglomerate, 'Conglomerate'] = 1
    
    # drop if mi(Conglomerate)
    segments_agg = segments_agg.dropna(subset=['Conglomerate'])
    print(f"After dropping missing Conglomerate: {segments_agg.shape}")
    
    # tab Conglomerate
    print(f"Conglomerate distribution:\\n{segments_agg['Conglomerate'].value_counts()}")
    
    # save tempConglomerate, replace
    tempConglomerate = segments_agg.copy()
    
    # ------------------------------------------------------------
    # Calculate Industry Returns (following Stata code lines 48-76 exactly)
    # ------------------------------------------------------------
    print("Calculating industry returns from stand-alones...")
    
    # Industry returns from stand-alones
    # keep if Conglomerate == 0
    stand_alone = tempConglomerate[tempConglomerate['Conglomerate'] == 0].copy()
    print(f"Stand-alone segments shape: {stand_alone.shape}")
    
    # Add identifiers for merging with stock returns
    # joinby gvkey using "$pathtemp/tempCW", update
    stand_alone = pd.merge(stand_alone, tempCW, on='gvkey', how='left')
    print(f"After merge with tempCW: {stand_alone.shape}")
    print(f"Columns after merge: {list(stand_alone.columns)}")
    
    # Use only if data date is within the validity period of the link
    # gen temp = (timeLinkStart_d <= datadate  & datadate <= timeLinkEnd_d)
    # Apply Trap #1: Handle missing dates according to Stata's infinity behavior
    
    # In Stata: missing <= anything is FALSE, anything <= missing is TRUE
    # For the AND condition to be TRUE, both parts must be TRUE
    condition1 = pd.Series(True, index=stand_alone.index)  # Default to True
    condition2 = pd.Series(True, index=stand_alone.index)  # Default to True
    
    # timeLinkStart_d <= datadate: if timeLinkStart_d is missing, this is FALSE
    mask_start_missing = stand_alone['timeLinkStart_d'].isna()
    mask_start_valid = ~mask_start_missing & (stand_alone['timeLinkStart_d'] <= stand_alone['datadate'])
    condition1 = mask_start_valid & ~mask_start_missing
    
    # datadate <= timeLinkEnd_d: if timeLinkEnd_d is missing, this is TRUE 
    mask_end_missing = stand_alone['timeLinkEnd_d'].isna()
    mask_end_valid = mask_end_missing | (stand_alone['datadate'] <= stand_alone['timeLinkEnd_d'])
    condition2 = mask_end_valid
    
    # If datadate is missing, both conditions become FALSE and TRUE respectively
    mask_data_missing = stand_alone['datadate'].isna()
    condition1 = condition1 & ~mask_data_missing  # datadate missing makes first condition FALSE
    condition2 = condition2 | mask_data_missing   # datadate missing makes second condition TRUE
    
    stand_alone['temp'] = condition1 & condition2
    
    # tab temp  
    print(f"Valid links: {stand_alone['temp'].sum():,} out of {len(stand_alone):,}")
    
    # keep if temp == 1
    stand_alone = stand_alone[stand_alone['temp'] == 1]
    
    # drop temp
    stand_alone = stand_alone.drop('temp', axis=1)
    print(f"After link validity filter: {stand_alone.shape}")
    
    # Merge stock returns
    # keep permno sic2D fyear
    # Handle permno column after merge (might be permno_x or permno_y)
    permno_col = 'permno_y' if 'permno_y' in stand_alone.columns else 'permno_x' if 'permno_x' in stand_alone.columns else 'permno'
    stand_alone = stand_alone[[permno_col, 'sic2D', 'fyear']].copy()
    if permno_col != 'permno':
        stand_alone = stand_alone.rename(columns={permno_col: 'permno'})
    
    # duplicates drop
    stand_alone = stand_alone.drop_duplicates()
    print(f"After duplicates drop: {stand_alone.shape}")
    
    # rename sic2D sic2DCSS  
    stand_alone = stand_alone.rename(columns={'sic2D': 'sic2DCSS'})
    
    # joinby permno using "$pathtemp/tempCRSP", unmatched(none)
    stand_alone = pd.merge(stand_alone, tempCRSP, on='permno', how='inner')
    print(f"After merge with tempCRSP: {stand_alone.shape}")
    
    # gen year = yofd(dofm(time_avail_m))
    stand_alone['year'] = pd.to_datetime(stand_alone['time_avail_m']).dt.year
    
    # keep if fyear == year
    stand_alone = stand_alone[stand_alone['fyear'] == stand_alone['year']]
    print(f"After year filter: {stand_alone.shape}")
    
    # gcollapse (mean) ret, by(sic2DCSS time_avail_m)
    industry_returns = stand_alone.groupby(['sic2DCSS', 'time_avail_m'])['ret'].mean().reset_index()
    
    # drop if sic2DCSS == "."
    industry_returns = industry_returns[industry_returns['sic2DCSS'] != '.']
    
    # save "$pathtemp/tempReturns", replace
    tempReturns = industry_returns.copy()
    print(f"Industry returns shape: {tempReturns.shape}")
    
    # ------------------------------------------------------------
    # SIGNAL CONSTRUCTION: CONGLOMERATE RETURNS (following Stata code lines 78-106)
    # ------------------------------------------------------------
    print("Constructing conglomerate returns signal...")
    
    # SIGNAL CONSTRUCTION
    # Now, match industry returns of stand-alones to conglomerates
    # use tempConglomerate, clear
    conglomerates = tempConglomerate[tempConglomerate['Conglomerate'] == 1].copy()
    print(f"Conglomerate segments shape: {conglomerates.shape}")
    
    # keep permno sic2D sales fyear
    conglomerates = conglomerates[['permno', 'sic2D', 'sales', 'fyear']].copy()
    
    # rename sic2D sic2DCSS
    conglomerates = conglomerates.rename(columns={'sic2D': 'sic2DCSS'})
    
    # drop if sic2DCSS == "."
    conglomerates = conglomerates[conglomerates['sic2DCSS'] != '.']
    print(f"After dropping missing sic2DCSS: {conglomerates.shape}")
    
    # joinby sic2DCSS using "$pathtemp/tempReturns", unmatched(none)
    conglomerates = pd.merge(conglomerates, tempReturns, on='sic2DCSS', how='inner')
    print(f"After merge with industry returns: {conglomerates.shape}")
    
    # gen year = yofd(dofm(time_avail_m))
    conglomerates['year'] = pd.to_datetime(conglomerates['time_avail_m']).dt.year
    
    # keep if fyear == year
    conglomerates = conglomerates[conglomerates['fyear'] == conglomerates['year']]
    print(f"After year filter: {conglomerates.shape}")
    
    # Now take weighted return
    # egen tempTotal = total(sales), by(permno time_avail_m)
    conglomerates['tempTotal'] = conglomerates.groupby(['permno', 'time_avail_m'])['sales'].transform('sum')
    
    # gen tempweight = sales/tempTotal
    conglomerates['tempweight'] = conglomerates['sales'] / conglomerates['tempTotal']
    
    # DEBUG: Check weights like original code comment
    print(f"Weight distribution:\\n{conglomerates['tempweight'].describe()}")
    print(f"Number of observations with weight < 1: {(conglomerates['tempweight'] < 1.0).sum()}")
    
    # gcollapse (mean) ret [iweight = tempweight], by(permno time_avail_m)
    # Stata's iweight collapse is equivalent to weighted average
    conglomerates['weighted_ret'] = conglomerates['ret'] * conglomerates['tempweight']
    result = conglomerates.groupby(['permno', 'time_avail_m'])['weighted_ret'].sum().reset_index()
    
    # rename ret retConglomerate
    result = result.rename(columns={'weighted_ret': 'retConglomerate'})
    # label var retConglomerate "Conglomerate return" - not needed in Python
    
    print(f"Final result shape: {result.shape}")
    
    # ------------------------------------------------------------
    # SAVE (following Stata code line 106)
    # ------------------------------------------------------------
    print("Saving predictor...")
    save_predictor(result, 'retConglomerate')
    
    print("retConglomerate predictor completed successfully!")

if __name__ == "__main__":
    main()
    