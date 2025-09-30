#!/usr/bin/env python3
"""
ABOUTME: Summary statistics generator for DataDownloads script outputs
ABOUTME: Computes counts, means, std dev, and percentiles for datasets

This script takes a DataDownloads script name, finds all datasets it produces
from 00_map.yaml, loads each dataset, and computes summary statistics for all
columns. Can process single scripts or all scripts in DataDownloads directory.

For all columns: count of non-missing values
For numeric columns: mean, standard deviation, 25th and 75th percentiles
(dropping missing values)

Arguments:
  script_name    Name of the DataDownloads script (e.g., 'B_CompustatAnnual')
  --all          Process all Python scripts in DataDownloads directory

Output:
  Saves summary statistics to ../Logs/sumout_dl_[script_name].md in markdown
  format (one file per script)

Usage examples:
  python3 utils/sum_dl.py B_CompustatAnnual  # Summarize specific script
  python3 utils/sum_dl.py I_CRSPmonthly     # Summarize specific script
  python3 utils/sum_dl.py --all             # Summarize all scripts
"""

import pandas as pd
import yaml
import sys
import os
from datetime import datetime
from pathlib import Path
import numpy as np
import glob
import argparse
import json


def load_dataset_map():
    """Load the dataset mapping configuration."""
    with open('DataDownloads/00_map.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def find_datasets_by_script(script_name, dataset_map):
    """Find all datasets produced by a given script."""
    datasets = []
    for dataset_name, config in dataset_map.items():
        python_script = config.get('python_script', '')
        if (python_script.startswith(script_name) or
                python_script == f"{script_name}.py"):
            datasets.append(dataset_name)
    return datasets



def compute_column_stats(df, column_name):
    """Compute summary statistics for a single column."""
    stats = {}

    # Count non-missing values
    stats['count'] = df[column_name].notna().sum()

    # For numeric columns, compute additional statistics
    if pd.api.types.is_numeric_dtype(df[column_name]):
        # Drop missing values for numeric computations
        numeric_data = df[column_name].dropna()
        if len(numeric_data) > 0:
            stats['mean'] = numeric_data.mean()
            stats['std'] = numeric_data.std()
            stats['p25'] = numeric_data.quantile(0.25)
            stats['p75'] = numeric_data.quantile(0.75)
        else:
            stats['mean'] = np.nan
            stats['std'] = np.nan
            stats['p25'] = np.nan
            stats['p75'] = np.nan
    else:
        # Non-numeric columns
        stats['mean'] = 'N/A'
        stats['std'] = 'N/A'
        stats['p25'] = 'N/A'
        stats['p75'] = 'N/A'

    return stats


def summarize_dataset(dataset_name, dataset_map):
    """Compute summary statistics for a single dataset."""
    config = dataset_map[dataset_name]
    python_file = f"../pyData/Intermediate/{config['python_file']}"

    if not os.path.exists(python_file):
        return None, f"File not found: {python_file}"

    try:
        # Load the dataset
        if python_file.endswith('.parquet'):
            df = pd.read_parquet(python_file)
        elif python_file.endswith('.csv'):
            df = pd.read_csv(python_file)
        else:
            return None, f"Unsupported file type: {python_file}"

        # Compute statistics for each column
        column_stats = {}
        for col in df.columns:
            column_stats[col] = compute_column_stats(df, col)

        return {
            'dataset_name': dataset_name,
            'file_path': python_file,
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'column_stats': column_stats
        }, None

    except Exception as e:
        return None, f"Error loading {python_file}: {str(e)}"


def format_stats_to_markdown(results, script_name):
    """Format summary statistics to markdown."""
    lines = []

    # Header
    lines.append(f"# Summary Statistics: {script_name}")
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    lines.append(f"Generated on: {timestamp}")
    lines.append("")

    if not results:
        lines.append("No datasets found for this script.")
        return "\n".join(lines)

    # Summary table
    lines.append(f"**Total datasets**: {len(results)}")
    lines.append("")

    for result in results:
        dataset_name = result['dataset_name']
        lines.append(f"## {dataset_name}")
        lines.append("")
        lines.append(f"**File**: `{result['file_path']}`")
        dimensions = f"{result['total_rows']:,} rows × "
        dimensions += f"{result['total_columns']} columns"
        lines.append(f"**Dimensions**: {dimensions}")
        lines.append("")

        # Configurable column width for statistics columns
        col_width = 10
        
        # Create dynamic statistics table header
        var_col = "Variable".center(20)
        count_col = "Count".center(col_width)
        mean_col = "Mean".center(col_width)
        std_col = "Std Dev".center(col_width)
        p25_col = "25th %".center(col_width)
        p75_col = "75th %".center(col_width)
        
        header = (f"| {var_col} | {count_col} | {mean_col} | "
                 f"{std_col} | {p25_col} | {p75_col} |")
        lines.append(header)
        
        # Create dynamic separator line
        var_sep = "-" * 22
        stat_sep = "-" * (col_width+2)
        separator = (f"|{var_sep}|{stat_sep}|{stat_sep}|"
                    f"{stat_sep}|{stat_sep}|{stat_sep}|")
        lines.append(separator)

        for col_name, stats in result['column_stats'].items():
            # Format count with comma separators, right-aligned in column
            count_str = f"{stats['count']:,}"
            count_formatted = count_str.rjust(col_width)[:col_width]

            # Format numeric statistics to fit within col_width
            if stats['mean'] == 'N/A':
                mean = std = p25 = p75 = 'N/A'.center(col_width)
            else:
                if pd.isna(stats['mean']):
                    mean = std = p25 = p75 = 'N/A'.center(col_width)
                else:
                    # Determine precision based on column width
                    if col_width >= 10:
                        precision = 4
                    elif col_width >= 8:
                        precision = 2
                    else:
                        precision = 1
                    
                    mean_val = f"{stats['mean']:.{precision}f}"
                    mean = mean_val.rjust(col_width)[:col_width]
                    std_val = f"{stats['std']:.{precision}f}"
                    std = std_val.rjust(col_width)[:col_width]
                    p25_val = f"{stats['p25']:.{precision}f}"
                    p25 = p25_val.rjust(col_width)[:col_width]
                    p75_val = f"{stats['p75']:.{precision}f}"
                    p75 = p75_val.rjust(col_width)[:col_width]

            # Ensure column name fits in 20 characters
            col_display = col_name[:20].ljust(20)

            line = f"| {col_display} | {count_formatted} | {mean} | {std} | "
            line += f"{p25} | {p75} |"
            lines.append(line)

        lines.append("")

    return "\n".join(lines)


def save_stats_to_json(results, script_name, vintage_label):
    """Save summary statistics to JSON format for vintage comparison."""
    # Convert numpy types to native Python types for JSON serialization
    json_results = []
    for result in results:
        json_result = {
            'dataset_name': result['dataset_name'],
            'file_path': result['file_path'],
            'total_rows': int(result['total_rows']),
            'total_columns': int(result['total_columns']),
            'column_stats': {}
        }
        
        for col_name, stats in result['column_stats'].items():
            json_stats = {}
            for key, value in stats.items():
                if value == 'N/A':
                    json_stats[key] = None
                elif pd.isna(value):
                    json_stats[key] = None
                elif isinstance(value, (np.integer, np.int64)):
                    json_stats[key] = int(value)
                elif isinstance(value, (np.floating, np.float64)):
                    json_stats[key] = float(value)
                else:
                    json_stats[key] = value
            json_result['column_stats'][col_name] = json_stats
        
        json_results.append(json_result)
    
    # Save with metadata
    json_output = {
        'script_name': script_name,
        'timestamp': datetime.now().isoformat(),
        'vintage_label': vintage_label,
        'datasets': json_results
    }
    
    # Create vintage-specific directory
    output_dir = Path(f"../Logs/sum_dl_{vintage_label}")
    output_dir.mkdir(exist_ok=True, parents=True)
    
    # Save with consistent filename (no timestamp in filename)
    json_file = output_dir / f"{script_name}.json"
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(json_output, f, indent=2)
    
    return json_file


def process_single_script(script_name, dataset_map, vintage_label='unlabelled'):
    """Process a single script and return success status."""
    print(f"🔍 Finding datasets for script: {script_name}")
    print(f"📁 Vintage: {vintage_label}")

    # Find datasets for this script
    datasets = find_datasets_by_script(script_name, dataset_map)
    if not datasets:
        print(f"No datasets found for script: {script_name}")
        return False

    print(f"📊 Found {len(datasets)} datasets: {', '.join(datasets)}")

    # Process each dataset
    results = []
    errors = []

    for dataset_name in datasets:
        print(f"Processing {dataset_name}...")
        result, error = summarize_dataset(dataset_name, dataset_map)
        if error:
            errors.append(f"{dataset_name}: {error}")
        else:
            results.append(result)

    # Report any errors
    if errors:
        print("Errors encountered:")
        for error in errors:
            print(f"  ❌ {error}")

    if not results:
        print("No datasets could be processed successfully.")
        return False

    # Generate markdown report
    markdown_content = format_stats_to_markdown(results, script_name)

    # Create vintage-specific directory
    output_dir = Path(f"../Logs/sum_dl_{vintage_label}")
    output_dir.mkdir(exist_ok=True, parents=True)
    
    # Save markdown file
    md_file = output_dir / f"{script_name}.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    print(f"✅ Markdown saved to: {md_file}")
    
    # Save to JSON for vintage comparison
    json_file = save_stats_to_json(results, script_name, vintage_label)
    print(f"📁 JSON saved to: {json_file}")
    
    print(f"📈 Processed {len(results)} datasets successfully")
    return True


def get_all_datadownloads_scripts():
    """Get list of all Python scripts in DataDownloads directory."""
    script_files = glob.glob("DataDownloads/*.py")
    script_names = []
    for script_file in script_files:
        # Extract script name without path and .py extension
        script_name = os.path.basename(script_file)[:-3]  # Remove .py
        script_names.append(script_name)
    return sorted(script_names)


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Generate summary statistics for DataDownloads script outputs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python3 utils/sum_dl.py B_CompustatAnnual  # Summarize specific script
  python3 utils/sum_dl.py --all              # Summarize all scripts
        ''')
    
    parser.add_argument('script_name', nargs='?', 
                        help='Name of the DataDownloads script (e.g., B_CompustatAnnual)')
    parser.add_argument('--all', action='store_true',
                        help='Process all Python scripts in DataDownloads directory')
    parser.add_argument('--vintage', default='unlabelled',
                        help='Vintage label for output folder (default: unlabelled)')
    
    args = parser.parse_args()

    # Check for conflicting arguments
    if args.all and args.script_name:
        print("ERROR: Cannot specify both --all and a script name")
        sys.exit(1)
    
    if not args.all and not args.script_name:
        print("ERROR: Must specify either --all or a script name")
        parser.print_help()
        sys.exit(1)

    # Check that script is being run from the correct directory (pyCode/)
    if not Path("01_DownloadData.py").exists():
        print("ERROR: This script must be run from the pyCode/ directory.")
        print("Usage: python3 utils/sum_dl.py <script_name>")
        sys.exit(1)

    # Load dataset mapping
    try:
        dataset_map = load_dataset_map()
    except Exception as e:
        print(f"Error loading dataset map: {e}")
        sys.exit(1)

    if args.all:
        # Process all scripts
        script_names = get_all_datadownloads_scripts()
        if not script_names:
            print("No Python scripts found in DataDownloads directory")
            sys.exit(1)
        
        print(f"🔄 Processing {len(script_names)} scripts in DataDownloads directory...")
        print("")
        
        successful_scripts = 0
        failed_scripts = []
        
        for script_name in script_names:
            print(f"{'='*60}")
            print(f"Processing script: {script_name}")
            print(f"{'='*60}")
            
            success = process_single_script(script_name, dataset_map, args.vintage)
            if success:
                successful_scripts += 1
            else:
                failed_scripts.append(script_name)
            print("")
        
        # Final summary
        print(f"{'='*60}")
        print(f"FINAL SUMMARY")
        print(f"{'='*60}")
        print(f"✅ Successfully processed: {successful_scripts}/{len(script_names)} scripts")
        if failed_scripts:
            print(f"❌ Failed scripts: {', '.join(failed_scripts)}")
    else:
        # Process single script
        success = process_single_script(args.script_name, dataset_map, args.vintage)
        if not success:
            sys.exit(1)


if __name__ == "__main__":
    main()