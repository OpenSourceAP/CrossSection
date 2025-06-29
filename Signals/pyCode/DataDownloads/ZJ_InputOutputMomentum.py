# ABOUTME: Downloads BEA Input-Output tables and creates customer/supplier momentum signals
# ABOUTME: Complete rewrite following R script ZJR_InputOutputMomentum.R exactly

import pandas as pd
import numpy as np
import requests
import zipfile
import tempfile
import os
from pathlib import Path
import re
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def generate_one_iomom(sheet63, sheet97, momentum_type):
    """
    Generate Input-Output momentum signals for one type (customer or supplier).
    
    This function exactly replicates the R function generate_one_iomom() from lines 60-302.
    
    Args:
        sheet63: Path to 1963-1996 Excel file
        sheet97: Path to 1997+ Excel file  
        momentum_type: 'customer' or 'supplier'
    
    Returns:
        DataFrame with columns: gvkey, year_avail, month_avail, beaind, retmatch, portind
    """
    logger.info(f"Processing {momentum_type} momentum...")
    
    # Read in IO tables - exactly matching R lines 71-146
    indweight = []
    
    # Process 1963-1996 data (R lines 74-107)
    logger.info("Processing 1963-1996 data...")
    xl_file = pd.ExcelFile(sheet63)
    yearlist = [sheet for sheet in xl_file.sheet_names if sheet not in ['Cover', 'Contents', 'ReadMe']]
    yearlist = [sheet for sheet in yearlist if sheet.isdigit()]  # Only numeric years
    
    for year in yearlist:
        logger.info(f"Processing year {year} from 1963-1996...")
        
        # Read sheet (R line 79: skip = 6)
        temp1 = pd.read_excel(sheet63, sheet_name=year, skiprows=6)
        if len(temp1.columns) < 2:
            logger.warning(f"Skipping sheet {year} - insufficient columns")
            continue
            
        # R line 80: rename(beaind = Code)
        temp1 = temp1.rename(columns={temp1.columns[0]: 'beaind'})
        # R line 81: select(-c(2))
        temp1 = temp1.drop(columns=[temp1.columns[1]])
        # R line 82: mutate_at(vars(-beaind), as.numeric)
        for col in temp1.columns[1:]:
            temp1[col] = pd.to_numeric(temp1[col], errors='coerce')
        
        # R lines 85-96: transpose if supplier momentum
        if momentum_type == 'supplier':
            # R line 87: tempa = temp1 %>% select(-c(beaind))
            tempa = temp1.drop(columns=['beaind'])
            # R line 88: rownames(tempa) = temp1$beaind
            tempa.index = temp1['beaind']
            # R line 89: tempb = tempa %>% as.matrix %>% t() %>% as.data.frame
            tempb = pd.DataFrame(tempa.values.T, columns=tempa.index, index=tempa.columns)
            # R lines 91-94: add industry column
            temp1 = pd.DataFrame({'beaind': tempb.index}).reset_index(drop=True)
            temp1 = pd.concat([temp1, tempb.reset_index(drop=True)], axis=1)
        
        # R lines 99-103: convert to long and add year
        temp2 = temp1.melt(id_vars=['beaind'], var_name='beaindmatch', value_name='weight')
        temp2 = temp2.dropna(subset=['weight'])
        temp2['year_avail'] = int(year) + 5  # R line 103: +5 year lag
        
        indweight.append(temp2)
    
    # Process 1997+ data (R lines 112-146)
    logger.info("Processing 1997+ data...")
    xl_file = pd.ExcelFile(sheet97)
    yearlist = [sheet for sheet in xl_file.sheet_names if sheet.isdigit()]
    
    for year in yearlist:
        logger.info(f"Processing year {year} from 1997+...")
        
        # Read sheet (R line 116: skip = 5)
        temp1 = pd.read_excel(sheet97, sheet_name=year, skiprows=5)
        if len(temp1.columns) < 2:
            logger.warning(f"Skipping sheet {year} - insufficient columns")
            continue
            
        # R line 117: rename(beaind = "...1")
        temp1 = temp1.rename(columns={temp1.columns[0]: 'beaind'})
        # R line 118: filter(beaind != "IOCode")
        temp1 = temp1[temp1['beaind'] != 'IOCode']
        # R line 119: select(-c(2))
        temp1 = temp1.drop(columns=[temp1.columns[1]])
        # R line 120: mutate_at(vars(-beaind), as.numeric)
        for col in temp1.columns[1:]:
            temp1[col] = pd.to_numeric(temp1[col], errors='coerce')
        
        # R lines 124-134: transpose if supplier momentum
        if momentum_type == 'supplier':
            # R line 125: tempa = temp1 %>% select(-c(beaind))
            tempa = temp1.drop(columns=['beaind'])
            # R line 126: rownames(tempa) = temp1$beaind
            tempa.index = temp1['beaind']
            # R line 127: tempb = tempa %>% as.matrix %>% t() %>% as.data.frame
            tempb = pd.DataFrame(tempa.values.T, columns=tempa.index, index=tempa.columns)
            # R lines 129-132: temp = cbind(tempc, tempb) (NOTE: temp1 in R line 138)
            temp1 = pd.DataFrame({'beaind': tempb.index}).reset_index(drop=True)
            temp1 = pd.concat([temp1, tempb.reset_index(drop=True)], axis=1)
        
        # R lines 138-142: convert to long and add year (NOTE: temp1 not temp)
        temp2 = temp1.melt(id_vars=['beaind'], var_name='beaindmatch', value_name='weight')
        temp2 = temp2.dropna(subset=['weight'])
        temp2['year_avail'] = int(year) + 5  # R line 142: +5 year lag
        
        indweight.append(temp2)
    
    # Combine all years
    indweight_df = pd.concat(indweight, ignore_index=True)
    logger.info(f"Combined I-O weights: {len(indweight_df):,} rows")
    
    # Load global datasets comp0, crsp0, ccm0 (these should be loaded globally)
    global comp0, crsp0, ccm0
    
    # Assign Compustat firm-years to BEA industries (R lines 151-189)
    logger.info("Creating industry mapping...")
    
    # R lines 152-156: create indlist with NAICS prefix
    indlist = indweight_df[['year_avail', 'beaind']].drop_duplicates()
    # R line 154: gsub("([0-9]+).*$", "\\1", beaind)
    indlist['naicspre'] = indlist['beaind'].str.extract(r'^(\d+)').astype(float)
    indlist = indlist.dropna(subset=['naicspre'])
    indlist['naicspre'] = indlist['naicspre'].astype(int)
    
    # R lines 162-167: create 2, 3, 4 digit NAICS codes
    temp1 = comp0.copy()
    temp1['naics2'] = np.floor(temp1['naics6'] / 1e4).astype(int)  # R: floor(naics6/1e4)
    temp1['naics3'] = np.floor(temp1['naics6'] / 1e3).astype(int)  # R: floor(naics6/1e3)
    temp1['naics4'] = np.floor(temp1['naics6'] / 1e2).astype(int)  # R: floor(naics6/1e2)
    
    # R lines 169-187: three separate left_join operations
    temp2 = temp1.merge(
        indlist.rename(columns={'beaind': 'beaind2'}),
        left_on=['year_avail', 'naics2'],
        right_on=['year_avail', 'naicspre'],
        how='left'
    )
    temp2 = temp2.merge(
        indlist.rename(columns={'beaind': 'beaind3'}),
        left_on=['year_avail', 'naics3'],
        right_on=['year_avail', 'naicspre'],
        how='left',
        suffixes=('', '_3')
    )
    temp2 = temp2.merge(
        indlist.rename(columns={'beaind': 'beaind4'}),
        left_on=['year_avail', 'naics4'],
        right_on=['year_avail', 'naicspre'],
        how='left',
        suffixes=('', '_4')
    )
    
    # R line 184: coalesce(beaind4, beaind3, beaind2)
    temp2['beaind'] = temp2['beaind4'].fillna(temp2['beaind3'].fillna(temp2['beaind2']))
    
    # R lines 185-187: select and filter
    comp = temp2[['gvkey', 'year_avail', 'naics6', 'beaind']].copy()
    comp = comp.dropna(subset=['beaind'])
    
    logger.info(f"Industry mapping: {len(comp):,} firm-years mapped")
    
    # Create BEA industry returns (R lines 193-220)
    logger.info("Creating industry returns...")
    
    # R lines 194-201: add gvkey to crsp
    temp1 = crsp0.merge(ccm0, on='permno', how='left')
    temp1 = temp1[(temp1['date'] >= temp1['linkdt']) & (temp1['date'] <= temp1['linkenddt'])]
    temp1 = temp1[['permno', 'date', 'ret', 'mve_c', 'gvkey']].copy()
    temp1['year'] = temp1['date'].dt.year
    temp1['month'] = temp1['date'].dt.month
    
    # R line 203: add bea industries
    temp2 = temp1.merge(comp, left_on=['gvkey', 'year'], right_on=['gvkey', 'year_avail'], how='left')
    temp2 = temp2.dropna(subset=['beaind'])
    crsp2 = temp2
    
    # R lines 209-214: create industry returns
    indret = crsp2.groupby(['year', 'month', 'beaind']).apply(
        lambda x: pd.Series({
            'ret': np.average(x['ret'], weights=x['mve_c']),
            'n': len(x)
        }), include_groups=False
    ).reset_index()
    
    # R line 218: remove years where NAICS is unavailable
    indret = indret[indret['year'] >= 1986]
    
    logger.info(f"Industry returns: {len(indret):,} observations")
    
    # Create matched industry return (R lines 225-244)
    logger.info("Creating matched industry returns...")
    
    # R lines 226-230: expand indweights and remove own-industry weights
    temp1 = indret[['year', 'month']].drop_duplicates().merge(
        indweight_df[indweight_df['beaind'] != indweight_df['beaindmatch']], 
        left_on='year', 
        right_on='year_avail',
        how='left'
    )
    
    # R lines 232-237: add matched-industry's returns
    temp2 = temp1.merge(
        indret[['year', 'month', 'beaind', 'ret']].rename(columns={'ret': 'retmatch', 'beaind': 'beaindmatch'}),
        on=['year', 'month', 'beaindmatch'],
        how='left'
    )
    temp2 = temp2.dropna(subset=['retmatch'])
    
    # R lines 239-243: find means using IO weights
    def safe_weighted_average(group):
        weights = group['weight']
        values = group['retmatch']
        
        # Handle zero weights by filtering them out
        valid_mask = (weights > 0) & (~pd.isna(weights)) & (~pd.isna(values))
        if valid_mask.sum() == 0:
            return pd.Series({'retmatch': np.nan})
        
        weights_clean = weights[valid_mask]
        values_clean = values[valid_mask]
        
        if weights_clean.sum() == 0:
            return pd.Series({'retmatch': np.nan})
        
        return pd.Series({
            'retmatch': np.average(values_clean, weights=weights_clean)
        })
    
    matchret = temp2.groupby(['year', 'month', 'beaind']).apply(
        safe_weighted_average, include_groups=False
    ).reset_index()
    
    # Remove NaN results
    matchret = matchret.dropna(subset=['retmatch'])
    
    logger.info(f"Matched returns: {len(matchret):,} observations")
    
    # Create firm level signal (R lines 251-300)
    logger.info("Creating firm-level signals...")
    
    # R lines 251-256: assign industries to portfolios each month
    def find_interval_quantiles(x):
        """Replicate R's findInterval with quantiles"""
        if len(x) < 2:
            return pd.Series([1] * len(x), index=x.index)
        
        # Get quantiles for bins
        quantiles = x.quantile([i/10 for i in range(11)]).values
        
        # Remove duplicates to handle edge cases
        unique_quantiles = pd.Series(quantiles).drop_duplicates().values
        
        if len(unique_quantiles) < 2:
            return pd.Series([1] * len(x), index=x.index)
        
        # Use pd.cut with proper number of labels
        try:
            bins = pd.cut(x, bins=unique_quantiles, labels=range(1, len(unique_quantiles)), 
                         include_lowest=True, duplicates='drop')
            result = pd.to_numeric(bins, errors='coerce').fillna(1).astype(int)
            return result
        except ValueError:
            # Fallback to ranking approach if cut fails
            ranks = x.rank(method='first', pct=True)
            portind = (ranks * 10).apply(lambda r: min(int(r) + 1, 10))
            return portind
    
    tempportind = matchret.dropna(subset=['retmatch']).copy()
    tempportind['portind'] = tempportind.groupby(['year', 'month'])['retmatch'].transform(find_interval_quantiles)
    
    # R lines 259-266: assign gvkey-months to industry portfolios (crossing logic)
    months_df = pd.DataFrame({'month_avail': range(1, 13)})
    # R equivalent of crossing(comp, data.frame(month_avail = 1:12))
    iomom = comp.merge(months_df, how='cross')
    
    # Add momentum signals
    iomom = iomom.merge(
        tempportind[['year', 'month', 'beaind', 'retmatch', 'portind']],
        left_on=['year_avail', 'month_avail', 'beaind'],
        right_on=['year', 'month', 'beaind'],
        how='left'
    )
    
    # R lines 269-298: validation check (stock assignments)
    logger.info("Validating stock assignments...")
    temp = crsp2.merge(
        iomom,
        left_on=['gvkey', 'year', 'month'],
        right_on=['gvkey', 'year_avail', 'month_avail'],
        how='left'
    )
    temp['iomom'] = temp.groupby('gvkey')['portind'].shift(1)  # R: lag(portind, n = 1)
    
    # Debug: check column names after merge
    logger.debug(f"Temp columns after merge: {temp.columns.tolist()}")
    
    # Use the year/month columns that exist (should be from crsp2)
    year_col = 'year' if 'year' in temp.columns else 'year_x'
    month_col = 'month' if 'month' in temp.columns else 'month_x'
    
    validation = temp.groupby([year_col, month_col, 'iomom']).agg({
        'ret': 'mean',
        'gvkey': 'count'
    }).rename(columns={'gvkey': 'nind'}).reset_index()
    validation = validation.rename(columns={year_col: 'year', month_col: 'month'})
    
    validation_summary = validation.pivot_table(
        index=['year', 'month'], 
        columns='iomom', 
        values='ret', 
        fill_value=np.nan
    )
    if len(validation_summary.columns) >= 10:
        validation_summary['portLS'] = validation_summary.iloc[:, -1] - validation_summary.iloc[:, 0]
    
    # Calculate summary statistics
    validation_stats = validation.groupby('iomom').agg({
        'ret': ['mean', 'std', 'count']
    }).reset_index()
    validation_stats.columns = ['port', 'mean', 'vol', 'nmonths']
    validation_stats['tstat'] = validation_stats['mean'] / validation_stats['vol'] * np.sqrt(validation_stats['nmonths'])
    
    logger.info("Validation statistics:")
    logger.info(validation_stats.to_string())
    
    # R line 300: return iomom
    return iomom[['gvkey', 'year_avail', 'month_avail', 'beaind', 'retmatch', 'portind']].copy()


