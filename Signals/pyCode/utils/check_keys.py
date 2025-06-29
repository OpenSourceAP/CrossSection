"""
ABOUTME: Checks whether keys in 00_map.yaml uniquely identify rows in DTA files
ABOUTME: Outputs simple markdown report showing dataset key uniqueness status
"""

from pathlib import Path
from datetime import datetime

import yaml
import pandas as pd


def main(maxrows=None):
    """Check key uniqueness for all datasets and generate report."""

    # Load dataset mapping
    with open('DataDownloads/00_map.yaml', 'r', encoding='utf-8') as f:
        datasets = yaml.safe_load(f)

    # Track results
    results = []
    total_datasets = 0
    unique_datasets = 0

    print(f"Checking key uniqueness for {len(datasets)} datasets...")

    for dataset_name, config in datasets.items():
        if isinstance(config, dict) and 'stata_file' in config:
            total_datasets += 1

            # Get all key columns (key1, key2, key3, etc.)
            key_cols = []
            key_num = 1
            while f'key{key_num}' in config and config.get(f'key{key_num}'):
                key_cols.append(config[f'key{key_num}'])
                key_num += 1
            
            if not key_cols:
                continue  # Skip datasets with no keys

            # Load file from pyData (parquet or CSV based on extension)
            if config['stata_file'].endswith('.dta'):
                # Convert DTA to parquet filename for pyData
                python_file = config['stata_file'].replace('.dta', '.parquet')
            else:
                # Keep CSV filename as-is for pyData
                python_file = config['stata_file']
            data_file = Path(f"../pyData/Intermediate/{python_file}")

            try:
                if not data_file.exists():
                    results.append({
                        'dataset': dataset_name,
                        'status': 'MISSING FILE',
                        'keys': ', '.join(key_cols),
                        'duplicates': 0
                    })
                    continue

                # Load and check uniqueness
                file_ext = data_file.suffix.lower()
                if file_ext == '.csv':
                    if maxrows:
                        df = pd.read_csv(data_file, nrows=maxrows)
                        print(f"  {dataset_name}: Testing first {maxrows} rows")
                    else:
                        df = pd.read_csv(data_file)
                elif file_ext == '.parquet':
                    df = pd.read_parquet(data_file)
                    if maxrows:
                        df = df.head(maxrows)
                        print(f"  {dataset_name}: Testing first {maxrows} rows")
                else:  # .dta file (fallback)
                    if maxrows:
                        df = pd.read_stata(data_file, preserve_dtypes=False, 
                                         chunksize=maxrows)
                        df = next(df)  # Get first chunk
                        print(f"  {dataset_name}: Testing first {maxrows} rows")
                    else:
                        df = pd.read_stata(data_file, preserve_dtypes=False)
                original_rows = len(df)

                # Check if key columns exist
                missing_cols = [c for c in key_cols if c not in df.columns]
                if missing_cols:
                    missing_str = ', '.join(missing_cols)
                    results.append({
                        'dataset': dataset_name,
                        'status': 'MISSING COLUMNS',
                        'keys': f"{', '.join(key_cols)} (missing: {missing_str})",
                        'duplicates': 0
                    })
                    continue

                # Check uniqueness
                unique_rows = len(df.drop_duplicates(subset=key_cols))
                duplicates = original_rows - unique_rows

                if duplicates == 0:
                    status = 'UNIQUE'
                    unique_datasets += 1
                else:
                    status = f'{duplicates} DUPLICATES'

                results.append({
                    'dataset': dataset_name,
                    'status': status,
                    'keys': ', '.join(key_cols),
                    'duplicates': duplicates
                })

                print(f"  {dataset_name}: {status}")

            except Exception as e:
                results.append({
                    'dataset': dataset_name,
                    'status': f'ERROR: {str(e)[:50]}',
                    'keys': ', '.join(key_cols),
                    'duplicates': 0
                })

    # Generate report
    report_path = Path("../Logs/key_uniqueness_check.md")
    report_path.parent.mkdir(exist_ok=True)

    total_dup = total_datasets - unique_datasets
    unique_pct = unique_datasets/total_datasets*100
    dup_pct = total_dup/total_datasets*100

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"""# Key Uniqueness Check Results
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
- **Total datasets**: {total_datasets}
- **Unique keys**: {unique_datasets} ({unique_pct:.1f}%)
- **Duplicate keys**: {total_dup} ({dup_pct:.1f}%)

## Details

""")

        for result in results:
            if result['status'] == 'UNIQUE':
                icon = '✅'
            elif 'DUPLICATES' in result['status']:
                icon = '❌'
            else:
                icon = '⚠️'

            keys_str = result['keys']
            status_str = result['status']
            f.write(f"{icon} **{result['dataset']}**: "
                    f"{status_str} ({keys_str})\n")

    print(f"\nReport saved to: {report_path}")
    print(f"Summary: {unique_datasets}/{total_datasets} datasets have "
          f"unique keys")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        maxrows = int(sys.argv[1])
        print(f"Testing with max {maxrows} rows per dataset")
        main(maxrows)
    else:
        main()