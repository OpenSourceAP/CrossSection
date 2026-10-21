# ABOUTME: Loads 2023-vintage OptionMetrics signals from Google Drive (issue #156)
# ABOUTME: Replaces openassetpricing downloads, which now hit Drive's anonymous quota

"""
optionm_patch.py

Usage:
    Run from [Repo-Root]/Signals/pyCode/

    from utils.optionm_patch import load_optionm_patch
    df = load_optionm_patch("CPVolSpread")

Inputs:
    - Open AP 2023 release CSV for the signal, downloaded with
      utils/gdrive_download.R (needs R googledrive and a cached login from
      an interactive `source("gdrive_login.R")`)

Outputs:
    - Polars DataFrame with columns [permno, time_avail_m, <signal>], where
      time_avail_m is yyyymm as Int32
    - Temporary ../pyData/temp/optionm2023_<signal>.csv, deleted after loading
    - On any failure: prints a WARNING and exits with status 1
"""

import shutil
import subprocess
import sys
from pathlib import Path

import polars as pl

# Google Drive file ids of the signal CSVs in the frozen 2023 release
OPTIONM_2023_IDS = {
    "CPVolSpread": "1FQZ1t7B5A8Ei48io6daobimtZ_0dB5Z8",
    "dCPVolSpread": "1FwvkI9Xq-9wqMyeASaEK0f1RzXMJa_-z",
    "dVolCall": "1FrUpLR1np4-reMJR7zQgiS7URxYIvNAM",
    "dVolPut": "1FWs3z--o_vfeyPimQcJxbtiPh-Dwd-iV",
    "skew1": "1HgLi4R0BdPtHZwAQ6Mwjuy7xTMvciGCH",
    "SmileSlope": "1HiSPX09VrJIRLwT8CAagW3mZW9sTlBik",
    "RIVolSpread": "1HU3buvLyjqRSnvHZGi7YU0mcA6Xq4DEO",
}

DOWNLOAD_SCRIPT = Path(__file__).resolve().parent / "gdrive_download.R"


def _fail(signal: str, reason: str):
    """Print the login instructions and exit non-zero."""
    print(f"WARNING: could not download 2023 vintage of {signal}: {reason}")
    print("See https://github.com/OpenSourceAP/CrossSection/issues/156")
    print('Log in once: from Signals/pyCode/, start R and run source("gdrive_login.R")')
    sys.exit(1)


def load_optionm_patch(signal: str) -> pl.DataFrame:
    """Download the 2023-vintage signal via utils/gdrive_download.R and
    return it with columns permno, time_avail_m, <signal>."""
    if shutil.which("Rscript") is None:
        _fail(signal, "Rscript not found on PATH")

    dest = Path("../pyData/temp") / f"optionm2023_{signal}.csv"
    dest.parent.mkdir(parents=True, exist_ok=True)

    result = subprocess.run(
        ["Rscript", str(DOWNLOAD_SCRIPT), OPTIONM_2023_IDS[signal], str(dest)],
        check=False,
    )
    if result.returncode != 0 or not dest.exists():
        _fail(signal, f"utils/gdrive_download.R exited with status {result.returncode}")

    # Drive returns an HTML page (e.g. "Quota exceeded") instead of the CSV on some errors
    with open(dest, "rb") as f:
        if f.read(1) == b"<":
            dest.unlink()
            _fail(signal, "Google Drive returned an HTML page instead of the CSV")

    # Match openassetpricing's dl_signal (signed=False): Int32 ids, no sign flip
    df = pl.read_csv(dest).with_columns(
        pl.col("permno").cast(pl.Int32), pl.col("yyyymm").cast(pl.Int32)
    )
    dest.unlink()
    return df.rename({"yyyymm": "time_avail_m"}).select(["permno", "time_avail_m", signal])
