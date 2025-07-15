"""
ABOUTME: Comprehensive dataset validation script comparing Python vs Stata datasets
ABOUTME: Checks column names, types, row counts, and performs by-keys deviation analysis

This script provides comprehensive validation that checks:
1. Column names match exactly
2. Column types match exactly  
3. Row count (Python can have slightly more rows, see MAX_ROW_COUNT_RATIO)
4. By-keys analysis: Imperfect rows / Total rows ratio
5. By-keys analysis: Imperfect cells / Total cells ratio
6. Value deviation statistics for worst columns
7. Sample CSV files for datasets with >0.1% imperfect ratio

Cell Matching Logic:
- Perfect cell: |stata_value - python_value| ≤ tolerance (default: 1e-12)
- Imperfect cell: |stata_value - python_value| > tolerance
- String cells: Exact match required (tolerance not applicable)

Arguments:
  --datasets, -d    Specific datasets to validate (default: all datasets)
  --list, -l        List all available datasets and exit
  --maxrows         Maximum rows to load per dataset (default: 1000)
  --tolerance       Tolerance for numeric comparisons (default: 1e-12)

Output: 
  Prints results to console with ✓/✗ symbols
  Also saves results to ../Logs/testout_dl.md in markdown format
  Creates CSV samples in ../Logs/detail/ for problematic datasets
  Creates missing rows analysis in ../Logs/detail/ for datasets with low common rows

Usage examples:
  python3 utils/test_dl.py                                   # Validate all datasets
  python3 utils/test_dl.py --list                            # Show available datasets
  python3 utils/test_dl.py -d m_QCompustat                   # Validate one dataset
  python3 utils/test_dl.py --maxrows 1000000                 # Limit to 1M rows
  python3 utils/test_dl.py -d CompustatAnnual --maxrows 5000 # Validate with row limit
"""

import pandas as pd
import yaml
import io
import sys
import gc
from datetime import datetime
from pathlib import Path
import time
import numpy as np

# ================================
# VALIDATION CONFIGURATION
# ================================

# Row count validation
MAX_ROW_COUNT_RATIO = 1.05  # Python can have up to 5% more rows than Stata

# By-keys validation  
DEFAULT_IMPERFECT_RATIO_THRESHOLD = 0.001  # 0.1% threshold for imperfect rows/cells
DEFAULT_TOLERANCE = 1e-12  # Numeric comparison tolerance

# Memory management
ROW_CAP_FOR_RAM = 10_000_000  # Maximum rows to load for RAM management

# Reporting
CSV_SAMPLE_THRESHOLD = 0.001  # Generate CSV samples when imperfect ratio > 0.1%
MAX_SAMPLE_ROWS = 1000  # Maximum rows in missing rows reports
MAX_WORST_COLUMNS = 4  # Number of worst columns to show in reports
MAX_WORST_ROWS_FOR_SAMPLE = 20  # Maximum rows in CSV samples


def compare_columns_directly(dta_bykey, parq_bykey, tolerance=1e-12):
    """Compare columns directly without heavy hashing - simpler approach like validate_by_keys."""
    common_cols = list(set(dta_bykey.columns) & set(parq_bykey.columns))
    
    column_differences = {}
    for col in common_cols:
        try:
            s1 = dta_bykey[col]
            s2 = parq_bykey[col]
            
            # Handle different data types like validate_by_keys
            if s1.dtype == 'object' and s2.dtype == 'object':
                # String comparison
                s1 = s1.astype(str).fillna('')
                s2 = s2.astype(str).fillna('')
                matches = (s1 == s2)
                # For string columns, set deviation metrics to N/A
                mean_dev_imperfect = "N/A"
                mean_col_level = "N/A"
            elif pd.api.types.is_numeric_dtype(s1) and pd.api.types.is_numeric_dtype(s2):
                # Numeric comparison with tolerance
                matches = np.isclose(s1, s2, rtol=tolerance, atol=tolerance, equal_nan=True)
                # Calculate deviation metrics for numeric columns
                abs_diff = np.abs(s1 - s2)
                imperfect_mask = ~matches
                if imperfect_mask.sum() > 0:
                    mean_dev_imperfect = abs_diff[imperfect_mask].mean()
                else:
                    mean_dev_imperfect = 0.0
                # Calculate mean column level (average of both columns)
                col_avg = (s1 + s2) / 2
                mean_col_level = col_avg.mean()
            else:
                # Mixed types - convert to string
                s1 = s1.astype(str).fillna('')
                s2 = s2.astype(str).fillna('')
                matches = (s1 == s2)
                # For mixed types, set deviation metrics to N/A
                mean_dev_imperfect = "N/A"
                mean_col_level = "N/A"
            
            # Calculate percentage of rows that deviate
            pct_pos = ((~matches).sum() / len(matches) * 100) if len(matches) > 0 else 0
            
            if pct_pos > 0:
                column_differences[col] = {
                    'pct_pos_bykey': pct_pos,
                    'deviating_rows': (~matches).sum(),
                    'mean_dev_imperfect': mean_dev_imperfect,
                    'mean_col_level': mean_col_level
                }
        except Exception as e:
            column_differences[col] = {'error': str(e)}
    
    return column_differences


