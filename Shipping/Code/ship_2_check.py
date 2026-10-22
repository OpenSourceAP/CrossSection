"""
ABOUTME: Step 2 of shipping: check the built release folder and write storage_checks.txt into it
ABOUTME: Python translation of 3_check_storage.r and 4_old_vs_new_check.R, plus layout checks

How to run (from anywhere):
    python Shipping/Code/ship_2_check.py [--out OUTPUT_DIR]
    --out overrides out_gdrive from ship_settings.yaml (useful for test builds)

INPUTS:
    - Shipping/Code/ship_settings.yaml (out_gdrive, old_release)
    - SignalDoc.csv
    - the release folder written by ship_1_build.py
    - Portfolios/Data/Portfolios/ (to confirm every source portfolio file was shipped)
    - <old_release>/Portfolios/Full Sets OP/PredictorPortsFull.parquet (or .csv for releases
      before 2026)

OUTPUTS:
    - <release folder>/storage_checks.txt (also echoed to the console). Its last
      line is 'AUTOMATED CHECKS: PASS' or 'AUTOMATED CHECKS: FAIL' plus the failures.
      ship_3_upload_hf.py refuses to upload without the PASS line.
    - Shipping/Data/temp/PredictorPortsCheck.csv (old-vs-new regressions by signal-port)
"""

import argparse
import datetime
import sys
from pathlib import Path

import polars as pl

from ship_utils import (
    ALT_DIR, CHECKS_FILE, CHECKS_PASS_LINE, DAILY_DIR, FIRM_DIR, KEYS, OP_DIR, PATH_PORTFOLIOS,
    PATH_SIGNALDOC, RESULTS_DIR, TEMP_DIR, WRDS_EXCLUDED, doc_lists, load_settings, read_signaldoc,
)

pl.Config.set_tbl_rows(1000)
pl.Config.set_tbl_cols(100)
pl.Config.set_tbl_width_chars(1000)
pl.Config.set_fmt_str_lengths(100)
pl.Config.set_tbl_hide_dataframe_shape(True)

THIS_YEAR = datetime.date.today().year
ALLOWED_SUFFIXES = {'.parquet', '.pdf', '.xlsx', '.txt', '.md'}


class Report:
    """Collects console + file output and a list of failures."""

    def __init__(self):
        self.lines = []
        self.failures = []

    def __call__(self, *items):
        text = ' '.join(str(x) for x in items)
        print(text, flush=True)
        self.lines.append(text)

    def fail(self, msg):
        self.failures.append(msg)
        self(f'FAIL: {msg}')

    def warn(self, msg):
        self(f'WARNING: {msg}')

    def section(self, title):
        self('')
        self(f' === {title} === ')
        self('')


# ==== LAYOUT ====

# Small explicit required list. Other alternative implementations (HoldPer, FF93style,
# other LiqScreens, EW variants) are optional: they must ship if the source has them
# (check_source_shipped), and are only warned about if the old release had them.
def expected_files(out):
    files = [
        'SignalDoc.parquet',
        'SignalDoc.csv',
        f'{FIRM_DIR}/Predictors.parquet',
        f'{FIRM_DIR}/Placebos.parquet',
        f'{FIRM_DIR}/signed_predictors_dl_wide.parquet',
        f'{OP_DIR}/PredictorPortsFull.parquet',
        f'{OP_DIR}/PlaceboPortsFull.parquet',
        f'{OP_DIR}/PredictorLSretWide.parquet',
        f'{OP_DIR}/PredictorSummary.xlsx',
        f'{OP_DIR}/PlaceboSummary.xlsx',
        f'{DAILY_DIR}/DailyPortSummary.xlsx',
        f'{ALT_DIR}/PlaceboPortsFull.parquet',
        f'{ALT_DIR}/PredictorAltPorts_LiqScreen_VWforce.parquet',
        f'{ALT_DIR}/PredictorAltPorts_Deciles.parquet',
        f'{ALT_DIR}/PredictorAltPorts_DecilesVW.parquet',
        f'{ALT_DIR}/PredictorAltPorts_Quintiles.parquet',
        f'{ALT_DIR}/PredictorAltPorts_QuintilesVW.parquet',
    ]
    files += [f'{DAILY_DIR}/{s}.parquet' for s in DAILY_SETS]
    return [out / f for f in files]


