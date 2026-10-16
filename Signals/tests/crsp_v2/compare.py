#!/usr/bin/env python3
"""Compare selected migration outputs against the frozen v1 baseline.

Run: python3 Signals/tests/crsp_v2/compare.py monthlyCRSP --candidate Signals/pyData-v2
Inputs: baseline/candidate Intermediate files, keys/windows/tolerances below.
Outputs: JSON column/coverage summary, complete key inventories, unmatched keys,
  duplicate-key reports and bounded mismatch examples under candidate/Logs/crsp_v2.
No WRDS connections. Selections apply independently before an outer key join.
Exit 0 means report generated, not that all differences have been resolved.
"""

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[3]
KEYS = {
    'monthlyCRSP': ['permno', 'time_avail_m'],
    'dailyCRSP': ['permno', 'time_d'],
    'dailyCRSPprc': ['permno', 'time_d'],
    'CRSPdistributions': ['permno', 'rcrddt', 'exdt', 'paydt', 'distcd'],
    'm_CRSPAcquisitions': ['permno'],
    'monthlyMarket': ['time_avail_m'],
    'CCMLinkingTable': ['gvkey', 'permno', 'permco', 'liid', 'linktype', 'linkprim', 'timeLinkStart_d'],
    'CompustatAnnual': ['gvkey', 'datadate'],
    'a_aCompustat': ['gvkey', 'permno', 'datadate'],
    'm_aCompustat': ['permno', 'time_avail_m'],
    'IBESCRSPLinkingTable': ['permno', 'time_avail_m'],
    'OPTIONMETRICSCRSPLinkingTable': ['secid', 'permno', 'sdate'],
}
WINDOWS = {
    'monthlyCRSP': ('time_avail_m', '1981-01-01', '1982-01-01'),
    'dailyCRSP': ('time_d', '1981-01-01', '1981-02-01'),
    'dailyCRSPprc': ('time_d', '1981-01-01', '1981-02-01'),
    'CRSPdistributions': ('exdt', '1981-01-01', '1982-01-01'),
    'CompustatAnnual': ('datadate', '1981-01-01', '1982-01-01'),
    'a_aCompustat': ('datadate', '1981-01-01', '1982-01-01'),
    'm_aCompustat': ('time_avail_m', '1981-01-01', '1982-01-01'),
}
# Fixed before comparisons: (absolute, relative), np.isclose(candidate, baseline).
# Identifiers, classifications, dates and strings require exact equality.
TOLERANCES = {
    'ret': (1e-7, 1e-7), 'retx': (1e-7, 1e-7), 'ret_b4_dl': (1e-7, 1e-7),
    'prc': (1e-6, 1e-8), 'bidlo': (1e-6, 1e-8), 'askhi': (1e-6, 1e-8),
    'cfacshr': (1e-7, 1e-8), 'cfacpr': (1e-7, 1e-8),
    'vol': (1e-6, 1e-8), 'shrout': (1e-8, 1e-8),
    'mve_c': (1e-6, 1e-8), 'mve_permco': (1e-6, 1e-8),
}