def load_raw_data():
    """Load raw data exactly matching R lines 309-341"""
    logger.info("Loading raw data...")
    
    # R lines 309-319: read compustat
    comp0 = pd.read_csv("../pyData/Intermediate/CompustatAnnual.csv")
    
    # R lines 312-318: process compustat exactly like R
    comp0['naicsstr'] = comp0['naicsh'].astype(str).str.pad(width=6, side='right', fillchar='0')  # R: str_pad(..., 6, "right", "0")
    comp0['naics6'] = pd.to_numeric(comp0['naicsstr'], errors='coerce')
    
    # R line 316: year(dmy(datadate) %m+% months(6) )+1
    comp0['datadate'] = pd.to_datetime(comp0['datadate'], format='%d%b%Y')  # R: dmy()
    comp0['year_avail'] = (comp0['datadate'] + pd.DateOffset(months=6)).dt.year + 1
    
    comp0 = comp0.dropna(subset=['naics6'])
    comp0 = comp0[['gvkey', 'year_avail', 'naics6', 'datadate']].copy()
    
    # R lines 322-329: read crsp
    crsp0 = pd.read_csv("../pyData/Intermediate/mCRSP.csv")
    crsp0['date'] = pd.to_datetime(crsp0['date'], format='%d%b%Y')  # R: dmy()
    crsp0['ret'] = crsp0['ret'] * 100  # R: 100*ret
    crsp0['mve_c'] = crsp0['prc'].abs() * crsp0['shrout']  # R: abs(prc)*shrout
    crsp0 = crsp0.dropna(subset=['ret', 'mve_c'])
    
    # R lines 332-340: read ccm
    ccm0 = pd.read_csv("../pyData/Intermediate/CCMLinkingTable.csv")
    ccm0['linkenddt'] = ccm0['linkenddt'].replace('', '31dec3000')  # R: ifelse(linkenddt=="", "31dec3000", linkenddt)
    ccm0['linkdt'] = pd.to_datetime(ccm0['linkdt'], format='%d%b%Y')  # R: dmy()
    ccm0['linkenddt'] = pd.to_datetime(ccm0['linkenddt'], format='%d%b%Y')  # R: dmy()
    ccm0 = ccm0.rename(columns={'lpermno': 'permno'})  # R: permno = lpermno
    ccm0 = ccm0[['gvkey', 'permno', 'linkprim', 'linkdt', 'linkenddt']].copy()
    
    logger.info(f"Loaded data - Compustat: {len(comp0):,}, CRSP: {len(crsp0):,}, CCM: {len(ccm0):,}")
    return comp0, crsp0, ccm0


