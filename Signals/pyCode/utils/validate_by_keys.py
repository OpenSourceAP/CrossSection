"""
ABOUTME: Validates Python vs Stata datasets using inner join on common identifiers
ABOUTME: Critical script for ensuring data pipeline accuracy across both systems

This script compares datasets between pyData/ and Data/ directories by:
1. Loading both Python (parquet) and Stata (DTA/CSV) versions
2. Extracting unique identifier combinations from BOTH versions
3. Finding intersection (common identifiers) to eliminate data recency differences
4. Filtering BOTH datasets to common identifiers only
5. Comparing aligned datasets for exact matches

The inner join approach eliminates false positives from data availability timing
differences while focusing on true data processing accuracy.

To use: `python3 utils/validate_by_keys.py --datasets CompustatAnnual m_QCompustat`
"""

import sys
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, Any
from datetime import datetime
import warnings

import pandas as pd
import numpy as np
warnings.filterwarnings('ignore')

# Configure logging
log_dir = Path("../Logs")
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / 'validation_log.txt'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Dataset identifier mapping based on documentation
DATASET_IDENTIFIERS = {
    # CCM Linking Tables
    'CCMLinkingTable.csv': {
        'stock': 'lpermno', 
        'time': 'linkdt',
        'stata_file': 'CCMLinkingTable.csv',
        'python_file': 'CCMLinkingTable.csv'
    },
    'CCMLinkingTable': {
        'stock': 'gvkey', 
        'time': 'timeLinkStart_d',
        'stata_file': 'CCMLinkingTable.dta',
        'python_file': 'CCMLinkingTable.parquet'
    },

    # Compustat Annual/Quarterly
    'CompustatAnnual': {
        'stock': 'gvkey', 
        'time': 'datadate',
        'stata_file': 'CompustatAnnual.csv',
        'python_file': 'CompustatAnnual.csv'
    },
    'a_aCompustat': {
        'stock': 'permno', 
        'time': 'time_avail_m',
        'stata_file': 'a_aCompustat.dta',
        'python_file': 'a_aCompustat.parquet'
    },
    'm_aCompustat': {
        'stock': 'permno', 
        'time': 'time_avail_m',
        'stata_file': 'm_aCompustat.dta',
        'python_file': 'm_aCompustat.parquet'
    },
    'm_QCompustat': {
        'stock': 'gvkey', 
        'time': 'time_avail_m',
        'stata_file': 'm_QCompustat.dta',
        'python_file': 'm_QCompustat.parquet'
    },

    # Compustat Specialized
    'CompustatPensions': {
        'stock': 'gvkey', 
        'time': 'year',
        'stata_file': 'CompustatPensions.dta',
        'python_file': 'CompustatPensions.parquet'
    },
    'CompustatSegments': {
        'stock': 'gvkey', 
        'time': 'datadate',
        'stata_file': 'CompustatSegments.dta',
        'python_file': 'CompustatSegments.parquet'
    },
    'CompustatSegmentDataCustomers': {
        'stock': 'gvkey', 
        'time': 'datadate',
        'stata_file': 'CompustatSegmentDataCustomers.csv',
        'python_file': 'CompustatSegmentDataCustomers.csv'
    },
    'monthlyShortInterest': {
        'stock': 'gvkey', 
        'time': 'time_avail_m',
        'stata_file': 'monthlyShortInterest.dta',
        'python_file': 'monthlyShortInterest.parquet'
    },

    # CRSP Data
    'CRSPdistributions': {
        'stock': 'permno', 
        'time': 'exdt',
        'stata_file': 'CRSPdistributions.dta',
        'python_file': 'CRSPdistributions.parquet'
    },
    'mCRSP': {
        'stock': 'permno', 
        'time': 'date',
        'stata_file': 'mCRSP.csv',
        'python_file': 'mCRSP.csv'
    },
    'monthlyCRSP': {
        'stock': 'permno', 
        'time': 'time_avail_m',
        'stata_file': 'monthlyCRSP.dta',
        'python_file': 'monthlyCRSP.parquet'
    },
    'monthlyCRSPraw': {
        'stock': 'permno', 
        'time': 'time_avail_m',
        'stata_file': 'monthlyCRSPraw.dta',
        'python_file': 'monthlyCRSPraw.parquet'
    },
    'dailyCRSP': {
        'stock': 'permno', 
        'time': 'time_d',
        'stata_file': 'dailyCRSP.dta',
        'python_file': 'dailyCRSP.parquet'
    },
    'dailyCRSPprc': {
        'stock': 'permno', 
        'time': 'time_d',
        'stata_file': 'dailyCRSPprc.dta',
        'python_file': 'dailyCRSPprc.parquet'
    },
    'm_CRSPAcquisitions': {
        'stock': 'permno', 
        'time': None,
        'stata_file': 'm_CRSPAcquisitions.dta',
        'python_file': 'm_CRSPAcquisitions.parquet'
    },

    # IBES Data
    'IBES_EPS_Unadj': {
        'stock': 'tickerIBES', 
        'time': 'time_avail_m',
        'stata_file': 'IBES_EPS_Unadj.dta',
        'python_file': 'IBES_EPS_Unadj.parquet'
    },
    'IBES_EPS_Adj': {
        'stock': 'tickerIBES', 
        'time': 'time_avail_m',
        'stata_file': 'IBES_EPS_Adj.dta',
        'python_file': 'IBES_EPS_Adj.parquet'
    },
    'IBES_Recommendations': {
        'stock': 'tickerIBES', 
        'time': 'time_avail_m',
        'stata_file': 'IBES_Recommendations.dta',
        'python_file': 'IBES_Recommendations.parquet'
    },
    'IBES_UnadjustedActuals': {
        'stock': 'tickerIBES', 
        'time': 'time_avail_m',
        'stata_file': 'IBES_UnadjustedActuals.dta',
        'python_file': 'IBES_UnadjustedActuals.parquet'
    },

    # Market-Level Data (no stock identifier)
    'dailyFF': {
        'stock': None, 
        'time': 'time_d',
        'stata_file': 'dailyFF.dta',
        'python_file': 'dailyFF.parquet'
    },
    'monthlyFF': {
        'stock': None, 
        'time': 'time_avail_m',
        'stata_file': 'monthlyFF.dta',
        'python_file': 'monthlyFF.parquet'
    },
    'monthlyMarket': {
        'stock': None, 
        'time': 'time_avail_m',
        'stata_file': 'monthlyMarket.dta',
        'python_file': 'monthlyMarket.parquet'
    },
    'monthlyLiquidity': {
        'stock': None, 
        'time': 'time_avail_m',
        'stata_file': 'monthlyLiquidity.dta',
        'python_file': 'monthlyLiquidity.parquet'
    },
    'd_qfactor': {
        'stock': None, 
        'time': 'time_d',
        'stata_file': 'd_qfactor.dta',
        'python_file': 'd_qfactor.parquet'
    },
    'd_vix': {
        'stock': None, 
        'time': 'time_d',
        'stata_file': 'd_vix.dta',
        'python_file': 'd_vix.parquet'
    },
    'GNPdefl': {
        'stock': None, 
        'time': 'time_avail_m',
        'stata_file': 'GNPdefl.dta',
        'python_file': 'GNPdefl.parquet'
    },
    'TBill3M': {
        'stock': None, 
        'time': ['qtr', 'year'],  # Composite time identifier
        'stata_file': 'TBill3M.dta',
        'python_file': 'TBill3M.parquet'
    },
    'brokerLev': {
        'stock': None, 
        'time': ['qtr', 'year'],  # Composite time identifier
        'stata_file': 'brokerLev.dta',
        'python_file': 'brokerLev.parquet'
    },

    # Credit Ratings
    'm_SP_creditratings': {
        'stock': 'gvkey', 
        'time': 'time_avail_m',
        'stata_file': 'm_SP_creditratings.dta',
        'python_file': 'm_SP_creditratings.parquet'
    },
    'm_CIQ_creditratings': {
        'stock': 'gvkey', 
        'time': 'time_avail_m',
        'stata_file': 'm_CIQ_creditratings.dta',
        'python_file': 'm_CIQ_creditratings.parquet'
    },

    # Other Specialized Data
    'IPODates': {
        'stock': 'ticker', 
        'time': None,
        'stata_file': 'IPODates.dta',
        'python_file': 'IPODates.parquet'
    },
    'pin_monthly': {
        'stock': 'permno', 
        'time': 'time_avail_m',
        'stata_file': 'pin_monthly.dta',
        'python_file': 'pin_monthly.parquet'
    },
    'GovIndex': {
        'stock': 'ticker', 
        'time': 'time_avail_m',
        'stata_file': 'GovIndex.dta',
        'python_file': 'GovIndex.parquet'
    },
    'BAspreadsCorwin': {
        'stock': 'permno', 
        'time': 'time_avail_m',
        'stata_file': 'BAspreadsCorwin.dta',
        'python_file': 'BAspreadsCorwin.parquet'
    },
    'TR_13F': {
        'stock': 'permno', 
        'time': 'time_avail_m',
        'stata_file': 'TR_13F.dta',
        'python_file': 'TR_13F.parquet'
    },
    'hf_spread': {
        'stock': 'permno', 
        'time': 'time_avail_m',
        'stata_file': 'hf_spread.dta',
        'python_file': 'hf_spread.parquet'
    },

    # OptionMetrics Data
    'OptionMetricsVolume': {
        'stock': 'secid', 
        'time': 'time_avail_m',
        'stata_file': 'OptionMetricsVolume.dta',
        'python_file': 'OptionMetricsVolume.parquet'
    },
    'OptionMetricsVolSurf': {
        'stock': 'secid', 
        'time': 'time_avail_m',
        'stata_file': 'OptionMetricsVolSurf.dta',
        'python_file': 'OptionMetricsVolSurf.parquet'
    },
    'OptionMetricsXZZ': {
        'stock': 'secid', 
        'time': 'time_avail_m',
        'stata_file': 'OptionMetricsXZZ.dta',
        'python_file': 'OptionMetricsXZZ.parquet'
    },
    'OptionMetricsBH': {
        'stock': 'secid', 
        'time': 'time_avail_m',
        'stata_file': 'OptionMetricsBH.dta',
        'python_file': 'OptionMetricsBH.parquet'
    },

    # Linking Tables (no time filtering needed)
    'IBESCRSPLinkingTable': {
        'stock': 'permno', 
        'time': None,
        'stata_file': 'IBESCRSPLinkingTable.dta',
        'python_file': 'IBESCRSPLinkingTable.parquet'
    },
    'OPTIONMETRICSCRSPLinkingTable': {
        'stock': 'permno', 
        'time': None,
        'stata_file': 'OPTIONMETRICSCRSPLinkingTable.dta',
        'python_file': 'OPTIONMETRICSCRSPLinkingTable.parquet'
    },

    # Patent Data
    'PatentDataProcessed': {
        'stock': 'gvkey', 
        'time': 'year',
        'stata_file': 'PatentDataProcessed.dta',
        'python_file': 'PatentDataProcessed.parquet'
    },

    # Input-Output Momentum Data
    'InputOutputMomentumProcessed': {
        'stock': 'gvkey', 
        'time': 'time_avail_m',
        'stata_file': 'InputOutputMomentumProcessed.dta',
        'python_file': 'InputOutputMomentumProcessed.parquet'
    },

    # Customer Momentum Data
    'customerMom': {
        'stock': 'permno', 
        'time': 'time_avail_m',
        'stata_file': 'customerMom.dta',
        'python_file': 'customerMom.parquet'
    }
}

