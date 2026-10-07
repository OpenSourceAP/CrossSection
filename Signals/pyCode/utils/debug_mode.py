"""Shared debug selections for data download scripts.

How to run: imported by DataDownloads scripts; set DEBUG_MODE in config.py.
Inputs: configured DEBUG_MODE, SQL date columns, or dataframes with date columns.
Outputs: SQL predicates/parameters, row caps, selected dataframes, and log messages.
No database connections or file writes occur here.

With DEBUG_MODE=True:
- Monthly CRSP: all securities in 1981; retain supporting name/delisting joins.
- Daily CRSP: all securities in January 1981.
- Distributions/acquisitions: all events with 1981 ex-dates. Missing ex-dates
  are counted separately by the scripts; record/payment dates are unrestricted.
- Compustat: only 1981 report dates feed both annual and monthly processing.
  Monthly output keeps 1981 availability months after expansion/deduplication.
  It intentionally omits observations supplied by reports from earlier years.
- Market returns and CCM, IBES, OptionMetrics links: full history. IBES needs
  a full stock-month calendar, supplied separately for Stage 1 (Stage 1.2).

Other converted downloads use DEBUG_ROW_LIMITS below, selected for small smoke
runs: 10,000 source rows for firm panels, 1,000 processed rows for local stock
files, and roughly ten years of rows for daily/monthly factor time series.
SQL limits apply per query (each CIQ ratings table and each short-interest feed);
13F limits source CSV rows; local-file and GNP limits apply after processing.
Processed panel outputs may contain more rows after monthly expansion. These
row samples are smoke tests and do not guarantee matching cross-file coverage
or complete firm histories. SQL samples without ORDER BY are not reproducible.
Broker-dealer leverage retains full history for seasonal/lag calculations.

With DEBUG_MODE=False all selections and row caps are disabled. Calendar starts
are inclusive, ends exclusive. Edit DEBUG_ROW_LIMITS here to tune smoke sizes.
"""

import pandas as pd

from config import DEBUG_MODE

WINDOWS = {
    "monthly": ("1981-01-01", "1982-01-01"),
    "daily": ("1981-01-01", "1981-02-01"),
    "events": ("1981-01-01", "1982-01-01"),
    "annual": ("1981-01-01", "1982-01-01"),
}

# Caps apply only to row-based smoke tests; CRSP calendar/link policies are separate.
DEBUG_ROW_LIMITS = {
    "IBESRecommendations": 10_000,
    "IBESEPSAdjusted": 10_000,
    "IBESEPSUnadjusted": 10_000,
    "IBESUnadjustedActuals": 10_000,
    "CompustatQuarterly": 10_000,
    "CompustatPensions": 10_000,
    "CompustatBusinessSegments": 10_000,
    "CompustatShortInterest": 10_000,
    "CIQCreditRatings": 10_000,
    "SPCreditRatings": 10_000,
    "InstitutionalHoldings13F": 10_000,
    "BidAskSpreads": 1_000,
    "IPODates": 1_000,
    "GovernanceIndex": 1_000,
    "PINData": 1_000,
    "FamaFrenchDaily": 2_520,
    "FamaFrenchMonthly": 120,
    "LiquidityFactor": 120,
    "GNPDeflator": 120,
}

POLICIES = {
    "CRSPMonthly": "1981 stock months, all securities; supporting joins retained",
    "CRSPDaily": "January 1981, all securities",
    "CRSPDistributions": "1981 ex-dates, all events",
    "CRSPAcquisitions": "1981 ex-dates, then existing distinct-child logic",
    "CompustatAnnual": "1981 report dates; monthly output from those reports, in 1981",
    "MarketReturns": "full market-return history",
    "CCMLinkingTable": "full link history",
    "IBESCRSPLink": "full link history and full stock-month calendar required",
    "OptionMetricsCRSPLink": "full link history",
    "BrokerDealerLeverage": "full history for seasonal and lag calculations",
}


def sql_date_window(column, selection):
    """Return a predicate and bound dates; column must be a code-owned SQL name."""
    start, end = WINDOWS[selection]
    if not DEBUG_MODE:
        return "TRUE", {}
    return (
        f"{column} >= %(debug_start)s AND {column} < %(debug_end)s",
        {"debug_start": start, "debug_end": end},
    )


def select_dates(data, column, selection):
    """Select a debug output window without modifying the working dataframe."""
    start, end = WINDOWS[selection]
    if not DEBUG_MODE:
        return data
    dates = pd.to_datetime(data[column])
    return data.loc[(dates >= start) & (dates < end)].copy()


def get_debug_row_limit(script):
    """Return the script's smoke-test cap, or None for a production run."""
    limit = DEBUG_ROW_LIMITS[script]
    return limit if DEBUG_MODE else None


def log_selection(script):
    """Print the active policy once at the beginning of a download."""
    if not DEBUG_MODE:
        policy = "full production output"
    elif script in DEBUG_ROW_LIMITS:
        policy = f"up to {DEBUG_ROW_LIMITS[script]:,} rows per query/read or processed output"
    else:
        policy = POLICIES[script]
    mode = "DEBUG MODE" if DEBUG_MODE else "PRODUCTION MODE"
    print(f"{mode}: {policy}", flush=True)
