# ABOUTME: OPLeverage.py - Operating Leverage predictor calculation
# ABOUTME: Calculates Operating Leverage predictor using polars

"""
OPLeverage.py

Operating Leverage predictor calculation

Usage: python3 OPLeverage.py
Inputs: ../pyData/Intermediate/m_aCompustat.parquet
Outputs: ../pyData/Predictors/OPLeverage.csv

Operating Leverage = (tempxsga + cogs) / at
where tempxsga = 0 if xsga is missing, else xsga

Calculation:
- Sets missing SGA expenses to zero
- Operating Leverage = (SGA expenses + COGS) / Total Assets
"""

import polars as pl
from pathlib import Path
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.save_standardized import save_predictor

# DATA LOAD
print("Loading m_aCompustat data...")
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet")

# Select only the columns we need
df = df.select(['gvkey', 'permno', 'time_avail_m', 'xsga', 'cogs', 'at'])

print(f"Loaded {len(df)} observations")

# SIGNAL CONSTRUCTION
# Remove duplicate permno-time_avail_m observations
df = df.group_by(['permno', 'time_avail_m']).first()
print(f"After removing duplicates: {len(df)} observations")

# Set missing SGA expenses to zero
df = df.with_columns([
    pl.when(pl.col('xsga').is_null()).then(0).otherwise(pl.col('xsga')).alias('tempxsga')
])

# Calculate operating leverage: (SGA + COGS) / Total Assets
df = df.with_columns([
    ((pl.col('tempxsga') + pl.col('cogs')) / pl.col('at')).alias('OPLeverage')
])

print(f"Calculated OPLeverage for {df.filter(pl.col('OPLeverage').is_not_null()).count()} observations")

# SAVE  
save_predictor(df, 'OPLeverage')

print("OPLeverage predictor completed successfully")