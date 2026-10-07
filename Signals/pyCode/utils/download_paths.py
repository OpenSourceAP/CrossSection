"""Paths and reusable inputs for the CRSP migration downloads.

How to run: imported by the nine migration DataDownloads scripts and the runner.
Inputs: OPENAP_DATA_ROOT, OPENAP_CRSP_CALENDAR, OPENAP_COMPUSTAT_EXTRACT.
Outputs: absolute paths; output/input directories are created when requested.

OPENAP_DATA_ROOT defaults to Signals/pyData, independent of working directory.
Debug IBES runs require an explicit full keys-only CRSP calendar; a debug
monthlyCRSP file only contains 1981 and cannot supply full linking coverage.
Compustat extracts preserve dataframe dates. The download script saves/reuses
them only when OPENAP_COMPUSTAT_EXTRACT is explicitly set; ordinary standalone
runs query fresh fundamentals rather than reading a previous extract.
Use the same explicit extract path for both Stage 1 runs. Use distinct roots
and extracts for debug and production to avoid reusing a partial fundamentals
history in a production run.
"""

import os
from pathlib import Path

from utils import debug_mode


def data_root() -> Path:
    """Resolve the selected data root without depending on the script's cwd."""
    configured = os.environ.get("OPENAP_DATA_ROOT")
    if configured:
        return Path(configured).expanduser().resolve()
    return Path(__file__).resolve().parents[2] / "pyData"


def intermediate_path(filename: str) -> Path:
    """Return an output filename after ensuring Intermediate exists."""
    directory = data_root() / "Intermediate"
    directory.mkdir(parents=True, exist_ok=True)
    return directory / filename


def crsp_calendar_path() -> Path:
    """Require the separate full calendar for a debug IBES download."""
    configured = os.environ.get("OPENAP_CRSP_CALENDAR")
    if configured:
        path = Path(configured).expanduser().resolve()
    elif debug_mode.DEBUG_MODE:
        raise RuntimeError(
            "Debug IBES requires OPENAP_CRSP_CALENDAR pointing to the full "
            "keys-only (permno, time_avail_m) CRSP calendar."
        )
    else:
        path = data_root() / "Intermediate" / "monthlyCRSP.parquet"
    if not path.is_file():
        raise FileNotFoundError(f"CRSP monthly calendar not found: {path}")
    return path


def compustat_extract_path() -> Path:
    """Return the reusable raw extract location and create its parent directory."""
    configured = os.environ.get("OPENAP_COMPUSTAT_EXTRACT")
    path = (
        Path(configured).expanduser().resolve()
        if configured
        else data_root() / "Inputs" / "CompustatAnnual_raw.parquet"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    return path