def generate_missing_rows_report(dataset_name: str, dta, parq, key_cols: list):
    """Generate detailed markdown report for datasets with missing common rows.
    
    Args:
        dataset_name: Name of the dataset
        dta: Stata dataframe (already indexed by key_cols)
        parq: Python dataframe (already indexed by key_cols)  
        key_cols: List of key column names
    """
    try:
        # Create detail directory
        detail_dir = Path("../Logs/detail")
        detail_dir.mkdir(parents=True, exist_ok=True)
        
        # Find rows in Stata that are not in Python
        stata_only_indices = dta.index.difference(parq.index)
        stata_only_df = dta.loc[stata_only_indices].reset_index() if len(stata_only_indices) > 0 else pd.DataFrame(columns=list(dta.columns) + key_cols)
        
        # Find rows in Python that are not in Stata  
        python_only_indices = parq.index.difference(dta.index)
        python_only_df = parq.loc[python_only_indices].reset_index() if len(python_only_indices) > 0 else pd.DataFrame(columns=list(parq.columns) + key_cols)
        
        # Sort the DataFrames by key columns (if they have any rows)
        if len(stata_only_df) > 0:
            stata_only_df = stata_only_df.sort_values(by=key_cols)
        if len(python_only_df) > 0:
            python_only_df = python_only_df.sort_values(by=key_cols)
        
        # Limit to first MAX_ROWS rows
        MAX_ROWS = MAX_SAMPLE_ROWS
        stata_cutoff = len(stata_only_df) > MAX_ROWS
        python_cutoff = len(python_only_df) > MAX_ROWS
        
        stata_only_display = stata_only_df.head(MAX_ROWS)
        python_only_display = python_only_df.head(MAX_ROWS)
        
        # Generate markdown content
        lines = []
        lines.append(f"# Missing Rows Analysis: {dataset_name}")
        lines.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        lines.append("## Summary")
        lines.append(f"- **Total Stata rows**: {len(dta):,}")
        lines.append(f"- **Total Python rows**: {len(parq):,}")
        lines.append(f"- **Rows in Stata but not Python**: {len(stata_only_df):,}")
        lines.append(f"- **Rows in Python but not Stata**: {len(python_only_df):,}")
        lines.append(f"- **Key columns**: {', '.join(key_cols)}")
        lines.append("")
        
        # Table 1: Rows in Stata that are not in Python
        lines.append("## Rows in Stata data that are not in Python")
        lines.append("")
        if len(stata_only_df) == 0:
            lines.append("*(No missing rows)*")
        else:
            if stata_cutoff:
                lines.append(f"*Showing first {MAX_ROWS:,} of {len(stata_only_df):,} rows*")
                lines.append("")
            
            # Convert DataFrame to markdown table
            lines.append(stata_only_display.to_markdown(index=False))
        
        lines.append("")
        lines.append("---")
        lines.append("")
        
        # Table 2: Rows in Python that are not in Stata
        lines.append("## Rows in Python data that are not in Stata")
        lines.append("")
        if len(python_only_df) == 0:
            lines.append("*(No missing rows)*")
        else:
            if python_cutoff:
                lines.append(f"*Showing first {MAX_ROWS:,} of {len(python_only_df):,} rows*")
                lines.append("")
            
            # Convert DataFrame to markdown table
            lines.append(python_only_display.to_markdown(index=False))
        
        # Save to file
        report_file = detail_dir / f"{dataset_name}_missing_rows.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        return f"../Logs/detail/{dataset_name}_missing_rows.md"
    
    except Exception as e:
        print(f"Warning: Failed to generate missing rows report for {dataset_name}: {e}")
        return None

def dataset_name_to_anchor(name: str) -> str:
    """Convert dataset name to markdown anchor format.
    
    Args:
        name: Dataset name (e.g., 'CCMLinkingTable.csv', 'm_QCompustat')
        
    Returns:
        str: Anchor format (e.g., 'ccmlinkingtablecsv', 'mqcompustat')
    """
    return name.lower().replace('.', '').replace('_', '').replace(' ', '').replace('-', '')

def wrap_dataset_name_with_link(text: str) -> str:
    """Wrap dataset name in text with markdown link.
    
    Args:
        text: Text containing dataset name, may have additional info
              Examples: 'monthlyShortInterest', 'CCMLinkingTable.csv: 0.15%', 
                       'CCMLinkingTable.csv: (lpermco)', 'CRSPdistributions (no common rows)'
    
    Returns:
        str: Text with dataset name wrapped in markdown link
    """
    # Handle different patterns
    if ': (' in text:  # Pattern like "CCMLinkingTable.csv: (lpermco)"
        dataset_name, rest = text.split(': (', 1)
        anchor = dataset_name_to_anchor(dataset_name)
        return f"[{dataset_name}](#{anchor}): ({rest}"
    elif ': ' in text:  # Pattern like "CCMLinkingTable.csv: 0.15%"
        dataset_name, rest = text.split(': ', 1)
        anchor = dataset_name_to_anchor(dataset_name)
        return f"[{dataset_name}](#{anchor}): {rest}"
    elif ' (' in text:  # Pattern like "CRSPdistributions (no common rows)"
        dataset_name, rest = text.split(' (', 1)
        anchor = dataset_name_to_anchor(dataset_name)
        return f"[{dataset_name}](#{anchor}) ({rest}"
    else:  # Simple dataset name
        anchor = dataset_name_to_anchor(text)
        return f"[{text}](#{anchor})"

def load_dataset_pair(dataset_name: str, max_rows: int = -1):
    """Load both Stata and Python datasets for a given dataset name.
    
    Returns:
        tuple: (dta, parq, key_cols, config) or (None, None, None, None) if error
    """
    # Load dataset configuration
    with open('DataDownloads/00_map.yaml', 'r', encoding='utf-8') as f:
        dataset_map = yaml.safe_load(f)
    
    if dataset_name not in dataset_map:
        return None, None, None, None
    
    config = dataset_map[dataset_name]
    stata_file = f"../Data/Intermediate/{config['stata_file']}"
    python_file = f"../pyData/Intermediate/{config['python_file']}"
    
    # Get key columns
    key_cols = []
    key_num = 1
    while f'key{key_num}' in config and config.get(f'key{key_num}'):
        key_cols.append(config[f'key{key_num}'])
        key_num += 1
    
    try:
        # Load Stata dataset
        if stata_file.endswith('.dta'):
            if max_rows > 0:
                dta = pd.read_stata(stata_file, chunksize=max_rows)
                dta = next(dta)
            else:
                dta = pd.read_stata(stata_file)
            # Apply row cap for RAM management
            if len(dta) > ROW_CAP_FOR_RAM:
                if key_cols:
                    dta = dta.sort_values(by=key_cols)
                dta = dta.head(ROW_CAP_FOR_RAM)
        elif stata_file.endswith('.csv'):
            nrows = None if max_rows <= 0 else max_rows
            dta = pd.read_csv(stata_file, nrows=nrows)
            # Apply row cap for RAM management
            if len(dta) > ROW_CAP_FOR_RAM:
                if key_cols:
                    dta = dta.sort_values(by=key_cols)
                dta = dta.head(ROW_CAP_FOR_RAM)
        else:
            return None, None, None, None
            
        # Load Python dataset
        if python_file.endswith('.parquet'):
            parq = pd.read_parquet(python_file)
            if max_rows > 0:
                parq = parq.head(max_rows)
            # Apply row cap for RAM management
            if len(parq) > ROW_CAP_FOR_RAM:
                if key_cols:
                    parq = parq.sort_values(by=key_cols)
                parq = parq.head(ROW_CAP_FOR_RAM)
        elif python_file.endswith('.csv'):
            nrows = None if max_rows <= 0 else max_rows
            parq = pd.read_csv(python_file, nrows=nrows)
            # Apply row cap for RAM management
            if len(parq) > ROW_CAP_FOR_RAM:
                if key_cols:
                    parq = parq.sort_values(by=key_cols)
                parq = parq.head(ROW_CAP_FOR_RAM)
        else:
            return None, None, None, None
        
        return dta, parq, key_cols, config
        
    except Exception:
        return None, None, None, None

