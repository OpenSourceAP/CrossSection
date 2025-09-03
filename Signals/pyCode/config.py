#!/usr/bin/env python3
"""
Global configuration for pyCode DataDownloads scripts.

This file contains configuration settings that control the behavior of
all DataDownloads scripts. It is version controlled and not private.
"""

# Row limit for DataDownloads scripts
# 1000 = debug mode (download only 1000 rows per query)
# -1 = production mode (download all rows)
MAX_ROWS_DL = -1

# Timeout for individual DataDownloads scripts (in minutes)
# 60 = 60 minutes (default for production, handles large downloads like J_CRSPdaily.py)
# 0.5 = 30 seconds (for quick testing, may cause timeouts on large downloads)
# Used by 01_DownloadData.py orchestrator script
SCRIPT_TIMEOUT_MINUTES = 60

# Patch Option Metrics Implied Vol signals
# https://github.com/OpenSourceAP/CrossSection/issues/156
PATCH_OPTIONM_IV = True 