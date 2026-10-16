"""Create the central WRDS SQLAlchemy engine used by the CRSP downloads.

How to run: import get_wrds_engine from a DataDownloads script.
Inputs: WRDS_USERNAME and WRDS_PASSWORD environment variables (or pyCode/.env).
Outputs: an engine; the calling script owns its connections and disposes it.
No connection is opened until a query or engine.connect() call is made.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.pool import NullPool


def get_wrds_engine():
    """Create a standalone engine; the caller disposes it after its queries."""
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