def val_one_basics(dataset_name: str, dta=None, parq=None) -> dict:
    """Validate basic properties of a single dataset.
    
    Returns:
        dict: Structured validation results containing status, validations, details, and error info
    """
    
    # Check if data was loaded successfully
    if dta is None or parq is None:
        return {
            'dataset_name': dataset_name,
            'status': 'error',
            'validations': [
                "**ERROR**: Failed to load datasets",
                "**ERROR**: Column names comparison failed", 
                "**ERROR**: Column types comparison failed",
                "**ERROR**: Row count comparison failed"
            ],
            'details': [f"**Error**: Could not load data for {dataset_name}"],
            'error': f"Could not load data for {dataset_name}"
        }
    
    try:
        # Track validation results for numbered format
        validation_results = []
        details = []
        
        # 1. Check column names
        if list(dta.columns) == list(parq.columns):
            validation_results.append("✓ Column names match")
        else:
            validation_results.append("✗ Column names differ")
            dta_only = set(dta.columns) - set(parq.columns)
            parq_only = set(parq.columns) - set(dta.columns)
            if dta_only:
                details.append(f"  - Stata only: {list(dta_only)}")
            if parq_only:
                details.append(f"  - Python only: {list(parq_only)}")
        
        # 2. Check column types
        common_cols = list(set(dta.columns) & set(parq.columns))
        type_match = True
        type_mismatches = []
        for col in common_cols:
            if dta[col].dtype != parq[col].dtype:
                type_match = False
                type_mismatches.append(f"  - {col}: Stata={dta[col].dtype} vs Python={parq[col].dtype}")
        
        if type_match:
            validation_results.append("✓ Column types match")
        else:
            validation_results.append("✗ Column types differ")
            details.extend(type_mismatches)
        
        # 3. Check row count
        stata_rows = len(dta)
        python_rows = len(parq)
        row_ratio = python_rows / stata_rows if stata_rows > 0 else float('inf')
        
        if python_rows == stata_rows:
            validation_results.append("✓ Row counts match exactly")
        elif row_ratio <= MAX_ROW_COUNT_RATIO:  # Python can have up to 0.1% more
            validation_results.append("✓ Row counts acceptable (Python ≤ 0.1% more)")
        else:
            validation_results.append(f"✗ Row count difference too large (ratio: {row_ratio:.3f})")
        
        # Store row info for details section
        row_details = f"**Rows**: Stata={stata_rows:,}, Python={python_rows:,}"
        
        return {
            'dataset_name': dataset_name,
            'status': 'success',
            'validations': validation_results,
            'details': [row_details] + details,
            'error': None
        }
        
    except Exception as e:
        return {
            'dataset_name': dataset_name,
            'status': 'error',
            'validations': [
                "**ERROR**: Column names comparison failed",
                "**ERROR**: Column types comparison failed", 
                "**ERROR**: Row count comparison failed"
            ],
            'details': [f"**Error**: {e}"],
            'error': str(e)
        }


