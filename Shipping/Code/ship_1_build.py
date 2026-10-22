"""
ABOUTME: Step 1 of shipping: build the release folder (parquet) in the Google Drive location
ABOUTME: Python replacement for 1_pack_signals.r and 2_pack_portfolios_and_results.r

How to run (from anywhere):
    python Shipping/Code/ship_1_build.py [--out OUTPUT_DIR]
    --out overrides out_gdrive from ship_settings.yaml (useful for test builds)

INPUTS:
    - Shipping/Code/ship_settings.yaml (out_gdrive)
    - SignalDoc.csv
    - Signals/pyData/Predictors/*.csv, Signals/pyData/Placebos/*.csv
    - Portfolios/Data/Portfolios/*.csv, *.xlsx
    - Portfolios/Data/DailyPortfolios/<set>/*_ret.csv, DailyPortSummary.xlsx
    - Results/* (all files)

OUTPUTS (under the output folder, which must be empty beforehand):
    - SignalDoc.parquet, SignalDoc.csv (copy)
    - Firm Level Characteristics/Predictors.parquet               (wide, unsigned)
    - Firm Level Characteristics/Placebos.parquet                 (wide)
    - Firm Level Characteristics/signed_predictors_dl_wide.parquet (wide, signed)
    - Portfolios/Full Sets OP/*.parquet, *.xlsx
    - Portfolios/Full Sets Alt/*.parquet
    - DailyPortfolios/<set>.parquet (long: signalname, port, date, ret), DailyPortSummary.xlsx
    - Results/* (copied as is: pdf, tex, xlsx, RDS)
    WRDS exclusions (Price, Size, STreversal, BidAskTAQ) are never written.
"""

import argparse
import shutil
import time
from pathlib import Path

import polars as pl

from ship_utils import (
    ALT_DIR, DAILY_DIR, FIRM_DIR, OP_DIR, PATH_DAILY, PATH_PLACEBOS, PATH_PORTFOLIOS,
    PATH_PREDICTORS, PATH_RESULTS, PATH_SIGNALDOC, PORT_SCHEMA, RESULTS_DIR,
    doc_lists, load_settings, read_signaldoc, require_empty_dir,
)

KEYS = ['permno', 'yyyymm']


def log(msg):
    print(f'[{time.strftime("%H:%M:%S")}] {msg}', flush=True)


def write_parquet(df, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    df.write_parquet(path, compression='zstd')
    log(f'wrote {path.name}: {df.height:,} rows x {df.width} cols')


# ==== FIRM LEVEL CHARACTERISTICS ====

def read_signal(folder, name):
    df = pl.read_csv(
        folder / f'{name}.csv',
        schema_overrides={'permno': pl.Int32, 'yyyymm': pl.Int32, name: pl.Float64},
    )
    # some csvs put the signal before yyyymm, so compare as sets
    if set(df.columns) != set(KEYS + [name]):
        raise ValueError(f'{name}.csv has unexpected columns {df.columns}')
    df = df.select(KEYS + [name])
    if df.select(KEYS).is_duplicated().any():
        raise ValueError(f'{name}.csv has duplicate permno-yyyymm rows')
    return df


def build_wide(folder, names):
    """One row per permno-yyyymm, one column per signal (outer union of all signals)."""
    signals = {}
    for i, name in enumerate(names, 1):
        if not (folder / f'{name}.csv').exists():
            log(f'WARNING: {name}.csv does not exist in {folder}')
            continue
        print(f'  reading {name} #{i} of {len(names)}', flush=True)
        signals[name] = read_signal(folder, name)

    keys = pl.concat([df.select(KEYS) for df in signals.values()]).unique().sort(KEYS)
    cols = [
        keys.join(df, on=KEYS, how='left', maintain_order='left')[name]
        for name, df in signals.items()
    ]
    return keys.hstack(cols)


def build_firm_level(out, lists, doc):
    log('Building Predictors.parquet and signed_predictors_dl_wide.parquet')
    pred = build_wide(PATH_PREDICTORS, lists['predictor_dl'])
    write_parquet(pred, out / FIRM_DIR / 'Predictors.parquet')

    signs = dict(doc.select('signalname', pl.col('Sign').cast(pl.Float64)).iter_rows())
    signed = pred.with_columns([pl.col(c) * signs[c] for c in pred.columns if c not in KEYS])
    write_parquet(signed, out / FIRM_DIR / 'signed_predictors_dl_wide.parquet')
    del pred, signed

    log('Building Placebos.parquet')
    plac = build_wide(PATH_PLACEBOS, lists['placebo_dl'])
    write_parquet(plac, out / FIRM_DIR / 'Placebos.parquet')


# ==== PORTFOLIOS ====

def portfolio_csv_to_parquet(csv_path, out_dir):
    if csv_path.name == 'PredictorLSretWide.csv':
        df = pl.read_csv(
            csv_path, null_values='NA', infer_schema_length=None,
            schema_overrides={'date': pl.Date},
        )
    else:
        df = pl.read_csv(csv_path, schema_overrides=PORT_SCHEMA, null_values='NA')
    write_parquet(df, out_dir / f'{csv_path.stem}.parquet')


def build_portfolios(out):
    # Full Sets OP: everything except the PredictorAlt files (as in the R code)
    log('Building Portfolios/Full Sets OP')
    for f in sorted(PATH_PORTFOLIOS.iterdir()):
        if 'PredictorAlt' in f.name:
            continue
        if f.suffix == '.csv':
            portfolio_csv_to_parquet(f, out / OP_DIR)
        elif f.suffix == '.xlsx':
            (out / OP_DIR).mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, out / OP_DIR / f.name)

    # Full Sets Alt: PredictorAlt files plus PlaceboPortsFull
    log('Building Portfolios/Full Sets Alt')
    alt = sorted(PATH_PORTFOLIOS.glob('PredictorAlt*.csv')) + [PATH_PORTFOLIOS / 'PlaceboPortsFull.csv']
    for f in alt:
        portfolio_csv_to_parquet(f, out / ALT_DIR)


