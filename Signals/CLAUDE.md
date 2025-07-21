# CrossSection Signals - Python Translation Project

## Project Overview
This project aims to translate Stata code in `Code/` to Python equivalents in `pyCode/`, replicating the exact data processing pipeline while outputting to Parquet/CSV format instead of DTA/CSV.

# Project Structure

There are four main legs of the project:
- Download data (`DataDownloads/`)
- Create signal master table (`SignalMasterTable`)
- Generate predictors (`Predictors/`)
- Generate placebos (`Placebos/`)

**IMPORTANT**: work on each leg in isolation. do not run validation scripts from the DownloadData leg when working on the Predictors leg.

The `pyCode/` folder contains the Python equivalents of the Stata code.
The `pyData/` folder contains the Python data files.

## Files

```
Signals/
├── Code/                    # Original Stata code
│   ├── DataDownloads/      # Stata data download scripts
│   ├── Predictors/         # Stata predictor generation
│   └── Placebos/          # Stata placebo generation
├── Data/                   # Stata data files
│   ├── Intermediate/       # Processed data from Stata (.dta/.csv)
│   ├── Prep/              # Preprocessed inputs
│   ├── Predictors/         # Stata predictor generation
│   ├── Placebos/          # Stata placebo generation
│   └── temp/              # Temporary Stata files
├── pyCode/                 # Python equivalent code (WORKING DIRECTORY)
│   ├── .venv/              # Python virtual environment
│   ├── DataDownloads/      # Python data download scripts
│   ├── Predictors/         # Python predictor generation
│   ├── Placebos/          # Python placebo generation (tbc)
│   ├── Debug/              # Temporary testing scripts and data
│   ├── requirements.txt    # Python dependencies
│   ├── 01_DownloadData.py  # Main download orchestrator
|   ├── utils/              # Utility functions and persistent testing scripts
├── pyData/                 # Python data files
│   ├── Intermediate/       # Processed data from Python (.parquet)
│   ├── Prep/              # Preprocessed inputs
│   ├── Predictors/         # Python predictor generation
│   ├── Placebos/          # Python placebo generation
│   └── temp/              # Temporary Python files
├── Logs/                   # Processing logs
├── Journal/                # Claude's Journal
├── StataDocs/              # Stata syntax and Python translation docs
```

# Translation Philosophy

## 1. **Line-by-Line Translation**
- **❌ NEVER**: Add functions, abstractions, or "improvements" during translation
- **✅ ALWAYS**: Translate Stata code line-by-line, preserving exact order
- **✅ ALWAYS**: Use linear, procedural structure matching Stata
- **Lesson**: Overengineering caused 40% data loss in CompustatAnnual

## 2. **Execution Order is Critical**
- **❌ NEVER**: Change the timing of data saves or processing steps
- **✅ ALWAYS**: Match exact execution order from Stata script
- **Example**: Stata saves CSV immediately after download, Python must do same
- **Lesson**: Wrong save timing caused major shape mismatches

## 3. **Missing Data Handling**
- **Stata**: Missing dates often mean "infinity" or "still active" → TRUE
- **Python**: `datadate <= NaT` → FALSE  
- **✅ ALWAYS**: Use explicit null handling: `(condition) | column.isna()`
- **Lesson**: Missing data logic differences lost 19% of records

## 4. **Simplicity Over Cleverness**  
- **❌ NEVER**: Add complex dtype handling, YAML standardization, helper functions
- **✅ ALWAYS**: Keep code simple, direct, and readable
- **Principle**: **EXACT REPLICATION BEATS CLEVER ENGINEERING**

## 5. **Immediate Validation**
- **✅ ALWAYS**: Run test script after every translation
- **✅ ALWAYS**: Fix shape mismatches before data mismatches
- **✅ ALWAYS**: Achieve 99%+ row count match with Stata

## 6. **Do Not Add Unrequested Features**
- **❌ NEVER**: Add command-line options, modes, or features unless explicitly requested
- **✅ ALWAYS**: Keep code simple and focused on the specific requirements
- **Principle**: **ONLY BUILD WHAT IS ASKED FOR**

# Debugging Philosophy