def val_one_crow(dataset_name: str, basic_results: dict, dta=None, parq=None, key_cols=None, tolerance: float = DEFAULT_TOLERANCE, imperfect_ratio_threshold: float = DEFAULT_IMPERFECT_RATIO_THRESHOLD) -> dict:
    """Validate dataset by keys and compute imperfect rows ratio.
    
    Args:
        dataset_name: Name of the dataset
        basic_results: Results from val_one_basics()
        dta: Stata dataframe
        parq: Python dataframe
        key_cols: List of key columns for comparison
        tolerance: Tolerance for numeric comparisons
        imperfect_ratio_threshold: Maximum ratio for imperfect rows/cells (default: DEFAULT_IMPERFECT_RATIO_THRESHOLD)
        
    Returns:
        dict: Combined validation results with basic + by-keys analysis
    """
    
    # Check if data was loaded successfully
    if dta is None or parq is None:
        return {
            'dataset_name': dataset_name,
            'status': 'error',
            'validations': basic_results['validations'] + ["**ERROR**: Failed to load datasets"],
            'details': basic_results['details'] + [f"**Error**: Could not load data for {dataset_name}"],
            'analysis': None,
            'worst_columns': [],
            'sample_file': None,
            'missing_rows_file': None,
            'error': f"Could not load data for {dataset_name}"
        }
    
    # Default to empty key columns if none provided
    if key_cols is None:
        key_cols = []
    
    if not key_cols:
        return {
            'dataset_name': dataset_name,
            'status': 'warning',
            'validations': basic_results['validations'] + ["⚠ No key columns found - skipping by-keys analysis"],
            'details': basic_results['details'],
            'analysis': None,
            'worst_columns': [],
            'sample_file': None,
            'missing_rows_file': None,
            'error': None
        }
    
    try:
        
        # Index by key columns and find common keys
        dta = dta.reset_index(drop=True)
        parq = parq.reset_index(drop=True)
        
        # Check if key columns exist in both datasets 
        missing_keys_dta = [k for k in key_cols if k not in dta.columns]
        missing_keys_parq = [k for k in key_cols if k not in parq.columns]
        
        if missing_keys_dta or missing_keys_parq:
            return {
                'dataset_name': dataset_name,
                'status': 'warning',
                'validations': basic_results['validations'] + [f"⚠ Missing key columns - Stata: {missing_keys_dta}, Python: {missing_keys_parq}"],
                'details': basic_results['details'],
                'analysis': None,
                'worst_columns': [],
                'sample_file': None,
                'missing_rows_file': None,
                'error': None
            }
        
        # Normalize key column types before indexing
        for col in key_cols:
            if col in dta.columns and col in parq.columns:
                # Convert datetime columns to strings for consistent comparison
                if pd.api.types.is_datetime64_any_dtype(dta[col]) or pd.api.types.is_datetime64_any_dtype(parq[col]):
                    dta[col] = pd.to_datetime(dta[col]).dt.strftime('%Y-%m-%d')
                    parq[col] = pd.to_datetime(parq[col]).dt.strftime('%Y-%m-%d')
        
        dta = dta.set_index(key_cols)
        parq = parq.set_index(key_cols)
        
        # Find common keys
        mask1 = dta.index.isin(parq.index)
        mask2 = parq.index.isin(dta.index)
        
        # Filter to common keys and sort
        dta_bykey = dta[mask1].sort_index()
        parq_bykey = parq[mask2].sort_index()
        
        if len(dta_bykey) == 0:
            return {
                'dataset_name': dataset_name,
                'status': 'warning',
                'validations': basic_results['validations'] + ["⚠ No common rows found"],
                'details': basic_results['details'],
                'analysis': None,
                'worst_columns': [],
                'sample_file': None,
                'missing_rows_file': None,
                'error': None
            }
        
        # Compare columns directly without heavy hashing
        column_differences = compare_columns_directly(dta_bykey, parq_bykey, tolerance=tolerance)
        
        # Count imperfect cells (individual cells that have deviations)
        common_cols = list(set(dta_bykey.columns) & set(parq_bykey.columns))
        imperfect_cells = 0
        for col, diff_info in column_differences.items():
            if 'error' not in diff_info:
                imperfect_cells += diff_info.get('deviating_rows', 0)
        
        total_cells = len(dta_bykey) * len(common_cols) if common_cols else 0
        imperfect_cells_ratio = imperfect_cells / total_cells if total_cells > 0 else 0
        
        # Count imperfect rows (rows with any differences in any column)
        imperfect_row_indices = set()
        for col, diff_info in column_differences.items():
            if 'error' not in diff_info and diff_info.get('deviating_rows', 0) > 0:
                # Find rows that differ for this column
                s1 = dta_bykey[col]
                s2 = parq_bykey[col]
                
                if s1.dtype == 'object' and s2.dtype == 'object':
                    s1 = s1.astype(str).fillna('')
                    s2 = s2.astype(str).fillna('')
                    mismatched_indices = s1.index[s1 != s2]
                elif pd.api.types.is_numeric_dtype(s1) and pd.api.types.is_numeric_dtype(s2):
                    mismatched_indices = s1.index[~np.isclose(s1, s2, rtol=tolerance, atol=tolerance, equal_nan=True)]
                else:
                    s1 = s1.astype(str).fillna('')
                    s2 = s2.astype(str).fillna('')
                    mismatched_indices = s1.index[s1 != s2]
                
                imperfect_row_indices.update(mismatched_indices)
        
        dev_rows = pd.Series([idx in imperfect_row_indices for idx in dta_bykey.index])
        
        # Report matching hierarchy
        full_data_rows = len(dta)
        matched_by_key_rows = len(dta_bykey)
        perfect_rows = matched_by_key_rows - dev_rows.sum()
        imperfect_rows = dev_rows.sum()
        imperfect_ratio = imperfect_rows / full_data_rows if full_data_rows > 0 else 0
        
        # Add Python common rows superset validation 
        all_stata_in_python = mask1.all()
        missing_stata_rows = (~mask1).sum()
        missing_rows_file = None
        if all_stata_in_python:
            common_rows_result = "✓ Python common rows are superset of Stata"
        else:
            common_rows_result = f"✗ Python missing some Stata rows ({missing_stata_rows})"
            # Generate missing rows report for datasets that fail superset check
            missing_rows_file = generate_missing_rows_report(dataset_name, dta, parq, key_cols)
        
        # Add imperfect rows ratio to validation results
        imperfect_pct = imperfect_ratio_threshold * 100
        if imperfect_ratio <= imperfect_ratio_threshold:
            bykeys_result = f"✓ Imperfect rows acceptable (≤ {imperfect_pct:.1f}%)"
        else:
            bykeys_result = f"✗ Imperfect rows high (> {imperfect_pct:.1f}%)"
        
        # Add imperfect cells ratio to validation results
        if imperfect_cells_ratio <= imperfect_ratio_threshold:
            cells_result = f"✓ Imperfect cells acceptable (≤ {imperfect_pct:.1f}%)"
        else:
            cells_result = f"✗ Imperfect cells high (> {imperfect_pct:.1f}%)"
        
        # Prepare analysis data
        analysis = {
            'full_data_rows': full_data_rows,
            'matched_by_key_rows': matched_by_key_rows,
            'perfect_rows': perfect_rows,
            'imperfect_rows': imperfect_rows,
            'imperfect_ratio': imperfect_ratio,
            'imperfect_cells': imperfect_cells,
            'total_cells': total_cells,
            'imperfect_cells_ratio': imperfect_cells_ratio,
            'missing_stata_rows': missing_stata_rows
        }
        
        # Prepare worst columns if there are deviations
        worst_columns = []
        sample_file = None
        
        if imperfect_rows > 0 and column_differences:
            # Sort columns by deviation percentage
            sorted_cols = sorted(column_differences.items(), 
                               key=lambda x: x[1].get('pct_pos_bykey', 0), 
                               reverse=True)
            
            # Show top 4 worst columns
            worst_4 = sorted_cols[:MAX_WORST_COLUMNS]
            for col, diff_info in worst_4:
                if 'error' in diff_info:
                    worst_columns.append(f"{col}: Error - {diff_info['error']}")
                else:
                    pct_dev = diff_info.get('pct_pos_bykey', 0)
                    mean_dev = diff_info.get('mean_dev_imperfect', 'N/A')
                    mean_col = diff_info.get('mean_col_level', 'N/A')
                    
                    # Format mean_dev and mean_col with scientific notation if numeric
                    if isinstance(mean_dev, (int, float)) and not isinstance(mean_dev, str):
                        mean_dev_str = f"{mean_dev:.1e}"
                    else:
                        mean_dev_str = str(mean_dev)
                    
                    if isinstance(mean_col, (int, float)) and not isinstance(mean_col, str):
                        mean_col_str = f"{mean_col:.1e}"
                    else:
                        mean_col_str = str(mean_col)
                    
                    worst_columns.append(f"{col}: imperfect rows {pct_dev:.3f}%; mean dev for imperfect {mean_dev_str}; mean col level {mean_col_str}")
            
            # Save CSV sample if imperfect ratio > 0.1%
            if imperfect_ratio > CSV_SAMPLE_THRESHOLD:
                # Create detail directory
                detail_dir = Path("../Logs/detail")
                detail_dir.mkdir(parents=True, exist_ok=True)
                
                # Get worst columns and rows for sample
                col_worst = [col for col, _ in sorted_cols[:20]]
                row_worst_idx = list(imperfect_row_indices)[:MAX_WORST_ROWS_FOR_SAMPLE]  # Take first N imperfect rows
                
                if col_worst and row_worst_idx:
                    # Create sample with both Stata and Python values
                    dta_sample = dta_bykey.loc[row_worst_idx, col_worst].assign(dsource='Stata').reset_index()
                    parq_sample = parq_bykey.loc[row_worst_idx, col_worst].assign(dsource='Python').reset_index()
                    
                    # Combine and save
                    sample_combined = pd.concat([dta_sample, parq_sample], axis=0).sort_values(key_cols + ['dsource'])
                    
                    csv_file = detail_dir / f"{dataset_name}_sample.csv"
                    sample_combined.to_csv(csv_file, index=False)
                    sample_file = f"../Logs/detail/{dataset_name}_sample.csv"
        
        return {
            'dataset_name': dataset_name,
            'status': 'success',
            'validations': basic_results['validations'] + [common_rows_result, bykeys_result, cells_result],
            'details': basic_results['details'],
            'analysis': analysis,
            'worst_columns': worst_columns,
            'sample_file': sample_file,
            'missing_rows_file': missing_rows_file,
            'error': None
        }
        
    except Exception as e:
        return {
            'dataset_name': dataset_name,
            'status': 'error',
            'validations': basic_results['validations'] + ["**ERROR**: By-keys analysis failed"],
            'details': basic_results['details'] + [f"**Error in by-keys analysis**: {e}"],
            'analysis': None,
            'worst_columns': [],
            'sample_file': None,
            'missing_rows_file': None,
            'error': str(e)
        }


