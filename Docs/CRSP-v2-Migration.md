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
The 882 returns that v2 adds in active months have not been investigated.

Decision (2026-10-06): accepted as close enough. The only downstream consumer
is `Signals/pyCode/Predictors/CustomerMomentum.py`, which drops missing values.
