"""Download CRSP CIZ distribution events with the legacy output schema.

How to run: python3 Signals/pyCode/DataDownloads/CRSPDistributions.py
Inputs: crsp.stkdistributions and the bundled CRSP CIZ-to-SIZ code crosswalk.
  DEBUG_MODE selects all events with 1981 ex-dates.
Outputs: OPENAP_DATA_ROOT/Intermediate/CRSPdistributions.parquet.
"""

import os
import sys

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import DEBUG_MODE
from utils.crsp_distribution_codes import restore_distcd
from utils.debug_mode import log_selection, sql_date_window
from utils.download_paths import intermediate_path
from utils.wrds_connection import get_wrds_engine, release_wrds_engine


OUTPUT_COLUMNS = [
    'permno', 'divamt', 'distcd', 'facshr', 'rcrddt', 'exdt', 'paydt',
    'cd1', 'cd2', 'cd3', 'cd4',
]
KEY = ['permno', 'rcrddt', 'exdt', 'paydt', 'distcd']


def prepare_distributions(source):
    """Restore legacy fields and apply the original event-key deduplication."""
    data = restore_distcd(source)
    data = data.rename(columns={
        'disdivamt': 'divamt', 'disfacshr': 'facshr',
        'disrecorddt': 'rcrddt', 'disexdt': 'exdt', 'dispaydt': 'paydt',
    })
    for column in ('rcrddt', 'exdt', 'paydt'):
        data[column] = pd.to_datetime(data[column])
    # In SIZ, noncash events report zero DIVAMT where CIZ leaves DisDivAmt null.
    data['divamt'] = data['divamt'].fillna(0).astype('float64')
    data['facshr'] = data['facshr'].astype('float64')
    data['permno'] = data['permno'].astype('int64')
    data['distcd'] = data['distcd'].astype('int64')
    data = data.sort_values(KEY + ['disseqnbr'], kind='stable')
    duplicate_count = int(data.duplicated(KEY).sum())
    data = data.drop_duplicates(KEY, keep='first').copy()
    print(f'Removed {duplicate_count} duplicate event keys', flush=True)
    digits = data['distcd'].astype(str).str.zfill(4)
    for position in range(4):
        data[f'cd{position + 1}'] = digits.str[position].astype('int64')
    if data[KEY].duplicated().any():
        raise ValueError('Distribution output contains duplicate event keys.')
    return data[OUTPUT_COLUMNS]


def main():
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
        release_wrds_engine(engine)
    print(f'Downloaded {len(source)} CIZ distribution events', flush=True)
    result = prepare_distributions(source)
    result.to_parquet(intermediate_path('CRSPdistributions.parquet'))
    print(f'Saved {len(result)} distribution events', flush=True)


if __name__ == '__main__':
    main()