# File paths
PYDATA_PATH = Path("../pyData/Intermediate")
DATA_PATH = Path("../Data/Intermediate")


def load_parquet_file(file_path: Path, maxrows: Optional[int] = None) -> pd.DataFrame:
    """Load parquet file with error handling."""
    try:
        df = pd.read_parquet(file_path)
        original_rows = len(df)
        
        if maxrows is not None and maxrows < original_rows:
            df = df.head(maxrows)
            logger.info(f"Loaded parquet file: {file_path.name} ({len(df):,} rows, limited from {original_rows:,})")
            logger.warning(f"Row limiting applied: validation uses subset of data ({maxrows:,}/{original_rows:,} rows)")
        else:
            logger.info(f"Loaded parquet file: {file_path.name} ({len(df):,} rows)")
        
        return df
    except Exception as e:
        logger.error(f"Error loading parquet {file_path}: {e}")
        raise


def load_csv_file(file_path: Path, maxrows: Optional[int] = None) -> pd.DataFrame:
    """Load CSV file with error handling and type inference."""
    try:
        # Try different encodings and separators
        encodings = ['utf-8', 'latin1', 'cp1252']
        for encoding in encodings:
            try:
                df = pd.read_csv(file_path, encoding=encoding, low_memory=False, nrows=maxrows)
                
                if maxrows is not None:
                    logger.info(f"Loaded CSV file: {file_path.name} ({len(df):,} rows, limited to maxrows={maxrows:,})")
                    logger.warning(f"Row limiting applied: validation uses subset of data (max {maxrows:,} rows)")
                else:
                    logger.info(f"Loaded CSV file: {file_path.name} ({len(df):,} rows)")
                
                return df
            except UnicodeDecodeError:
                continue

        # If all encodings fail, raise error
        raise ValueError(f"Could not decode {file_path} with any encoding")

    except Exception as e:
        logger.error(f"Error loading CSV {file_path}: {e}")
        raise


def load_dta_file(file_path: Path, maxrows: Optional[int] = None) -> pd.DataFrame:
    """Load Stata DTA file with error handling."""
    try:
        if maxrows is not None:
            # For DTA files, we need to read in chunks or limit rows after loading
            df = pd.read_stata(file_path, preserve_dtypes=False, chunksize=maxrows)
            df = next(df)  # Get first chunk
            logger.info(f"Loaded DTA file: {file_path.name} ({len(df):,} rows, limited to maxrows={maxrows:,})")
            logger.warning(f"Row limiting applied: validation uses subset of data (max {maxrows:,} rows)")
        else:
            df = pd.read_stata(file_path, preserve_dtypes=False)
            logger.info(f"Loaded DTA file: {file_path.name} ({len(df):,} rows)")
        
        return df
    except Exception as e:
        logger.error(f"Error loading DTA {file_path}: {e}")
        raise