DAILY_SETS = [
    'Predictor', 'PredictorVW',
    'CtsPredictorDecile', 'CtsPredictorDecileVW', 'CtsPredictorQuintile', 'CtsPredictorQuintileVW',
]


def check_source_shipped(out, old_release, r):
    """Every portfolio csv/xlsx in the source folder has a counterpart in the release."""
    for f in sorted(PATH_PORTFOLIOS.iterdir()):
        if f.suffix not in ('.csv', '.xlsx'):
            continue
        sub = ALT_DIR if 'PredictorAlt' in f.name else OP_DIR
        target = out / sub / (f.name if f.suffix == '.xlsx' else f'{f.stem}.parquet')
        if not target.exists():
            r.fail(f'source file {f.name} not shipped as {target.relative_to(out)}')

    old_alt = Path(old_release) / ALT_DIR
    if old_alt.exists():
        new_alt = {p.stem for p in (out / ALT_DIR).glob('*.parquet')}
        dropped = sorted({p.stem for p in old_alt.iterdir() if p.suffix in ('.zip', '.csv', '.parquet')} - new_alt)
        if dropped:
            r.warn(f'alternative portfolio sets in the old release but not this one: {dropped}')


def check_layout(out, r):
    r.section('RELEASE LAYOUT')
    files = sorted(p for p in out.rglob('*') if p.is_file() and p.name != '.DS_Store')
    for p in files:
        r(f'{p.stat().st_size / 1e6:10.1f} MB  {p.relative_to(out)}')
    r(f'Total: {sum(p.stat().st_size for p in files) / 1e9:.2f} GB in {len(files)} files')
    r('')

    for p in expected_files(out):
        if not p.exists():
            r.fail(f'missing {p.relative_to(out)}')

    for p in files:
        rel = p.relative_to(out)
        if 'Individual' in rel.parts or p.name.endswith('Indiv.zip'):
            r.fail(f'omitted item is present: {rel}')
        # Results/ is shipped as is; elsewhere data must be parquet (SignalDoc.csv is a convenience copy)
        if rel.parts[0] != RESULTS_DIR and p.suffix not in ALLOWED_SUFFIXES and str(rel) != 'SignalDoc.csv':
            r.fail(f'unexpected file type: {rel}')

    pdfs = list((out / RESULTS_DIR).glob('*.pdf'))
    r(f'Results pdfs: {len(pdfs)}')
    if not pdfs:
        r.fail('no pdfs in Results/')

    if (out / 'SignalDoc.csv').read_bytes() != PATH_SIGNALDOC.read_bytes():
        r.fail('SignalDoc.csv differs from the repo copy')
    else:
        r('SignalDoc.csv is identical to the repo copy')

    doc_csv = pl.read_csv(PATH_SIGNALDOC, infer_schema_length=None)
    doc_pq = pl.read_parquet(out / 'SignalDoc.parquet')
    if not doc_pq.equals(doc_csv):
        r.fail('SignalDoc.parquet does not match SignalDoc.csv')
    else:
        r(f'SignalDoc.parquet matches SignalDoc.csv ({doc_pq.height} signals)')


# ==== SIGNAL LISTS VS SIGNALDOC ====

def check_doc(r, label, found, expected):
    """Translation of check_doc() in 3_check_storage.r: compare signal names to SignalDoc."""
    found, expected = set(found), set(expected)
    if found == expected:
        r('The signals in the following file match SignalDoc.csv!')
        r(label)
    else:
        r.fail(f'signals in {label} do not match SignalDoc.csv')
        r('  in SignalDoc but not in file:', sorted(expected - found))
        r('  in file but not in SignalDoc:', sorted(found - expected))
    r('')


