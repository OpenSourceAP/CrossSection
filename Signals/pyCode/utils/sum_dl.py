#!/usr/bin/env python3
"""
ABOUTME: Summary statistics generator for DataDownloads script outputs
ABOUTME: Computes counts, means, std dev, and percentiles for datasets

This script takes a DataDownloads script name, finds all datasets it produces
from 00_map.yaml, loads each dataset, and computes summary statistics for all
columns.

For all columns: count of non-missing values
For numeric columns: mean, standard deviation, 25th and 75th percentiles
(dropping missing values)

Arguments:
  script_name    Name of the DataDownloads script (e.g., 'B_CompustatAnnual')

Output:
  Saves summary statistics to ../Logs/sum_dl_[script_name].md in markdown format

Usage examples:
  python3 utils/sum_dl.py B_CompustatAnnual  # Summarize annual outputs
  python3 utils/sum_dl.py I_CRSPmonthly     # Summarize monthly outputs
"""

import pandas as pd
import yaml
import sys
import os
from datetime import datetime
from pathlib import Path
import numpy as np


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
    lines.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
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

        # Create fixed-width statistics table
        lines.append("|      Variable      | Count |   Mean   | Std Dev  |  25th %  |  75th %  |")
        lines.append("|--------------------|-------|----------|----------|----------|----------|")

        for col_name, stats in result['column_stats'].items():
            count = f"{stats['count']:,}"

            # Format numeric statistics
            if stats['mean'] == 'N/A':
                mean = std = p25 = p75 = '  N/A    '
            else:
                if pd.isna(stats['mean']):
                    mean = std = p25 = p75 = '  N/A    '
                else:
                    mean = f"{stats['mean']:8.4f}"
                    std = f"{stats['std']:8.4f}"
                    p25 = f"{stats['p25']:8.4f}"
                    p75 = f"{stats['p75']:8.4f}"

            # Ensure column name fits 
            col_display = col_name[:17].ljust(17)

            line = f"| {col_display} | {count:>5} | {mean} | {std} | "
            line += f"{p25} | {p75} |"
            lines.append(line)

        lines.append("")

    return "\n".join(lines)

def main():
    """Main execution function."""
    if len(sys.argv) != 2:
        print("Usage: python3 utils/sum_dl.py <script_name>")
        print("Example: python3 utils/sum_dl.py B_CompustatAnnual")
        sys.exit(1)

    script_name = sys.argv[1]

    # Check that script is being run from the correct directory (pyCode/)
    if not Path("01_DownloadData.py").exists():
        print("ERROR: This script must be run from the pyCode/ directory.")
        print("Usage: cd pyCode/ && python3 utils/sum_dl.py <script_name>")
        sys.exit(1)

    print(f"🔍 Finding datasets for script: {script_name}")

    # Load dataset mapping
    try:
        dataset_map = load_dataset_map()
    except Exception as e:
        print(f"Error loading dataset map: {e}")
        sys.exit(1)

    # Find datasets for this script
    datasets = find_datasets_by_script(script_name, dataset_map)
    if not datasets:
        print(f"No datasets found for script: {script_name}")
        sys.exit(1)

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
        sys.exit(1)

    # Generate markdown report
    markdown_content = format_stats_to_markdown(results, script_name)

    # Save to file
    output_dir = Path("../Logs")
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f"sumout_dl_{script_name}.md"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    print(f"✅ Summary statistics saved to: {output_file}")
    print(f"📈 Processed {len(results)} datasets successfully")


if __name__ == "__main__":
    main()