def load_dataset(file_path: Path, maxrows: Optional[int] = None) -> pd.DataFrame:
    """Load dataset based on file extension."""
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    suffix = file_path.suffix.lower()
    if suffix == '.parquet':
        return load_parquet_file(file_path, maxrows)
    elif suffix == '.csv':
        return load_csv_file(file_path, maxrows)
    elif suffix == '.dta':
        return load_dta_file(file_path, maxrows)
    else:
        raise ValueError(f"Unsupported file format: {suffix}")


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names by stripping whitespace and lowercasing."""
    df.columns = df.columns.str.strip().str.lower()
    return df


def normalize_date_columns(df: pd.DataFrame, date_cols: List[str]) -> pd.DataFrame:
    """Normalize date columns to consistent format."""
    df = df.copy()
    for col in date_cols:
        if col in df.columns:
            try:
                # Handle string dates
                if df[col].dtype == 'object':
                    # Try different date formats
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                # Convert to date only (remove time component)
                df[col] = df[col].dt.date
            except Exception as e:
                logger.warning(f"Could not normalize date column {col}: {e}")
    return df


def normalize_identifier_types(df: pd.DataFrame, id_cols: List[str]) -> pd.DataFrame:
    """Normalize identifier column types."""
    df = df.copy()
    for col in id_cols:
        if col in df.columns:
            # Convert to string for consistent comparison
            try:
                df[col] = df[col].astype(str)
                # Remove .0 from float-converted integers
                df[col] = df[col].str.replace(r'\.0$', '', regex=True)
                # Handle 'nan' strings
                df[col] = df[col].replace('nan', np.nan)
            except Exception as e:
                logger.warning(f"Could not normalize identifier column {col}: {e}")
    return df


def get_identifier_columns(dataset_name: str) -> Tuple[Optional[str], Union[str, List[str], None]]:
    """Get stock and time identifier columns for a dataset."""
    if dataset_name not in DATASET_IDENTIFIERS:
        raise ValueError(f"Dataset {dataset_name} not found in identifier mapping")

    config = DATASET_IDENTIFIERS[dataset_name]
    return config['stock'], config['time']


def create_composite_identifier(df: pd.DataFrame, time_cols: List[str]) -> pd.Series:
    """Create composite identifier from multiple time columns."""
    if len(time_cols) == 2 and set(time_cols) == {'qtr', 'year'}:
        # Special handling for quarter-year combinations
        return df['year'].astype(str) + '-Q' + df['qtr'].astype(str)
    else:
        # General case: concatenate all columns
        return df[time_cols].astype(str).apply(lambda x: '_'.join(x), axis=1)


def extract_identifiers(df: pd.DataFrame, stock_col: Optional[str], 
                       time_col: Union[str, List[str], None]) -> pd.DataFrame:
    """Extract unique identifier combinations from dataset."""
    id_cols = []

    # Add stock identifier if present
    if stock_col and stock_col in df.columns:
        id_cols.append(stock_col)

    # Handle time identifier(s)
    if time_col:
        if isinstance(time_col, list):
            # Composite time identifier
            if all(col in df.columns for col in time_col):
                df = df.copy()
                composite_time = create_composite_identifier(df, time_col)
                df['_composite_time'] = composite_time
                id_cols.append('_composite_time')
            else:
                missing_cols = [col for col in time_col if col not in df.columns]
                logger.warning(f"Missing time columns: {missing_cols}")
        else:
            # Single time identifier
            if time_col in df.columns:
                id_cols.append(time_col)
            else:
                logger.warning(f"Missing time column: {time_col}")

    if not id_cols:
        # No identifiers found - return all rows
        logger.warning("No identifier columns found - using all rows")
        return df.copy()

    # Extract unique combinations
    unique_ids = df[id_cols].drop_duplicates()
    logger.info(f"Extracted {len(unique_ids):,} unique identifier combinations")

    return unique_ids


def analyze_identifier_compatibility(python_df: pd.DataFrame, stata_df: pd.DataFrame,
                                   stock_col: Optional[str], 
                                   time_col: Union[str, List[str], None]) -> Dict[str, Any]:
    """Analyze identifier type compatibility between Python and Stata datasets."""
    analysis = {
        'compatible': True,
        'issues': [],
        'stock_analysis': None,
        'time_analysis': None,
        'overlap_analysis': None
    }
    
    # Analyze stock identifier
    if stock_col and stock_col in python_df.columns and stock_col in stata_df.columns:
        py_type = python_df[stock_col].dtype
        stata_type = stata_df[stock_col].dtype
        
        py_samples = python_df[stock_col].dropna().head(5).tolist()
        stata_samples = stata_df[stock_col].dropna().head(5).tolist()
        
        # Check for type mismatches
        type_mismatch = False
        if py_type == 'object' and pd.api.types.is_numeric_dtype(stata_type):
            type_mismatch = True
            analysis['issues'].append(f"Stock identifier type mismatch: Python={py_type} (strings), Stata={stata_type} (numeric)")
        elif pd.api.types.is_numeric_dtype(py_type) and stata_type == 'object':
            type_mismatch = True
            analysis['issues'].append(f"Stock identifier type mismatch: Python={py_type} (numeric), Stata={stata_type} (strings)")
        
        # Test overlap
        py_values = set(str(v) for v in python_df[stock_col].dropna().unique()[:1000])
        stata_values = set(str(v) for v in stata_df[stock_col].dropna().unique()[:1000])
        direct_overlap = len(py_values.intersection(stata_values))
        
        # Try numeric conversion if string/int mismatch
        numeric_overlap = 0
        if type_mismatch:
            try:
                py_numeric = set()
                for val in python_df[stock_col].dropna().unique()[:1000]:
                    try:
                        py_numeric.add(int(float(str(val))))
                    except:
                        pass
                        
                stata_numeric = set()
                for val in stata_df[stock_col].dropna().unique()[:1000]:
                    try:
                        stata_numeric.add(int(float(str(val))))
                    except:
                        pass
                        
                numeric_overlap = len(py_numeric.intersection(stata_numeric))
            except:
                pass
        
        analysis['stock_analysis'] = {
            'column': stock_col,
            'python_type': str(py_type),
            'stata_type': str(stata_type),
            'python_samples': py_samples,
            'stata_samples': stata_samples,
            'type_mismatch': type_mismatch,
            'direct_overlap': direct_overlap,
            'numeric_overlap': numeric_overlap,
            'python_unique_count': len(py_values),
            'stata_unique_count': len(stata_values)
        }
        
        if direct_overlap == 0 and numeric_overlap == 0:
            analysis['compatible'] = False
            analysis['issues'].append(f"No identifier overlap found for {stock_col}")
    
    # Analyze time identifier
    if time_col and not isinstance(time_col, list):
        if time_col in python_df.columns and time_col in stata_df.columns:
            py_type = python_df[time_col].dtype
            stata_type = stata_df[time_col].dtype
            
            py_samples = python_df[time_col].dropna().head(5).tolist()
            stata_samples = stata_df[time_col].dropna().head(5).tolist()
            
            # Check for date format mismatches
            date_mismatch = False
            if pd.api.types.is_datetime64_any_dtype(py_type) and stata_type == 'object':
                date_mismatch = True
                analysis['issues'].append(f"Time identifier format mismatch: Python=datetime, Stata=string")
            elif py_type == 'object' and pd.api.types.is_datetime64_any_dtype(stata_type):
                date_mismatch = True
                analysis['issues'].append(f"Time identifier format mismatch: Python=string, Stata=datetime")
            
            analysis['time_analysis'] = {
                'column': time_col,
                'python_type': str(py_type),
                'stata_type': str(stata_type),
                'python_samples': [str(s) for s in py_samples],
                'stata_samples': [str(s) for s in stata_samples],
                'date_mismatch': date_mismatch
            }
            
            if date_mismatch:
                analysis['compatible'] = False
    
    return analysis


def filter_dataset_by_identifiers(df: pd.DataFrame, identifiers: pd.DataFrame,
                                 stock_col: Optional[str], 
                                 time_col: Union[str, List[str], None]) -> pd.DataFrame:
    """Filter dataset to only include rows matching the given identifiers."""
    if len(identifiers) == 0:
        logger.warning("No identifiers provided - returning empty dataset")
        return df.iloc[:0].copy()

    # Prepare merge columns
    merge_cols = []
    df_copy = df.copy()

    # Handle stock identifier
    if stock_col and stock_col in df.columns and stock_col in identifiers.columns:
        merge_cols.append(stock_col)

    # Handle time identifier(s)
    if time_col:
        if isinstance(time_col, list):
            # Composite time identifier
            if all(col in df.columns for col in time_col):
                composite_time = create_composite_identifier(df_copy, time_col)
                df_copy['_composite_time'] = composite_time
                merge_cols.append('_composite_time')
        else:
            # Single time identifier
            if time_col in df.columns and time_col in identifiers.columns:
                merge_cols.append(time_col)

    if not merge_cols:
        logger.warning("No matching columns for filtering - returning original dataset")
        return df.copy()

    # Perform inner join to filter
    filtered_df = df_copy.merge(identifiers[merge_cols], on=merge_cols, how='inner')

    # Remove composite time column if added
    if '_composite_time' in filtered_df.columns:
        filtered_df = filtered_df.drop('_composite_time', axis=1)

    logger.info(f"Filtered dataset from {len(df):,} to {len(filtered_df):,} rows")

    return filtered_df


def compare_datasets(df1: pd.DataFrame, df2: pd.DataFrame, 
                    dataset_name: str, tolerance: float = 1e-6) -> Dict[str, Any]:
    """Compare two datasets and return detailed comparison results."""
    comparison = {
        'dataset': dataset_name,
        'match_status': 'unknown',
        'row_count_match': False,
        'column_count_match': False,
        'column_names_match': False,
        'data_match': False,
        'details': {},
        'errors': []
    }

    try:
        # Basic shape comparison
        comparison['details']['df1_shape'] = df1.shape
        comparison['details']['df2_shape'] = df2.shape
        comparison['row_count_match'] = df1.shape[0] == df2.shape[0]
        comparison['column_count_match'] = df1.shape[1] == df2.shape[1]
        
        # Warn if shape mismatch after alignment
        if df1.shape[0] != df2.shape[0]:
            logger.warning(f"Dataset shape mismatch after alignment: {df1.shape[0]} vs {df2.shape[0]}")

        # Column name comparison
        cols1 = set(df1.columns.str.lower().str.strip())
        cols2 = set(df2.columns.str.lower().str.strip())
        comparison['column_names_match'] = cols1 == cols2
        comparison['details']['common_columns'] = list(cols1.intersection(cols2))
        comparison['details']['df1_only_columns'] = list(cols1 - cols2)
        comparison['details']['df2_only_columns'] = list(cols2 - cols1)

        # Data comparison for common columns
        if comparison['details']['common_columns']:
            # Normalize column names for comparison
            df1_norm = normalize_column_names(df1.copy())
            df2_norm = normalize_column_names(df2.copy())

            # Compare common columns
            common_cols = comparison['details']['common_columns']
            data_differences = {}

            for col in common_cols:
                try:
                    # Handle different data types
                    s1 = df1_norm[col]
                    s2 = df2_norm[col]

                    # Convert to comparable types
                    if s1.dtype == 'object' and s2.dtype == 'object':
                        # String comparison
                        s1 = s1.astype(str).fillna('')
                        s2 = s2.astype(str).fillna('')
                        matches = (s1 == s2)
                    elif pd.api.types.is_numeric_dtype(s1) and pd.api.types.is_numeric_dtype(s2):
                        # Numeric comparison with tolerance
                        matches = np.isclose(s1, s2, rtol=tolerance, atol=tolerance, equal_nan=True)
                    else:
                        # Mixed types - convert to string
                        s1 = s1.astype(str).fillna('')
                        s2 = s2.astype(str).fillna('')
                        matches = (s1 == s2)

                    match_rate = matches.mean() if len(matches) > 0 else 0
                    if match_rate < 1.0:
                        # Get sample of mismatched rows for diagnosis
                        mismatched_mask = ~matches
                        if hasattr(mismatched_mask, 'index'):
                            mismatched_indices = mismatched_mask[mismatched_mask].index[:20]  # First 20 mismatches
                        else:
                            # Handle numpy arrays
                            mismatched_indices = np.where(mismatched_mask)[0][:5]
                        mismatch_samples = []
                        
                        for idx in mismatched_indices:
                            if idx < len(df1_norm) and idx < len(df2_norm):
                                sample = {
                                    'row_index': int(idx),
                                    'df1_value': str(s1.iloc[idx]) if idx < len(s1) else 'N/A',
                                    'df2_value': str(s2.iloc[idx]) if idx < len(s2) else 'N/A'
                                }
                                # Add identifier columns if available
                                if 'gvkey' in df1_norm.columns:
                                    sample['gvkey'] = str(df1_norm.iloc[idx]['gvkey']) if idx < len(df1_norm) else 'N/A'
                                if 'time_avail_m' in df1_norm.columns:
                                    sample['time_avail_m'] = str(df1_norm.iloc[idx]['time_avail_m']) if idx < len(df1_norm) else 'N/A'
                                mismatch_samples.append(sample)
                        
                        data_differences[col] = {
                            'match_rate': match_rate,
                            'total_rows': len(matches),
                            'mismatched_rows': (~matches).sum(),
                            'mismatch_samples': mismatch_samples
                        }

                except Exception as e:
                    data_differences[col] = {'error': str(e)}

            comparison['details']['data_differences'] = data_differences
            comparison['data_match'] = len(data_differences) == 0
            
            # Store full row data for creating comparison tables
            if data_differences:
                # Find rows with any mismatches for table generation
                all_mismatched_indices = set()
                for col, diff in data_differences.items():
                    if 'mismatch_samples' in diff:
                        for sample in diff['mismatch_samples']:
                            all_mismatched_indices.add(sample['row_index'])
                
                # Collect full row data for mismatched records (limit to first 5)
                comparison_table_data = []
                for idx in sorted(list(all_mismatched_indices))[:5]:
                    if idx < len(df1_norm) and idx < len(df2_norm):
                        # Python row
                        python_row = {'source': 'Python', 'row_index': idx}
                        python_row.update(df1_norm.iloc[idx].to_dict())
                        
                        # Stata row  
                        stata_row = {'source': 'Stata', 'row_index': idx}
                        stata_row.update(df2_norm.iloc[idx].to_dict())
                        
                        comparison_table_data.extend([python_row, stata_row])
                
                comparison['details']['comparison_table_data'] = comparison_table_data

        # Overall match status
        if (comparison['row_count_match'] and 
            comparison['column_names_match'] and 
            comparison['data_match']):
            comparison['match_status'] = 'perfect_match'
        elif (comparison['row_count_match'] and 
              len(comparison['details']['common_columns']) > 0 and
              all(diff.get('match_rate', 0) > 0.99 
                  for diff in comparison['details']['data_differences'].values()
                  if 'error' not in diff)):
            comparison['match_status'] = 'minor_differences'
        else:
            comparison['match_status'] = 'major_differences'

    except Exception as e:
        comparison['errors'].append(str(e))
        comparison['match_status'] = 'error'
        logger.error(f"Error comparing datasets {dataset_name}: {e}")

    return comparison


def validate_single_dataset(dataset_name: str, tolerance: float = 1e-6, maxrows: Optional[int] = None) -> Dict[str, Any]:
    """Validate a single dataset by comparing Python vs Stata versions."""
    logger.info(f"Validating dataset: {dataset_name}")

    result = {
        'dataset': dataset_name,
        'status': 'unknown',
        'comparison': None,
        'errors': [],
        'processing_time': 0
    }

    start_time = datetime.now()

    try:
        # Get dataset configuration
        if dataset_name not in DATASET_IDENTIFIERS:
            raise ValueError(f"Dataset {dataset_name} not found in configuration")

        config = DATASET_IDENTIFIERS[dataset_name]
        stock_col, time_col = config['stock'], config['time']

        # Build file paths
        python_file = PYDATA_PATH / config['python_file']
        stata_file = DATA_PATH / config['stata_file']

        # Check if files exist
        if not python_file.exists():
            raise FileNotFoundError(f"Python file not found: {python_file}")
        if not stata_file.exists():
            raise FileNotFoundError(f"Stata file not found: {stata_file}")

        # Load datasets
        logger.info(f"Loading Python file: {python_file}")
        python_df = load_dataset(python_file, maxrows)

        logger.info(f"Loading Stata file: {stata_file}")
        stata_df = load_dataset(stata_file, maxrows)

        # Normalize data for comparison
        id_cols = []
        if stock_col:
            id_cols.append(stock_col)
        if time_col:
            if isinstance(time_col, list):
                id_cols.extend(time_col)
            else:
                id_cols.append(time_col)

        # Analyze identifier compatibility BEFORE normalization
        identifier_analysis = analyze_identifier_compatibility(
            python_df, stata_df, stock_col, time_col
        )

        # Normalize identifier types
        if id_cols:
            python_df = normalize_identifier_types(python_df, id_cols)
            stata_df = normalize_identifier_types(stata_df, id_cols)

        # Extract identifiers from BOTH datasets for inner join approach
        python_identifiers = extract_identifiers(python_df, stock_col, time_col)
        stata_identifiers = extract_identifiers(stata_df, stock_col, time_col)
        
        # Find common identifiers (intersection) to eliminate data recency differences
        if len(python_identifiers) > 0 and len(stata_identifiers) > 0:
            # Get merge columns for intersection
            merge_cols = []
            if stock_col and stock_col in python_identifiers.columns and stock_col in stata_identifiers.columns:
                merge_cols.append(stock_col)
            if time_col:
                if isinstance(time_col, list):
                    if '_composite_time' in python_identifiers.columns and '_composite_time' in stata_identifiers.columns:
                        merge_cols.append('_composite_time')
                else:
                    if time_col in python_identifiers.columns and time_col in stata_identifiers.columns:
                        merge_cols.append(time_col)
            
            if merge_cols:
                # Find intersection of identifiers
                common_identifiers = python_identifiers[merge_cols].merge(
                    stata_identifiers[merge_cols], on=merge_cols, how='inner'
                )
                logger.info(f"Common identifiers: {len(common_identifiers):,} (Python: {len(python_identifiers):,}, Stata: {len(stata_identifiers):,})")
            else:
                logger.warning("No merge columns found - using Python identifiers as fallback")
                common_identifiers = python_identifiers
        else:
            logger.warning("One dataset has no identifiers - using Python identifiers as fallback")
            common_identifiers = python_identifiers

        # Filter BOTH datasets to common identifiers only
        filtered_python_df = filter_dataset_by_identifiers(
            python_df, common_identifiers, stock_col, time_col
        )
        filtered_stata_df = filter_dataset_by_identifiers(
            stata_df, common_identifiers, stock_col, time_col
        )

        # Log identifier compatibility issues
        if not identifier_analysis['compatible']:
            for issue in identifier_analysis['issues']:
                logger.warning(f"Identifier issue: {issue}")
        
        # Warn if filtering returned no results
        if len(filtered_stata_df) == 0 and len(common_identifiers) > 0:
            logger.warning(f"Filtering returned 0 rows despite {len(common_identifiers)} common identifiers - likely identifier format mismatch")

        # Create backbone from common identifiers to ensure exact alignment
        id_cols = []
        if stock_col: 
            id_cols.append(stock_col)
        if time_col:
            if isinstance(time_col, list): 
                id_cols.extend(time_col)
            else: 
                id_cols.append(time_col)

        if id_cols:
            # Use common identifiers as backbone for perfect alignment
            common_backbone = common_identifiers[id_cols].copy()
            
            # Merge both datasets onto common backbone to ensure identical structure
            aligned_python_df = common_backbone.merge(
                filtered_python_df, on=id_cols, how='left'
            )
            aligned_stata_df = common_backbone.merge(
                filtered_stata_df, on=id_cols, how='left'
            )
            
            logger.info(f"Aligned datasets: Python {len(aligned_python_df)}, Stata {len(aligned_stata_df)}")
        else:
            # Fallback for datasets without identifiers
            aligned_python_df = filtered_python_df
            aligned_stata_df = filtered_stata_df
            logger.warning("No identifier columns found - using unaligned comparison")

        # Compare the aligned datasets (now both filtered to common identifiers)
        comparison = compare_datasets(
            aligned_python_df, aligned_stata_df, dataset_name, tolerance
        )

        # Add identifier analysis to results
        comparison['identifier_analysis'] = identifier_analysis

        result['comparison'] = comparison
        result['status'] = 'completed'

        logger.info(f"Validation completed for {dataset_name}: {comparison['match_status']}")

    except Exception as e:
        error_msg = str(e)
        result['errors'].append(error_msg)
        result['status'] = 'error'
        logger.error(f"Error validating {dataset_name}: {error_msg}")

    finally:
        result['processing_time'] = (datetime.now() - start_time).total_seconds()

    return result


def validate_all_datasets(datasets: Optional[List[str]] = None, 
                         tolerance: float = 1e-6, maxrows: Optional[int] = None) -> List[Dict[str, Any]]:
    """Validate all or specified datasets."""
    if datasets is None:
        datasets = list(DATASET_IDENTIFIERS.keys())

    logger.info(f"Starting validation of {len(datasets)} datasets")

    results = []
    for dataset in datasets:
        try:
            result = validate_single_dataset(dataset, tolerance, maxrows)
            results.append(result)
        except Exception as e:
            logger.error(f"Failed to validate {dataset}: {e}")
            results.append({
                'dataset': dataset,
                'status': 'error',
                'errors': [str(e)],
                'comparison': None,
                'processing_time': 0
            })

    logger.info(f"Completed validation of {len(results)} datasets")
    return results


def generate_summary_report(results: List[Dict[str, Any]]) -> str:
    """Generate a summary report of validation results."""
    total_datasets = len(results)
    perfect_matches = sum(1 for r in results 
                         if r.get('comparison') and r['comparison'].get('match_status') == 'perfect_match')
    minor_differences = sum(1 for r in results 
                           if r.get('comparison') and r['comparison'].get('match_status') == 'minor_differences')
    major_differences = sum(1 for r in results 
                           if r.get('comparison') and r['comparison'].get('match_status') == 'major_differences')
    errors = sum(1 for r in results if r['status'] == 'error')
    
    # Categorize errors
    missing_datasets = [r for r in results if r['status'] == 'error' and 
                       any('not found' in str(err) for err in r.get('errors', []))]
    processing_errors = [r for r in results if r['status'] == 'error' and 
                        not any('not found' in str(err) for err in r.get('errors', []))]

    total_processing_time = sum(r.get('processing_time', 0) for r in results)

    report = f"""
