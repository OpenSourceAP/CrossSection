# ABOUTME: Enterprise book-to-market (EBM) and BP minus EBM (BPEBM) predictors
# ABOUTME: Usage: python3 ZZ1_EBM_BPEBM.py (run from pyCode/ directory)

import polars as pl
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from savepredictor import save_predictor

# DATA LOAD
# Line 3: use gvkey permno time_avail_m che dltt dlc dc dvpa tstkp ceq using "$pathDataIntermediate/m_aCompustat", clear
df = pl.read_parquet("../pyData/Intermediate/m_aCompustat.parquet").select([
    "gvkey", "permno", "time_avail_m", "che", "dltt", "dlc", "dc", "dvpa", "tstkp", "ceq"
])

# Line 4: bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
df = df.group_by(["permno", "time_avail_m"]).first()

# Line 5: merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(using match) nogenerate keepusing(mve_c)
signal_master = pl.read_parquet("../pyData/Intermediate/SignalMasterTable.parquet").select([
    "permno", "time_avail_m", "mve_c"
])
df = df.join(signal_master, on=["permno", "time_avail_m"], how="inner")

# Line 6: xtset permno time_avail_m (sort data by permno and time)
df = df.sort(["permno", "time_avail_m"])

# SIGNAL CONSTRUCTION
# Line 8: gen temp = che - dltt - dlc - dc - dvpa + tstkp
df = df.with_columns([
    (pl.col("che") - pl.col("dltt") - pl.col("dlc") - pl.col("dc") - pl.col("dvpa") + pl.col("tstkp")).alias("temp")
])

# Line 9: gen EBM = (ceq + temp)/(mve_c + temp)
df = df.with_columns([
    ((pl.col("ceq") + pl.col("temp")) / (pl.col("mve_c") + pl.col("temp"))).alias("EBM")
])

# Line 10: gen BP = (ceq + tstkp - dvpa)/mve_c
df = df.with_columns([
    ((pl.col("ceq") + pl.col("tstkp") - pl.col("dvpa")) / pl.col("mve_c")).alias("BP")
])

# Line 11: gen BPEBM = BP - EBM
df = df.with_columns([
    (pl.col("BP") - pl.col("EBM")).alias("BPEBM")
])

# SAVE
# Line 16: do "$pathCode/savepredictor" EBM
ebm_result = df.select(["permno", "time_avail_m", "EBM"])
save_predictor(ebm_result, "EBM")

# Line 17: do "$pathCode/savepredictor" BPEBM
bpebm_result = df.select(["permno", "time_avail_m", "BPEBM"])
save_predictor(bpebm_result, "BPEBM")