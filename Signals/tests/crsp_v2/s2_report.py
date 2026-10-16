#!/usr/bin/env python3
"""Stage 2 review report: summary stats and simple comparisons for one output.

Run: /opt/venv/projects/openap/bin/python3 Signals/tests/crsp_v2/s2_report.py monthlyCRSP
Inputs: baseline (default temp/pyData25) and candidate (default Signals/pyData)
  Intermediate files; keys, loaders, windows and tolerances from compare.py.
Outputs: markdown report printed and saved to candidate/Logs/crsp_v2/s2_<output>.md.
Rows dated after the baseline's last date are counted separately and excluded
from every other statistic. Value checks on matched keys use the full common
range, except outputs in VALUE_WINDOW, which use their Stage 1 window.
No WRDS connections.
"""

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from compare import KEYS, TOLERANCES, WINDOWS, load  # noqa: E402

REPO = Path(__file__).resolve().parents[3]
DATE = {
    'monthlyCRSP': 'time_avail_m', 'dailyCRSP': 'time_d', 'dailyCRSPprc': 'time_d',
    'CRSPdistributions': 'exdt', 'm_CRSPAcquisitions': None, 'monthlyMarket': 'time_avail_m',
    'CCMLinkingTable': 'timeLinkStart_d', 'CompustatAnnual': 'datadate', 'a_aCompustat': 'datadate',
    'm_aCompustat': 'time_avail_m', 'IBESCRSPLinkingTable': 'time_avail_m',
    'OPTIONMETRICSCRSPLinkingTable': 'sdate',
}
VALUE_WINDOW = {'dailyCRSP', 'dailyCRSPprc'}
# Columns for the means-by-decade table; default is every numeric column.
MAIN = {'monthlyCRSP': ['ret', 'retx', 'vol', 'shrout', 'prc', 'mve_c'],
        'dailyCRSP': ['ret', 'vol', 'prc', 'shrout'], 'dailyCRSPprc': ['prc', 'shrout'],
        'CompustatAnnual': ['at', 'sale', 'ceq', 'ib'], 'a_aCompustat': ['at', 'sale', 'ceq', 'ib'],
        'm_aCompustat': ['at', 'sale', 'ceq', 'ib']}


def fmt(x):
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return ''
    if isinstance(x, (int, np.integer)) or (isinstance(x, float) and x.is_integer() and abs(x) >= 1e4):
        return f'{x:,.0f}'
    return f'{x:.4g}'


def table(df):
    cols = [str(c) for c in df.columns]
    lines = ['| ' + ' | '.join([''] + cols) + ' |', '|' + '---|' * (len(cols) + 1)]
    for idx, row in df.iterrows():
        lines.append('| ' + ' | '.join([str(idx)] + [fmt(v) if not isinstance(v, str) else v for v in row]) + ' |')
    return '\n'.join(lines)