def check_wrds(r, label, found):
    bad = sorted(set(found) & set(WRDS_EXCLUDED))
    if bad:
        r.fail(f'WRDS-excluded signals present in {label}: {bad}')
    else:
        r(f'No WRDS-excluded signals ({", ".join(WRDS_EXCLUDED)}) in {label}')


def wide_signals(path):
    return [c for c in pl.read_parquet_schema(path) if c not in ('permno', 'yyyymm')]


def port_signals(path):
    return pl.scan_parquet(path).select(pl.col('signalname').unique()).collect()['signalname'].to_list()


# ==== PORTFOLIO FULL SETS ====

def check_portfull(path, doc):
    """Mean LS return by sample period for each signal (check_portfull in 3_check_storage.r)."""
    yr = pl.col('date').dt.year()
    ls = (
        pl.scan_parquet(path)
        .filter(pl.col('port') == 'LS')
        .join(
            doc.lazy().select('signalname', 'SampleStartYear', 'SampleEndYear', pl.col('Year').alias('PubYear')),
            on='signalname', how='left',
        )
        .with_columns(
            samptype=pl.when(yr < pl.col('SampleStartYear')).then(pl.lit('before'))
            .when((yr >= pl.col('SampleStartYear')) & (yr <= pl.col('SampleEndYear'))).then(pl.lit('insamp'))
            .when((yr > pl.col('SampleEndYear')) & (yr <= pl.col('PubYear'))).then(pl.lit('between'))
            .when(yr > pl.col('PubYear')).then(pl.lit('postpub'))
        )
        .collect()
    )
    lastyear = str(THIS_YEAR - 1)
    rbar = pl.concat([
        ls.filter(pl.col('samptype').is_not_null()).group_by('signalname', 'samptype').agg(rbar=pl.col('ret').mean()),
        ls.filter(yr >= THIS_YEAR - 5).group_by('signalname').agg(rbar=pl.col('ret').mean())
        .with_columns(samptype=pl.lit('last5years')).select('signalname', 'samptype', 'rbar'),
        ls.filter(yr == THIS_YEAR - 1).group_by('signalname').agg(rbar=pl.col('ret').mean())
        .with_columns(samptype=pl.lit(lastyear)).select('signalname', 'samptype', 'rbar'),
    ])
    wide = rbar.pivot(on='samptype', index='signalname', values='rbar')
    cols = ['before', 'insamp', 'between', 'postpub', 'last5years', lastyear]
    wide = wide.with_columns([pl.lit(None, pl.Float64).alias(c) for c in cols if c not in wide.columns])
    return wide.select('signalname', *cols).sort('signalname')


def check_port_full_sets(out, doc, r):
    r.section('PORTFOLIO FULL SETS')
    base_path = out / OP_DIR / 'PredictorPortsFull.parquet'
    port = pl.read_parquet(base_path)

    r('Count of predictors with long-short returns by month')
    counts = (
        port.filter(
            pl.col('port') == 'LS', pl.col('ret').is_not_null(),
            pl.col('date').dt.month() == 12, pl.col('date').dt.year() >= 2000,
        )
        .group_by('date').agg(n_signals=pl.col('signalname').n_unique())
        .sort('date', descending=True)
    )
    r(counts)
    r('')

    rbarbase = check_portfull(base_path, doc)
    summaries = []
    for path in sorted((out / ALT_DIR).glob('*.parquet')):
        summaries.append(
            check_portfull(path, doc).select(pl.exclude('signalname').mean())
            .with_columns(impname=pl.lit(path.stem))
        )
    summaries.append(rbarbase.select(pl.exclude('signalname').mean()).with_columns(impname=pl.lit('PredictorPortsFull')))
    rbarimp = pl.concat(summaries)

    impname = pl.col('impname')
    rbarimp = (
        rbarimp.with_columns(
            impid=pl.when(impname.str.contains('PredictorPortsFull')).then(1)
            .when(impname.str.contains('HoldPer')).then(2)
            .when(impname.str.contains('LiqScreen')).then(3)
            .when(impname.str.contains('Quintiles')).then(4)
            .when(impname.str.contains('Deciles')).then(5)
            .when(impname.str.contains('FF93style')).then(6),
            impname=impname.str.replace('PredictorAltPorts_', '').str.replace('LiqScreen_', ''),
        )
        .sort('impid', 'impname', nulls_last=True)
        .select('impname', pl.exclude('impname').round(2))
    )
    r('Summary of portfolio full set mean monthly long-short returns')
    r(rbarimp)
    r('')

    r('Predictor signal-level mean monthly long-short returns (OP implementations)')
    r(rbarbase.with_columns(pl.exclude('signalname').round(2)))
    r('')


