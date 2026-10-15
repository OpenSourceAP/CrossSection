"""Identify child securities from CRSP CIZ distribution events.

How to run: python3 Signals/pyCode/DataDownloads/CRSPAcquisitions.py
Inputs: crsp.stkdistributions. DEBUG_MODE selects 1981 source ex-dates.
Outputs: OPENAP_DATA_ROOT/Intermediate/m_CRSPAcquisitions.parquet.
The output preserves the legacy distinct-child rule, regardless of DISTCD.
"""

import os
import sys

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import DATA_ROOT, DEBUG_MODE
from utils.debug_mode import log_selection, sql_date_window
from utils.wrds_connection import get_wrds_engine


def prepare_acquisitions(source):
    """Apply the legacy ACPERM > 999 rule and keep unique child PERMNOs."""
    rows = source.loc[source['dispermno'].gt(999) & source['disexdt'].notna(),
                      ['dispermno']].copy()
    result = rows.rename(columns={'dispermno': 'permno'}).drop_duplicates()
    result['permno'] = result['permno'].astype('int64')
    result['SpinoffCo'] = 1
    if result.permno.duplicated().any():
        raise ValueError('Acquisition output contains duplicate child PERMNOs.')
    print(f'{len(rows)} qualifying events; {len(result)} distinct child securities',
          flush=True)
    return result[['permno', 'SpinoffCo']]


def main():
    (DATA_ROOT / 'Intermediate').mkdir(parents=True, exist_ok=True)
    log_selection('CRSPAcquisitions')
    predicate, params = sql_date_window('d.disexdt', 'events')
    query = f"""
        SELECT d.disexdt, d.dispermno
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
    result = prepare_acquisitions(source)
    result.to_parquet(DATA_ROOT / 'Intermediate/m_CRSPAcquisitions.parquet', index=False)
    print(f'Saved {len(result)} distinct child securities', flush=True)


if __name__ == '__main__':
    main()