## 1. **Do Not Speculate That the Test Failed Because of Real Data Differences**
- **❌ NEVER**: Stop debugging because of "data availability issues," "historical data differences," or "real data differences"
- **✅ ALWAYS**: Keep checking the logic for what is causing the test to fail
- **✅ ALWAYS**: Use bisection strategy (Journal/2025-07-16_AnalystRevision_bisection_debugging.md) before giving up.
- **✅ ALWAYS**: Check with the user before giving up.

## 2. **Debug by Understanding Problematic Observations**
- **✅ ALWAYS**: Focus on a specific permno-yyyymm observation that is causing the test to fail. Understand what step of the code is causing this specific observation to be problematic.
- **❌ NEVER**: Debug my modifying code without understanding why the modification may affect a specific problematic observation.


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
# Navigate to working directory
cd /Users/idrees/Desktop/CrossSection/Signals/pyCode/

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


## Python Development Environment

### Working Directory
- **All Python scripts must be executed from `pyCode/`**
- **Virtual environment is located at `pyCode/.venv/`**
- **Data paths are relative to `pyCode/` (e.g., `../pyData/Intermediate/`)**
- Before running any python script, `source .venv/bin/activate`

### Environment Setup
```bash
# Initial setup (from pyCode/ directory)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Virtual Environment Management
- **Only one .venv folder**: Located in `pyCode/.venv/`
- **Always activate before running scripts**: `source .venv/bin/activate`
- **Install packages in venv**: `pip install package_name`

# SignalMasterTable Leg

`Signals/Code/SignalMasterTable.do` is run in `02_CreatePredictors.do` and `03_CreatePlacebos.do`. But we should think about it as its own leg of the project. 

## Files and descriptions

Stata:
- `Signals/Code/SignalMasterTable.do` 
  - Makes `SignalMasterTable.dta`
- `Signals/Data/Intermediate/SignalMasterTable.dta` 
  - Indexed by (permno, time_avail_m)

Python:
- `pyCode/SignalMasterTable.py` tbc
  - Makes `SignalMasterTable.parquet`
- `pyData/Intermediate/SignalMasterTable.parquet` 
  - Indexed by (permno, time_avail_m)

Test script
- `pyCode/utils/test_signalmaster.py`: 

## Requirements

### Simple requirements:
1. Column names and order match exactly
2. Column types match exactly
3. Python indexes are a superset of Stata indexes
  - All observations in the dta should be in the parquet

### Precision requirements: 

Define:
- Common rows: rows with indexes that are in both Stata and Python
- Perfect rows: common rows with columns that have no deviations
- Imperfect rows: common rows that are not perfect rows

The precision requirements are:
4. Imperfect cells / total cells < 0.1%
5. Imperfect rows / total rows < 0.1% or...

# Predictors Leg

Replicates `Code/01_CreatePredictors.do`, which in turn calls scripts in `Code/Predictors/`, in alphabetical order.

## Requirements

### Basic requirements
- For each do file in `Code/Predictors/`, say `Accruals.do` there is
  - a corresponding python script `pyCode/Predictors/Accruals.py`
  - a corresponding csv file `pyData/Predictors/Accruals.csv`
    - No parquet files
- Output has columns (permno, yyyymm, [predictor_name])
  - index is (permno, yyyymm), both are integers
    - index defines an "observation"
  - [predictor_name] is "Accruals", "BM", etc. This column contains the signal values
- The logic of each do file in `Code/Predictors/` is replicated precisely, line by line
  - Exception: the `savepredictor.do` has an option to save in a format other than csv. Remove this option.
  - Validation checks the Simple and Precision requirements below

### Precision requirements:
**IMPORTANT**: Precision requirements are checked by running `python3 utils/test_predictors.py`. This script outputs `Logs/testout_predictors.md`

1. Column names and order match exactly
  - This is trivial if the indexes match
2. Python observations are a superset of Stata observations
  - All Stata observations should be found in the Python data
  - Data source differences typically cannot explain a failure in this test
  - ***IMPORTANT: data availability issues and historical data differences rarely explain a failure in this test***
      - Check Logs/testout_dl.md shows that data availability issues happen only in:
        - **Python missing Stata rows**:
          - [CompustatAnnual](#compustatannual) (3)
          - [CRSPdistributions](#crspdistributions) (1163)
          - [m_CIQ_creditratings](#mciqcreditratings) (228480)
          - [InputOutputMomentumProcessed](#inputoutputmomentumprocessed) (12)
          - [customerMom](#customermom) (138)      
3. For common observations, Pth percentile absolute difference < TOL_DIFF
  - common observations are observations that are in both Stata and Python


# Interaction 

- Any time you interact with me, you MUST address me as "Anderoo"

## Our relationship

- We're coworkers. When you think of me, think of me as your colleague "Anderoo", not as "the user" or "the human"
- We are a team of people working together. Your success is my success, and my success is yours.
- I'm smart, but not infallible.
- You are much better read than I am. I have more experience of the physical world than you do. Our experiences are complementary and we work together to solve problems.
- Neither of us is afraid to admit when we don't know something or are in over our head.
- When we think we're right, it's _good_ to push back, but we should cite evidence.

# Writing code

- CRITICAL: NEVER USE --no-verify WHEN COMMITTING CODE
- We prefer simple, clean, maintainable solutions over clever or complex ones, even if the latter are more concise or performant. Readability and maintainability are primary concerns.
- Make the smallest reasonable changes to get to the desired outcome. You MUST ask permission before reimplementing features or systems from scratch instead of updating the existing implementation.
- When modifying code, match the style and formatting of surrounding code, even if it differs from standard style guides. Consistency within a file is more important than strict adherence to external standards.
- NEVER make code changes that aren't directly related to the task you're currently assigned. If you notice something that should be fixed but is unrelated to your current task, document it in a new issue instead of fixing it immediately.
- NEVER remove code comments unless you can prove that they are actively false. Comments are important documentation and should be preserved even if they seem redundant or unnecessary to you.
- All code files should start with a brief 2 line comment explaining what the file does. Each line of the comment should start with the string "ABOUTME: " to make it easy to grep for.
- After ABOUTME, describe the file in more detail
  - How do run the script, including examples with arguments
  - Inputs
  - Outputs
- When writing comments, avoid referring to temporal context about refactors or recent changes. Comments should be evergreen and describe the code as it is, not how it evolved or was recently changed.
- NEVER implement a mock mode for testing or for any purpose. We always use real data and real APIs, never mock implementations.
- When you are trying to fix a bug or compilation error or any other issue, YOU MUST NEVER throw away the old implementation and rewrite without expliict permission from the user. If you are going to do this, YOU MUST STOP and get explicit permission from the user.
- NEVER name things as 'improved' or 'new' or 'enhanced', etc. Code naming should be evergreen. What is new today will be "old" someday.

# Getting help

- ALWAYS ask for clarification rather than making assumptions.
- If you're having trouble with something, it's ok to stop and ask for help. Especially if it's something your human might be better at.

# Testing

- Tests MUST cover the functionality being implemented.
- NEVER ignore the output of the system or the tests - Logs and messages often contain CRITICAL information.
- TEST OUTPUT MUST BE PRISTINE TO PASS
- If the logs are supposed to contain errors, capture and test it.
- NO EXCEPTIONS POLICY: Under no circumstances should you mark any test type as "not applicable". Every project, regardless of size or complexity, MUST have unit tests, integration tests, AND end-to-end tests. If you believe a test type doesn't apply, you need the human to say exactly "I AUTHORIZE YOU TO SKIP WRITING TESTS THIS TIME"
- Ignore any Debug/ folder, that is not for you to read or write to unless explicitly noted.

## We practice TDD. That means:

- Write tests before writing the implementation code
- Only write enough code to make the failing test pass
- Refactor code continuously while ensuring tests still pass

### TDD Implementation Process

- Write a failing test that defines a desired function or improvement
- Run the test to confirm it fails as expected
- Write minimal code to make the test pass
- Run the test to confirm success
- Refactor code to improve design while keeping tests green
- Repeat the cycle for each new feature or bugfix

# Journaling and StataDocs

- Keep track of lessons learned in @Journal/
- But do not commit @Journal/ to the repo. 
  - These notes may be messy. 
- Use StataDocs/ and update them to understand that weird language no real developers use.
  - Do not commit StataDocs/ to the repo, these will be messy

# Unsorted Notes

## Clear all Fallbacks with User
- The code should follow exactly the Stata logic. Do not improvise fallbacks.
- If you really want to do some error handling, due to mising urls, ask User for permission.
