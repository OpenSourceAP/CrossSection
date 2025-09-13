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

## Folder Structure

Check the user's `~/.claude/CLAUDE.md` for full path of `Signals`
- search for "SIGNALSPATH"
- if "SIGNALSPATH" is not found, ask the user to add it to `~/.claude/CLAUDE.md`

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
│   ├── requirements.txt    # Python dependencies
│   ├── 01_DownloadData.py  # Main download orchestrator
|   ├── utils/              # Utility functions and persistent testing scripts
|   ├── Debug/              # Debugging scripts
├── pyData/                 # Python data files
│   ├── Intermediate/       # Processed data from Python (.parquet)
│   ├── Prep/              # Preprocessed inputs
│   ├── Predictors/         # Python predictor generation
│   ├── Placebos/          # Python placebo generation
│   └── temp/              # Temporary Python files
├── Logs/                   # Processing logs
├── Journal/                # Claude's Journal
├── DocsForClaude/          # Claude's Docs
├── Plan/                   # Claude's Planning docs
```

# Coding Environment, Tools, and Docs

## Working Directory
- **All Python scripts must be executed from `pyCode/`**
  - Check SIGNALSPATH for full path of `Signals/pyCode/`
- **Virtual environment is located at `pyCode/.venv/`**
  - Do not create any new virtual environments.
- **Data paths are relative to `pyCode/` (e.g., `../pyData/Intermediate/`)**

## Tools 
- Do not use long Bash commands. 
  - If a Bash command is more then 3 lines, write a py script in `pyCode/Debug/` that generates test output instead.
  - This ensures that the permissions are correct and avoids unneeded user intervention.

## Docs
- `DocsForClaude/` contains long-term docs about the project
  - `stata_*.md` are docs about Stata commands
  - `leg*.md` are docs about the project legs
- `Journal/` contains messy notes about the project
  - Recent Journal/ entries may be helpful for passing tests.

# Translation Philosophy

## **Line-by-Line Translation**
- **❌ NEVER**: Add functions, abstractions, or "improvements" during translation
- **✅ ALWAYS**: Translate Stata code line-by-line, preserving exact order
- **✅ ALWAYS**: Use linear, procedural structure matching Stata
- **Lesson**: Overengineering caused 40% data loss in CompustatAnnual

## **Execution Order is Critical**
- **❌ NEVER**: Change the timing of data saves or processing steps
- **✅ ALWAYS**: Match exact execution order from Stata script
- **Example**: Stata saves CSV immediately after download, Python must do same
- **Lesson**: Wrong save timing caused major shape mismatches

## **Missing Data Handling**
- **Stata**: Missing dates often mean "infinity" or "still active" → TRUE
- **Python**: `datadate <= NaT` → FALSE  
- **✅ ALWAYS**: Use explicit null handling: `(condition) | column.isna()`
- **Lesson**: Missing data logic differences lost 19% of records

## **Simplicity Over Cleverness**  
- **❌ NEVER**: Add complex dtype handling, YAML standardization, helper functions
- **✅ ALWAYS**: Keep code simple, direct, and readable
- **Principle**: **EXACT REPLICATION BEATS CLEVER ENGINEERING**

## **Immediate Validation**
- **✅ ALWAYS**: Run test script after every translation
- **✅ ALWAYS**: Fix shape mismatches before data mismatches
- **✅ ALWAYS**: Achieve 99%+ row count match with Stata

## **Do Not Add Unrequested Features**
- **❌ NEVER**: Add command-line options, modes, or features unless explicitly requested
- **✅ ALWAYS**: Keep code simple and focused on the specific requirements
- **Principle**: **ONLY BUILD WHAT IS ASKED FOR**

# Debugging Philosophy

## **Do Not Speculate That the Test Failed Because of Real Data Differences**
- **❌ NEVER**: Stop debugging because of "data availability issues," "historical data differences," or "real data differences"
- **✅ ALWAYS**: Keep checking the logic for what is causing the test to fail
- **✅ ALWAYS**: Check with the user before giving up.

## **Debug by Understanding Problematic Observations**
- **✅ ALWAYS**: Focus on a specific permno-yyyymm observation that is causing the test to fail. Understand what step of the code is causing this specific observation to be problematic.
- **❌ NEVER**: Debug my modifying code without understanding why the modification may affect a specific problematic observation.

## **Understand Stata's Exact Behavior First**
- **❌ WRONG**: Assume Python pandas methods match Stata operators
- **✅ RIGHT**: Research StataDocs and trace Stata's exact processing logic
- **Key Discovery**: Stata's `l6.` uses calendar-based lags, not position-based `shift(6)`

## **Write Debugging py scripts**
- **WRONG**: Run a long bash command that to generate test output.
- **RIGHT**: Write a py script in `pyCode/Debug/` that generates test output.

# Journal, Documentation, and Planning

The notes go in the following folders:
- `Journal/`
  - This is a messy folder, put whatever you want in it.
  - format filenames like "[MMDD]n[id]-[title].md" 
- `DocsForClaude/`
  - This folder has long-term docs about the project. It includes important lessons from `Journal/`
- `Plan/`
  - This folder contains plans for coding across Claude Code sessions. If one session gets too long, put the next steps and required context for the next Claude Code session in this folder.
  - Each md file here should be one self-contained plan.

**IMPORTANT**: all of these documents may become out of date. Only rely on them if the user asks you to.

# Context for Current Task
We're working on the Predictors leg: `DocsForClaude/leg3-predictors.md`.

# Predictor Script Validation

## Before/After Testing with sum_pred.py
When modifying predictor scripts, use `utils/sum_pred.py` for validation:

**Before changes:**
```bash
python utils/sum_pred.py [ScriptName] --vintage before_changes
```

**After changes:**
```bash
python utils/sum_pred.py [ScriptName] --vintage after_changes
```

**Validation criteria:**
- Identical row counts in output files
- Matching column statistics (mean, std, percentiles)
- Same data types for all columns
- Compare log files in `../Logs/sum_pred_[vintage]/[ScriptName].md`

## Comparing Summary Statistics Between Vintages
Use `utils/compare_sum.py` to compare summary statistics between any two vintages:

**Basic usage:**
```bash
python utils/compare_sum.py vintage1 vintage2 --type [dl|pred] --script ScriptName
```

**Examples:**
```bash
# Compare predictor script changes
python utils/compare_sum.py before_changes after_changes --type pred --script CustomerMomentum

# Compare data download script changes
python utils/compare_sum.py unlabelled v1.0_baseline --type dl --script B_CompustatAnnual

# Save report to file
python utils/compare_sum.py v1 v2 --type pred --script Beta --output comparison_report.md

# Use custom tolerance for statistical differences (default: 1%)
python utils/compare_sum.py v1 v2 --type pred --script Beta --tolerance 0.001
```

**Report includes:**
- **Vintage Statistics**: Detailed statistical comparison table showing Count, Mean, Std Dev, and percentiles (5th, 10th, 25th, 75th, 90th, 95th) for each data column
- **Structure Changes**: New/removed datasets
- **Row Count Changes**: Datasets with different row counts
- **Column Changes**: New/removed columns
- **Statistical Changes**: Columns with significant statistical differences
- **Difference Statistics**: Summary of change magnitudes and distributions
- **Summary**: Overall assessment of differences found

**When to use:**
- Before and after major script modifications
- Validating data pipeline changes
- Debugging unexpected differences between vintages
- Documenting the impact of code changes
