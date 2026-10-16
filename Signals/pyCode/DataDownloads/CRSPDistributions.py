"""Download CRSP CIZ distribution events with the legacy output schema.

How to run: python3 Signals/pyCode/DataDownloads/CRSPDistributions.py
Inputs: crsp.stkdistributions and the bundled CRSP CIZ-to-SIZ code crosswalk.
  DEBUG_MODE selects all events with 1981 ex-dates.
Outputs: OPENAP_DATA_ROOT/Intermediate/CRSPdistributions.parquet.

Use the project Python environment at /opt/venv/projects/openap.
"""

import os
from pathlib import Path
import sys

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import DATA_ROOT, DEBUG_MODE
from utils.debug_mode import log_selection, sql_date_window
from utils.wrds_connection import get_wrds_engine

# Recover legacy distribution codes so signals can identify the same event types.
# The official crosswalk uses these seven flags; literal N/A values are valid codes.
CODE_FIELDS = [
    'distype', 'disfreqtype', 'dispaymenttype', 'disdetailtype',
    'distaxtype', 'disorigcurtype', 'disamountsourcetype',
]
MAP_PATH = Path(__file__).resolve().parents[1] / 'utils/crsp_distribution_code_map.csv'

OUTPUT_COLUMNS = [
    'permno', 'divamt', 'distcd', 'facshr', 'rcrddt', 'exdt', 'paydt',
    'cd1', 'cd2', 'cd3', 'cd4',
]
KEY = ['permno', 'rcrddt', 'exdt', 'paydt', 'distcd']


def prepare_distributions(source):
    """Provide one record per legacy distribution event, with its type and cash amount."""
    mapping = pd.read_csv(MAP_PATH, dtype={field: 'string' for field in CODE_FIELDS},
                          keep_default_na=False)
    if mapping.duplicated(CODE_FIELDS).any():
        raise ValueError('CRSP distribution crosswalk has ambiguous CIZ flag tuples.')
    if source[CODE_FIELDS].isna().any().any():
        raise ValueError('CIZ distribution rows have null code fields.')
    data = source.merge(mapping, on=CODE_FIELDS, how='left', validate='many_to_one',
                        indicator=True, sort=False)
    unknown = data['_merge'] != 'both'
    if unknown.any():
        examples = data.loc[unknown, CODE_FIELDS].drop_duplicates().head(10)
        raise ValueError(f'{unknown.sum()} CIZ distribution rows have unmapped flags:\n'
                         f'{examples.to_string(index=False)}')
    data = data.drop(columns='_merge')
    data = data.rename(columns={
        'disdivamt': 'divamt', 'disfacshr': 'facshr',
        'disrecorddt': 'rcrddt', 'disexdt': 'exdt', 'dispaydt': 'paydt',
    })
    for column in ('rcrddt', 'exdt', 'paydt'):
        data[column] = pd.to_datetime(data[column])
    # Preserve the legacy zero-cash amount for events whose cash amount is missing.
    data['divamt'] = data['divamt'].fillna(0).astype('float64')
    data['facshr'] = data['facshr'].astype('float64')
    data['permno'] = data['permno'].astype('int64')
    data['distcd'] = data['distcd'].astype('int64')
    # Keep the lowest source sequence number when several records describe the same event.
    data = data.sort_values(KEY + ['disseqnbr'], kind='stable')
    duplicate_count = int(data.duplicated(KEY).sum())
    data = data.drop_duplicates(KEY, keep='first').copy()
    print(f'Removed {duplicate_count} duplicate event keys', flush=True)
    # Expose each distribution-code component for downstream event filters.
    digits = data['distcd'].astype(str).str.zfill(4)
    for position in range(4):
        data[f'cd{position + 1}'] = digits.str[position].astype('int64')
    if data[KEY].duplicated().any():
        raise ValueError('Distribution output contains duplicate event keys.')
    return data[OUTPUT_COLUMNS]


def main():
    (DATA_ROOT / 'Intermediate').mkdir(parents=True, exist_ok=True)
    log_selection('CRSPDistributions')
    predicate, params = sql_date_window('d.disexdt', 'events')
    query = f"""
        SELECT d.permno, d.disseqnbr, d.disdivamt, d.disfacshr,
               d.disrecorddt, d.disexdt, d.dispaydt,
               d.distype, d.disfreqtype, d.dispaymenttype, d.disdetailtype,
               d.distaxtype, d.disorigcurtype, d.disamountsourcetype
        FROM crsp.stkdistributions AS d
        WHERE {predicate}
    """
    engine = get_wrds_engine()
    try:
        source = pd.read_sql_query(query, engine, params=params)
        if DEBUG_MODE:
            missing = pd.read_sql_query(
                'SELECT COUNT(*) AS n FROM crsp.stkdistributions WHERE disexdt IS NULL',
                engine).iloc[0]['n']
            print(f'Source events with missing ex-date (outside debug window): {missing}',
                  flush=True)
    finally:
        engine.dispose()
    print(f'Downloaded {len(source)} CIZ distribution events', flush=True)
    result = prepare_distributions(source)
    result.to_parquet(DATA_ROOT / 'Intermediate/CRSPdistributions.parquet')
    print(f'Saved {len(result)} distribution events', flush=True)


if __name__ == '__main__':
    main()