def download_bea_data():
    """Download BEA data exactly matching R lines 345-374"""
    logger.info("Downloading BEA data...")
    
    data_dir = Path("../Data/Intermediate")
    data_dir.mkdir(exist_ok=True)
    
    # Download Make table before 1997 (R lines 345-349)
    make_1963_path = data_dir / "IOMake_Before_Redefinitions_1963-1996_Summary.xlsx"
    if not make_1963_path.exists():
        logger.info("Downloading Make table 1963-1996...")
        response = requests.get("https://apps.bea.gov/industry/xls/io-annual/IOMake_Before_Redefinitions_1963-1996_Summary.xlsx")
        response.raise_for_status()
        with open(make_1963_path, 'wb') as f:
            f.write(response.content)
    
    # Download Use table before 1997 (R lines 351-355)
    use_1963_path = data_dir / "IOUse_Before_Redefinitions_PRO_1963-1996_Summary.xlsx"
    if not use_1963_path.exists():
        logger.info("Downloading Use table 1963-1996...")
        response = requests.get("https://apps.bea.gov/industry/xls/io-annual/IOUse_Before_Redefinitions_PRO_1963-1996_Summary.xlsx")
        response.raise_for_status()
        with open(use_1963_path, 'wb') as f:
            f.write(response.content)
    
    # Download and extract current tables (R lines 358-373)
    logger.info("Downloading current tables (1997+)...")
    with tempfile.NamedTemporaryFile() as tmp:
        response = requests.get("https://apps.bea.gov//industry/iTables%20Static%20Files/AllTablesSUP.zip")
        response.raise_for_status()
        tmp.write(response.content)
        tmp.flush()
        
        with zipfile.ZipFile(tmp.name, 'r') as zip_ref:
            file_list = zip_ref.namelist()
            
            # R lines 365-366: find relevant files
            supply_files = [f for f in file_list if re.search(r"Supply_Tables_1997-2\d{3}_Summary\.xlsx", f, re.IGNORECASE)]
            use_files = [f for f in file_list if re.search(r"Supply-Use_Framework_1997-2\d{3}_Summary\.xlsx", f, re.IGNORECASE)]
            
            if not supply_files or not use_files:
                raise ValueError("Could not find Supply or Use tables in BEA zip file")
            
            supply_file = supply_files[0]
            use_file = use_files[0]
            
            # R lines 371-373: extract files
            zip_ref.extract(supply_file, data_dir)
            zip_ref.extract(use_file, data_dir)
            
            supply_1997_path = data_dir / supply_file
            use_1997_path = data_dir / use_file
    
    return {
        'make_1963': make_1963_path,
        'use_1963': use_1963_path,
        'supply_1997': supply_1997_path,
        'use_1997': use_1997_path
    }