def get_failure_priority(result: dict) -> int:
    """Determine failure priority for sorting datasets by severity.
    
    Args:
        result: Validation result dictionary
        
    Returns:
        int: Priority level (lower number = higher priority/more severe)
             0 = Execution errors (load failures, no common rows)
             1 = High imperfect rows/cells (> 0.1%)
             2 = Column type/name differences
             3 = All checks passing
    """
    validations = result['validations']
    
    # Check for execution errors (highest priority)
    for validation in validations:
        if ("No common rows" in validation or 
            "Failed to load" in validation or 
            "ERROR" in validation):
            return 0
    
    # Check for high imperfect ratios (high priority)
    for validation in validations:
        if ("Imperfect rows high" in validation and "✗" in validation) or \
           ("Imperfect cells high" in validation and "✗" in validation):
            return 1
    
    # Check for column differences (medium priority)
    for validation in validations:
        if ("Column names differ" in validation and "✗" in validation) or \
           ("Column types differ" in validation and "✗" in validation) or \
           ("Row count" in validation and "✗" in validation):
            return 2
    
    # All checks passing (lowest priority)
    return 3


def sort_results_by_failure_priority(results_list: list) -> list:
    """Sort validation results by failure priority.
    
    Args:
        results_list: List of validation result dictionaries
        
    Returns:
        list: Sorted results with failed datasets first
    """
    return sorted(results_list, key=lambda x: (get_failure_priority(x), x['dataset_name']))


