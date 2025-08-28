# DataDownloads Leg

## DataDownloads Script Mapping

The DataDownloads leg is complicated. yaml files can help you get around
- DataDownloads/00_map.yaml
- DataDownloads/column_schemas.yaml


## Basic Requirements
- Python code should follow the stata counterpart as closely as possible
- The Python code must **not** use any data or code from the Stata project.
  - Do **not** use anything in `Data/`, including `Data/Intermediate/` or `Data/Prep/`
  - Do **not** use any code in `Code/`
- Output is parquet
  - Not pkl

## Validation 

**IMPORTANT**: Validation is done by running `python3 utils/test_dl.py`
  - Use `--max_rows` to limit the number of rows to test (-1 for all rows)
  - Use `--datasets` to specify datset(s)

### Basic Validation
This simple validation is fast and easy. 

Valid data satisfies:
1. Column names (exact match)
2. Column types (exact match)
3. Row count (Python can have more rows, but only 0.1% more)
  - Drop rows with missing keys before counting

### Common Rows Validation
This validation requires more careful analysis.

Define:
- Common rows: rows in both Stata and Python data that share the same keys 
  - Keys are based on @DataDownloads/00_map.yaml
- Perfect rows: common rows with columns that have no deviations
- Imperfect rows: common rows that are not perfect rows

Valid data satisfies:
4. Python common rows are a superset of Stata common rows
  - The Python data may contain recent observations that are not in the Stata data. 
  - But the Python data should not be missing any rows that are in the Stata data, since it was downloaded after the Stata data.
5. Imperfect cells / total cells < 0.1%
6. Imperfect rows / total rows < 0.1% or...
7. If Imperfect rows / total rows > 0.1%, have User appove:
  - Worst column stats look OK.
  - Sample of worst rows and columns look OK.

## Data Processing Standards
1. **Maintain data integrity**: Exact same filtering, cleaning, and transformations
2. **Preserve column names**: Keep original variable names from Stata
3. **Handle missing values**: Replicate Stata's missing value conventions
4. **Date formatting**: Ensure consistent date handling across files
5. **Data types**: Match Stata numeric precision where possible

## Error Handling
- Implement robust error handling for database connections
- Log processing times and success/failure status
- Create error flag system similar to Stata's `01_DownloadDataFlags`

## Paths and Filenames

**IMPORTANT**: All Python commands must be run from the `pyCode/` directory.

```bash
# Activate virtual environment (required for all operations)
source .venv/bin/activate

# Install/update dependencies
pip install -r requirements.txt

# Run all downloads
python3 01_DownloadData.py

# Run individual DataDownloads script
python3 DataDownloads/[SCRIPT_NAME].py

```
- check pyCode/DataDownloads/00_map.yaml to see which scripts should be used to download a given dataset
