# CRSP v2 (CIZ) migration: known output differences

This file records accepted differences between the legacy CRSP (v1, SIZ) downloads
and the CRSP v2 (CIZ) downloads. Comparisons use the frozen v1 baseline in
`Signals/pyData-v1/` (code revision `ff623e3`) and the Stage 1 selections in
`Signals/tests/crsp_v2/README.md`.

## monthlyCRSP: `ret_b4_dl` (return before delisting)

### Definition

CIZ has no monthly return-before-delisting field: `mthret` already includes the
delisting return. `CRSPMonthly.py` rebuilds `ret_b4_dl` from monthly data:

| `mthdelflg` | Last price at month end? | `ret_b4_dl` |
|---|---|---|
| N (active) | any | `mthret` |
| A, P, V (delisting return included) | yes | `(1 + mthret) / (1 + delret) - 1`; missing if `delret = -1` |
| G, M (delisting return excluded) | yes | `mthret` |
| A, P, V, G, M | no (mid-month delisting) | missing |

`delret` comes from `crsp.stkdelists` (one event per PERMNO). The mid-month rule
reproduces v1. There, `msf.ret` is missing in a delisting month whenever the last
price comes before month end; all 196 such A/P/V months in 1981 follow this rule.

### Match to v1 (1981, all securities, offline probe 2026-10-06)

| | Rows | `ret_b4_dl` missing |
|---|---|---|
| v1 | 65,652 | 3,599 (5.48%) |
| v2 | 65,042 | 2,110 (3.24%) |

- Keys: 65,039 matched; 613 v1-only, all with missing `ret_b4_dl`; 3 v2-only.
- Missingness on matched keys: 2,104 both missing; 882 v1 missing → v2
  present, all in non-delisting (`N`) months; 3 v1 present → v2 missing.
- Values on the 62,050 rows where both are present:

| Absolute difference | Share of rows |
|---|---|
| ≤ 1e-7 | 84.5% |
| ≤ 1e-4 | 86.9% |
| ≤ 1e-3 | 97.1% |
| ≤ 1e-2 | 99.8% |

  The median difference is 0, the 90th percentile 0.00023, the 99th percentile
  0.0019, and the maximum 1.74.
- Delisting months: all 39 P and all 49 M months match. 160 of 181 A months
  are within tolerance; most of the rest are within about 1e-6.
- The rule leaves two delisting months unmatched:
  - one A month with `delret = -1`, which cannot be inverted (v2 missing, v1 −0.33);
  - one G month that differs by 0.011.

### Interpretation

The small differences in returns fit CIZ's change in dividend reinvestment
convention. The CRSP v2 paper ("Rewriting CRSP History", JFQA) finds that 9.6% of
monthly returns change by more than 1bp. This has not been confirmed row by row.
The 882 returns that v2 adds in active months are partial-period returns; see
"Partial-period prices and returns" below.

Decision (2026-10-06): accepted as close enough. The only downstream consumer
is `Signals/pyCode/Predictors/CustomerMomentum.py`, which drops missing values.

## monthlyCRSP: mid-month delisting months

In v1, the name-history record (`msenames`) ends on the last trading day. In a
month where a security delists before month end, the name join therefore fails:
`shrcd`, `exchcd`, `sicCRSP`, `sic2D`, `ticker`, `shrcls`, `prc`, `retx` and
`mve_c` are missing, `cfacshr` is 0, and the row drops out of
`SignalMasterTable` (`shrcd ∈ {10,11,12}`, `exchcd ∈ {1,2,3}`).

`CRSPMonthly.py` joins CIZ security information on the month's last price date
(`mthprcdt`), so these rows keep their descriptors, last price and market equity.
`cfacshr` is missing rather than 0.

In 1981, this affects 244 security-months, all in delisting months (154 A,
43 M, 38 P, 8 G, 1 V). Of these, 235 would pass the `SignalMasterTable` filter,
so the master table gains roughly that many final-month rows per year relative to
v1. This group accounts for the 244-row blocks in the `shrcd`, `exchcd`,
`sicCRSP`, `sic2D` and `cfacshr` comparisons, and for 244 of the 456 `prc` and 452
`mve_c` missing-to-present rows. Pre-delisting returns in these months stay missing
(see above).

