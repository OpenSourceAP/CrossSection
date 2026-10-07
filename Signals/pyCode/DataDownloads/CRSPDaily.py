# ABOUTME: Downloads regular CRSP CIZ daily stock observations in yearly chunks.
"""Run: python3 Signals/pyCode/DataDownloads/CRSPDaily.py with the project venv.

Inputs: crsp.dsf_v2. DEBUG_MODE selects January 1981; production uses full years
from 1926 through the current year. Delisting-event rows are excluded because
v1 dsf did not contain the separate CIZ delisting return observations.
Outputs: OPENAP_DATA_ROOT/Intermediate/dailyCRSP.parquet and dailyCRSPprc.parquet
(default Signals/pyData). Both retain the v1 column order and units.
Mapping: Signals/tests/crsp_v2/daily_mapping.md.
"""

import os
import sys
from contextlib import nullcontext
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from sqlalchemy.engine import Engine

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import DEBUG_MODE
from utils.debug_mode import log_selection, sql_date_window
from utils.download_paths import intermediate_path
from utils.wrds_connection import get_wrds_engine, release_wrds_engine


FULL_COLUMNS = ['permno', 'time_d', 'ret', 'vol', 'prc', 'cfacpr', 'shrout']
PRICE_COLUMNS = ['permno', 'time_d', 'prc', 'cfacpr', 'shrout']
FULL_SCHEMA = pa.schema([
    ('permno', pa.int32()), ('time_d', pa.timestamp('ns')),
    ('ret', pa.float64()), ('vol', pa.float64()), ('prc', pa.float64()),
    ('cfacpr', pa.float64()), ('shrout', pa.float64()),
])
PRICE_SCHEMA = pa.schema([FULL_SCHEMA.field(c) for c in PRICE_COLUMNS])


def get_crsp_daily_year(year, engine):
    """Fetch regular stock days, preserving native daily return and volume units."""
    if DEBUG_MODE:
        predicate, params = sql_date_window('a.dlycaldt', 'daily')
    else:
        predicate = 'a.dlycaldt >= %(year_start)s AND a.dlycaldt < %(next_year)s'
        params = {'year_start': f'{year}-01-01', 'next_year': f'{year + 1}-01-01'}
    query = f"""
    SELECT a.permno, a.dlycaldt AS time_d, a.dlyret AS ret, a.dlyvol AS vol,
           a.dlyprc AS prc, a.dlyprcflg, a.dlycumfacpr AS cfacpr, a.shrout
    FROM crsp.dsf_v2 AS a
    WHERE a.dlydelflg = 'N' AND {predicate}
    """
    return pd.read_sql_query(query, engine, params=params)


def restore_legacy_daily(data):
    """Restore the v1 price sign and output types without changing CIZ returns."""
    if data.duplicated(['permno', 'time_d']).any():
        raise ValueError('CIZ daily data contain duplicate security-date keys.')
    if data.permno.isna().any() or data.time_d.isna().any():
        raise ValueError('CIZ daily data contain null security-date keys.')
    data = data.copy()
    data['permno'] = data.permno.astype('int32')
    data['time_d'] = pd.to_datetime(data.time_d).dt.floor('D')
    data['prc'] = np.where(data.dlyprcflg.eq('BA'), -data.prc, data.prc)
    for column in ('ret', 'vol', 'prc', 'cfacpr', 'shrout'):
        data[column] = pd.to_numeric(data[column], errors='raise').astype('float64')
    return data[FULL_COLUMNS]


def main():
    log_selection('CRSPDaily')
    years = [1981] if DEBUG_MODE else range(1926, datetime.now().year + 1)
    full_path = intermediate_path('dailyCRSP.parquet')
    price_path = intermediate_path('dailyCRSPprc.parquet')
    full_tmp = Path(str(full_path) + '.tmp')
    price_tmp = Path(str(price_path) + '.tmp')
    engine = get_wrds_engine()
    full_writer = price_writer = None
    total = 0
    try:
        full_writer = pq.ParquetWriter(full_tmp, FULL_SCHEMA)
        price_writer = pq.ParquetWriter(price_tmp, PRICE_SCHEMA)
        # A standalone run opens one session for all yearly queries. A migration
        # runner may already supply its shared SQLAlchemy Connection.
        session = engine.connect() if isinstance(engine, Engine) else nullcontext(engine)
        with session as connection:
            for year in years:
                daily = restore_legacy_daily(get_crsp_daily_year(year, connection))
                if daily.empty:
                    print(f'{year}: no regular observations', flush=True)
                    continue
                full_writer.write_table(pa.Table.from_pandas(daily, schema=FULL_SCHEMA, preserve_index=False))
                price_writer.write_table(pa.Table.from_pandas(
                    daily[PRICE_COLUMNS], schema=PRICE_SCHEMA, preserve_index=False))
                total += len(daily)
                print(f'{year}: {len(daily):,} regular observations', flush=True)
        full_writer.close()
        full_writer = None
        price_writer.close()
        price_writer = None
        full_tmp.replace(full_path)
        price_tmp.replace(price_path)
        print(f'Saved {total:,} daily CRSP rows to both outputs', flush=True)
    finally:
        if full_writer is not None:
            full_writer.close()
        if price_writer is not None:
            price_writer.close()
        full_tmp.unlink(missing_ok=True)
        price_tmp.unlink(missing_ok=True)
        release_wrds_engine(engine)


if __name__ == '__main__':
    main()