def factor_diagnostics(matched, column, keys, raw_mismatch, out, name):
    """Compare within-PERMNO trajectories without changing the raw diagnostics.

    Anchor each vintage to its own factor on the earliest common positive,
    finite date. The rebased comparison uses the existing numeric tolerances,
    now in units of each anchor. Null/nonpositive factors are not normalized.
    A constant ratio is consistent with vintage normalization, not proof of it.
    """
    old = pd.to_numeric(matched[column+'_v1']).astype(float)
    new = pd.to_numeric(matched[column+'_v2']).astype(float)
    eligible = old.gt(0) & new.gt(0) & np.isfinite(old) & np.isfinite(new)
    anchor_rows = matched.loc[eligible].sort_values(keys).drop_duplicates('permno')
    anchors = anchor_rows[keys+[column+'_v1', column+'_v2']].copy()
    anchors['candidate_to_baseline_ratio'] = (
        anchors[column+'_v2'] / anchors[column+'_v1'])
    anchors.to_parquet(out / f'{name}_{column}_normalization_anchors.parquet', index=False)
    by_permno = anchors.set_index('permno')
    old_anchor = matched.permno.map(by_permno[column+'_v1']).astype(float)
    new_anchor = matched.permno.map(by_permno[column+'_v2']).astype(float)
    old_rebased, new_rebased = old / old_anchor, new / new_anchor
    atol, rtol = TOLERANCES[column]
    rebased_equal = pd.Series(False, index=matched.index)
    rebased_equal.loc[eligible] = np.isclose(
        new_rebased[eligible], old_rebased[eligible], atol=atol, rtol=rtol)
    ratio_relative_to_anchor = (new / old) / (new_anchor / old_anchor)
    ratio_equal = pd.Series(False, index=matched.index)
    ratio_equal.loc[eligible] = np.isclose(
        ratio_relative_to_anchor[eligible], 1.0, atol=atol, rtol=rtol)
    difference = (new_rebased[eligible] - old_rebased[eligible]).abs()
    explained = eligible & raw_mismatch & rebased_equal
    remaining = eligible & ~rebased_equal
    both_present = old.notna() & new.notna()
    details = {
        'interpretation': 'Constant within-PERMNO scaling is consistent with vintage normalization; raw differences remain diagnostics.',
        'anchor': 'Earliest selected common date with finite positive factors in both vintages, separately for each PERMNO.',
        'tolerance': {'absolute': atol, 'relative': rtol, 'units': 'Factors divided by their own vintage anchor; unchanged numeric tolerances.'},
        'anchor_permnos': len(anchors),
        'permnos_with_only_one_comparable_date': int((matched.loc[eligible].groupby('permno').size() == 1).sum()),
        'comparable_positive_rows': int(eligible.sum()),
        'raw_value_mismatches_consistent_with_normalization': int(explained.sum()),
        'remaining_rebased_value_mismatches': int(remaining.sum()),
        'remaining_raw_value_mismatches_after_rebasing': int((eligible & raw_mismatch & ~rebased_equal).sum()),
        'rebased_mismatches_with_raw_values_equal': int((eligible & ~raw_mismatch & ~rebased_equal).sum()),
        'ratio_changes_relative_to_anchor': int((eligible & ~ratio_equal).sum()),
        'present_rows_not_normalized': int((both_present & ~eligible).sum()),
        'raw_mismatches_not_normalized': int((raw_mismatch & both_present & ~eligible).sum()),
        'missing_to_present': int((old.isna() & new.notna()).sum()),
        'present_to_missing': int((old.notna() & new.isna()).sum()),
        'both_missing': int((old.isna() & new.isna()).sum()),
        'p99_rebased_absolute_difference': float(difference.quantile(.99)) if len(difference) else None,
        'maximum_rebased_absolute_difference': float(difference.max()) if len(difference) else None,
    }
    if remaining.any():
        examples = matched.loc[remaining, keys+[column+'_v1', column+'_v2']].copy()
        examples['baseline_rebased'] = old_rebased[remaining]
        examples['candidate_rebased'] = new_rebased[remaining]
        examples['ratio_relative_to_anchor'] = ratio_relative_to_anchor[remaining]
        examples.head(100).to_csv(out / f'{name}_{column}_rebased_examples.csv', index=False)
    return details


def load(root, name):
    path = root / 'Intermediate' / (name + ('.csv' if name == 'CompustatAnnual' else '.parquet'))
    data = pd.read_csv(path) if path.suffix == '.csv' else pd.read_parquet(path)
    for column in data.columns:
        if column in ('datadate', 'exdt', 'rcrddt', 'paydt', 'sdate', 'edate') or column.startswith('time'):
            data[column] = pd.to_datetime(data[column], format='%d%b%Y' if path.suffix == '.csv' and column == 'datadate' else None)
    return data


def select(data, name):
    if name not in WINDOWS:
        return data
    column, start, end = WINDOWS[name]
    return data.loc[(data[column] >= start) & (data[column] < end)].copy()