# ==== SIGNALS ====

def check_signals(out, doc, lists, r):
    r.section('SIGNAL FULL SETS (WIDE PARQUET)')
    firm = out / FIRM_DIR
    for fname, expected in [
        ('Predictors.parquet', lists['predictor_dl']),
        ('signed_predictors_dl_wide.parquet', lists['predictor_dl']),
        ('Placebos.parquet', lists['placebo_dl']),
    ]:
        found = wide_signals(firm / fname)
        check_wrds(r, fname, found)
        check_doc(r, f'{FIRM_DIR}/{fname}', found, expected)

    # signed = sign * unsigned, and both share the same rows
    pred = pl.read_parquet(firm / 'Predictors.parquet')
    signed = pl.read_parquet(firm / 'signed_predictors_dl_wide.parquet')
    if pred.select(KEYS).equals(signed.select(KEYS)):
        r('Predictors.parquet and signed_predictors_dl_wide.parquet have identical permno-yyyymm rows')
        signs = dict(doc.select('signalname', pl.col('Sign').cast(pl.Float64)).iter_rows())
        cols = [c for c in pred.columns if c not in KEYS]
        if set(cols) != set(signed.columns) - set(KEYS):
            r.fail('Predictors.parquet and signed_predictors_dl_wide.parquet have different signal columns')
        else:
            bad = [c for c in cols if not signed[c].eq_missing(pred[c] * signs[c]).all()]
            if bad:
                r.fail(f'signed != Sign * unsigned for {len(bad)} signals: {bad[:10]}')
            else:
                r(f'signed = Sign * unsigned for all {len(cols)} signals')
    else:
        r.fail('Predictors.parquet and signed_predictors_dl_wide.parquet have different rows')
    del pred

    # data availability in signed wide signals (indirect check on everything else)
    for label, df in [('signed_predictors_dl_wide.parquet', signed), ('Placebos.parquet', None)]:
        if df is None:
            df = pl.read_parquet(firm / label)
        obs = df.drop('permno').group_by('yyyymm').agg(pl.all().count())
        widesum = (
            obs.unpivot(index='yyyymm', variable_name='signalname', value_name='obs')
            .filter(pl.col('obs') >= 1)
            .group_by('signalname')
            .agg(
                date_begin=pl.col('yyyymm').min(),
                date_end=pl.col('yyyymm').max(),
                mean_firmobs_per_month=pl.col('obs').mean().floor().cast(pl.Int64),
            )
            .sort('signalname')
        )
        r(f'Downloadable signal data availability summary: {label}')
        r(widesum)
        r('')
        del df


# ==== PORTFOLIO SIGNAL LISTS ====

