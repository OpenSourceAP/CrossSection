"""WRDS engine creation and an optional single-session download context.

How to run: imported by DataDownloads scripts or temp/dl_crsp_v2.py.
Inputs: WRDS_USERNAME and WRDS_PASSWORD environment variables (or pyCode/.env).
Outputs: a SQLAlchemy engine, or the runner's existing connection; no data files.
The shared context attempts one connection and never retries or reconnects.
"""

from contextlib import contextmanager
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.pool import NullPool

_shared_connection = None


def _new_engine():
    load_dotenv(Path(__file__).resolve().parents[1] / '.env')
    username = os.getenv('WRDS_USERNAME')
    password = os.getenv('WRDS_PASSWORD')
    if not username or not password:
        raise RuntimeError('WRDS_USERNAME and WRDS_PASSWORD must be set.')
    url = URL.create(
        'postgresql+psycopg2', username=username, password=password,
        host='wrds-pgdata.wharton.upenn.edu', port=9737, database='wrds',
    )
    return create_engine(url, poolclass=NullPool, connect_args={'connect_timeout': 30})


def get_wrds_engine():
    """Reuse a runner connection, or return a standalone script's engine."""
    if _shared_connection is not None:
        if _shared_connection.closed or _shared_connection.invalidated:
            raise RuntimeError('The shared WRDS connection was lost; reconnecting requires permission.')
        return _shared_connection
    return _new_engine()


def release_wrds_engine(engine):
    """Leave a shared session open between scripts; dispose standalone engines."""
    if engine is not _shared_connection:
        engine.dispose()


@contextmanager
def shared_wrds_connection():
    """Open one connection, reuse it across downloads, and close it on exit."""
    global _shared_connection
    if _shared_connection is not None:
        raise RuntimeError('A shared WRDS connection is already active.')
    engine = _new_engine()
    try:
        with engine.connect() as connection:
            _shared_connection = connection
            try:
                yield connection
            finally:
                _shared_connection = None
    finally:
        engine.dispose()
