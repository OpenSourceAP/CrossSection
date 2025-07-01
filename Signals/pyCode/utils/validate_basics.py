"""
ABOUTME: Basic dataset validation script comparing Python vs Stata datasets
ABOUTME: Checks only column names, column types, and row count with simple output

This script provides basic validation that checks:
1. Column names match exactly
2. Column types match exactly  
3. Row count (Python can have slightly more rows, up to 0.1% more)

Arguments:
  --datasets, -d    Specific datasets to validate (default: all datasets)
  --list, -l        List all available datasets and exit
  --maxrows         Maximum rows to load per dataset (default: unlimited)

Output: 
  Prints results to console with ✓/✗ symbols
  Also saves results to ../Logs/valbasic.md in markdown format

Usage examples:
  python3 utils/validate_basics.py                           # Validate all datasets
  python3 utils/validate_basics.py --list                    # Show available datasets
  python3 utils/validate_basics.py -d m_QCompustat          # Validate one dataset
  python3 utils/validate_basics.py --maxrows 1000           # Limit to 1000 rows
  python3 utils/validate_basics.py -d CompustatAnnual --maxrows 5000
"""

import pandas as pd
import yaml
import io
import sys
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

def validate_single_dataset(dataset_name: str, max_rows: int = -1, output=None) -> None:
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
        
        # 1. Check column names
        if list(dta.columns) == list(parq.columns):
            output.print("✓ Column names match")
        else:
            output.print("✗ Column names differ")
            dta_only = set(dta.columns) - set(parq.columns)
            parq_only = set(parq.columns) - set(dta.columns)
            if dta_only:
                output.print(f"  - Stata only: {list(dta_only)}")
            if parq_only:
                output.print(f"  - Python only: {list(parq_only)}")
        
        # 2. Check column types
        common_cols = list(set(dta.columns) & set(parq.columns))
        type_match = True
        type_mismatches = []
        for col in common_cols:
            if dta[col].dtype != parq[col].dtype:
                type_match = False
                type_mismatches.append(f"  - {col}: Stata={dta[col].dtype} vs Python={parq[col].dtype}")
        
        if type_match:
            output.print("✓ Column types match")
        else:
            output.print("✗ Column types differ")
            for mismatch in type_mismatches:
                output.print(mismatch)
        
        # 3. Check row count
        stata_rows = len(dta)
        python_rows = len(parq)
        row_ratio = python_rows / stata_rows if stata_rows > 0 else float('inf')
        
        output.print(f"**Rows**: Stata={stata_rows:,}, Python={python_rows:,}")
        
        if python_rows == stata_rows:
            output.print("✓ Row counts match exactly")
        elif row_ratio <= 1.001:  # Python can have up to 0.1% more
            output.print("✓ Row counts acceptable (Python ≤ 0.1% more)")
        else:
            output.print(f"✗ Row count difference too large (ratio: {row_ratio:.3f})")
        
    except Exception as e:
        output.print(f"**ERROR**: {e}")


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
    output.print("# Basic Dataset Validation Report")
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
        validate_single_dataset(dataset, max_rows, output)
    
    # Save to markdown file
    log_dir = Path("../Logs")
    log_dir.mkdir(exist_ok=True)
    
    output_file = log_dir / "valbasic.md"
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
        print("Usage: cd pyCode/ && python3 utils/validate_basics.py")
        sys.exit(1)
    
    parser = argparse.ArgumentParser(
        description="Basic validation of Python vs Stata datasets (column names, types, row counts)"
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