def check_portfolio_lists(out, lists, r):
    # replaces the Portfolios/Individual folder checks: same source files, same expected lists
    r.section('PORTFOLIO SIGNAL LISTS')
    for rel, expected in [
        (f'{OP_DIR}/PredictorPortsFull.parquet', lists['predictor']),
        (f'{ALT_DIR}/PredictorAltPorts_LiqScreen_VWforce.parquet', lists['predictor']),
        (f'{ALT_DIR}/PredictorAltPorts_Deciles.parquet', lists['predictor_cts']),
        (f'{ALT_DIR}/PredictorAltPorts_DecilesVW.parquet', lists['predictor_cts']),
        (f'{ALT_DIR}/PredictorAltPorts_Quintiles.parquet', lists['predictor_cts']),
        (f'{ALT_DIR}/PredictorAltPorts_QuintilesVW.parquet', lists['predictor_cts']),
    ]:
        check_doc(r, rel, port_signals(out / rel), expected)

    r.section('DAILY PORTFOLIOS')
    for s in DAILY_SETS:
        expected = lists['predictor'] if s.startswith('Predictor') else lists['predictor_cts']
        check_doc(r, f'{DAILY_DIR}/{s}.parquet', port_signals(out / DAILY_DIR / f'{s}.parquet'), expected)


# ==== OLD VS NEW ====

def ols_stats():
    # callers pass complete old/new pairs only, as lm() drops NA rows in the R version
    x, y = pl.col('old_ret'), pl.col('new_ret')
    slope = pl.cov(x, y) / x.var()
    return [
        pl.len().alias('nobs'),
        (y.mean() - slope * x.mean()).alias('intercept'),
        slope.alias('slope'),
        (pl.corr(x, y) ** 2 * 100).alias('rsq'),
        y.mean().alias('new_rbar'),
        x.mean().alias('old_rbar'),
    ]


