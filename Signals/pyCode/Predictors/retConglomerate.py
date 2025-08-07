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

def main():
    print("Starting retConglomerate predictor...")
    
    # DATA LOAD
    # Prepare crosswalk
    print("Loading CCMLinkingTable...")
    crosswalk = pd.read_parquet('../pyData/Intermediate/CCMLinkingTable.parquet',
                                columns=['gvkey', 'permno', 'timeLinkStart_d', 'timeLinkEnd_d'])
    # destring gvkey, replace
    crosswalk['gvkey'] = pd.to_numeric(crosswalk['gvkey'], errors='coerce')
    # save "$pathtemp/tempCW", replace
    tempCW = crosswalk.copy()
    print(f"Loaded {len(tempCW):,} linking records")
    
    # Prepare returns
    print("Loading monthlyCRSP...")
    crsp_df = pd.read_parquet('../pyData/Intermediate/monthlyCRSP.parquet',
                             columns=['permno', 'time_avail_m', 'ret'])
    # save "$pathtemp/tempCRSP", replace
    tempCRSP = crsp_df.copy()
    print(f"Loaded {len(tempCRSP):,} CRSP returns")
    
    # Annual sales from CS
    print("Loading a_aCompustat...")
    compustat_annual = pd.read_parquet('../pyData/Intermediate/a_aCompustat.parquet',
                                       columns=['gvkey', 'permno', 'sale', 'fyear'])
    # rename sale saleACS
    compustat_annual = compustat_annual.rename(columns={'sale': 'saleACS'})
    # drop if saleACS <0 | mi(saleACS)
    compustat_annual = compustat_annual[(compustat_annual['saleACS'] > 0) & compustat_annual['saleACS'].notna()]
    # save "$pathtemp/tempCS", replace
    tempCS = compustat_annual.copy()
    print(f"Loaded {len(tempCS):,} annual sales records")
    
    # Conglomerates from CS segment data
    print("Loading CompustatSegments...")
    segments_df = pd.read_parquet('../pyData/Intermediate/CompustatSegments.parquet',
                                 columns=['gvkey', 'datadate', 'stype', 'sics1', 'sales'])
    # keep if stype == "OPSEG" | stype == "BUSSEG"
    segments_df = segments_df[segments_df['stype'].isin(['OPSEG', 'BUSSEG'])]
    # drop if sales < 0 | mi(sales)
    segments_df = segments_df[(segments_df['sales'] > 0) & segments_df['sales'].notna()]
    # tostring sics1, replace
    segments_df['sics1'] = segments_df['sics1'].astype(str)
    # gen sic2D = substr(sics1, 1,2)
    segments_df['sic2D'] = segments_df['sics1'].str[:2]
    
    # gcollapse (sum) sales, by(gvkey sic2D datadate)
    segments_agg = segments_df.groupby(['gvkey', 'sic2D', 'datadate'])['sales'].sum().reset_index()
    
    # gen fyear = yofd(datadate)
    segments_agg['fyear'] = pd.to_datetime(segments_agg['datadate']).dt.year
    
    # merge m:1 gvkey fyear using "$pathtemp/tempCS", keep(match) nogenerate
    segments_agg = pd.merge(segments_agg, tempCS, on=['gvkey', 'fyear'], how='inner')
    
    # egen temptotalSales = total(sales), by(gvkey fyear)
    segments_agg['temptotalSales'] = segments_agg.groupby(['gvkey', 'fyear'])['sales'].transform('sum')
    
    # gen tempCSSegmentShare = sales/saleACS
    segments_agg['tempCSSegmentShare'] = segments_agg['sales'] / segments_agg['saleACS']
    
    # bys gvkey datadate: gen tempNInd = _N
    segments_agg['tempNInd'] = segments_agg.groupby(['gvkey', 'datadate'])['gvkey'].transform('count')
    
    # tab tempNInd
    print(f"Industry count distribution:\n{segments_agg['tempNInd'].value_counts().head()}")
    
    # gen Conglomerate = 0 if tempNInd == 1 & tempCSSegmentShare > .8
    # replace Conglomerate = 1 if tempNInd > 1 & tempCSSegmentShare > .8
    segments_agg['Conglomerate'] = np.where(
        (segments_agg['tempNInd'] == 1) & (segments_agg['tempCSSegmentShare'] > 0.8), 0,
        np.where((segments_agg['tempNInd'] > 1) & (segments_agg['tempCSSegmentShare'] > 0.8), 1, np.nan)
    )
    
    # drop if mi(Conglomerate)
    segments_agg = segments_agg.dropna(subset=['Conglomerate'])
    
    # tab Conglomerate
    print(f"Conglomerate distribution:\n{segments_agg['Conglomerate'].value_counts()}")
    
    # save tempConglomerate, replace
    tempConglomerate = segments_agg.copy()
    
    # Industry returns from stand-alones
    # keep if Conglomerate == 0
    stand_alone = tempConglomerate[tempConglomerate['Conglomerate'] == 0].copy()
    
    # Add identifiers for merging with stock returns
    # joinby gvkey using "$pathtemp/tempCW", update
    stand_alone = pd.merge(stand_alone, tempCW, on='gvkey', how='left')
    
    # Use only if data date is within the validity period of the link
    # gen temp = (timeLinkStart_d <= datadate  & datadate <= timeLinkEnd_d)
    stand_alone['temp'] = (
        (stand_alone['timeLinkStart_d'] <= stand_alone['datadate']) & 
        (stand_alone['datadate'] <= stand_alone['timeLinkEnd_d'])
    )
    
    # tab temp
    print(f"Valid links: {stand_alone['temp'].sum():,} out of {len(stand_alone):,}")
    
    # keep if temp == 1
    stand_alone = stand_alone[stand_alone['temp'] == 1]
    # drop temp
    stand_alone = stand_alone.drop('temp', axis=1)
    
    # Merge stock returns
    # keep permno sic2D fyear
    # Note: permno comes from the merge with tempCW
    if 'permno' not in stand_alone.columns:
        print("Warning: permno not in columns after merge. Available columns:", stand_alone.columns.tolist())
        # The merge with tempCW should have added permno - check if it's named differently
        stand_alone = stand_alone[['permno_y' if 'permno_y' in stand_alone.columns else 'permno_x', 'sic2D', 'fyear']].copy()
        # Rename to standard permno
        if 'permno_y' in stand_alone.columns or 'permno_x' in stand_alone.columns:
            stand_alone = stand_alone.rename(columns={'permno_y': 'permno', 'permno_x': 'permno'})
    else:
        stand_alone = stand_alone[['permno', 'sic2D', 'fyear']].copy()
    # duplicates drop
    stand_alone = stand_alone.drop_duplicates()
    
    # rename sic2D sic2DCSS
    stand_alone = stand_alone.rename(columns={'sic2D': 'sic2DCSS'})
    
    # joinby permno using "$pathtemp/tempCRSP", unmatched(none)
    stand_alone = pd.merge(stand_alone, tempCRSP, on='permno', how='inner')
    
    # gen year = yofd(dofm(time_avail_m))
    stand_alone['year'] = pd.to_datetime(stand_alone['time_avail_m']).dt.year
    
    # keep if fyear == year
    stand_alone = stand_alone[stand_alone['fyear'] == stand_alone['year']]
    
    # gcollapse (mean) ret, by(sic2DCSS time_avail_m)
    industry_returns = stand_alone.groupby(['sic2DCSS', 'time_avail_m'])['ret'].mean().reset_index()
    
    # drop if sic2DCSS == "."
    industry_returns = industry_returns[industry_returns['sic2DCSS'] != '.']
    
    # save "$pathtemp/tempReturns", replace
    tempReturns = industry_returns.copy()
    print(f"Calculated industry returns for {len(tempReturns):,} industry-months")
    
    # SIGNAL CONSTRUCTION
    # Now, match industry returns of stand-alones to conglomerates
    # use tempConglomerate, clear
    conglomerates = tempConglomerate[tempConglomerate['Conglomerate'] == 1].copy()
    
    # keep permno sic2D sales fyear
    conglomerates = conglomerates[['permno', 'sic2D', 'sales', 'fyear']].copy()
    
    # rename sic2D sic2DCSS
    conglomerates = conglomerates.rename(columns={'sic2D': 'sic2DCSS'})
    
    # drop if sic2DCSS == "."
    conglomerates = conglomerates[conglomerates['sic2DCSS'] != '.']
    
    # joinby sic2DCSS using "$pathtemp/tempReturns", unmatched(none)
    conglomerates = pd.merge(conglomerates, tempReturns, on='sic2DCSS', how='inner')
    
    # gen year = yofd(dofm(time_avail_m))
    conglomerates['year'] = pd.to_datetime(conglomerates['time_avail_m']).dt.year
    
    # keep if fyear == year
    conglomerates = conglomerates[conglomerates['fyear'] == conglomerates['year']]
    
    # Now take weighted return
    # egen tempTotal = total(sales), by(permno time_avail_m)
    conglomerates['tempTotal'] = conglomerates.groupby(['permno', 'time_avail_m'])['sales'].transform('sum')
    
    # gen tempweight = sales/tempTotal
    conglomerates['tempweight'] = conglomerates['sales'] / conglomerates['tempTotal']
    
    # ALL WEIGHTS ALMOST 1. WHERE ARE THE CONGLOMERATES?
    print(f"Weight distribution:\n{conglomerates['tempweight'].describe()}")
    
    # gcollapse (mean) ret [iweight = tempweight], by(permno time_avail_m)
    # Weighted average using groupby
    conglomerates['weighted_ret'] = conglomerates['ret'] * conglomerates['tempweight']
    result = conglomerates.groupby(['permno', 'time_avail_m'])['weighted_ret'].sum().reset_index()
    
    # rename ret retConglomerate
    result = result.rename(columns={'weighted_ret': 'retConglomerate'})
    
    print(f"Generated retConglomerate for {len(result):,} observations")
    
    # SAVE
    print("Saving predictor...")
    save_predictor(result, 'retConglomerate')
    
    print("retConglomerate predictor completed successfully!")

if __name__ == "__main__":
    main()