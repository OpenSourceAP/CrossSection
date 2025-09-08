#!/usr/bin/env python3
"""
ABOUTME: Summary statistics generator for Predictors script outputs
ABOUTME: Computes counts, means, std dev, and percentiles for predictor datasets

This script takes a Predictors script name, finds all predictor datasets it produces
from 00_map_predictors.yaml, loads each dataset, and computes summary statistics for all
columns. Can process single scripts or all scripts in Predictors directory.

For all columns: count of non-missing values
For numeric columns: mean, standard deviation, 25th and 75th percentiles
(dropping missing values)

Arguments:
  script_name    Name of the Predictors script (e.g., 'ZZ1_Activism1_Activism2')
  --all          Process all Python scripts in Predictors directory

Output:
  Saves summary statistics to ../Logs/sumout_p_[script_name].md in markdown
  format (one file per script)

Usage examples:
  python3 utils/sum_pred.py ZZ1_Activism1_Activism2  # Summarize specific script
  python3 utils/sum_pred.py Beta                     # Summarize specific script
  python3 utils/sum_pred.py --all                    # Summarize all scripts
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


def load_dataset_map():
    """Load the predictor mapping configuration."""
    with open('Predictors/00_map_predictors.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def find_datasets_by_script(script_name, dataset_map):
    """Find all predictor datasets produced by a given script."""
    script_key = f"{script_name}.py"
    if script_key in dataset_map:
        return dataset_map[script_key].get('predictors', [])
    return []


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
            stats['p5'] = numeric_data.quantile(0.05)
            stats['p10'] = numeric_data.quantile(0.10)
            stats['p25'] = numeric_data.quantile(0.25)
            stats['p75'] = numeric_data.quantile(0.75)
            stats['p90'] = numeric_data.quantile(0.90)
            stats['p95'] = numeric_data.quantile(0.95)
        else:
            stats['mean'] = np.nan
            stats['std'] = np.nan
            stats['p5'] = np.nan
            stats['p10'] = np.nan
            stats['p25'] = np.nan
            stats['p75'] = np.nan
            stats['p90'] = np.nan
            stats['p95'] = np.nan
    else:
        # Non-numeric columns
        stats['mean'] = 'N/A'
        stats['std'] = 'N/A'
        stats['p5'] = 'N/A'
        stats['p10'] = 'N/A'
        stats['p25'] = 'N/A'
        stats['p75'] = 'N/A'
        stats['p90'] = 'N/A'
        stats['p95'] = 'N/A'

    return stats


def summarize_dataset(dataset_name, dataset_map):
    """Compute summary statistics for a single predictor dataset."""
    python_file = f"../pyData/Predictors/{dataset_name}"

    if not os.path.exists(python_file):
        return None, f"File not found: {python_file}"

    try:
        # Load the dataset (all predictor files are CSV)
        df = pd.read_csv(python_file)

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
    """Format summary statistics to markdown with transposed table format."""
    lines = []

    # Header
    lines.append(f"# Summary Statistics: {script_name}")
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    lines.append(f"Generated on: {timestamp}")
    lines.append("")

    if not results:
        lines.append("No predictor datasets found for this script.")
        return "\n".join(lines)

    # Summary table
    lines.append(f"**Total predictor datasets**: {len(results)}")
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

        # Get column names (variables)
        column_names = list(result['column_stats'].keys())
        
        # Define statistics to display (in order)
        stat_names = ['Count', 'Mean', 'Std Dev', '5th %', '10th %', '25th %', '75th %', '90th %', '95th %']
        stat_keys = ['count', 'mean', 'std', 'p5', 'p10', 'p25', 'p75', 'p90', 'p95']
        
        # Determine column widths
        stat_col_width = 12  # Width for statistic names column
        var_col_width = 12   # Minimum width for variable columns
        
        # Adjust variable column width based on variable names and data
        for col_name in column_names:
            var_col_width = max(var_col_width, len(col_name) + 2)
        var_col_width = min(var_col_width, 15)  # Cap at 15 chars
        
        # Build table header
        header_parts = ["Statistic".ljust(stat_col_width)]
        for col_name in column_names:
            col_display = col_name[:var_col_width-2].center(var_col_width)
            header_parts.append(col_display)
        header = "| " + " | ".join(header_parts) + " |"
        lines.append(header)
        
        # Build separator line
        sep_parts = ["-" * stat_col_width]
        for _ in column_names:
            sep_parts.append("-" * var_col_width)
        separator = "|" + "|".join(sep_parts) + "|"
        lines.append(separator)
        
        # Build data rows (one per statistic)
        for stat_name, stat_key in zip(stat_names, stat_keys):
            row_parts = [stat_name.ljust(stat_col_width)]
            
            for col_name in column_names:
                stats = result['column_stats'][col_name]
                stat_value = stats[stat_key]
                
                # Format the statistic value
                if stat_value == 'N/A':
                    formatted_value = 'N/A'.center(var_col_width)
                elif pd.isna(stat_value):
                    formatted_value = 'N/A'.center(var_col_width)
                else:
                    if stat_key == 'count':
                        # Format count with commas
                        value_str = f"{int(stat_value):,}"
                    else:
                        # Format numeric values with appropriate precision
                        if var_col_width >= 12:
                            precision = 2
                        else:
                            precision = 1
                        value_str = f"{stat_value:.{precision}f}"
                    
                    # Right-align numbers in the column
                    formatted_value = value_str.rjust(var_col_width)[:var_col_width]
                
                row_parts.append(formatted_value)
            
            row = "| " + " | ".join(row_parts) + " |"
            lines.append(row)

        lines.append("")

    return "\n".join(lines)


def process_single_script(script_name, dataset_map):
    """Process a single script and return success status."""
    print(f"🔍 Finding predictor datasets for script: {script_name}")

    # Find datasets for this script
    datasets = find_datasets_by_script(script_name, dataset_map)
    if not datasets:
        print(f"No predictor datasets found for script: {script_name}")
        return False

    print(f"📊 Found {len(datasets)} predictor datasets: {', '.join(datasets)}")

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
        print("No predictor datasets could be processed successfully.")
        return False

    # Generate markdown report
    markdown_content = format_stats_to_markdown(results, script_name)

    # Save to file
    output_dir = Path("../Logs")
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f"sumout_p_{script_name}.md"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    print(f"✅ Summary statistics saved to: {output_file}")
    print(f"📈 Processed {len(results)} predictor datasets successfully")
    return True


def get_all_predictors_scripts():
    """Get list of all Python scripts in Predictors directory."""
    script_files = glob.glob("Predictors/*.py")
    script_names = []
    for script_file in script_files:
        # Extract script name without path and .py extension
        script_name = os.path.basename(script_file)[:-3]  # Remove .py
        script_names.append(script_name)
    return sorted(script_names)


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Generate summary statistics for Predictors script outputs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python3 utils/sum_pred.py ZZ1_Activism1_Activism2  # Summarize specific script
  python3 utils/sum_pred.py --all                    # Summarize all scripts
        ''')
    
    parser.add_argument('script_name', nargs='?', 
                        help='Name of the Predictors script (e.g., ZZ1_Activism1_Activism2)')
    parser.add_argument('--all', action='store_true',
                        help='Process all Python scripts in Predictors directory')
    
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
    if not Path("02_CreatePredictors.py").exists():
        print("ERROR: This script must be run from the pyCode/ directory.")
        print("Usage: cd pyCode/ && python3 utils/sum_pred.py <script_name>")
        sys.exit(1)

    # Load dataset mapping
    try:
        dataset_map = load_dataset_map()
    except Exception as e:
        print(f"Error loading predictor dataset map: {e}")
        sys.exit(1)

    if args.all:
        # Process all scripts
        script_names = get_all_predictors_scripts()
        if not script_names:
            print("No Python scripts found in Predictors directory")
            sys.exit(1)
        
        print(f"🔄 Processing {len(script_names)} scripts in Predictors directory...")
        print("")
        
        successful_scripts = 0
        failed_scripts = []
        
        for script_name in script_names:
            print(f"{'='*60}")
            print(f"Processing script: {script_name}")
            print(f"{'='*60}")
            
            success = process_single_script(script_name, dataset_map)
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
        success = process_single_script(args.script_name, dataset_map)
        if not success:
            sys.exit(1)


if __name__ == "__main__":
    main()