# Dataset Validation Summary Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overall Results
- **Total Datasets Processed**: {total_datasets}
- **Perfect Matches**: {perfect_matches} ({perfect_matches/total_datasets*100:.1f}%)
- **Minor Differences**: {minor_differences} ({minor_differences/total_datasets*100:.1f}%)
- **Major Differences**: {major_differences} ({major_differences/total_datasets*100:.1f}%)
- **⚠️ MISSING DATASETS**: {len(missing_datasets)} ({len(missing_datasets)/total_datasets*100:.1f}%)
- **Processing Errors**: {len(processing_errors)} ({len(processing_errors)/total_datasets*100:.1f}%)
- **Total Processing Time**: {total_processing_time:.1f} seconds

## Status Breakdown
"""

    # Add missing datasets section first for high visibility
    if missing_datasets:
        report += f"""
### ⚠️ MISSING DATASETS ({len(missing_datasets)} datasets) ⚠️
**CRITICAL: These datasets could not be found and need immediate attention!**

"""
        for result in missing_datasets:
            dataset = result['dataset']
            errors_list = result['errors']
            report += f"- **{dataset}**: {'; '.join(errors_list)}\n"

    report += f"""

### Perfect Matches ({perfect_matches} datasets)
"""

    # List perfect matches
    perfect_match_datasets = [r['dataset'] for r in results 
                             if r.get('comparison') and r['comparison'].get('match_status') == 'perfect_match']
    for dataset in perfect_match_datasets:
        report += f"- {dataset}\n"

    report += f"\n### Minor Differences ({minor_differences} datasets)\n"

    # List minor differences with details
    minor_diff_datasets = [r for r in results 
                          if r.get('comparison') and r['comparison'].get('match_status') == 'minor_differences']
    for result in minor_diff_datasets:
        dataset = result['dataset']
        comparison = result['comparison']
        report += f"- **{dataset}**:\n"
        if 'data_differences' in comparison['details']:
            for col, diff in comparison['details']['data_differences'].items():
                if 'match_rate' in diff:
                    report += f"  - {col}: {diff['match_rate']:.3f} match rate ({diff['mismatched_rows']} mismatched rows)\n"

    report += f"\n### Major Differences ({major_differences} datasets)\n"

    # List major differences with details
    major_diff_datasets = [r for r in results 
                          if r.get('comparison') and r['comparison'].get('match_status') == 'major_differences']
    for result in major_diff_datasets:
        dataset = result['dataset']
        comparison = result['comparison']
        report += f"- **{dataset}**:\n"
        report += f"  - Row count match: {comparison['row_count_match']}\n"
        report += f"  - Column names match: {comparison['column_names_match']}\n"
        report += f"  - Data match: {comparison['data_match']}\n"
        if comparison['details']['df1_only_columns']:
            report += f"  - Python-only columns: {comparison['details']['df1_only_columns']}\n"
        if comparison['details']['df2_only_columns']:
            report += f"  - Stata-only columns: {comparison['details']['df2_only_columns']}\n"

    report += f"\n### Processing Errors ({len(processing_errors)} datasets)\n"

    # List processing errors (excluding missing datasets which are shown above)
    for result in processing_errors:
        dataset = result['dataset']
        errors_list = result['errors']
        report += f"- **{dataset}**: {'; '.join(errors_list)}\n"

    return report


def generate_comparison_table_text(table_data: List[Dict[str, Any]]) -> str:
    """Generate text table for side-by-side comparison of mismatched rows (tibble-like format)."""
    if not table_data:
        return ""
    
    # Get all column names (excluding internal ones)
    exclude_cols = {'row_index'}
    all_columns = set()
    for row in table_data:
        all_columns.update(row.keys())
    all_columns -= exclude_cols
    
    # Sort columns with important ones first
    priority_cols = ['source', 'gvkey', 'time_avail_m', 'datadateq', 'fyearq', 'fqtr', 'datacqtr', 'datafqtr']
    sorted_columns = []
    for col in priority_cols:
        if col in all_columns:
            sorted_columns.append(col)
            all_columns.remove(col)
    sorted_columns.extend(sorted(all_columns))
    
    # Calculate column widths
    col_widths = {}
    for col in sorted_columns:
        col_widths[col] = max(len(str(col)), 
                             max(len(str(row.get(col, 'NaN'))) for row in table_data))
        # Limit column width to reasonable max
        col_widths[col] = min(col_widths[col], 20)
    
    # Format values helper function
    def format_value(value):
        if pd.isna(value) or value is None:
            return 'NaN'
        elif isinstance(value, float):
            return f'{value:.3f}' if abs(value) < 1000 else f'{value:.2e}'
        return str(value)
    
    # Build text table
    text = '\n```\n'
    
    # Header row
    header_parts = []
    for col in sorted_columns:
        header_parts.append(f"{col:<{col_widths[col]}}")
    text += '  ' + ' | '.join(header_parts) + '\n'
    
    # Separator row
    sep_parts = []
    for col in sorted_columns:
        sep_parts.append('-' * col_widths[col])
    text += '  ' + '-+-'.join(sep_parts) + '\n'
    
    # Data rows
    for i, row in enumerate(table_data):
        if i >= 10:  # Limit to first 10 rows for readability
            remaining = len(table_data) - i
            text += f'  ... and {remaining} more rows\n'
            break
            
        row_parts = []
        for col in sorted_columns:
            value = format_value(row.get(col, 'NaN'))
            # Truncate if too long
            if len(value) > col_widths[col]:
                value = value[:col_widths[col]-2] + '..'
            row_parts.append(f"{value:<{col_widths[col]}}")
        text += '  ' + ' | '.join(row_parts) + '\n'
    
    text += '```\n'
    text += f'*Showing {min(len(table_data), 10)} mismatched rows (Python vs Stata comparison) with {len(sorted_columns)} columns*\n\n'
    
    return text


def generate_difference_table_text(table_data: List[Dict[str, Any]]) -> str:
    """Generate text table showing numeric differences (Stata - Python) in scientific notation."""
    if not table_data:
        return ""
    
    # Group data by row index to pair Python and Stata values
    rows_by_index = {}
    for row in table_data:
        idx = row.get('row_index')
        if idx is not None:
            if idx not in rows_by_index:
                rows_by_index[idx] = {}
            source = row.get('source')
            if source:
                rows_by_index[idx][source] = row
    
    # Calculate differences for rows with both Python and Stata data
    difference_data = []
    for idx, sources in rows_by_index.items():
        if 'Python' in sources and 'Stata' in sources:
            python_row = sources['Python']
            stata_row = sources['Stata']
            
            diff_row = {'row_index': idx}
            
            # Add identifier columns to difference row for easy identification
            identifier_cols = ['gvkey', 'time_avail_m']
            
            # Get all columns (excluding internal ones)
            exclude_cols = {'source', 'row_index'}
            all_columns = set()
            all_columns.update(python_row.keys())
            all_columns.update(stata_row.keys())
            all_columns -= exclude_cols
            
            for col in sorted(all_columns):
                python_val = python_row.get(col)
                stata_val = stata_row.get(col)
                
                # For identifier columns, show actual values instead of differences
                if col in identifier_cols:
                    # Show the actual value since they match by construction
                    diff_row[col] = python_val if python_val is not None else stata_val
                else:
                    # Check for exact matches first (including N/A cases)
                    if ((pd.isna(python_val) or python_val is None or str(python_val) == 'nan') and 
                        (pd.isna(stata_val) or stata_val is None or str(stata_val) == 'nan')):
                        # Both are N/A/None/nan - exact match
                        diff_row[col] = 'same'
                    elif python_val == stata_val:
                        # Exact value match
                        diff_row[col] = 'same'
                    else:
                        # Calculate difference for numeric columns
                        try:
                            if (pd.api.types.is_numeric_dtype(type(python_val)) and 
                                pd.api.types.is_numeric_dtype(type(stata_val)) and
                                python_val is not None and stata_val is not None and
                                not pd.isna(python_val) and not pd.isna(stata_val)):
                                
                                py_num = float(python_val)
                                stata_num = float(stata_val)
                                difference = stata_num - py_num
                                if abs(difference) < 1e-15:  # Handle floating point precision
                                    diff_row[col] = 'same'
                                else:
                                    diff_row[col] = f'{difference:.2e}'
                            else:
                                # Non-numeric or missing values that differ
                                diff_row[col] = 'N/A'
                        except (ValueError, TypeError, OverflowError):
                            diff_row[col] = 'N/A'
            
            difference_data.append(diff_row)
    
    if not difference_data:
        return ""
    
    # Get all difference columns
    exclude_cols = {'row_index'}
    all_columns = set()
    for row in difference_data:
        all_columns.update(row.keys())
    all_columns -= exclude_cols
    
    # Sort columns to match data sample table order (excluding 'source')
    priority_cols = ['gvkey', 'time_avail_m', 'datadateq', 'fyearq', 'fqtr', 'datacqtr', 'datafqtr']
    sorted_columns = []
    for col in priority_cols:
        if col in all_columns:
            sorted_columns.append(col)
            all_columns.remove(col)
    sorted_columns.extend(sorted(all_columns))
    
    # Calculate column widths (no limit for scrollable display)
    col_widths = {}
    for col in sorted_columns:
        col_widths[col] = max(len(str(col)), 
                             max(len(str(row.get(col, 'N/A'))) for row in difference_data))
    
    # Build text table
    text = '\n```\n'
    
    # Header row
    header_parts = []
    for col in sorted_columns:
        header_parts.append(f"{col:<{col_widths[col]}}")
    text += '  ' + ' | '.join(header_parts) + '\n'
    
    # Separator row
    sep_parts = []
    for col in sorted_columns:
        sep_parts.append('-' * col_widths[col])
    text += '  ' + '-+-'.join(sep_parts) + '\n'
    
    # Data rows
    for i, row in enumerate(difference_data):
        if i >= 5:  # Limit to first 5 rows for readability
            remaining = len(difference_data) - i
            text += f'  ... and {remaining} more rows\n'
            break
            
        row_parts = []
        for col in sorted_columns:
            value = str(row.get(col, 'N/A'))
            row_parts.append(f"{value:<{col_widths[col]}}")
        text += '  ' + ' | '.join(row_parts) + '\n'
    
    text += '```\n'
    text += f'*Showing differences (Stata - Python) for {min(len(difference_data), 5)} mismatched rows with {len(sorted_columns)} columns*\n\n'
    
    return text


def generate_detailed_report(results: List[Dict[str, Any]]) -> str:
    """Generate a detailed report with full comparison results."""
    # Categorize errors for prominent display
    missing_datasets = [r for r in results if r['status'] == 'error' and 
                       any('not found' in str(err) for err in r.get('errors', []))]
    processing_errors = [r for r in results if r['status'] == 'error' and 
                        not any('not found' in str(err) for err in r.get('errors', []))]
    successful_results = [r for r in results if r['status'] != 'error']
    
    report = f"""
