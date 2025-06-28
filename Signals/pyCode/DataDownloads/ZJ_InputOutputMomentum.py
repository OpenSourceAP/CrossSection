# ABOUTME: Downloads BEA Input-Output tables and creates customer/supplier momentum signals
# ABOUTME: Follows Menzly-Ozbas methodology for Input-Output based momentum predictors

import pandas as pd
import numpy as np
import requests
import zipfile
import tempfile
import os
from pathlib import Path
import re
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class InputOutputMomentum:
    """
    Processes BEA Input-Output tables to create momentum signals based on
    customer-supplier relationships following Menzly-Ozbas methodology.
    """
    
    def __init__(self, data_dir="../pyData/Intermediate"):
        self.data_dir = Path(data_dir)
        self.intermediate_dir = Path("../Data/Intermediate")
        self.temp_dir = self.intermediate_dir / "temp_io"
        self.temp_dir.mkdir(exist_ok=True)
        
        # BEA download URLs
        self.bea_urls = {
            'make_1963_1996': 'https://apps.bea.gov/industry/xls/io-annual/IOMake_Before_Redefinitions_1963-1996_Summary.xlsx',
            'use_1963_1996': 'https://apps.bea.gov/industry/xls/io-annual/IOUse_Before_Redefinitions_PRO_1963-1996_Summary.xlsx',
            'current_tables': 'https://apps.bea.gov//industry/iTables%20Static%20Files/AllTablesSUP.zip'
        }
        
        logger.info(f"Initialized InputOutputMomentum with data_dir: {self.data_dir}")
    
    def download_bea_data(self):
        """Download BEA Input-Output tables."""
        logger.info("Downloading BEA Input-Output tables...")
        
        # Download pre-1997 Make table
        make_1963_path = self.temp_dir / "IOMake_Before_Redefinitions_1963-1996_Summary.xlsx"
        if not make_1963_path.exists():
            logger.info("Downloading Make table 1963-1996...")
            response = requests.get(self.bea_urls['make_1963_1996'])
            response.raise_for_status()
            with open(make_1963_path, 'wb') as f:
                f.write(response.content)
        
        # Download pre-1997 Use table
        use_1963_path = self.temp_dir / "IOUse_Before_Redefinitions_PRO_1963-1996_Summary.xlsx"
        if not use_1963_path.exists():
            logger.info("Downloading Use table 1963-1996...")
            response = requests.get(self.bea_urls['use_1963_1996'])
            response.raise_for_status()
            with open(use_1963_path, 'wb') as f:
                f.write(response.content)
        
        # Download and extract current tables
        logger.info("Downloading current tables (1997+)...")
        with tempfile.NamedTemporaryFile() as tmp:
            response = requests.get(self.bea_urls['current_tables'])
            response.raise_for_status()
            tmp.write(response.content)
            tmp.flush()
            
            with zipfile.ZipFile(tmp.name, 'r') as zip_ref:
                file_list = zip_ref.namelist()
                
                # Find Supply and Use tables
                supply_pattern = r"Supply.*_1997-2[0-9]{3}.*Summary\.xlsx"
                use_pattern = r"Supply-Use.*_1997-2[0-9]{3}.*Summary\.xlsx"
                
                supply_files = [f for f in file_list if re.search(supply_pattern, f, re.IGNORECASE)]
                use_files = [f for f in file_list if re.search(use_pattern, f, re.IGNORECASE)]
                
                if not supply_files or not use_files:
                    raise ValueError("Could not find Supply or Use tables in BEA zip file")
                
                supply_file = supply_files[0]
                use_file = use_files[0]
                
                # Extract files
                zip_ref.extract(supply_file, self.temp_dir)
                zip_ref.extract(use_file, self.temp_dir)
                
                logger.info(f"Extracted: {supply_file}, {use_file}")
                
                return {
                    'make_1963_1996': make_1963_path,
                    'use_1963_1996': use_1963_path,
                    'supply_1997_current': self.temp_dir / supply_file,
                    'use_1997_current': self.temp_dir / use_file
                }
    
    def read_input_data(self):
        """Read Compustat, CRSP, and CCM linking data from CSV files."""
        logger.info("Reading input data from CSV files...")
        
        # Read Compustat Annual from CSV (matching R implementation)
        compustat_csv_path = "../Data/Intermediate/CompustatAnnual.csv"
        logger.info(f"Reading Compustat from: {compustat_csv_path}")
        
        comp = pd.read_csv(compustat_csv_path)
        logger.info(f"Raw Compustat loaded: {len(comp):,} rows, {len(comp.columns)} columns")
        
        # Create NAICS codes (matching R implementation logic)
        comp['naicsstr'] = comp['naicsh'].astype(str).str.zfill(6)
        comp['naics6'] = pd.to_numeric(comp['naicsstr'], errors='coerce')
        
        # Create year_avail as 1 year after datadate + 6 months (matching R logic)
        comp['datadate'] = pd.to_datetime(comp['datadate'], format='%d%b%Y')
        comp['year_avail'] = (comp['datadate'] + pd.DateOffset(months=6)).dt.year + 1
        
        # Filter valid NAICS and select columns
        comp = comp.dropna(subset=['naics6'])
        comp = comp[['gvkey', 'year_avail', 'naics6', 'datadate']].copy()
        logger.info(f"Compustat after processing: {len(comp):,} rows")
        logger.info(f"Missing NAICS6: {comp['naics6'].isna().sum():,} rows")
        
        # Read CRSP monthly from CSV (matching R implementation)
        crsp_csv_path = "../Data/Intermediate/mCRSP.csv"
        logger.info(f"Reading CRSP from: {crsp_csv_path}")
        
        crsp = pd.read_csv(crsp_csv_path)
        logger.info(f"Raw CRSP loaded: {len(crsp):,} rows, {len(crsp.columns)} columns")
        
        # Process CRSP data (matching R implementation)
        crsp['date'] = pd.to_datetime(crsp['date'], format='%d%b%Y')
        crsp['ret'] = crsp['ret'] * 100  # Convert to percentage
        crsp['mve_c'] = (crsp['prc'].abs() * crsp['shrout'])  # Calculate market cap like R
        
        # Filter valid returns and market cap
        crsp = crsp.dropna(subset=['ret', 'mve_c'])
        crsp = crsp[['permno', 'date', 'ret', 'mve_c']].copy()
        logger.info(f"CRSP after processing: {len(crsp):,} rows")
        logger.info(f"Missing returns: {crsp['ret'].isna().sum():,} rows")
        logger.info(f"Missing mve_c: {crsp['mve_c'].isna().sum():,} rows")
        
        # Read CCM linking table from CSV (matching R implementation)
        ccm_csv_path = "../Data/Intermediate/CCMLinkingTable.csv"
        logger.info(f"Reading CCM from: {ccm_csv_path}")
        
        ccm = pd.read_csv(ccm_csv_path)
        logger.info(f"Raw CCM loaded: {len(ccm):,} rows, {len(ccm.columns)} columns")
        
        # Process CCM data (matching R implementation)
        ccm['linkdt'] = pd.to_datetime(ccm['linkdt'], format='%d%b%Y')
        # Handle missing linkenddt by replacing empty strings with far future date
        ccm['linkenddt'] = ccm['linkenddt'].replace('', '31dec3000')
        ccm['linkenddt'] = pd.to_datetime(ccm['linkenddt'], format='%d%b%Y')
        
        # Rename permno column to match R logic
        ccm = ccm.rename(columns={'lpermno': 'permno'})
        ccm = ccm[['gvkey', 'permno', 'linkprim', 'linkdt', 'linkenddt']].copy()
        logger.info(f"CCM after processing: {len(ccm):,} rows")
        
        logger.info(f"Final data loaded - Compustat: {len(comp):,}, CRSP: {len(crsp):,}, CCM: {len(ccm):,}")
        
        return comp, crsp, ccm
    
    def process_io_table(self, sheet_path_1963, sheet_path_1997, momentum_type):
        """
        Process Input-Output tables for either customer or supplier momentum.
        
        Args:
            sheet_path_1963: Path to 1963-1996 Excel file
            sheet_path_1997: Path to 1997+ Excel file  
            momentum_type: 'customer' or 'supplier'
        """
        logger.info(f"Processing I-O tables for {momentum_type} momentum...")
        
        indweight = []
        
        # Process 1963-1996 data
        sheet_names = pd.ExcelFile(sheet_path_1963).sheet_names
        sheet_names = [s for s in sheet_names if s not in ['Cover', 'Contents', 'ReadMe']]
        # Filter to numeric year sheets only
        sheet_names = [s for s in sheet_names if s.isdigit()]
        
        for year in sheet_names:
            logger.info(f"Processing year {year} from 1963-1996 data...")
            
            # Read sheet
            df = pd.read_excel(sheet_path_1963, sheet_name=year, skiprows=6)
            if len(df.columns) < 2:
                logger.warning(f"Skipping sheet {year} - insufficient columns")
                continue
            df = df.rename(columns={df.columns[0]: 'beaind'})
            df = df.drop(columns=[df.columns[1]])  # Drop second column
            
            # Convert to numeric (except first column)
            for col in df.columns[1:]:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Transpose if supplier momentum (use table) - matching R logic carefully
            if momentum_type == 'supplier':
                df_values = df.set_index('beaind').T
                df = df_values.reset_index().rename(columns={'index': 'beaind'})
                logger.debug(f"Transposed supplier table for year {year}: {df.shape}")
            
            # Convert to long format
            df_long = df.melt(id_vars=['beaind'], var_name='beaindmatch', value_name='weight')
            df_long = df_long.dropna(subset=['weight'])
            df_long['year_avail'] = int(year) + 5  # 5-year lag (matching R)
            logger.debug(f"Year {year}: {len(df_long):,} weight observations after melt and filter")
            
            indweight.append(df_long)
        
        # Process 1997+ data
        sheet_names = pd.ExcelFile(sheet_path_1997).sheet_names
        # Filter to numeric year sheets only
        sheet_names = [s for s in sheet_names if s.isdigit()]
        
        for year in sheet_names:
            logger.info(f"Processing year {year} from 1997+ data...")
            
            # Read sheet
            df = pd.read_excel(sheet_path_1997, sheet_name=year, skiprows=5)
            if len(df.columns) < 2:
                logger.warning(f"Skipping sheet {year} - insufficient columns")
                continue
            df = df.rename(columns={df.columns[0]: 'beaind'})
            df = df[df['beaind'] != 'IOCode']  # Remove IOCode row
            df = df.drop(columns=[df.columns[1]])  # Drop second column
            
            # Convert to numeric (except first column)
            for col in df.columns[1:]:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Transpose if supplier momentum (use table) - matching R logic carefully
            if momentum_type == 'supplier':
                df_values = df.set_index('beaind').T
                df = df_values.reset_index().rename(columns={'index': 'beaind'})
                logger.debug(f"Transposed supplier table for year {year}: {df.shape}")
            
            # Convert to long format
            df_long = df.melt(id_vars=['beaind'], var_name='beaindmatch', value_name='weight')
            df_long = df_long.dropna(subset=['weight'])
            df_long['year_avail'] = int(year) + 5  # 5-year lag (matching R)
            logger.debug(f"Year {year}: {len(df_long):,} weight observations after melt and filter")
            
            indweight.append(df_long)
        
        # Combine all years
        indweight_df = pd.concat(indweight, ignore_index=True)
        
        logger.info(f"Combined I-O weights: {len(indweight_df):,} rows")
        return indweight_df
    
    def create_industry_mapping(self, indweight_df, comp_df):
        """Create mapping from NAICS codes to BEA industry codes."""
        logger.info("Creating industry mapping...")
        logger.info(f"Input: indweight_df has {len(indweight_df):,} rows, comp_df has {len(comp_df):,} rows")
        
        # Extract NAICS prefixes from BEA industry codes
        indlist = indweight_df[['year_avail', 'beaind']].drop_duplicates()
        logger.info(f"Unique BEA industries by year: {len(indlist):,}")
        
        indlist['naicspre'] = indlist['beaind'].str.extract(r'^(\d+)').astype(float)
        indlist = indlist.dropna(subset=['naicspre'])
        indlist['naicspre'] = indlist['naicspre'].astype(int)
        logger.info(f"BEA industries with valid NAICS prefixes: {len(indlist):,}")
        
        # Create 2, 3, 4 digit NAICS codes (matching R logic: floor(naics6/1e4), etc.)
        comp_df['naics2'] = (comp_df['naics6'] / 10000).astype(int)
        comp_df['naics3'] = (comp_df['naics6'] / 1000).astype(int)
        comp_df['naics4'] = (comp_df['naics6'] / 100).astype(int)
        logger.info(f"Created NAICS digit codes - sample naics6: {comp_df['naics6'].iloc[:5].tolist()}")
        logger.info(f"Sample naics2: {comp_df['naics2'].iloc[:5].tolist()}")
        
        # Merge with NAICS codes (try 4, 3, 2 digit in that order)
        comp_mapped = comp_df.merge(
            indlist.rename(columns={'beaind': 'beaind2'}),
            left_on=['year_avail', 'naics2'],
            right_on=['year_avail', 'naicspre'],
            how='left'
        )
        
        comp_mapped = comp_mapped.merge(
            indlist.rename(columns={'beaind': 'beaind3'}),
            left_on=['year_avail', 'naics3'],
            right_on=['year_avail', 'naicspre'],
            how='left',
            suffixes=('', '_3')
        )
        
        comp_mapped = comp_mapped.merge(
            indlist.rename(columns={'beaind': 'beaind4'}),
            left_on=['year_avail', 'naics4'],
            right_on=['year_avail', 'naicspre'],
            how='left',
            suffixes=('', '_4')
        )
        
        # Use the most specific match available
        comp_mapped['beaind'] = comp_mapped['beaind4'].fillna(
            comp_mapped['beaind3'].fillna(comp_mapped['beaind2'])
        )
        
        # Debug: Check mapping results before filtering
        beaind2_mapped = (~comp_mapped['beaind2'].isna()).sum()
        beaind3_mapped = (~comp_mapped['beaind3'].isna()).sum() 
        beaind4_mapped = (~comp_mapped['beaind4'].isna()).sum()
        total_before_filter = len(comp_mapped)
        
        logger.info(f"Mapping results: 2-digit NAICS: {beaind2_mapped:,}, 3-digit: {beaind3_mapped:,}, 4-digit: {beaind4_mapped:,}")
        
        # Debug: Check which NAICS codes are being used most
        logger.info(f"Most common 2-digit NAICS: {comp_mapped['naics2'].value_counts().head().to_dict()}")
        logger.info(f"Most common BEA industry prefixes: {indlist['naicspre'].value_counts().head().to_dict()}")
        
        # Filter to valid mappings
        comp_mapped = comp_mapped.dropna(subset=['beaind'])
        comp_mapped = comp_mapped[['gvkey', 'year_avail', 'naics6', 'beaind']].copy()
        
        # Ensure gvkey is string for consistent merging
        comp_mapped['gvkey'] = comp_mapped['gvkey'].astype(str)
        
        mapping_success_rate = len(comp_mapped) / total_before_filter * 100 if total_before_filter > 0 else 0
        logger.info(f"Industry mapping: {len(comp_mapped):,} firm-years mapped ({mapping_success_rate:.2f}% success rate)")
        logger.info(f"Sample mapped data: {comp_mapped.head(3).to_dict('records')}")
        return comp_mapped
    
    def create_industry_returns(self, comp_mapped, crsp_df, ccm_df):
        """Create BEA industry returns using CRSP data."""
        logger.info("Creating industry returns...")
        logger.info(f"Input data - comp_mapped: {len(comp_mapped):,}, crsp: {len(crsp_df):,}, ccm: {len(ccm_df):,}")
        
        # Add gvkey to CRSP via CCM linking
        crsp_df['year'] = crsp_df['date'].dt.year
        crsp_df['month'] = crsp_df['date'].dt.month
        logger.info(f"CRSP date range: {crsp_df['date'].min()} to {crsp_df['date'].max()}")
        logger.info(f"CRSP year range: {crsp_df['year'].min()} to {crsp_df['year'].max()}")
        
        # Ensure consistent data types for gvkey before merging
        ccm_df['gvkey'] = ccm_df['gvkey'].astype(str)
        logger.info(f"CCM gvkey sample: {ccm_df['gvkey'].head().tolist()}")
        logger.info(f"CCM permno sample: {ccm_df['permno'].head().tolist()}")
        
        # Merge CRSP with CCM
        crsp_linked = crsp_df.merge(ccm_df, on='permno', how='left')
        logger.info(f"After CCM merge: {len(crsp_linked):,} rows")
        logger.info(f"CRSP-CCM merge success rate: {(~crsp_linked['gvkey'].isna()).sum() / len(crsp_linked) * 100:.2f}%")
        
        crsp_linked = crsp_linked[
            (crsp_linked['date'] >= crsp_linked['linkdt']) &
            (crsp_linked['date'] <= crsp_linked['linkenddt'])
        ]
        logger.info(f"After date filter: {len(crsp_linked):,} rows")
        
        # Add BEA industry codes
        logger.info(f"Comp_mapped year range: {comp_mapped['year_avail'].min()} to {comp_mapped['year_avail'].max()}")
        logger.info(f"Sample comp_mapped gvkeys: {comp_mapped['gvkey'].head().tolist()}")
        
        crsp_linked = crsp_linked.merge(
            comp_mapped,
            left_on=['gvkey', 'year'],
            right_on=['gvkey', 'year_avail'],
            how='left'
        )
        logger.info(f"After industry mapping: {len(crsp_linked):,} rows")
        
        # Debug: Check NaN beaind before filtering
        nan_beaind_count = crsp_linked['beaind'].isna().sum()
        logger.info(f"NaN beaind count: {nan_beaind_count:,} ({nan_beaind_count/len(crsp_linked)*100:.2f}%)")
        
        if nan_beaind_count > 0:
            logger.info(f"Sample rows with missing beaind:")
            sample_missing = crsp_linked[crsp_linked['beaind'].isna()][['gvkey', 'year', 'permno']].head(5)
            logger.info(f"{sample_missing.to_string()}")
        
        crsp_linked = crsp_linked.dropna(subset=['beaind'])
        logger.info(f"After dropping NaN beaind: {len(crsp_linked):,} rows")
        
        # Create industry returns (value-weighted)
        logger.info(f"Creating value-weighted industry returns...")
        logger.info(f"Unique BEA industries in CRSP data: {crsp_linked['beaind'].nunique()}")
        logger.info(f"Sample BEA industries: {crsp_linked['beaind'].value_counts().head().to_dict()}")
        
        def weighted_return_stats(group):
            try:
                weights = group['mve_c']
                returns = group['ret']
                if len(weights) > 0 and weights.sum() > 0:
                    weighted_ret = np.average(returns, weights=weights)
                    return pd.Series({
                        'ret': weighted_ret,
                        'n': len(group),
                        'total_mve': weights.sum()
                    })
                else:
                    return pd.Series({'ret': np.nan, 'n': 0, 'total_mve': 0})
            except Exception as e:
                logger.warning(f"Error in weighted average: {e}")
                return pd.Series({'ret': np.nan, 'n': 0, 'total_mve': 0})
        
        indret = crsp_linked.groupby(['year', 'month', 'beaind']).apply(
            weighted_return_stats, include_groups=False
        ).reset_index()
        
        logger.info(f"Industry returns before date filter: {len(indret):,} observations")
        logger.info(f"Non-NaN returns: {(~indret['ret'].isna()).sum():,} ({(~indret['ret'].isna()).sum()/len(indret)*100:.2f}%)")
        
        # Filter to years where NAICS is available (1986+)
        indret = indret[indret['year'] >= 1986]
        
        logger.info(f"Industry returns after 1986+ filter: {len(indret):,} industry-month observations")
        logger.info(f"Sample industry returns: {indret.head().to_dict('records')}")
        return indret
    
    def generate_momentum_signals(self, indweight_df, indret_df, momentum_type):
        """Generate momentum signals using I-O weights."""
        logger.info(f"Generating {momentum_type} momentum signals...")
        logger.info(f"Input: indweight_df={len(indweight_df):,}, indret_df={len(indret_df):,}")
        
        # Check if indret_df is empty
        if len(indret_df) == 0:
            logger.warning(f"Empty industry returns data for {momentum_type} momentum - returning empty result")
            return pd.DataFrame(columns=['year', 'month', 'beaind', 'retmatch', 'portind'])
        
        # Remove self-industry weights
        before_self_filter = len(indweight_df)
        indweight_filtered = indweight_df[indweight_df['beaind'] != indweight_df['beaindmatch']]
        logger.info(f"After removing self-industry weights: {len(indweight_filtered):,} (removed {before_self_filter - len(indweight_filtered):,})")
        
        # Debug: Check weight distribution
        logger.info(f"Weight distribution - min: {indweight_filtered['weight'].min():.6f}, max: {indweight_filtered['weight'].max():.6f}")
        logger.info(f"Unique beaind in weights: {indweight_filtered['beaind'].nunique()}, beaindmatch: {indweight_filtered['beaindmatch'].nunique()}")
        
        # Expand to monthly data
        months_years = indret_df[['year', 'month']].drop_duplicates()
        logger.info(f"Time periods to process: {len(months_years):,} year-month combinations")
        logger.info(f"Year range in returns: {indret_df['year'].min()}-{indret_df['year'].max()}")
        
        # Merge weights with monthly data
        momentum_data = months_years.merge(
            indweight_filtered,
            left_on='year',
            right_on='year_avail',
            how='left'
        )
        logger.info(f"After merging weights with monthly data: {len(momentum_data):,} rows")
        logger.info(f"Non-null weights after merge: {(~momentum_data['weight'].isna()).sum():,}")
        
        # Add matched industry returns
        momentum_data = momentum_data.merge(
            indret_df.rename(columns={'ret': 'retmatch'})[['year', 'month', 'beaind', 'retmatch']],
            left_on=['year', 'month', 'beaindmatch'],
            right_on=['year', 'month', 'beaind'],
            how='left',
            suffixes=('', '_match')
        )
        logger.info(f"After adding matched returns: {len(momentum_data):,} rows")
        logger.info(f"Non-null matched returns: {(~momentum_data['retmatch'].isna()).sum():,}")
        
        momentum_data = momentum_data.dropna(subset=['retmatch'])
        logger.info(f"After dropping NaN retmatch: {len(momentum_data):,} rows")
        
        # Check if momentum_data is empty after filtering
        if len(momentum_data) == 0:
            logger.warning(f"No valid momentum data after filtering for {momentum_type} - returning empty result")
            return pd.DataFrame(columns=['year', 'month', 'beaind', 'retmatch', 'portind'])
        
        # Calculate weighted average returns, filtering out zero-weight groups
        def safe_weighted_average(group):
            weights = group['weight']
            values = group['retmatch']
            
            # Filter out NaN values from both weights and values
            valid_mask = ~(pd.isna(weights) | pd.isna(values))
            weights_clean = weights[valid_mask]
            values_clean = values[valid_mask]
            
            # Check if we have valid data after filtering
            if len(weights_clean) == 0:
                return np.nan
            if weights_clean.sum() == 0:
                logger.debug(f"Zero weight sum for group with {len(weights_clean)} observations")
                return np.nan
            
            try:
                result = np.average(values_clean, weights=weights_clean)
                return result
            except ZeroDivisionError:
                logger.warning(f"ZeroDivisionError in weighted average calculation")
                return np.nan
            except Exception as e:
                logger.warning(f"Error in weighted average calculation: {e}")
                return np.nan
        
        logger.info(f"Computing weighted averages for {momentum_data.groupby(['year', 'month', 'beaind']).ngroups:,} industry-month groups")
        
        matchret = momentum_data.groupby(['year', 'month', 'beaind']).apply(
            safe_weighted_average,
            include_groups=False
        ).reset_index()
        
        logger.info(f"Raw weighted average results: {len(matchret):,} observations")
        logger.info(f"Non-NaN weighted averages: {(~matchret.iloc[:, 3].isna()).sum():,}")
        
        # Remove NaN results from zero-weight groups
        matchret = matchret.dropna()
        logger.info(f"After removing NaN results: {len(matchret):,} observations")
        
        # Handle column naming based on actual result
        if len(matchret.columns) == 4:
            matchret.columns = ['year', 'month', 'beaind', 'retmatch']
        else:
            logger.warning(f"Unexpected number of columns in groupby result: {len(matchret.columns)}. Columns: {list(matchret.columns)}")
            return pd.DataFrame(columns=['year', 'month', 'beaind', 'retmatch', 'portind'])
        
        if len(matchret) > 0:
            logger.info(f"Sample weighted averages: {matchret.head().to_dict('records')}")
            logger.info(f"Retmatch stats - min: {matchret['retmatch'].min():.4f}, max: {matchret['retmatch'].max():.4f}, mean: {matchret['retmatch'].mean():.4f}")
        
        # Create portfolio rankings with robust handling for edge cases (matching R findInterval logic)
        def safe_qcut(x):
            if len(x) == 0:
                return pd.Series([], dtype='int')
            
            n_unique = len(x.unique())
            if n_unique <= 1:
                return pd.Series([1] * len(x), index=x.index)
            
            # Use the same logic as R's findInterval with quantiles (matching R implementation)
            try:
                # R uses quantile(retmatch, 0:10/10) then findInterval
                quantiles = x.quantile([i/10 for i in range(11)])
                # Use searchsorted to match R's findInterval behavior
                bins = pd.cut(x, bins=quantiles, labels=range(1, 11), include_lowest=True, duplicates='drop')
                # Convert to numeric, filling NaN with 1 (similar to R behavior)
                result = pd.to_numeric(bins, errors='coerce').fillna(1).astype(int)
                return result
            except ValueError as e:
                logger.debug(f"qcut failed with {n_unique} unique values: {e}")
                try:
                    # Fallback: use fewer quantiles
                    n_bins = min(n_unique, 10)
                    if n_bins < 2:
                        return pd.Series([1] * len(x), index=x.index)
                    quantiles = x.quantile([i/n_bins for i in range(n_bins+1)])
                    bins = pd.cut(x, bins=quantiles, labels=range(1, n_bins + 1), include_lowest=True, duplicates='drop')
                    result = pd.to_numeric(bins, errors='coerce').fillna(1).astype(int)
                    return result
                except ValueError:
                    # Final fallback: rank-based approach
                    ranks = x.rank(method='first', pct=True)
                    portind = (ranks * 10).apply(lambda r: min(int(r) + 1, 10))
                    return portind
        
        if len(matchret) == 0:
            logger.warning(f"No weighted averages computed for {momentum_type} momentum")
            return pd.DataFrame(columns=['year', 'month', 'beaind', 'retmatch', 'portind'])
        
        # Create portfolio rankings
        logger.info("Creating portfolio rankings...")
        matchret['portind'] = matchret.groupby(['year', 'month'])['retmatch'].transform(safe_qcut)
        
        portfolio_counts = matchret['portind'].value_counts().sort_index()
        logger.info(f"Portfolio distribution: {portfolio_counts.to_dict()}")
        
        logger.info(f"{momentum_type} momentum signals: {len(matchret):,} observations")
        logger.info(f"Final non-NaN portfolio assignments: {(~matchret['portind'].isna()).sum():,}")
        return matchret
    
    def create_final_output(self, comp_mapped, customer_momentum, supplier_momentum):
        """Create final output with customer and supplier momentum combined."""
        logger.info("Creating final output...")
        
        # Check if we have valid data
        if len(comp_mapped) == 0:
            logger.warning("No mapped companies - returning empty output")
            return pd.DataFrame(columns=['gvkey', 'time_avail_m', 'retmatchcustomer', 
                                       'portindcustomer', 'retmatchsupplier', 'portindsupplier'])
        
        if len(customer_momentum) == 0 and len(supplier_momentum) == 0:
            logger.warning("No momentum data available - returning empty output")
            return pd.DataFrame(columns=['gvkey', 'time_avail_m', 'retmatchcustomer', 
                                       'portindcustomer', 'retmatchsupplier', 'portindsupplier'])
        
        # Create monthly grid for all firm-years
        months_df = pd.DataFrame({'month_avail': range(1, 13)})
        firm_months = comp_mapped.merge(months_df, how='cross')
        
        # Merge customer momentum (if available)
        if len(customer_momentum) > 0:
            firm_months = firm_months.merge(
                customer_momentum[['year', 'month', 'beaind', 'retmatch', 'portind']],
                left_on=['year_avail', 'month_avail', 'beaind'],
                right_on=['year', 'month', 'beaind'],
                how='left',
                suffixes=('', '_customer')
            )
        else:
            firm_months['retmatch_customer'] = np.nan
            firm_months['portind_customer'] = np.nan
        
        # Merge supplier momentum (if available)
        if len(supplier_momentum) > 0:
            firm_months = firm_months.merge(
                supplier_momentum[['year', 'month', 'beaind', 'retmatch', 'portind']],
                left_on=['year_avail', 'month_avail', 'beaind'],
                right_on=['year', 'month', 'beaind'],
                how='left',
                suffixes=('_customer', '_supplier')
            )
        else:
            firm_months['retmatch_supplier'] = np.nan
            firm_months['portind_supplier'] = np.nan
        
        # Create time_avail_m
        firm_months['time_avail_m'] = pd.to_datetime(
            firm_months[['year_avail', 'month_avail']].rename(
                columns={'year_avail': 'year', 'month_avail': 'month'}
            ).assign(day=1)
        )
        
        # Select and rename final columns
        final_columns = {
            'gvkey': 'gvkey',
            'time_avail_m': 'time_avail_m',
            'retmatch_customer': 'retmatchcustomer',
            'portind_customer': 'portindcustomer',
            'retmatch_supplier': 'retmatchsupplier',
            'portind_supplier': 'portindsupplier'
        }
        
        # Check which columns actually exist
        available_columns = [col for col in final_columns.keys() if col in firm_months.columns]
        if len(available_columns) < len(final_columns):
            missing_cols = set(final_columns.keys()) - set(available_columns)
            logger.warning(f"Missing columns in final output: {missing_cols}")
            # Add missing columns with NaN
            for col in missing_cols:
                if col not in firm_months.columns:
                    firm_months[col] = np.nan
        
        output_df = firm_months[list(final_columns.keys())].rename(columns=final_columns)
        
        # Convert gvkey back to int32 for consistent data type
        output_df['gvkey'] = pd.to_numeric(output_df['gvkey'], errors='coerce').astype('Int64')
        
        # Apply missing value standardization for numeric columns to match Stata format
        numeric_columns = ['retmatchcustomer', 'portindcustomer', 'retmatchsupplier', 'portindsupplier']
        for col in numeric_columns:
            if col in output_df.columns:
                # Keep NaN as NaN for numeric columns - this matches Stata's missing value representation
                pass  # No change needed for numeric NaN values
        
        # Keep all rows (don't filter out NaN) to maintain structure
        logger.info(f"Final output: {len(output_df):,} rows")
        return output_df
    
    def run(self):
        """Run the complete InputOutputMomentum processing pipeline."""
        logger.info("Starting InputOutputMomentum processing...")
        
        try:
            # Download BEA data
            bea_files = self.download_bea_data()
            
            # Read input data
            comp, crsp, ccm = self.read_input_data()
            
            # Process customer momentum (Make/Supply tables)
            customer_weights = self.process_io_table(
                bea_files['make_1963_1996'],
                bea_files['supply_1997_current'],
                'customer'
            )
            
            # Process supplier momentum (Use tables)
            supplier_weights = self.process_io_table(
                bea_files['use_1963_1996'],
                bea_files['use_1997_current'],
                'supplier'
            )
            
            # Create industry mappings
            comp_mapped_customer = self.create_industry_mapping(customer_weights, comp)
            comp_mapped_supplier = self.create_industry_mapping(supplier_weights, comp)
            
            # Use the customer mapping for both (they should be similar)
            comp_mapped = comp_mapped_customer
            
            # Create industry returns
            indret = self.create_industry_returns(comp_mapped, crsp, ccm)
            
            # Generate momentum signals
            customer_momentum = self.generate_momentum_signals(customer_weights, indret, 'customer')
            supplier_momentum = self.generate_momentum_signals(supplier_weights, indret, 'supplier')
            
            # Create final output
            output_df = self.create_final_output(comp_mapped, customer_momentum, supplier_momentum)
            
            # Save to parquet
            output_path = self.data_dir / "InputOutputMomentumProcessed.parquet"
            output_df.to_parquet(output_path, index=False)
            
            logger.info(f"Successfully saved {len(output_df):,} rows to {output_path}")
            logger.info("InputOutputMomentum processing completed successfully!")
            
            return output_df
            
        except Exception as e:
            logger.error(f"Error in InputOutputMomentum processing: {str(e)}")
            raise


def main():
    """Main execution function."""
    processor = InputOutputMomentum()
    processor.run()


if __name__ == "__main__":
    main()