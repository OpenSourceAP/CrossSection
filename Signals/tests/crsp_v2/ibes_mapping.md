# IBES–CRSP link mapping and Stage 1 comparison

`IBESCRSPLink.py` expands historical I/B/E/S–PERMNO intervals over a full
stock-month calendar. Its output is `IBESCRSPLinkingTable.parquet`; the key is
`(permno, time_avail_m)`. The script keeps the legacy interval rule: both
`sdate` and `edate` are converted to months, then **one month is subtracted from
`edate`**; the resulting monthly bounds are inclusive. When intervals overlap,
the lowest `score` wins. This rule is retained pending a separate sample decision.

## Inputs and column rules

WRDS metadata inspected on 2026-10-07 showed
`wrdsapps_link_crsp_ibes.ibcrsphist` and `wrdsapps.ibcrsphist` have the same six
columns, description, update date (2026-02-16), and 37,662 rows. Bidirectional
`EXCEPT ALL` found zero differences. The dedicated schema is used in the migrated
script; **there is no distinct CIZ-specific link table in the inspected WRDS
schemas**. The link remains a WRDS-supplied mapping rather than a rederived CIZ
mapping. The query keeps 30,325 records with nonnull PERMNO.

| Output column | Status | Source and rule |
|---|---|---|
| `permno` | exact | `ibcrsphist.permno`, nullable Int32; retained only for a matching stock-month. |
| `time_avail_m` | derived | Month-start date from the full `crsp.msf_v2.mthcaldt` stock calendar. |
| `tickerIBES` | derived | `ibcrsphist.ticker` renamed after interval expansion and lowest-score selection; null tickers excluded. |
| `score` | exact | Selected `ibcrsphist.score`, nullable Int32. |

No output column is redefined on common keys. `SignalMasterTable.py` joins all
four columns on `(permno, time_avail_m)`. Its `tickerIBES` then supplies the
I/B/E/S forecast, recommendation, and analyst-count predictors and placebos.
The new CIZ calendar keys can therefore change the downstream stock-month
sample even though the link values on old keys are unchanged.

The frozen v1 keys-only calendar has 5,153,763 unique rows through 2024-12.
The existing v2 `monthlyCRSP.parquet` has only 65,042 rows in 1981 and **is not
a full calendar**. A separate `crsp.msf_v2` keys-only extract was written to
`Signals/pyData-v2/Inputs/CRSP_stock_month_calendar.parquet`: 5,240,606 unique
rows from 1925-12 through 2025-12, with no null keys. Calendar comparison:
5,117,046 common, 36,717 v1-only, and 123,560 v2-only stock-months (570 before
2025 and 122,990 in 2025). The script checks for null/duplicate calendar keys
and rejects a truncated debug calendar
before connecting to WRDS. The interval expansion intentionally has multiple
link rows per PERMNO; it found 92 overlapping candidates across 46 stock-months
and selected one row per key by lowest score, then IBES ticker.

## Stage 1 result

Run with `DEBUG_MODE=True` set in memory, `OPENAP_DATA_ROOT=Signals/pyData-v2`,
`OPENAP_CRSP_CALENDAR=Signals/pyData-v2/Inputs/CRSP_stock_month_calendar.parquet`,
and `/opt/venv/projects/openap/bin/python3`. The standard command
`Signals/tests/crsp_v2/compare.py IBESCRSPLinkingTable` reports:

| Measure | Result |
|---|---:|
| v1 / v2 output rows | 2,684,399 / 2,734,928 |
| Common / v1-only / v2-only keys | 2,684,399 / 0 / 50,529 |
| Ticker and score mismatches on common keys | 0 / 0 |
| Schema, dtype, or missingness differences on common keys | 0 |

Every v2-only link key is absent from the v1 stock calendar. Of these, 50,240
are in 2025 (4,822 PERMNOs), after the v1 cutoff. The other 289 are CIZ-only
historical calendar keys, all score 1, for seven PERMNOs: 78836 (161 months),
14675 (54), 77327 (31), 92449 (22), 22338 (17), 20402 (3), and 12796 (1).
There are no v1-only link keys, including among the 36,717 v1-only calendar
keys. Filtering the v2 link output to the v1 calendar reproduces the frozen v1
output exactly. Thus all observed output differences are calendar coverage;
the comparison gives no evidence of a link-source revision on shared keys.

## Sample decisions (2026-10-07)

- The seven CIZ-only historical PERMNOs and their 289 linked months enter
  downstream samples. The link follows the full CIZ calendar.
- The 50,240 linked 2025 months are used in Stage 2.
- Equal-score overlaps go to the first IBES ticker: the selection sorts on
  `score`, then `ticker`. A rerun with this rule matched v1 on every common key
  (ticker and score mismatches 0 / 0; coverage unchanged).

Rationale: the project favors simple code over exact v1 reproduction; see
`Docs/CRSP-v2-Migration.md`.