# Detailed Dataset Validation Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""

    # Add missing datasets section first with high visibility
    if missing_datasets:
        report += f"""
# ⚠️ CRITICAL: MISSING DATASETS ⚠️

**{len(missing_datasets)} DATASETS COULD NOT BE FOUND AND NEED IMMEDIATE ATTENTION!**

"""
        for result in missing_datasets:
            dataset = result['dataset']
            errors_list = result['errors']
            processing_time = result.get('processing_time', 0)
            
            report += f"""
## ❌ MISSING: {dataset}
- **STATUS**: MISSING FILE
- **PROCESSING TIME**: {processing_time:.2f} seconds
- **ERRORS**: {'; '.join(errors_list)}

"""

    # Process successful results and processing errors
    all_other_results = successful_results + processing_errors
    for result in all_other_results:
        dataset = result['dataset']
        status = result['status']
        processing_time = result.get('processing_time', 0)

        report += f"## {dataset}\n"
        report += f"- **Status**: {status}\n"
        report += f"- **Processing Time**: {processing_time:.2f} seconds\n"

        if result['errors']:
            report += f"- **Errors**: {'; '.join(result['errors'])}\n"

        if result['comparison']:
            comp = result['comparison']
            report += f"- **Match Status**: {comp['match_status']}\n"
            report += f"- **Row Count Match**: {comp['row_count_match']}\n"
            report += f"- **Column Names Match**: {comp['column_names_match']}\n"
            report += f"- **Data Match**: {comp['data_match']}\n"

            # Shape details
            details = comp['details']
            report += f"- **Python Shape**: {details['df1_shape']}\n"
            report += f"- **Stata Shape**: {details['df2_shape']}\n"

            # Column differences
            if details['df1_only_columns']:
                report += f"- **Python-only Columns**: {details['df1_only_columns']}\n"
            if details['df2_only_columns']:
                report += f"- **Stata-only Columns**: {details['df2_only_columns']}\n"

            # Identifier analysis
            if 'identifier_analysis' in comp:
                id_analysis = comp['identifier_analysis']
                if not id_analysis['compatible'] or id_analysis['issues']:
                    report += f"- **Identifier Compatibility Issues**:\n"
                    for issue in id_analysis['issues']:
                        report += f"  - {issue}\n"
                
                # Stock identifier details
                if id_analysis['stock_analysis']:
                    stock = id_analysis['stock_analysis']
                    report += f"- **Stock Identifier Analysis ({stock['column']})**:\n"
                    report += f"  - Python type: {stock['python_type']}, samples: {stock['python_samples']}\n"
                    report += f"  - Stata type: {stock['stata_type']}, samples: {stock['stata_samples']}\n"
                    report += f"  - Direct overlap: {stock['direct_overlap']}/{min(stock['python_unique_count'], stock['stata_unique_count'])} identifiers\n"
                    if stock['numeric_overlap'] > 0:
                        report += f"  - Numeric conversion overlap: {stock['numeric_overlap']} identifiers\n"
                
                # Time identifier details
                if id_analysis['time_analysis']:
                    time = id_analysis['time_analysis']
                    report += f"- **Time Identifier Analysis ({time['column']})**:\n"
                    report += f"  - Python type: {time['python_type']}, samples: {time['python_samples']}\n"
                    report += f"  - Stata type: {time['stata_type']}, samples: {time['stata_samples']}\n"

            # Data differences
            if 'data_differences' in details and details['data_differences']:
                report += f"- **Data Differences**:\n"
                for col, diff in details['data_differences'].items():
                    if 'error' in diff:
                        report += f"  - {col}: Error - {diff['error']}\n"
                    else:
                        report += f"  - {col}: {diff['match_rate']:.4f} match rate ({diff['mismatched_rows']}/{diff['total_rows']} mismatched)\n"
                        
                
                # Add comparison tables if available
                if 'comparison_table_data' in details and details['comparison_table_data']:
                    report += f"\n- **Mismatched data sample**:\n"
                    report += generate_comparison_table_text(details['comparison_table_data'])
                    
                    report += f"- **Mismatched row differences**:\n"
                    report += generate_difference_table_text(details['comparison_table_data'])

        report += "\n"

    return report


