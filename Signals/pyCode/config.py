#!/usr/bin/env python3
"""
Global configuration for pyCode DataDownloads scripts.

This file contains configuration settings that control the behavior of
all DataDownloads scripts. It is version controlled and not private.
"""

# Row limit for DataDownloads scripts
# 10 = debug mode (download only 10 rows per query)
# -1 = production mode (download all rows)
MAX_ROWS_DL = 10

# Debug mode flag for additional debugging features
DEBUG_MODE = True

# Timeout for individual DataDownloads scripts (in minutes)
# 10 = 10 minutes (default for production, handles large downloads like ZB_PIN.py)
# 0.5 = 30 seconds (for quick testing, may cause timeouts on large downloads)
# 15 = 15 minutes (for very large downloads or slow connections)
# Used by 01_DownloadData.py orchestrator script
SCRIPT_TIMEOUT_MINUTES = 10

# Additional configuration options can be added here as needed
SAVE_CSV = True  # Whether to save intermediate CSV files
VERBOSE_OUTPUT = True  # Whether to print detailed progress messages