def generate_summary(results_list: list, imperfect_ratio_threshold: float = DEFAULT_IMPERFECT_RATIO_THRESHOLD) -> str:
    """Generate summary statistics from validation results.
    
    Args:
        results_list: List of validation result dictionaries
        imperfect_ratio_threshold: Maximum ratio for imperfect rows/cells (default: DEFAULT_IMPERFECT_RATIO_THRESHOLD)
        
    Returns:
        str: Formatted markdown summary section
    """
    total_datasets = len(results_list)
    
    # Count passes for each validation check
    col_names_pass = 0
    col_types_pass = 0
    row_counts_pass = 0
    common_rows_pass = 0
    imperfect_ratio_pass = 0
    imperfect_cells_pass = 0
    
    # Collect failures by category
    col_names_fail = []
    col_types_fail = []
    row_counts_fail = []
    common_rows_fail = []
    high_imperfect = []
    high_imperfect_cells = []
    execution_errors = []
    
    for result in results_list:
        dataset_name = result['dataset_name']
        validations = result['validations']
        details = result['details']
        
        # Check each validation result
        for validation in validations:
            if "Column names match" in validation and "✓" in validation:
                col_names_pass += 1
            elif "Column names" in validation and "✗" in validation:
                col_names_fail.append(dataset_name)
                
            if "Column types match" in validation and "✓" in validation:
                col_types_pass += 1
            elif "Column types" in validation and "✗" in validation:
                # Extract column type mismatches from details
                type_mismatches = []
                for detail in details:
                    if "Stata=" in detail and "vs Python=" in detail:
                        # Extract column name from "  - colname: Stata=type vs Python=type"
                        parts = detail.strip().split(":")
                        if len(parts) >= 2:
                            col_name = parts[0].replace("- ", "").strip()
                            type_mismatches.append(col_name)
                
                if type_mismatches:
                    col_types_fail.append(f"{dataset_name}: ({', '.join(type_mismatches)})")
                else:
                    col_types_fail.append(dataset_name)
                
            if ("Row count" in validation and "✓" in validation) or ("Row counts" in validation and "✓" in validation):
                row_counts_pass += 1
            elif ("Row count" in validation and "✗" in validation) or ("Row counts" in validation and "✗" in validation):
                row_counts_fail.append(dataset_name)
                
            if "Python common rows are superset of Stata" in validation and "✓" in validation:
                common_rows_pass += 1
            elif "Python missing some Stata rows" in validation and "✗" in validation:
                # Extract missing row count from validation message
                if result['analysis'] and 'missing_stata_rows' in result['analysis']:
                    missing_count = result['analysis']['missing_stata_rows']
                    common_rows_fail.append(f"{dataset_name} ({missing_count})")
                else:
                    common_rows_fail.append(dataset_name)
                
            if "Imperfect rows acceptable" in validation and "✓" in validation:
                imperfect_ratio_pass += 1
            elif "Imperfect rows high" in validation and "✗" in validation:
                # Get the imperfect ratio from analysis
                if result['analysis'] and 'imperfect_ratio' in result['analysis']:
                    ratio_pct = result['analysis']['imperfect_ratio'] * 100
                    high_imperfect.append(f"{dataset_name}: {ratio_pct:.2f}%")
                else:
                    high_imperfect.append(dataset_name)
                    
            if "Imperfect cells acceptable" in validation and "✓" in validation:
                imperfect_cells_pass += 1
            elif "Imperfect cells high" in validation and "✗" in validation:
                # Get the imperfect cells ratio from analysis
                if result['analysis'] and 'imperfect_cells_ratio' in result['analysis']:
                    cells_ratio_pct = result['analysis']['imperfect_cells_ratio'] * 100
                    high_imperfect_cells.append(f"{dataset_name}: {cells_ratio_pct:.2f}%")
                else:
                    high_imperfect_cells.append(dataset_name)
            
            if ("No common rows" in validation or "Failed to load" in validation or "ERROR" in validation):
                # Check if this dataset already has an execution error recorded
                existing_issue = next((issue for issue in execution_errors if dataset_name in issue), None)
                if not existing_issue:
                    if "No common rows" in validation:
                        execution_errors.append(f"{dataset_name} (no common rows)")
                    elif "Failed to load" in validation or "ERROR" in validation:
                        execution_errors.append(f"{dataset_name} (load error)")
    
    # Format summary
    lines = []
    lines.append("## Summary")
    lines.append("")
    lines.append("**Validation Thresholds**:")
    lines.append(f"- Imperfect ratio threshold: {imperfect_ratio_threshold * 100:.1f}%")
    lines.append("")
    lines.append("**Validation Results**:")
    lines.append(f"- ✓ Column names match: {col_names_pass}/{total_datasets} datasets")
    lines.append(f"- ✓ Column types match: {col_types_pass}/{total_datasets} datasets")
    lines.append(f"- ✓ Row counts acceptable: {row_counts_pass}/{total_datasets} datasets")
    lines.append(f"- ✓ Python common rows are superset: {common_rows_pass}/{total_datasets} datasets")
    lines.append(f"- ✓ Imperfect rows acceptable: {imperfect_ratio_pass}/{total_datasets} datasets")
    lines.append(f"- ✓ Imperfect cells acceptable: {imperfect_cells_pass}/{total_datasets} datasets")
    lines.append("")
    lines.append("**Failed Checks**:")
    
    # Column names differ
    if col_names_fail:
        lines.append("- **Column names differ**:")
        for dataset in col_names_fail:
            linked_dataset = wrap_dataset_name_with_link(dataset)
            lines.append(f"  - {linked_dataset}")
    else:
        lines.append("- **Column names differ**: (none)")
        
    # Column types differ
    if col_types_fail:
        lines.append("- **Column types differ**:")
        for dataset_info in col_types_fail:
            linked_dataset_info = wrap_dataset_name_with_link(dataset_info)
            lines.append(f"  - {linked_dataset_info}")
    else:
        lines.append("- **Column types differ**: (none)")
        
    # Row count issues
    if row_counts_fail:
        lines.append("- **Row count issues**:")
        for dataset in row_counts_fail:
            linked_dataset = wrap_dataset_name_with_link(dataset)
            lines.append(f"  - {linked_dataset}")
    else:
        lines.append("- **Row count issues**: (none)")
        
    # Python missing Stata rows
    if common_rows_fail:
        lines.append("- **Python missing Stata rows**:")
        for dataset in common_rows_fail:
            linked_dataset = wrap_dataset_name_with_link(dataset)
            lines.append(f"  - {linked_dataset}")
    else:
        lines.append("- **Python missing Stata rows**: (none)")
        
    # High imperfect rows
    if high_imperfect:
        lines.append("- **High imperfect rows**:")
        for dataset_info in high_imperfect:
            linked_dataset_info = wrap_dataset_name_with_link(dataset_info)
            lines.append(f"  - {linked_dataset_info}")
    else:
        lines.append("- **High imperfect rows**: (none)")
        
    # High imperfect cells
    if high_imperfect_cells:
        lines.append("- **High imperfect cells**:")
        for dataset_info in high_imperfect_cells:
            linked_dataset_info = wrap_dataset_name_with_link(dataset_info)
            lines.append(f"  - {linked_dataset_info}")
    else:
        lines.append("- **High imperfect cells**: (none)")
        
    # Execution errors
    if execution_errors:
        lines.append("- **Execution Errors**:")
        for error_info in execution_errors:
            linked_error_info = wrap_dataset_name_with_link(error_info)
            lines.append(f"  - {linked_error_info}")
    else:
        lines.append("- **Execution Errors**: (none)")
    
    lines.append("")
    lines.append("---")
    lines.append("")
    
    return "\n".join(lines)