def save_reports(results: List[Dict[str, Any]], output_dir: str = ".") -> None:
    """Save both summary and detailed reports to files."""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # Generate reports
    summary_report = generate_summary_report(results)
    detailed_report = generate_detailed_report(results)

    # Save summary report
    summary_file = output_path / "validation_summary.md"
    with open(summary_file, 'w') as f:
        f.write(summary_report)
    logger.info(f"Summary report saved to: {summary_file}")

    # Save detailed report
    detailed_file = output_path / "validation_detailed.md"
    with open(detailed_file, 'w') as f:
        f.write(detailed_report)
    logger.info(f"Detailed report saved to: {detailed_file}")

    # Save raw results as JSON for further analysis
    results_file = output_path / "validation_results.json"
    import json
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    logger.info(f"Raw results saved to: {results_file}")


def print_summary_stats(results: List[Dict[str, Any]]) -> None:
    """Print summary statistics to console."""
    total_datasets = len(results)
    perfect_matches = sum(1 for r in results 
                         if r.get('comparison') and r['comparison'].get('match_status') == 'perfect_match')
    minor_differences = sum(1 for r in results 
                           if r.get('comparison') and r['comparison'].get('match_status') == 'minor_differences')
    major_differences = sum(1 for r in results 
                           if r.get('comparison') and r['comparison'].get('match_status') == 'major_differences')
    
    # Categorize errors
    missing_datasets = [r for r in results if r['status'] == 'error' and 
                       any('not found' in str(err) for err in r.get('errors', []))]
    processing_errors = [r for r in results if r['status'] == 'error' and 
                        not any('not found' in str(err) for err in r.get('errors', []))]

    print(f"\n{'='*60}")
    print(f"VALIDATION SUMMARY")
    print(f"{'='*60}")
    print(f"Total Datasets:     {total_datasets}")
    print(f"Perfect Matches:    {perfect_matches:3d} ({perfect_matches/total_datasets*100:5.1f}%)")
    print(f"Minor Differences:  {minor_differences:3d} ({minor_differences/total_datasets*100:5.1f}%)")
    print(f"Major Differences:  {major_differences:3d} ({major_differences/total_datasets*100:5.1f}%)")
    if missing_datasets:
        print(f"⚠️  MISSING FILES:   {len(missing_datasets):3d} ({len(missing_datasets)/total_datasets*100:5.1f}%) ⚠️")
    print(f"Processing Errors:  {len(processing_errors):3d} ({len(processing_errors)/total_datasets*100:5.1f}%)")
    print(f"{'='*60}")
    
    # Show missing datasets prominently
    if missing_datasets:
        print(f"\n⚠️  CRITICAL: {len(missing_datasets)} MISSING DATASETS:")
        for result in missing_datasets:
            print(f"  - {result['dataset']}")
        print()


