# Repository Guidelines

## Project Structure & Module Organization
- `Signals/pyCode/` houses the modern Python pipeline; it writes intermediates to `Signals/pyData/` and detailed run logs to `Signals/Logs/`.
- `Signals/LegacyStataCode/` maintains the original Stata implementation and expects outputs in `Signals/Data/` for backward compatibility.
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

## Testing Guidelines
- Re-run the smallest pipeline slice touched by your change (e.g. `python 02_CreatePredictors.py`, selected R sources, or a Stata module) before submitting.
- Validate the Placebos leg by `cd`-ing into `Signals/pyCode/`, activating the venv, and running `python StataComparison/test_placebos.py --placebos <Name1> <Name2>` (use `--list` to discover available placebos); review the pytest output and confirm the generated diffs under `Signals/Logs/` are clean before proceeding.
- Review freshly generated logs under `Signals/Logs/` and spot-check key CSVs in `Signals/pyData/` or `Portfolios/Data/Portfolios/` for schema or row-count drift.
- When comparing vintages, run `python utils/sum_pred.py <ScriptName> --vintage before|after` (or `sum_dl.py`) and diff using `python utils/compare_sum.py before after --type pred --script <ScriptName>`, then link the report in your PR.
- Summarize validation evidence—row counts, checksum deltas, or exhibit previews—in your PR so collaborators can reproduce the check.
