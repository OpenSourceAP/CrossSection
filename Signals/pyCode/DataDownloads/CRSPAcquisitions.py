"""Identify child securities from CRSP CIZ distribution events.

How to run: python3 Signals/pyCode/DataDownloads/CRSPAcquisitions.py
Inputs: crsp.stkdistributions. DEBUG_MODE selects 1981 source ex-dates.
Outputs: OPENAP_DATA_ROOT/Intermediate/m_CRSPAcquisitions.parquet.
The output preserves the legacy distinct-child rule, regardless of DISTCD.

Use the project Python environment at /opt/venv/projects/openap.
"""

import os
import sys

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import DATA_ROOT, DEBUG_MODE
from utils.debug_mode import log_selection, sql_date_window
from utils.wrds_connection import get_wrds_engine


def prepare_acquisitions(source):
    """Flag distinct child securities, retaining the legacy identifier cutoff."""
    is_qualifying_child = (source['dispermno'] > 999) & source['disexdt'].notna()
    rows = source.loc[is_qualifying_child, ['dispermno']].copy()
    result = rows.rename(columns={'dispermno': 'permno'})
    result = result.drop_duplicates()
    result['permno'] = result['permno'].astype('int64')
    # Mark each qualifying child security once, regardless of its number of events.
    result['SpinoffCo'] = 1
    if result['permno'].duplicated().any():
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