def numeric(df, keys):
    return [c for c in df.columns if c not in keys and pd.api.types.is_numeric_dtype(df[c])]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', choices=list(KEYS))
    parser.add_argument('--baseline', type=Path, default=REPO / 'temp/pyData25')
    parser.add_argument('--candidate', type=Path, default=REPO / 'Signals/pyData')
    args = parser.parse_args()
    name, keys, date = args.output, KEYS[args.output], DATE[args.output]
    old, new = load(args.baseline, name), load(args.candidate, name)
    out = [f'# Stage 2 review: {name}', '',
           f'Baseline `{args.baseline.relative_to(REPO)}`, candidate `{args.candidate.relative_to(REPO)}`. Key: `{", ".join(keys)}`.', '']

    for label, df in (('baseline', old), ('candidate', new)):
        dup = int(df.duplicated(keys).sum())
        if dup:
            raise ValueError(f'{label} has {dup} duplicate keys; resolve before comparing.')

    # Restrict to the baseline's coverage; report later candidate rows separately.
    if date:
        cutoff = old[date].max()
        later = new[new[date] > cutoff]
        new = new[~(new[date] > cutoff)]
        out += [f'Baseline coverage: {old[date].min():%Y-%m-%d} to {cutoff:%Y-%m-%d}. '
                f'Candidate rows after it (excluded below): {len(later):,}'
                + (f', {later[date].min():%Y-%m-%d} to {later[date].max():%Y-%m-%d}.' if len(later) else '.'), '']

    # 1. Summary statistics.
    out += ['## 1. Summary statistics', '',
            table(pd.DataFrame({'baseline': [len(old)], 'candidate': [len(new)]}, index=['rows'])), '']
    cols = [c for c in old.columns if c in new.columns]
    miss = pd.DataFrame({'baseline %': old[cols].isna().mean() * 100, 'candidate %': new[cols].isna().mean() * 100})
    miss = miss[(miss.sum(axis=1) > 0)]
    out += ['Missing values (columns with any):', '', table(miss) if len(miss) else 'None.', '']
    rows = []
    for c in numeric(old, keys):
        if c not in new.columns:
            continue
        for label, s in (('base', old[c]), ('cand', new[c])):
            s = s.astype(float)
            rows.append(pd.Series({'mean': s.mean(), 'sd': s.std(), 'p1': s.quantile(.01), 'p50': s.median(),
                                   'p99': s.quantile(.99)}, name=f'{c} {label}'))
    if rows:
        out += ['Distributions:', '', table(pd.DataFrame(rows)), '']

    # 2. Key coverage by decade (or overall when undated).
    j = old[keys].merge(new[keys], on=keys, how='outer', indicator=True)
    j['_merge'] = j['_merge'].map({'both': 'matched', 'left_only': 'baseline only', 'right_only': 'candidate only'})
    # Undated rows get their own row instead of being dropped by crosstab.
    group = ((j[date].dt.year // 10 * 10).astype('Int64').astype(str).replace('<NA>', 'no date').rename('decade')
             if date else pd.Series('all', index=j.index, name=''))
    cov = pd.crosstab(group, j['_merge']).reindex(columns=['matched', 'baseline only', 'candidate only'], fill_value=0)
    cov.loc['total'] = cov.sum()
    out += ['## 2. Key coverage', '', table(cov), '']

    # Means by decade on each version, for the numeric columns.
    if date:
        num = [c for c in MAIN.get(name, numeric(old, keys)) if c in new.columns]
        means = pd.concat({lab: df.groupby((df[date].dt.year // 10 * 10).astype('Int64'))[num].mean()
                           for lab, df in (('base', old), ('cand', new))}, axis=1)
        means.columns = [f'{c} {lab}' for lab, c in means.columns]
        means = means[[f'{c} {lab}' for c in num for lab in ('base', 'cand')]]
        means.index.name = 'decade'
        out += ['Means by decade:', '', table(means), '']

    # 3. Value agreement on matched keys.
    o, n = old, new
    scope = 'all matched keys'
    if name in VALUE_WINDOW:
        o, n = (df.loc[(df[WINDOWS[name][0]] >= WINDOWS[name][1]) & (df[WINDOWS[name][0]] < WINDOWS[name][2])]
                for df in (old, new))
        scope = f'matched keys in {WINDOWS[name][1]} to {WINDOWS[name][2]}'
    m = o.merge(n, on=keys, how='inner', suffixes=('_b', '_c'), validate='one_to_one')
    rows = {}
    for c in [c for c in cols if c not in keys]:
        b, d = m[c + '_b'], m[c + '_c']
        both = b.notna() & d.notna()
        if pd.api.types.is_numeric_dtype(b) and pd.api.types.is_numeric_dtype(d):
            atol, rtol = TOLERANCES.get(c, (0, 0))
            eq = pd.Series(False, index=m.index)
            eq[both] = np.isclose(d[both].astype(float), b[both].astype(float), atol=atol, rtol=rtol)
            maxdiff = float((d[both] - b[both]).abs().max()) if both.any() else None
        else:
            eq, maxdiff = (b == d).fillna(False), None
        differ = ~eq & both
        rows[c] = {'differ %': differ.mean() * 100, 'max abs diff': maxdiff,
                   'missing→present': int((b.isna() & d.notna()).sum()),
                   'present→missing': int((b.notna() & d.isna()).sum())}
    out += [f'## 3. Value agreement ({scope}: {len(m):,} rows)', '',
            'Numeric columns use the Stage 1 tolerances; others require equality.', '',
            table(pd.DataFrame(rows).T), '']

    text = '\n'.join(out)
    path = args.candidate / 'Logs/crsp_v2' / f's2_{name}.md'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    print(text)


if __name__ == '__main__':
    main()