Decision (2026-10-07): keep the v2 values.

## monthlyCRSP: share and exchange codes

`Signals/pyCode/utils/crsp_v2_codes.py` rebuilds `shrcd` and `exchcd` from CIZ
classifications. It matches the WRDS CIZ-to-SIZ macro exactly, and its share
codes match Appendix B of the CRSP cross-reference guide (July 2026). Appendix B's
extra row (75 for non-US ETV units) is covered by the default code 75.

Apart from the delisting months above, 1981 differences are:

- `shrcd` 10 → 11 (12 rows): CIZ classifies the issuer as `CORP` rather than
  `ACOR`. Both codes pass every downstream share-code filter.
- `exchcd` 10, 16, 17, 20 → 0 (195 rows): CIZ has no legacy regional and OTC
  exchange codes; the macro maps them (`primaryexch = X`, `conditionaltype = NT`)
  to 0. Both are excluded by downstream filters, which use only codes 1–3.

## monthlyCRSP: partial-period prices and returns

v1 monthly prices and returns are missing when there is no valid month-end price,
or no valid previous month-end price to compound from. CIZ instead uses the last
price within the month and flags partial periods in `mthretflg`. In 1981
non-delisting months, v2 adds:

| Case | `mthretflg` | Rows | v2 adds |
|---|---|---|---|
| Last price before month end (1–28 days, median 4) | mostly IP | 212 | `prc`, `mve_c`, `ret` |
| First month of a new security | NS | 577 | `ret` |
| Incomplete period | IP | 56 | `ret` |
| Gap during period | GP | 43 | `ret` |

These account for all 882 `ret_b4_dl` missing-to-present rows, and for the
non-delisting `prc` and `mve_c` missing-to-present rows. The remaining
missing-to-present rows are the mid-month delisting months above.

Decision (2026-10-07): keep the v2 values, consistent with the delisting-month
decision. To restore v1 behavior, blank returns with these `mthretflg` values and
prices dated before month end.

## monthlyCRSP: other column differences (1981)

- `ret`: 9,654 matched values differ. 9,486 of them (98%) fall in dividend months
  (v1 `ret ≠ retx`), consistent with CIZ reinvesting dividends on the ex-date;
  85% of dividend months differ. The other 168 are mostly partial-period flags
  (IP 61, GP 35, DE 30, MP 1) plus 41 regular (CR) months; 33 are delisting
  months.
- `retx`: 251 matched values differ (0.4%), even though prices are identical
  in all but 3 of these rows. 148 are partial-period months (IP, GP, DE, MP) where
  CIZ compounds from a different base price. 103 are regular months with no
  price-factor change (median relative difference 1.1e-4); these are probably
  non-ordinary distributions, which `retx` includes, affected by the
  reinvestment change. This has not been confirmed. Missing-to-present `retx`
  rows (1,126) are the delisting and partial-period cases above.
- `cfacshr`: after rebasing each PERMNO to its first common date, 632 rows
  differ. v1 stores factors to exactly 6 decimal places and v2 at full
  precision. 625 rows differ by a relative 1e-7 to 1e-6. The other 7 belong to
  PERMNO 18148, whose factor (1.9e-5) loses about 5% to 6-decimal rounding.
  The 244 present-to-missing rows are delisting months (v1 0, v2 missing).
- `vol`: 30 rows differ by at most 5e-5 million shares; v1 monthly volume is in
  hundreds of shares, while v2 reports exact shares.
- `shrout`: 19 rows are 0 in v1 and missing in v2 (CIZ has no shares
  outstanding there), so `mve_c` is 0 in v1 and missing in v2.
- `sicCRSP`: 2 rows have SIC 0 (unknown) in v1 and a real code in v2.
- `ticker` (234 rows) and `shrcls` (6 rows): all are mid-month delisting months
  where v1 was empty.
- `prc`, `bidlo`, `askhi`: value differences are at most 5e-6, which is rounding.
- Coverage: the 613 v1-only rows are one empty month per PERMNO, with every
  value missing. 590 fall in the month before the security's first v2 month;
  the other 23 PERMNOs have no v2 month in 1981, presumably because their first
  month is in 1982 (not checked). No data are lost. The 3 v2-only rows (PERMNO
  18383 and 80550 in January, 31377 in April) have not been investigated.
