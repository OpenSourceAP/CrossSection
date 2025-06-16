#!/usr/bin/env python3

import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host="wrds-pgdata.wharton.upenn.edu",
    port=9737,
    database="wrds",
    user=os.getenv("WRDS_USERNAME"),
    password=os.getenv("WRDS_PASSWORD")
)

query = """
SELECT a.gvkey, a.conm, a.tic, a.cusip, a.cik, a.sic, a.naics, b.linkprim, 
       b.linktype, b.liid, b.lpermno, b.lpermco, b.linkdt, b.linkenddt
FROM comp.names as a
INNER JOIN crsp.ccmxpf_lnkhist as b
ON a.gvkey = b.gvkey
WHERE b.linktype in ('LC', 'LU')
AND b.linkprim in ('P', 'C')
ORDER BY a.gvkey
"""

ccm_data = pd.read_sql_query(query, conn)
conn.close()

ccm_data = ccm_data.rename(columns={
    'linkdt': 'timelinkstart_d',
    'linkenddt': 'timelinkend_d',
    'lpermno': 'permno'
})

ccm_data.to_csv("CCMLinkingTable.csv", index=False)
ccm_data.to_pickle("CCMLinkingTable.pkl")

print(f"CCM Linking Table downloaded with {len(ccm_data)} records")