def compare(name, baseline, candidate, out):
    out.mkdir(parents=True, exist_ok=True)
    left, right = load(baseline, name), load(candidate, name)
    report = {'output': name, 'baseline_rows_full': len(left), 'candidate_rows_full': len(right),
              'baseline_schema': {c: str(t) for c, t in left.dtypes.items()},
              'candidate_schema': {c: str(t) for c, t in right.dtypes.items()},
              'columns_only_baseline': sorted(set(left)-set(right)),
              'columns_only_candidate': sorted(set(right)-set(left)),
              'dtype_differences': {c: [str(left[c].dtype), str(right[c].dtype)] for c in set(left)&set(right)
                                    if str(left[c].dtype) != str(right[c].dtype)}}
    left, right = select(left, name), select(right, name)
    keys = KEYS[name]
    for label, data in [('baseline', left), ('candidate', right)]:
        data[keys].to_parquet(out / f'{name}_{label}_keys.parquet', index=False)
        duplicates = data.loc[data.duplicated(keys, keep=False)]
        if len(duplicates):
            duplicates.to_parquet(out / f'{name}_{label}_duplicate_keys.parquet', index=False)
            raise ValueError(f'{name}: {len(duplicates)} rows have duplicate {label} keys; resolve before joining.')
    joined = left.merge(right, on=keys, how='outer', indicator=True, suffixes=('_v1','_v2'), validate='one_to_one')
    # Pandas explicitly matches null key components; they stay in the inventories.
    report['coverage'] = joined._merge.value_counts().to_dict()
    joined.loc[joined._merge != 'both', keys+['_merge']].to_parquet(out / f'{name}_unmatched_keys.parquet', index=False)
    matched = joined.loc[joined._merge == 'both']
    report['columns'] = {}
    for column in sorted((set(left)&set(right))-set(keys)):
        old, new = matched[column+'_v1'], matched[column+'_v2']
        both_present = old.notna() & new.notna()
        both_missing = old.isna() & new.isna()
        details = {'missing_to_present': int((old.isna() & new.notna()).sum()),
                   'present_to_missing': int((old.notna() & new.isna()).sum()),
                   'both_missing': int(both_missing.sum())}
        if pd.api.types.is_numeric_dtype(old) and pd.api.types.is_numeric_dtype(new):
            atol, rtol = TOLERANCES.get(column, (0,0))
            details['tolerance'] = {'absolute':atol,'relative':rtol}
            difference = (new[both_present]-old[both_present]).abs().astype(float)
            equal = pd.Series(False,index=matched.index)
            equal.loc[both_present] = np.isclose(new[both_present].astype(float),old[both_present].astype(float),atol=atol,rtol=rtol)
            details['p99_absolute_difference'] = float(difference.quantile(.99)) if len(difference) else None
            details['maximum_absolute_difference'] = float(difference.max()) if len(difference) else None
        else:
            equal = (old == new).fillna(False)
        mismatch = ~(equal | both_missing)
        details['mismatches'] = int(mismatch.sum())
        details['mismatch_percent'] = float(mismatch.mean()*100) if len(matched) else None
        if column in ('cfacshr', 'cfacpr') and 'permno' in keys:
            details['raw_comparison_role'] = 'Diagnostic: cumulative factors can differ by vintage normalization.'
            details['within_permno_normalization'] = factor_diagnostics(
                matched, column, keys, mismatch, out, name)
        report['columns'][column] = details
        if mismatch.any():
            matched.loc[mismatch, keys+[column+'_v1',column+'_v2']].head(100).to_csv(out / f'{name}_{column}_examples.csv',index=False)
    (out / f'{name}_comparison.json').write_text(json.dumps(report, indent=2)+'\n')
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output',choices=list(KEYS))
    parser.add_argument('--baseline',type=Path,default=REPO/'Signals/pyData-v1')
    parser.add_argument('--candidate',type=Path,default=REPO/'Signals/pyData-v2')
    args=parser.parse_args()
    report=compare(args.output,args.baseline,args.candidate,args.candidate/'Logs/crsp_v2')
    print(json.dumps({'output':args.output,'coverage':report['coverage'],'dtype_differences':report['dtype_differences'],
                      'mismatch_percent':{c:d['mismatch_percent'] for c,d in report['columns'].items()},
                      'factor_diagnostics':{c:{'raw_comparison_role':d['raw_comparison_role'],
                                               'within_permno_normalization':d['within_permno_normalization']}
                                            for c,d in report['columns'].items() if 'raw_comparison_role' in d}},indent=2))


if __name__=='__main__':
    main()
