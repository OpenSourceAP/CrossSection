"""
ABOUTME: Comprehensive dataset validation script comparing Python vs Stata datasets
ABOUTME: Checks column names, types, row counts, and performs by-keys deviation analysis

This script provides comprehensive validation that checks:
1. Column names match exactly
2. Column types match exactly  
3. Row count (Python can have slightly more rows, up to 0.1% more)
4. By-keys analysis: Imperfect Rows / Total Rows ratio
5. Value deviation statistics for worst columns
6. Sample CSV files for datasets with >0.1% imperfect ratio

Arguments:
  --datasets, -d    Specific datasets to validate (default: all datasets)
  --list, -l        List all available datasets and exit
  --maxrows         Maximum rows to load per dataset (default: 1000)

Output: 
  Prints results to console with ✓/✗ symbols
  Also saves results to ../Logs/test_dl.md in markdown format
  Creates CSV samples in ../Logs/detail/ for problematic datasets

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
import hashlib
from datetime import datetime
from pathlib import Path

class OutputCapture:
    """Capture output for both console and file writing."""
    def __init__(self):
        self.content = []
    
    def print(self, text=""):
        """Print to both console and capture for file."""
        print(text)
        self.content.append(text)
    
    def get_content(self):
        """Get captured content as string."""
        return "\n".join(self.content)


def simple_hash(s):
    """Convert string to numeric hash for comparison."""
    if pd.isna(s):
        return -1
    return int(hashlib.sha1(s.encode('utf-8')).hexdigest(), 16) % (10**8)  # truncate to 8 digits


def hash_df(df):
    """Convert dataframe to all-numeric for comparison by hashing strings and converting dates."""
    df = df.copy()
    
    # convert strings to numeric
    col_string = df.select_dtypes(include='object').columns
    for col in col_string:
        df[col] = df[col].apply(simple_hash)
    
    # convert datetime to numeric (handle both strings and datetime objects)
    col_datetime = df.select_dtypes(include=['datetime', 'datetime64']).columns
    for col in col_datetime:
        if df[col].dtype.name.startswith('datetime'):
            df[col] = df[col].astype('int64') // 10**9  # Convert to seconds
        else:
            df[col] = pd.to_datetime(df[col], errors='coerce').astype('int64') // 10**9
    
    # Round floating point numbers to avoid precision issues
    col_float = df.select_dtypes(include=['float64', 'float32']).columns
    for col in col_float:
        df[col] = df[col].round(6)  # Round to 6 decimal places
    
    # convert na to -999
    df = df.fillna(-999)
    
    return df

def val_one_basics(dataset_name: str, max_rows: int = -1, output=None) -> None:
    """Validate basic properties of a single dataset."""
    
    if output is None:
        output = OutputCapture()
    
    # Load dataset configuration
    with open('DataDownloads/00_map.yaml', 'r', encoding='utf-8') as f:
        dataset_map = yaml.safe_load(f)
    
    if dataset_name not in dataset_map:
        output.print(f"ERROR: {dataset_name} not found in map")
        return
    
    config = dataset_map[dataset_name]
    stata_file = f"../Data/Intermediate/{config['stata_file']}"
    python_file = f"../pyData/Intermediate/{config['python_file']}"
    
    output.print(f"\n## {dataset_name}")
    output.print("")
    
    try:
        # Load datasets with row limits
        if stata_file.endswith('.dta'):
            if max_rows > 0:
                dta = pd.read_stata(stata_file, chunksize=max_rows)
                dta = next(dta)
            else:
                dta = pd.read_stata(stata_file)
        elif stata_file.endswith('.csv'):
            nrows = None if max_rows <= 0 else max_rows
            dta = pd.read_csv(stata_file, nrows=nrows)
        else:
            output.print(f"ERROR: Unsupported Stata file format")
            return
            
        # Load Python file (can be parquet or csv)
        if python_file.endswith('.parquet'):
            parq = pd.read_parquet(python_file)
            if max_rows > 0:
                parq = parq.head(max_rows)
        elif python_file.endswith('.csv'):
            nrows = None if max_rows <= 0 else max_rows
            parq = pd.read_csv(python_file, nrows=nrows)
        else:
            output.print(f"ERROR: Unsupported Python file format")
            return
        
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
        elif row_ratio <= 1.001:  # Python can have up to 0.1% more
            validation_results.append("✓ Row counts acceptable (Python ≤ 0.1% more)")
        else:
            validation_results.append(f"✗ Row count difference too large (ratio: {row_ratio:.3f})")
        
        # Store row info for details section
        row_details = f"**Rows**: Stata={stata_rows:,}, Python={python_rows:,}"
        
        # Store results for integration with bykeys analysis
        output._basic_validation_results = validation_results
        output._basic_details = [row_details] + details
        
        # Store for integration with bykeys - don't output here
        
    except Exception as e:
        output.print("1. **ERROR**: Column names comparison failed")
        output.print("2. **ERROR**: Column types comparison failed")
        output.print("3. **ERROR**: Row count comparison failed")
        output.print(f"\n**Details**")
        output.print(f"- **Error**: {e}")


def val_one_bykeys(dataset_name: str, max_rows: int = -1, output=None) -> None:
    """Validate dataset by keys and compute imperfect rows ratio."""
    
    if output is None:
        output = OutputCapture()
    
    # Load dataset configuration
    with open('DataDownloads/00_map.yaml', 'r', encoding='utf-8') as f:
        dataset_map = yaml.safe_load(f)
    
    if dataset_name not in dataset_map:
        output.print(f"ERROR: {dataset_name} not found in map")
        return
    
    config = dataset_map[dataset_name]
    stata_file = f"../Data/Intermediate/{config['stata_file']}"
    python_file = f"../pyData/Intermediate/{config['python_file']}"
    
    # Get key columns from yaml
    key_cols = []
    key_num = 1
    while f'key{key_num}' in config and config.get(f'key{key_num}'):
        key_cols.append(config[f'key{key_num}'])
        key_num += 1
    
    if not key_cols:
        # Get basic validation if available, add warning for #4
        if hasattr(output, '_basic_validation_results'):
            all_results = output._basic_validation_results[:]
            all_details = output._basic_details[:]
        else:
            all_results = []
            all_details = []
        
        all_results.append("⚠ No key columns found - skipping by-keys analysis")
        
        # Output results
        for i, result in enumerate(all_results, 1):
            output.print(f"{i}. {result}")
        
        if all_details:
            output.print(f"\n**Details**")
            for detail in all_details:
                output.print(f"- {detail}")
        
        return
    
    try:
        # Load datasets with row limits
        if stata_file.endswith('.dta'):
            if max_rows > 0:
                dta = pd.read_stata(stata_file, chunksize=max_rows)
                dta = next(dta)
            else:
                dta = pd.read_stata(stata_file)
        elif stata_file.endswith('.csv'):
            nrows = None if max_rows <= 0 else max_rows
            dta = pd.read_csv(stata_file, nrows=nrows)
        else:
            output.print(f"ERROR: Unsupported Stata file format")
            return
            
        # Load Python file
        if python_file.endswith('.parquet'):
            parq = pd.read_parquet(python_file)
            if max_rows > 0:
                parq = parq.head(max_rows)
        elif python_file.endswith('.csv'):
            nrows = None if max_rows <= 0 else max_rows
            parq = pd.read_csv(python_file, nrows=nrows)
        else:
            output.print(f"ERROR: Unsupported Python file format")
            return
        
        # Index by key columns and find common keys
        dta = dta.reset_index(drop=True)
        parq = parq.reset_index(drop=True)
        
        # Check if key columns exist in both datasets 
        missing_keys_dta = [k for k in key_cols if k not in dta.columns]
        missing_keys_parq = [k for k in key_cols if k not in parq.columns]
        
        if missing_keys_dta or missing_keys_parq:
            # Get basic validation if available
            if hasattr(output, '_basic_validation_results'):
                all_results = output._basic_validation_results[:]
                all_details = output._basic_details[:]
            else:
                all_results = []
                all_details = []
            
            all_results.append(f"⚠ Missing key columns - Stata: {missing_keys_dta}, Python: {missing_keys_parq}")
            
            # Output results
            for i, result in enumerate(all_results, 1):
                output.print(f"{i}. {result}")
            
            if all_details:
                output.print(f"\n**Details**")
                for detail in all_details:
                    output.print(f"- {detail}")
            
            return
        
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
            # Get basic validation if available
            if hasattr(output, '_basic_validation_results'):
                all_results = output._basic_validation_results[:]
                all_details = output._basic_details[:]
            else:
                all_results = []
                all_details = []
            
            all_results.append("⚠ No common keys found")
            
            # Output results
            for i, result in enumerate(all_results, 1):
                output.print(f"{i}. {result}")
            
            if all_details:
                output.print(f"\n**Details**")
                for detail in all_details:
                    output.print(f"- {detail}")
            
            return
        
        # Convert to numeric for comparison
        dta_numeric = hash_df(dta_bykey)
        parq_numeric = hash_df(parq_bykey)
        
        # Calculate deviations
        diff_bykey = (dta_numeric - parq_numeric).abs()
        
        # Count imperfect rows (rows with any non-zero difference)
        dev_rows = diff_bykey.sum(axis=1) > 0
        
        # Report matching hierarchy
        full_data_rows = len(dta)
        matched_by_key_rows = len(dta_bykey)
        perfect_rows = matched_by_key_rows - dev_rows.sum()
        imperfect_rows = dev_rows.sum()
        imperfect_ratio = imperfect_rows / full_data_rows if full_data_rows > 0 else 0
        
        # Get basic validation results if they exist
        if hasattr(output, '_basic_validation_results'):
            all_results = output._basic_validation_results[:]
            all_details = output._basic_details[:]
        else:
            # No basic validation was run
            all_results = []
            all_details = [f"**Rows**: Stata={full_data_rows:,}, Python={len(parq):,}"]
        
        # Add imperfect ratio to validation results
        if imperfect_ratio <= 0.001:  # 0.1%
            all_results.append("✓ Imperfect ratio acceptable (≤ 0.1%)")
        else:
            all_results.append("✗ Imperfect ratio high (> 0.1%)")
        
        # Output numbered validation results
        for i, result in enumerate(all_results, 1):
            output.print(f"{i}. {result}")
        
        # Output detailed information
        output.print(f"\n**Details**")
        for detail in all_details:
            output.print(f"- {detail}")
        output.print(f"- **By-Keys Analysis**:")
        output.print(f"    - Full data rows: {full_data_rows:,}")
        output.print(f"    - Matched by key rows: {matched_by_key_rows:,}")
        output.print(f"    - Perfect rows: {perfect_rows:,}")
        output.print(f"    - Imperfect rows: {imperfect_rows:,}")
        output.print(f"    - **Imperfect / Total: {imperfect_ratio:.2%}**")
        
        # Report worst columns if there are deviations
        if imperfect_rows > 0:
            # Calculate average values for mean_col (levels, not deviations)
            ave_bykey = (dta_numeric + parq_numeric) / 2
            
            # Calculate column deviation stats
            dev_stats_list = []
            for col in diff_bykey.columns:
                s = diff_bykey[col]
                pct_pos = (s > 0).mean() * 100
                mean_if_pos = s[s > 0].mean() if (s > 0).any() else 0
                mean_col = ave_bykey[col].mean()
                
                dev_stats_list.append({
                    'col': col,
                    'pct_pos_bykey': pct_pos,
                    'mean_if_pos_bykey': mean_if_pos,
                    'mean_col_bykey': mean_col
                })
            
            dev_stats = pd.DataFrame(dev_stats_list)
            dev_stats = dev_stats.sort_values(by='pct_pos_bykey', ascending=False)
            
            # Show top 4 worst columns
            worst_4 = dev_stats.head(4)
            output.print(f"- **4 Worst Columns by Deviation %**:")
            for _, row in worst_4.iterrows():
                output.print(f"    - {row['col']}: {row['pct_pos_bykey']:.3f}% deviate (mean dev | pos: {row['mean_if_pos_bykey']:.2f}, mean col: {row['mean_col_bykey']:.2f})")
            
            # Save CSV sample if imperfect ratio > 0.1%
            if imperfect_ratio > 0.001:
                # Create detail directory
                detail_dir = Path("../Logs/detail")
                detail_dir.mkdir(parents=True, exist_ok=True)
                
                # Get worst columns and rows for sample
                col_worst = dev_stats.head(20)['col'].tolist()
                diff_worst = diff_bykey[col_worst]
                row_worst_idx = (diff_worst > 0).sum(axis=1).sort_values(ascending=False).head(20).index
                
                # Create sample with both Stata and Python values
                dta_sample = dta_bykey.loc[row_worst_idx, col_worst].assign(dsource='Stata').reset_index()
                parq_sample = parq_bykey.loc[row_worst_idx, col_worst].assign(dsource='Python').reset_index()
                
                # Combine and save
                sample_combined = pd.concat([dta_sample, parq_sample], axis=0).sort_values(key_cols + ['dsource'])
                
                csv_file = detail_dir / f"{dataset_name}_sample.csv"
                sample_combined.to_csv(csv_file, index=False)
                
                output.print(f"- **Sample saved**: [CSV Sample](../Logs/detail/{dataset_name}_sample.csv)")
        
    except Exception as e:
        # Get basic validation if available
        if hasattr(output, '_basic_validation_results'):
            all_results = output._basic_validation_results[:]
            all_details = output._basic_details[:]
        else:
            all_results = []
            all_details = []
        
        all_results.append("**ERROR**: By-keys analysis failed")
        
        # Output results
        for i, result in enumerate(all_results, 1):
            output.print(f"{i}. {result}")
        
        output.print(f"\n**Details**")
        for detail in all_details:
            output.print(f"- {detail}")
        output.print(f"- **Error in by-keys analysis**: {e}")


def validate_all_datasets(datasets=None, max_rows=-1):
    """Validate all or specified datasets and save to markdown file."""
    # Load dataset configuration
    with open('DataDownloads/00_map.yaml', 'r', encoding='utf-8') as f:
        dataset_map = yaml.safe_load(f)
    
    if datasets is None:
        datasets = list(dataset_map.keys())
    
    # Create output capture
    output = OutputCapture()
    
    # Header
    output.print("# Dataset Validation Report")
    output.print(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output.print("")
    output.print(f"**Datasets validated**: {len(datasets)}")
    if max_rows > 0:
        output.print(f"**Row limit**: {max_rows:,} rows per dataset")
    else:
        output.print("**Row limit**: unlimited")
    output.print("")
    
    # Validate each dataset
    for dataset in datasets:
        val_one_basics(dataset, max_rows, output)
        val_one_bykeys(dataset, max_rows, output)
        output.print("")  # Add spacing between datasets
    
    # Save to markdown file
    log_dir = Path("../Logs")
    log_dir.mkdir(exist_ok=True)
    
    output_file = log_dir / "test_dl.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output.get_content())
    
    print(f"\nResults saved to: {output_file}")
    return output.get_content()


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
    
    # Run validation
    validate_all_datasets(datasets_to_validate, args.maxrows)


if __name__ == "__main__":
    main()