def main():
    """Main function exactly matching R lines 379-407"""
    logger.info("Starting InputOutputMomentum processing...")
    
    # Make datasets global for use in generate_one_iomom
    global comp0, crsp0, ccm0
    
    # Load raw data
    comp0, crsp0, ccm0 = load_raw_data()
    
    # Download BEA data
    bea_files = download_bea_data()
    
    # Generate customer momentum (R lines 383-384: Make table)
    logger.info("Generating customer momentum...")
    iomomcust = generate_one_iomom(bea_files['make_1963'], bea_files['supply_1997'], 'customer')
    iomomcust['type'] = 'customer'  # R line 396
    
    # Generate supplier momentum (R lines 386-388: Use table)  
    logger.info("Generating supplier momentum...")
    iomomsupp = generate_one_iomom(bea_files['use_1963'], bea_files['use_1997'], 'supplier')
    iomomsupp['type'] = 'supplier'  # R line 400
    
    # Bind and store (R lines 394-407)
    logger.info("Combining results...")
    iomom = pd.concat([iomomcust, iomomsupp], ignore_index=True)  # R: rbind()
    iomom = iomom.dropna(subset=['retmatch'])  # R: filter(!is.na(retmatch))
    
    logger.info(f"Combined dataset: {len(iomom):,} rows")
    
    # Stata post-processing from .do file
    logger.info("Applying Stata post-processing...")
    
    # gen time_avail_m = ym(year_avail, month_avail)
    iomom['time_avail_m'] = pd.to_datetime(
        iomom[['year_avail', 'month_avail']].rename(columns={'year_avail': 'year', 'month_avail': 'month'}).assign(day=1)
    )
    
    # gcollapse (mean) retmatch portind, by(gvkey time_avail_m type)
    iomom_collapsed = iomom.groupby(['gvkey', 'time_avail_m', 'type']).agg({
        'retmatch': 'mean',
        'portind': 'mean'
    }).reset_index()
    
    # reshape wide retmatch portind, i(gvkey time_avail_m) j(type) string
    iomom_wide = iomom_collapsed.pivot_table(
        index=['gvkey', 'time_avail_m'],
        columns='type',
        values=['retmatch', 'portind'],
        fill_value=np.nan
    ).reset_index()
    
    # Flatten column names
    iomom_wide.columns = [f'{col[0]}{col[1]}' if col[1] else col[0] for col in iomom_wide.columns]
    
    # Ensure we have expected columns
    expected_cols = ['gvkey', 'time_avail_m', 'retmatchcustomer', 'portindcustomer', 'retmatchsupplier', 'portindsupplier']
    for col in expected_cols:
        if col not in iomom_wide.columns:
            iomom_wide[col] = np.nan
    
    final_output = iomom_wide[expected_cols].copy()
    
    # Convert gvkey to Int64 for consistency
    final_output['gvkey'] = pd.to_numeric(final_output['gvkey'], errors='coerce').astype('Int64')
    
    # Save to parquet
    output_path = "../pyData/Intermediate/InputOutputMomentumProcessed.parquet"
    final_output.to_parquet(output_path, index=False)
    
    logger.info(f"Successfully saved {len(final_output):,} rows to {output_path}")
    logger.info("InputOutputMomentum processing completed successfully!")
    
    return final_output


if __name__ == "__main__":
    main()