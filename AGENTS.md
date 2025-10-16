# Repository Guidelines

## Project Structure & Module Organization
- `Signals/pyCode/` houses the modern Python pipeline; it writes intermediates to `Signals/pyData/` and detailed run logs to `Signals/Logs/`.
    - **IMPORTANT** The code here should never load data from `Signals/Data/`
- `Signals/LegacyStataCode/` this is the retired Stata code. It outputs and inputs using `Signals/Data/`. Both folders are only kept for reference.
- `Portfolios/Code/` contains R scripts that turn signals into portfolios (`Portfolios/Data/Portfolios/`) and paper exhibits (`Results/`).
- `Shipping/Code/` bundles cleaned outputs for distribution; run it only after verifying the upstream pipelines.

## Build, Test, and Development Commands
- From `Signals/pyCode/`, run `python set_up_pyCode.py` once, then `python master.py` for the full download→predictor workflow. Use `python 01_DownloadData.py` or `python 02_CreatePredictors.py` when iterating on a single stage.
- Set `pathProject` in `Portfolios/Code/master.R`, then call `Rscript master.R`; for smoke tests, toggle `quickrun = TRUE` while keeping `skipdaily = TRUE`.
- Update `pathProject` and the WRDS DSN in `Signals/LegacyStataCode/master.do`, then batch with your local Stata binary (e.g. `stata-mp -b do master.do`).

## Coding Style & Naming Conventions
- Python code uses 4-space indentation, snake_case, pathlib, and explicit docstrings (see `Signals/pyCode/master.py`). Log progress instead of printing silent failures.
- R scripts follow tidyverse idioms, lowercase object names, and section markers (`####`). Preserve `quickrun` pathways so reviewers can re-run subsets quickly.
- Stata do-files employ lowercase variables and local macros; match existing temp-file patterns when extending automation.
- Example commit message:
    - title `Fixed ZZ2_FailureProbability_FailureProbabilityJune.py`
    - body
        ```
        - Use a descending ordinal rank so the top-500 market-cap filter matches the Stata recursion.
        - Compute NIMTA/TLMTA/CASHMTA with raw denominators instead of inserting zeros that shrank book values.
        - Winsorize every temp* intermediate at the 5/95 clip just like winsor2, eliminating the R-squared gap.
        ```         

## Testing Guidelines
- Re-run the smallest pipeline slice touched by your change (e.g. `python 02_CreatePredictors.py`, selected R sources, or a Stata module) before submitting.
- Validate the Placebos leg by `cd`-ing into `Signals/pyCode/`, activating the venv, and running `python StataComparison/test_placebos.py --placebos <Name1> <Name2>` (use `--list` to discover available placebos). 
- Review freshly generated logs under `Signals/Logs/` and spot-check key CSVs in `Signals/pyData/` or `Portfolios/Data/Portfolios/` for schema or row-count drift.
- When comparing vintages, run `python utils/sum_pred.py <ScriptName> --vintage before|after` (or `sum_dl.py`) and diff using `python utils/compare_sum.py before after --type pred --script <ScriptName>`, then link the report in your PR.
- Summarize validation evidence—row counts, checksum deltas, or exhibit previews—in your PR so collaborators can reproduce the check.

## Python environment
- Use `source ~/venvloc/openalpha/bin/activate` to activate the virtual environment.
