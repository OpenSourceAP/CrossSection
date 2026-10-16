#!/usr/bin/env python3
"""
Global configuration for pyCode DataDownloads scripts.

This file contains configuration settings that control the behavior of
the DataDownloads scripts. It is version controlled and not private.

How to run: imported by the download scripts.
Inputs: optional OPENAP_DATA_ROOT environment variable.
Outputs: configuration constants; no file writes.
"""

import os
from pathlib import Path

# Resolve output paths independently of the working directory. Set the environment
# override before importing config, using separate roots for debug and production.
DATA_ROOT = (
    Path(os.environ['OPENAP_DATA_ROOT']).expanduser().resolve()
    if os.environ.get('OPENAP_DATA_ROOT')
    else Path(__file__).resolve().parents[1] / 'pyData'
)

# Debug selections for DataDownloads scripts.
# True = debug selections documented in utils/debug_mode.py
# False = full production output
DEBUG_MODE = False

# Timeout for individual DataDownloads scripts (in minutes)
# 60 = 60 minutes (default for production, handles large downloads like J_CRSPdaily.py)
# 0.5 = 30 seconds (for quick testing, may cause timeouts on large downloads)
# Used by 01_DownloadData.py orchestrator script
SCRIPT_TIMEOUT_MINUTES = 60

# Patch Option Metrics Implied Vol signals
# https://github.com/OpenSourceAP/CrossSection/issues/156
PATCH_OPTIONM_IV = True