def main():
    """Main execution function with command-line interface."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Validate Python vs Stata datasets by comparing on matching identifiers"
    )
    parser.add_argument(
        '--datasets', '-d', 
        nargs='*',
        help='Specific datasets to validate (default: all datasets)'
    )
    parser.add_argument(
        '--list', '-l', 
        action='store_true',
        help='List all available datasets and exit'
    )
    parser.add_argument(
        '--tolerance', '-t',
        type=float,
        default=1e-6,
        help='Tolerance for numeric comparisons (default: 1e-6)'
    )
    parser.add_argument(
        '--output-dir', '-o',
        default='../Logs',
        help='Output directory for reports (default: ../Logs)'
    )
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress console output except errors'
    )
    parser.add_argument(
        '--no-reports',
        action='store_true',
        help='Skip generating report files'
    )
    parser.add_argument(
        '--maxrows',
        type=int,
        default=1000,
        help='Maximum number of rows to load from each dataset (default: unlimited)'
    )

    args = parser.parse_args()

    # Configure logging based on quiet flag
    if args.quiet:
        logging.getLogger().setLevel(logging.ERROR)

    # List datasets if requested
    if args.list:
        print("Available datasets for validation:")
        print("=" * 50)
        for i, dataset in enumerate(sorted(DATASET_IDENTIFIERS.keys()), 1):
            config = DATASET_IDENTIFIERS[dataset]
            stock_col = config['stock'] or 'None'
            time_col = config['time'] or 'None'
            if isinstance(time_col, list):
                time_col = '+'.join(time_col)
            print(f"{i:2d}. {dataset:<30} (stock: {stock_col:<15} time: {time_col})")
        print(f"\nTotal: {len(DATASET_IDENTIFIERS)} datasets")
        return

    # Determine which datasets to validate
    if args.datasets:
        # Validate that requested datasets exist
        invalid_datasets = [d for d in args.datasets if d not in DATASET_IDENTIFIERS]
        if invalid_datasets:
            print(f"Error: Invalid datasets specified: {invalid_datasets}")
            print("Use --list to see available datasets")
            return
        datasets_to_validate = args.datasets
    else:
        datasets_to_validate = list(DATASET_IDENTIFIERS.keys())

    print(f"Starting validation of {len(datasets_to_validate)} datasets...")
    print(f"Tolerance: {args.tolerance}")
    if args.maxrows:
        print(f"Max rows per dataset: {args.maxrows:,}")
    if not args.quiet:
        print(f"Output directory: {args.output_dir}")

    # Run validation
    try:
        results = validate_all_datasets(datasets_to_validate, args.tolerance, args.maxrows)

        # Print summary statistics
        if not args.quiet:
            print_summary_stats(results)

        # Generate and save reports
        if not args.no_reports:
            save_reports(results, args.output_dir)
            if not args.quiet:
                print(f"Reports saved to {args.output_dir}")

        # Return appropriate exit code
        # Only exit with non-zero code for actual processing errors, not data differences
        errors = sum(1 for r in results if r['status'] == 'error')
        major_differences = sum(1 for r in results 
                               if r.get('comparison') and r['comparison'].get('match_status') == 'major_differences')
        perfect_matches = sum(1 for r in results 
                             if r.get('comparison') and r['comparison'].get('match_status') == 'perfect_match')

        if errors > 0:
            print(f"Validation completed with {errors} processing errors")
            sys.exit(2)  # Only exit with error code for actual processing errors
        else:
            # Successful validation completion - report results but exit with success code
            if not args.quiet:
                if perfect_matches == len(results):
                    print("Validation completed successfully - all datasets have perfect matches!")
                elif major_differences > 0:
                    print(f"Validation completed successfully - found {major_differences} datasets with data differences (see reports for details)")
                else:
                    print("Validation completed successfully!")
            sys.exit(0)  # Always exit successfully if no processing errors occurred

    except Exception as e:
        logger.error(f"Fatal error during validation: {e}")
        sys.exit(3)


if __name__ == "__main__":
    main()