def reorder_markdown_by_failure_priority(markdown_content: str) -> str:
    """Reorder dataset sections in markdown content by failure priority.
    
    Args:
        markdown_content: Original markdown content with datasets in processing order
        
    Returns:
        str: Markdown content with dataset sections reordered (failed datasets first)
    """
    lines = markdown_content.split('\n')
    
    # Find where dataset sections start (after the summary and separator)
    dataset_start_idx = None
    for i, line in enumerate(lines):
        if line.strip() == '---' and i > 10:  # Summary separator
            dataset_start_idx = i + 2  # Skip separator and blank line
            break
    
    if dataset_start_idx is None:
        return markdown_content  # Return original if can't find structure
    
    # Split into header/summary part and dataset sections
    header_lines = lines[:dataset_start_idx]
    dataset_lines = lines[dataset_start_idx:]
    
    # Parse dataset sections
    dataset_sections = []
    current_section = []
    current_dataset_name = None
    
    for line in dataset_lines:
        if line.startswith('## ') and line != '## Summary':
            # New dataset section found
            if current_section and current_dataset_name:
                dataset_sections.append((current_dataset_name, current_section))
            current_dataset_name = line[3:].strip()  # Remove "## "
            current_section = [line]
        else:
            current_section.append(line)
    
    # Add the last section
    if current_section and current_dataset_name:
        dataset_sections.append((current_dataset_name, current_section))
    
    # Create mock results for sorting (extract priority from section content)
    mock_results = []
    for dataset_name, section_lines in dataset_sections:
        # Find validation results in the section
        validations = []
        for line in section_lines:
            if line.strip() and (line.strip()[0].isdigit() or line.strip().startswith('**ERROR**')):
                validations.append(line.strip())
        
        mock_result = {
            'dataset_name': dataset_name,
            'validations': validations
        }
        mock_results.append((mock_result, section_lines))
    
    # Sort using existing failure priority logic
    sorted_sections = sorted(mock_results, key=lambda x: (get_failure_priority(x[0]), x[0]['dataset_name']))
    
    # Reassemble markdown
    result_lines = header_lines[:]
    for _, section_lines in sorted_sections:
        result_lines.extend(section_lines)
    
    return '\n'.join(result_lines)


def format_results_to_markdown(results_list: list, max_rows: int, tolerance: float, execution_time: float, imperfect_ratio_threshold: float = DEFAULT_IMPERFECT_RATIO_THRESHOLD) -> str:
    """Format validation results to markdown string.
    
    Args:
        results_list: List of validation result dictionaries  
        max_rows: Maximum rows limit used in validation
        tolerance: Tolerance used for numeric comparisons
        execution_time: Execution time in minutes
        imperfect_ratio_threshold: Maximum ratio for imperfect rows/cells (default: DEFAULT_IMPERFECT_RATIO_THRESHOLD)
        
    Returns:
        str: Formatted markdown content
    """
    lines = []
    
    # Header
    lines.append("# Dataset Validation Report")
    lines.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append(f"**Datasets validated**: {len(results_list)}")
    if max_rows > 0:
        lines.append(f"**Row limit**: {max_rows:,} rows per dataset")
    else:
        lines.append("**Row limit**: unlimited")
    lines.append(f"**Tolerance**: {tolerance}")
    lines.append(f"**Imperfect ratio threshold**: {imperfect_ratio_threshold * 100:.1f}%")
    lines.append(f"**Execution time**: {execution_time:.2f} minutes")
    lines.append("")
    lines.append("**Cell Matching Logic**:")
    lines.append(f"- Perfect cell: |stata_value - python_value| ≤ {tolerance}")
    lines.append(f"- Imperfect cell: |stata_value - python_value| > {tolerance}")
    lines.append("- String cells: Exact match required (tolerance not applicable)")
    lines.append("")
    
    # Add summary section
    summary_text = generate_summary(results_list, imperfect_ratio_threshold)
    lines.append(summary_text)
    
    # Process each dataset result  
    for result in results_list:
        dataset_name = result['dataset_name']
        lines.append(f"## {dataset_name}")
        lines.append("")
        
        # Output numbered validation results
        for i, validation in enumerate(result['validations'], 1):
            lines.append(f"{i}. {validation}")
        
        # Output detailed information
        lines.append("")
        lines.append("**Details**")
        for detail in result['details']:
            lines.append(f"- {detail}")
        
        # Add by-keys analysis if available
        if result['analysis']:
            analysis = result['analysis']
            lines.append("- **By-Keys Analysis**:")
            lines.append(f"    - Total Stata rows: {analysis['full_data_rows']:,}")
            lines.append(f"    - Common rows: {analysis['matched_by_key_rows']:,}")
            lines.append(f"    - Perfect rows: {analysis['perfect_rows']:,}")
            lines.append(f"    - Imperfect rows: {analysis['imperfect_rows']:,}")
            lines.append(f"    - **Imperfect rows / Total rows: {analysis['imperfect_ratio']:.2%}**")
            if 'imperfect_cells' in analysis:
                lines.append(f"    - Imperfect cells: {analysis['imperfect_cells']:,}")
                lines.append(f"    - Total cells: {analysis['total_cells']:,}")
                lines.append(f"    - **Imperfect cells / Total cells: {analysis['imperfect_cells_ratio']:.2%}**")
        
        # Add worst columns if available
        if result['worst_columns']:
            lines.append("- **4 Worst Columns by Deviation %**:")
            for col_info in result['worst_columns']:
                lines.append(f"    - {col_info}")
        
        # Add sample file link if available
        if result['sample_file']:
            sample_filename = result['sample_file'].split('/')[-1]
            lines.append(f"- **Sample saved**: [CSV Sample](../Logs/detail/{sample_filename})")
        
        # Add missing rows file link if available
        if result.get('missing_rows_file'):
            missing_rows_filename = result['missing_rows_file'].split('/')[-1]
            lines.append(f"- **Missing rows analysis**: [Missing Rows Report](../Logs/detail/{missing_rows_filename})")
        
        lines.append("")  # Add spacing between datasets
    
    return "\n".join(lines)


def display_configuration(datasets, max_rows, tolerance, imperfect_ratio_threshold):
    """Display current validation configuration to the user."""
    print("\n" + "="*60)
    print("DATASET VALIDATION CONFIGURATION")
    print("="*60)
    
    # Display validation thresholds
    print("Validation Thresholds:")
    print(f"  • Max row count ratio: {MAX_ROW_COUNT_RATIO:.3f} (Python can have up to {(MAX_ROW_COUNT_RATIO-1)*100:.1f}% more rows)")
    print(f"  • Imperfect ratio threshold: {imperfect_ratio_threshold:.3f} ({imperfect_ratio_threshold*100:.1f}%)")
    print(f"  • Numeric tolerance: {tolerance}")
    print(f"  • CSV sample threshold: {CSV_SAMPLE_THRESHOLD:.3f} ({CSV_SAMPLE_THRESHOLD*100:.1f}%)")
    
    # Display memory management
    print("\nMemory Management:")
    print(f"  • Row cap for RAM: {ROW_CAP_FOR_RAM:,} rows")
    print(f"  • Max rows per dataset: {max_rows:,} rows" if max_rows > 0 else "  • Max rows per dataset: unlimited")
    
    # Display reporting settings
    print("\nReporting Settings:")
    print(f"  • Max sample rows in reports: {MAX_SAMPLE_ROWS:,}")
    print(f"  • Max worst columns shown: {MAX_WORST_COLUMNS}")
    print(f"  • Max worst rows in CSV samples: {MAX_WORST_ROWS_FOR_SAMPLE}")
    
    # Display dataset selection
    print("\nDataset Selection:")
    if datasets is None:
        print("  • Validating: ALL datasets")
    else:
        print(f"  • Validating: {len(datasets)} dataset(s)")
        for i, dataset in enumerate(datasets[:10], 1):  # Show first 10
            print(f"    {i}. {dataset}")
        if len(datasets) > 10:
            print(f"    ... and {len(datasets) - 10} more")
    
    print("="*60)