def build_daily(out):
    """Each DailyPortfolios/<set>/ folder of wide csvs becomes one long parquet."""
    log('Building DailyPortfolios')
    sets = sorted(d for d in PATH_DAILY.iterdir() if d.is_dir() and 'Predictor' in d.name)
    for d in sets:
        frames = []
        for f in sorted(d.glob('*_ret.csv')):
            wide = pl.read_csv(f, schema_overrides={'date': pl.Date}, null_values='NA', infer_schema_length=None)
            frames.append(
                wide.with_columns(pl.exclude('date').cast(pl.Float64))
                .unpivot(index='date', variable_name='port', value_name='ret')
                .with_columns(
                    signalname=pl.lit(f.name.removesuffix('_ret.csv')),
                    port=pl.col('port').str.strip_prefix('port'),
                )
                .filter(pl.col('ret').is_not_null())
            )
        df = pl.concat(frames).select('signalname', 'port', 'date', 'ret').sort('signalname', 'port', 'date')
        write_parquet(df, out / DAILY_DIR / f'{d.name}.parquet')

    shutil.copy2(PATH_DAILY / 'DailyPortSummary.xlsx', out / DAILY_DIR / 'DailyPortSummary.xlsx')


# ==== SIGNALDOC AND RESULTS ====

def build_doc_and_results(out):
    log('Writing SignalDoc (parquet and csv) and Results')
    write_parquet(pl.read_csv(PATH_SIGNALDOC, infer_schema_length=None), out / 'SignalDoc.parquet')
    shutil.copy2(PATH_SIGNALDOC, out / 'SignalDoc.csv')

    (out / RESULTS_DIR).mkdir(parents=True, exist_ok=True)
    results = sorted(f for f in PATH_RESULTS.iterdir() if f.is_file() and f.name != '.DS_Store')
    for f in results:
        shutil.copy2(f, out / RESULTS_DIR / f.name)
    log(f'copied {len(results)} files to {RESULTS_DIR}/')


def main(out):
    out = Path(out)
    log(f'Building release in {out}')
    require_empty_dir(out)

    doc = read_signaldoc()
    lists = doc_lists(doc)

    start = time.time()
    build_doc_and_results(out)
    build_portfolios(out)
    build_daily(out)
    build_firm_level(out, lists, doc)
    log(f'Done building release in {(time.time() - start) / 60:.1f} min')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--out', help='output folder (default: out_gdrive in ship_settings.yaml)')
    args = parser.parse_args()
    main(args.out or load_settings()['out_gdrive'])