def check_old_vs_new(out, old_release, doc, r):
    """Translation of 4_old_vs_new_check.R: regress new LS returns on the previous release's."""
    r.section('OLD VS NEW (PredictorPortsFull)')
    # releases up to 2025 shipped csv; ship_1_build.py ships parquet
    old_dir = Path(old_release) / OP_DIR
    candidates = [old_dir / 'PredictorPortsFull.parquet', old_dir / 'PredictorPortsFull.csv']
    old_path = next((p for p in candidates if p.exists()), None)
    if old_path is None:
        r.fail(f'old release file not found: {candidates[0]} (or .csv)')
        return
    r(f'old: {old_path}')

    pad = pl.when(pl.col('port').str.len_chars() == 2).then(pl.col('port')).otherwise('0' + pl.col('port'))
    if old_path.suffix == '.parquet':
        old = pl.read_parquet(old_path, columns=['signalname', 'port', 'date', 'ret'])
    else:
        old = pl.read_csv(
            old_path, schema_overrides={'port': pl.String, 'date': pl.Date, 'ret': pl.Float64}, null_values='NA',
        )
    old = old.select('signalname', pad.alias('port'), 'date', pl.col('ret').cast(pl.Float64).alias('old_ret'))
    new = (
        pl.read_parquet(out / OP_DIR / 'PredictorPortsFull.parquet')
        .select('signalname', pad.alias('port'), 'date', pl.col('ret').alias('new_ret'))
    )
    yr = pl.col('date').dt.year()
    both = (
        old.join(new, on=['signalname', 'port', 'date'], how='inner')
        .filter(pl.col('old_ret').is_finite(), pl.col('new_ret').is_finite())
        .join(
            doc.select('signalname', pl.col('Year').alias('YearPub'), 'SampleStartYear', 'SampleEndYear'),
            on='signalname', how='inner',
        )
        .with_columns(
            samptype=pl.when((pl.col('SampleStartYear') <= yr) & (yr <= pl.col('SampleEndYear'))).then(pl.lit('in-samp'))
            .when(yr > pl.col('YearPub')).then(pl.lit('post-pub'))
        )
    )

    r(f'overlapping signal-port-months with old and new returns: {both.height:,}')
    if both.is_empty():
        r.fail('old and new PredictorPortsFull share no signal-port-months with returns')
        return

    temp1 = both.filter(pl.col('samptype').is_not_null()).group_by('signalname', 'port', 'samptype').agg(ols_stats())
    temp2 = (
        both.filter(yr >= pl.col('SampleStartYear')).group_by('signalname', 'port').agg(ols_stats())
        .with_columns(samptype=pl.lit('full-samp'))
    )
    check = pl.concat([temp1, temp2.select(temp1.columns)]).sort('signalname', 'port', 'samptype')
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    check.write_csv(TEMP_DIR / 'PredictorPortsCheck.csv')
    r(f'Wrote {TEMP_DIR / "PredictorPortsCheck.csv"}')

    check_ls = check.filter(
        pl.col('port') == 'LS', pl.col('samptype').is_not_null(), pl.col('slope').is_not_null(),
        pl.col('slope').is_finite(),
    )
    # every LS signal in both releases needs a usable full-sample regression
    def ls_signals(df, col):
        return set(df.filter(pl.col('port') == 'LS', pl.col(col).is_not_null())['signalname'])
    common = ls_signals(old, 'old_ret') & ls_signals(new, 'new_ret')
    usable = set(check_ls.filter(pl.col('samptype') == 'full-samp', pl.col('nobs') >= 3)['signalname'])
    r(f'LS signals in both releases: {len(common)}; with usable full-sample regressions: {len(common & usable)}')
    if not common:
        r.fail('no long-short signals in common between old and new releases')
    elif common - usable:
        r.fail(f'{len(common - usable)} common LS signals lack a usable full-sample regression: '
               f'{sorted(common - usable)[:10]}')
    r(check_ls.select(
        slope_p05=pl.col('slope').quantile(0.05, 'linear'),
        rsq_p05=pl.col('rsq').quantile(0.05, 'linear'),
    ))
    r('')
    r('Rsq from regressing new long-short OP returns on old')
    r(
        check_ls.group_by('samptype').agg(
            [pl.col('rsq').quantile(q, 'linear').alias(f'p{int(q * 100):02d}') for q in (0.05, 0.10, 0.25, 0.50)]
        ).sort('samptype')
    )
    r('')
    r('Signals with rsq < 98.4: mean abs and mean change in average return')
    r(
        check_ls.filter(pl.col('rsq') < 98.4)
        .with_columns(dret=pl.col('new_rbar') - pl.col('old_rbar'))
        .group_by('samptype')
        .agg(mean_abs_dret=pl.col('dret').abs().mean(), mean_dret=pl.col('dret').mean())
        .sort('samptype')
    )
    r('')
    r('20 signals with lowest Rsq')
    r(
        check_ls.filter(pl.col('samptype') == 'full-samp')
        .select('signalname', 'samptype', 'rsq', 'new_rbar', 'old_rbar')
        .sort('rsq').head(20)
    )


def main(out, old_release):
    out = Path(out)
    if not out.exists():
        raise SystemExit(f'Release folder not found: {out}')
    (out / CHECKS_FILE).unlink(missing_ok=True)

    r = Report()
    r('Checking storage for completeness and basic statistics')
    r(f'release folder: {out}')
    r(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    doc = read_signaldoc()
    lists = doc_lists(doc)

    check_layout(out, r)
    check_source_shipped(out, old_release, r)
    check_port_full_sets(out, doc, r)
    check_signals(out, doc, lists, r)
    check_portfolio_lists(out, lists, r)
    check_old_vs_new(out, old_release, doc, r)

    r.section('SUMMARY')
    if r.failures:
        r('AUTOMATED CHECKS: FAIL')
        for f in r.failures:
            r(f'  - {f}')
    else:
        r(CHECKS_PASS_LINE)

    (out / CHECKS_FILE).write_text('\n'.join(r.lines) + '\n')
    print(f'\nWrote {out / CHECKS_FILE}')
    return not r.failures


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--out', help='release folder (default: out_gdrive in ship_settings.yaml)')
    args = parser.parse_args()
    settings = load_settings()
    ok = main(args.out or settings['out_gdrive'], settings['old_release'])
    sys.exit(0 if ok else 1)