def confirm_execution():
    """Ask user for confirmation before proceeding with validation."""
    while True:
        response = input("\nProceed with validation? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            print("Validation cancelled.")
            return False
        else:
            print("Please enter 'y' for yes or 'n' for no.")


def validate_all_datasets(datasets=None, max_rows=-1, tolerance=DEFAULT_TOLERANCE, imperfect_ratio_threshold=DEFAULT_IMPERFECT_RATIO_THRESHOLD):
    """Validate all or specified datasets and save to markdown file."""

    start_time = time.time()

    # Load dataset configuration
    with open('DataDownloads/00_map.yaml', 'r', encoding='utf-8') as f:
        dataset_map = yaml.safe_load(f)
    
    if datasets is None:
        datasets = list(dataset_map.keys())
    
    # Collect validation results
    all_results = []
    
    # Validate each dataset
    for dataset in datasets:
        # Load data once for both validation functions
        dta, parq, key_cols, config = load_dataset_pair(dataset, max_rows)
        
        # Run validation functions and collect results
        basic_result = val_one_basics(dataset, dta, parq)
        combined_result = val_one_crow(dataset, basic_result, dta, parq, key_cols, tolerance, imperfect_ratio_threshold)
        all_results.append(combined_result)
        
        # Print immediate feedback for this dataset (streaming output)
        print(f"\n=== {dataset} ===")
        for validation in combined_result['validations']:
            print(validation)
        if combined_result['details']:
            for detail in combined_result['details']:
                print(detail)
        print("") # blank line after each dataset
        
        # Force garbage collection after each dataset to free memory
        gc.collect()
    
    # Calculate execution time
    end_time = time.time()
    execution_time = (end_time - start_time) / 60  # Convert to minutes
    
    # Generate markdown content (will be reordered later for file output)
    markdown_content = format_results_to_markdown(all_results, max_rows, tolerance, execution_time, imperfect_ratio_threshold)
    
    # Console output already streamed above, just show final summary
    summary_text = generate_summary(all_results, imperfect_ratio_threshold)
    print("\n" + "="*50)
    print("FINAL SUMMARY")
    print("="*50)
    print(summary_text)
    
    # Save to markdown file (with failed datasets first)
    log_dir = Path("../Logs")
    log_dir.mkdir(exist_ok=True)
    
    # Reorder markdown content for file output (failed datasets first)
    reordered_markdown = reorder_markdown_by_failure_priority(markdown_content)
    
    output_file = log_dir / "testout_dl.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(reordered_markdown)
    
    print(f"\nResults saved to: {output_file}")
    print(f"Time taken: {execution_time:.2f} minutes")
    
    return markdown_content


def main():
    """Main execution function with command-line interface."""
    import argparse
    import sys
    from pathlib import Path
    
    # Check that script is being run from the correct directory (pyCode/)
    if not Path("01_DownloadData.py").exists():
        print("ERROR: This script must be run from the pyCode/ directory.")
        print("Usage: cd pyCode/ && python3 utils/test_dl.py")
        sys.exit(1)
    
    parser = argparse.ArgumentParser(
        description="Comprehensive validation of Python vs Stata datasets (basic + by-keys analysis)"
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
        '--maxrows',
        type=int,
        default=1000,
        help='Maximum number of rows to load from each dataset (default: 1000, use -1 for all rows)'
    )
    parser.add_argument(
        '--tolerance',
        type=float,
        default=DEFAULT_TOLERANCE,
        help=f'Tolerance for a "perfect" cell (default: {DEFAULT_TOLERANCE})'
    )
    parser.add_argument(
        '--imperfect-ratio-threshold',
        type=float,
        default=DEFAULT_IMPERFECT_RATIO_THRESHOLD,
        help=f'Maximum ratio for imperfect rows/cells acceptance (default: {DEFAULT_IMPERFECT_RATIO_THRESHOLD})'
    )
    
    args = parser.parse_args()
    
    # Load dataset configuration for --list option
    with open('DataDownloads/00_map.yaml', 'r', encoding='utf-8') as f:
        dataset_map = yaml.safe_load(f)
    
    # List datasets if requested
    if args.list:
        print("Available datasets for validation:")
        print("=" * 50)
        for i, dataset in enumerate(sorted(dataset_map.keys()), 1):
            config = dataset_map[dataset]
            # Get keys
            keys = []
            key_num = 1
            while f'key{key_num}' in config and config.get(f'key{key_num}'):
                keys.append(config[f'key{key_num}'])
                key_num += 1
            key_str = '+'.join(keys) if keys else 'None'
            print(f"{i:2d}. {dataset:<30} (keys: {key_str})")
        print(f"\nTotal: {len(dataset_map)} datasets")
        return
    
    # Determine which datasets to validate
    if args.datasets:
        # Validate that requested datasets exist
        invalid_datasets = [d for d in args.datasets if d not in dataset_map]
        if invalid_datasets:
            print(f"Error: Invalid datasets specified: {invalid_datasets}")
            print("Use --list to see available datasets")
            return
        datasets_to_validate = args.datasets
    else:
        datasets_to_validate = None  # Will validate all
    
    # Display configuration and ask for confirmation
    display_configuration(datasets_to_validate, args.maxrows, args.tolerance, args.imperfect_ratio_threshold)
    if not confirm_execution():
        return
    
    # Run validation
    validate_all_datasets(datasets_to_validate, args.maxrows, args.tolerance, args.imperfect_ratio_threshold)


if __name__ == "__main__":
    main()