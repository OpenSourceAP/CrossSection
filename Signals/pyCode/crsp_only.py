# ABOUTME: Downloads CRSP and builds the three CRSP predictors, nothing else.
# ABOUTME: For users who download the finished signals and only need CRSP to build portfolios.
"""
crsp_only.py

The public signal zips exclude the three predictors built directly from CRSP
(Price, Size, STreversal) and the portfolio code needs CRSP returns. This script
produces exactly those inputs so Portfolios/Code/master.R can run without the
full signals pipeline. Everything it runs is also part of master.py, and the
outputs are identical.

Usage:
    cd Signals/pyCode
    python crsp_only.py               # monthly and daily CRSP, then Price, Size, STreversal
    python crsp_only.py --skip-daily  # if master.R will run with skipdaily = T

Inputs:
    - .env with WRDS_USERNAME and WRDS_PASSWORD (copy dotenv.template)

Outputs:
    - ../pyData/Intermediate/monthlyCRSP.parquet
    - ../pyData/Intermediate/dailyCRSP.parquet and dailyCRSPprc.parquet (unless --skip-daily)
    - ../pyData/Predictors/Price.csv, Size.csv, STreversal.csv
"""

import argparse
import subprocess
import sys

from utils.pipeline_checks import check_environment, require_pycode_cwd, run_settings

DOWNLOADS = ["DataDownloads/CRSPMonthly.py", "DataDownloads/CRSPDaily.py"]
PREDICTORS = ["Predictors/Price.py", "Predictors/Size.py", "Predictors/STreversal.py"]


def run_script(script):
    """Run one pipeline script in this interpreter, streaming its output."""
    print("\n" + "=" * 60)
    print(f"Running {script}")
    print("=" * 60, flush=True)
    subprocess.run([sys.executable, "-u", script], check=True)
    print(f"✓ {script} completed", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--skip-daily",
        action="store_true",
        help="skip the daily CRSP download (about an hour); use with skipdaily = T in master.R",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("CRSP-only pipeline: CRSP downloads and CRSP predictors")
    print("=" * 60)

    if not require_pycode_cwd():
        sys.exit(1)
    if not check_environment():
        sys.exit(1)
    run_settings()

    scripts = [script for script in DOWNLOADS if not (args.skip_daily and "Daily" in script)]
    scripts += PREDICTORS

    for script in scripts:
        try:
            run_script(script)
        except subprocess.CalledProcessError as error:
            print(f"ERROR in {script}: return code {error.returncode}")
            sys.exit(1)

    print("\n" + "=" * 60)
    print("CRSP-only pipeline completed. You can now run Portfolios/Code/master.R")
    print("=" * 60)


if __name__ == "__main__":
    main()
