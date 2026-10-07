# Daily CRSP mapping and Stage 1 comparison

`CRSPDaily.py` reads regular (`dlydelflg = 'N'`) observations from
`crsp.dsf_v2`. CIZ's separate delisting-event observations (`Y`) do not occur in
v1 `dsf` and are excluded. In January 1981 there are 108,923 regular rows and
29 delisting-event rows. The two outputs have identical keys; `dailyCRSPprc` is
exactly the five-column projection of `dailyCRSP`.

| Output column | Mapping | v2 field / rule |
|---|---|---|
| `permno` | exact | `permno`, stored as int32 |
| `time_d` | derived | `dlycaldt`, normalized to a day timestamp |
| `ret` | direct | `dlyret`; preserve native daily return, with no extra delisting adjustment |
| `vol` | direct | `dlyvol` in shares, the same unit as v1 daily volume |
| `prc` | derived | `dlyprc`, negated only for `dlyprcflg = 'BA'` to preserve the v1 bid/ask sign |
| `cfacpr` | direct | `dlycumfacpr`; compare within-security ratios across vintages |
| `shrout` | direct | `shrout` in thousands of shares |

WRDS `information_schema.columns` and `crsp.metaiteminfo` confirmed these
fields and units on 2026-10-07. The WRDS transition FAQ defines `BA` as a bid/ask
average and CIZ's `Y` rows as separate delisting returns. All other retained
columns have the v1 names, order, and dtypes. The script raises on duplicate or
null security-date keys and writes each year before reading the next, so a
full-history run does not concatenate all years in memory.

The frozen v1 files and the v2 debug run each have 108,923 January 1981 rows.
Every `(permno, time_d)` key matches, as do all missingness patterns. `vol` and
`shrout` match exactly. Under the fixed tolerances in `README.md`, the remaining
diagnostics are:

| Column | Rows beyond tolerance | Explanation |
|---|---:|---|
| `prc` | 912 | All are negative bid/ask prices differing by exactly `0.000005`, half of the v1 price's last stored decimal. |
| `ret` | 60 | All differ by exactly `0.000001`; this is a precision-level difference, though the upstream rounding rule is unverified. |
| `cfacpr` | 15,884 raw | 15,745 pass after rebasing to each PERMNO's first common factor. The other 139 raw mismatches, and 42 rebased-only mismatches, fit v1 six-decimal factor rounding: for all 5,224 PERMNOs, one fixed positive scale can put every v2 factor within half a unit of the corresponding v1 factor's sixth decimal. |

The factor feasibility check demonstrates consistency with fixed vintage scaling
and rounding; it does not identify the historical endpoint used to normalize each
factor. No keys, missingness, or January sample membership changed. Downstream
consumers of the daily files use returns, prices, volume, shares, and factors;
their full-history behavior remains for Stage 2 review.
