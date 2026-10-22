"""
ABOUTME: Shared settings, paths, and SignalDoc helpers for the ship_*.py scripts
ABOUTME: Imported by ship_1_build.py, ship_2_check.py, ship_3_upload_hf.py, ship_master.py

How to run: not run directly; `import ship_utils` from Shipping/Code/.

INPUTS:
    - Shipping/Code/ship_settings.yaml
    - <repo root>/SignalDoc.csv

OUTPUTS:
    - none (helpers only)
"""

from pathlib import Path

import polars as pl
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
CODE_DIR = REPO_ROOT / 'Shipping' / 'Code'
TEMP_DIR = REPO_ROOT / 'Shipping' / 'Data' / 'temp'

PATH_PREDICTORS = REPO_ROOT / 'Signals' / 'pyData' / 'Predictors'
PATH_PLACEBOS = REPO_ROOT / 'Signals' / 'pyData' / 'Placebos'
PATH_PORTFOLIOS = REPO_ROOT / 'Portfolios' / 'Data' / 'Portfolios'
PATH_DAILY = REPO_ROOT / 'Portfolios' / 'Data' / 'DailyPortfolios'
PATH_RESULTS = REPO_ROOT / 'Results'
PATH_SIGNALDOC = REPO_ROOT / 'SignalDoc.csv'

# WRDS exclusions: CRSP-only predictors and TAQ spreads cannot be redistributed
WRDS_EXCLUDED_PREDICTORS = ['Price', 'Size', 'STreversal']
WRDS_EXCLUDED_PLACEBOS = ['BidAskTAQ']
WRDS_EXCLUDED = WRDS_EXCLUDED_PREDICTORS + WRDS_EXCLUDED_PLACEBOS

# firm-level keys
KEYS = ['permno', 'yyyymm']

# portfolio csvs: keep port as text ('01', 'LS')
PORT_SCHEMA = {
    'signalname': pl.String,
    'port': pl.String,
    'date': pl.Date,
    'ret': pl.Float64,
    'signallag': pl.Float64,
    'Nlong': pl.Int64,
    'Nshort': pl.Int64,
}

# release layout, relative to the output folder
FIRM_DIR = 'Firm Level Characteristics'
OP_DIR = 'Portfolios/Full Sets OP'
ALT_DIR = 'Portfolios/Full Sets Alt'
DAILY_DIR = 'DailyPortfolios'
RESULTS_DIR = 'Results'
CHECKS_FILE = 'storage_checks.txt'
CHECKS_PASS_LINE = 'AUTOMATED CHECKS: PASS'


def load_settings():
    with open(CODE_DIR / 'ship_settings.yaml') as f:
        settings = yaml.safe_load(f)
    for key in ['out_gdrive', 'old_release']:
        settings[key] = Path(settings[key]).expanduser()
    return settings


def require_empty_dir(path):
    """Create path if missing; stop if it holds anything besides .DS_Store."""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    contents = [p.name for p in path.iterdir() if p.name != '.DS_Store']
    if contents:
        raise SystemExit(
            f'Output folder is not empty: {path}\n'
            f'Found {len(contents)} entries, e.g. {contents[:5]}\n'
            'Empty it by hand (or point the config elsewhere) and rerun.'
        )


def read_signaldoc():
    """SignalDoc.csv with Acronym renamed to signalname, sorted by signalname."""
    doc = pl.read_csv(PATH_SIGNALDOC, infer_schema_length=None)
    return doc.rename({'Acronym': 'signalname'}).sort('signalname')


def doc_lists(doc):
    """Signal lists used by the build and the checks."""
    pred = doc.filter(pl.col('Cat.Signal') == 'Predictor')
    plac = doc.filter(pl.col('Cat.Signal') == 'Placebo')
    return {
        'predictor': pred['signalname'].to_list(),
        'predictor_dl': [s for s in pred['signalname'] if s not in WRDS_EXCLUDED_PREDICTORS],
        'predictor_cts': pred.filter(pl.col('Cat.Form') == 'continuous')['signalname'].to_list(),
        'placebo_dl': [s for s in plac['signalname'] if s not in WRDS_EXCLUDED_PLACEBOS],
    }
