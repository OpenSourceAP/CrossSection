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
        """Read Compustat, CRSP, and CCM linking data."""
        logger.info("Reading input data...")
        
        # Read Compustat Annual
        compustat_path = self.data_dir / "CompustatAnnual.parquet"
        if not compustat_path.exists():
            raise FileNotFoundError(f"CompustatAnnual.parquet not found at {compustat_path}")
        
        comp = pd.read_parquet(compustat_path)
        
        # Create year_avail as 1 year after datadate + 6 months
        comp['datadate'] = pd.to_datetime(comp['datadate'])
        comp['year_avail'] = (comp['datadate'] + pd.DateOffset(months=6)).dt.year + 1
        
        # Create NAICS codes
        comp['naicsstr'] = comp['naicsh'].astype(str).str.zfill(6)
        comp['naics6'] = pd.to_numeric(comp['naicsstr'], errors='coerce')
        
        # Filter valid NAICS and select columns
        comp = comp.dropna(subset=['naics6'])
        comp = comp[['gvkey', 'year_avail', 'naics6', 'datadate']].copy()
        
        # Read CRSP monthly
        crsp_path = self.data_dir / "monthlyCRSP.parquet"
        if not crsp_path.exists():
            raise FileNotFoundError(f"monthlyCRSP.parquet not found at {crsp_path}")
        
        crsp = pd.read_parquet(crsp_path)
        crsp['date'] = pd.to_datetime(crsp['time_avail_m'])
        crsp['ret'] = crsp['ret'] * 100  # Convert to percentage
        # mve_c already exists in the parquet file
        
        # Filter valid returns and market cap
        crsp = crsp.dropna(subset=['ret', 'mve_c'])
        crsp = crsp[['permno', 'date', 'ret', 'mve_c']].copy()
        
        # Read CCM linking table
        ccm_path = self.data_dir / "CCMLinkingTable.parquet"
        if not ccm_path.exists():
            raise FileNotFoundError(f"CCMLinkingTable.parquet not found at {ccm_path}")
        
        ccm = pd.read_parquet(ccm_path)
        ccm['linkdt'] = pd.to_datetime(ccm['timeLinkStart_d'])
        ccm['linkenddt'] = pd.to_datetime(ccm['timeLinkEnd_d'])
        ccm['linkenddt'] = ccm['linkenddt'].fillna(pd.Timestamp('2030-12-31'))
        
        ccm = ccm[['gvkey', 'permno', 'linkprim', 'linkdt', 'linkenddt']].copy()
        
        logger.info(f"Loaded Compustat: {len(comp):,} rows")
        logger.info(f"Loaded CRSP: {len(crsp):,} rows")
        logger.info(f"Loaded CCM: {len(ccm):,} rows")
        
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
            
            # Transpose if supplier momentum (use table)
            if momentum_type == 'supplier':
                df_values = df.set_index('beaind').T
                df = df_values.reset_index().rename(columns={'index': 'beaind'})
            
            # Convert to long format
            df_long = df.melt(id_vars=['beaind'], var_name='beaindmatch', value_name='weight')
            df_long = df_long.dropna(subset=['weight'])
            df_long['year_avail'] = int(year) + 5  # 5-year lag
            
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
            
            # Transpose if supplier momentum (use table)
            if momentum_type == 'supplier':
                df_values = df.set_index('beaind').T
                df = df_values.reset_index().rename(columns={'index': 'beaind'})
            
            # Convert to long format
            df_long = df.melt(id_vars=['beaind'], var_name='beaindmatch', value_name='weight')
            df_long = df_long.dropna(subset=['weight'])
            df_long['year_avail'] = int(year) + 5  # 5-year lag
            
            indweight.append(df_long)
        
        # Combine all years
        indweight_df = pd.concat(indweight, ignore_index=True)
        
        logger.info(f"Combined I-O weights: {len(indweight_df):,} rows")
        return indweight_df
    
    def create_industry_mapping(self, indweight_df, comp_df):
        """Create mapping from NAICS codes to BEA industry codes."""
        logger.info("Creating industry mapping...")
        
        # Extract NAICS prefixes from BEA industry codes
        indlist = indweight_df[['year_avail', 'beaind']].drop_duplicates()
        indlist['naicspre'] = indlist['beaind'].str.extract(r'^(\d+)').astype(float)
        indlist = indlist.dropna(subset=['naicspre'])
        indlist['naicspre'] = indlist['naicspre'].astype(int)
        
        # Create 2, 3, 4 digit NAICS codes
        comp_df['naics2'] = (comp_df['naics6'] / 10000).astype(int)
        comp_df['naics3'] = (comp_df['naics6'] / 1000).astype(int)
        comp_df['naics4'] = (comp_df['naics6'] / 100).astype(int)
        
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
        
        # Filter to valid mappings
        comp_mapped = comp_mapped.dropna(subset=['beaind'])
        comp_mapped = comp_mapped[['gvkey', 'year_avail', 'naics6', 'beaind']].copy()
        
        logger.info(f"Industry mapping: {len(comp_mapped):,} firm-years mapped")
        return comp_mapped
    
    def create_industry_returns(self, comp_mapped, crsp_df, ccm_df):
        """Create BEA industry returns using CRSP data."""
        logger.info("Creating industry returns...")
        
        # Add gvkey to CRSP via CCM linking
        crsp_df['year'] = crsp_df['date'].dt.year
        crsp_df['month'] = crsp_df['date'].dt.month
        
        # Merge CRSP with CCM
        crsp_linked = crsp_df.merge(ccm_df, on='permno', how='left')
        logger.info(f"After CCM merge: {len(crsp_linked):,} rows")
        
        crsp_linked = crsp_linked[
            (crsp_linked['date'] >= crsp_linked['linkdt']) &
            (crsp_linked['date'] <= crsp_linked['linkenddt'])
        ]
        logger.info(f"After date filter: {len(crsp_linked):,} rows")
        
        # Add BEA industry codes
        crsp_linked = crsp_linked.merge(
            comp_mapped,
            left_on=['gvkey', 'year'],
            right_on=['gvkey', 'year_avail'],
            how='left'
        )
        logger.info(f"After industry mapping: {len(crsp_linked):,} rows")
        
        crsp_linked = crsp_linked.dropna(subset=['beaind'])
        logger.info(f"After dropping NaN beaind: {len(crsp_linked):,} rows")
        
        # Create industry returns (value-weighted)
        indret = crsp_linked.groupby(['year', 'month', 'beaind']).apply(
            lambda x: pd.Series({
                'ret': np.average(x['ret'], weights=x['mve_c']),
                'n': len(x)
            }), include_groups=False
        ).reset_index()
        
        # Filter to years where NAICS is available (1986+)
        indret = indret[indret['year'] >= 1986]
        
        logger.info(f"Industry returns: {len(indret):,} industry-month observations")
        return indret
    
    def generate_momentum_signals(self, indweight_df, indret_df, momentum_type):
        """Generate momentum signals using I-O weights."""
        logger.info(f"Generating {momentum_type} momentum signals...")
        
        # Check if indret_df is empty
        if len(indret_df) == 0:
            logger.warning(f"Empty industry returns data for {momentum_type} momentum - returning empty result")
            return pd.DataFrame(columns=['year', 'month', 'beaind', 'retmatch', 'portind'])
        
        # Remove self-industry weights
        indweight_filtered = indweight_df[indweight_df['beaind'] != indweight_df['beaindmatch']]
        
        # Expand to monthly data
        months_years = indret_df[['year', 'month']].drop_duplicates()
        
        # Merge weights with monthly data
        momentum_data = months_years.merge(
            indweight_filtered,
            left_on='year',
            right_on='year_avail',
            how='left'
        )
        
        # Add matched industry returns
        momentum_data = momentum_data.merge(
            indret_df.rename(columns={'ret': 'retmatch'})[['year', 'month', 'beaind', 'retmatch']],
            left_on=['year', 'month', 'beaindmatch'],
            right_on=['year', 'month', 'beaind'],
            how='left',
            suffixes=('', '_match')
        )
        
        momentum_data = momentum_data.dropna(subset=['retmatch'])
        
        # Check if momentum_data is empty after filtering
        if len(momentum_data) == 0:
            logger.warning(f"No valid momentum data after filtering for {momentum_type} - returning empty result")
            return pd.DataFrame(columns=['year', 'month', 'beaind', 'retmatch', 'portind'])
        
        # Calculate weighted average returns
        matchret = momentum_data.groupby(['year', 'month', 'beaind']).apply(
            lambda x: np.average(x['retmatch'], weights=x['weight']),
            include_groups=False
        ).reset_index()
        
        # Handle column naming based on actual result
        if len(matchret.columns) == 4:
            matchret.columns = ['year', 'month', 'beaind', 'retmatch']
        else:
            logger.warning(f"Unexpected number of columns in groupby result: {len(matchret.columns)}. Columns: {list(matchret.columns)}")
            return pd.DataFrame(columns=['year', 'month', 'beaind', 'retmatch', 'portind'])
        
        # Create portfolio rankings
        matchret['portind'] = matchret.groupby(['year', 'month'])['retmatch'].transform(
            lambda x: pd.qcut(x, q=10, labels=range(1, 11), duplicates='drop')
        )
        
        logger.info(f"{momentum_type} momentum signals: {len(matchret):,} observations")
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
            firm_months[['year_avail', 'month_avail']].assign(day=1)
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