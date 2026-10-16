# Monthly market index mapping and Stage 1 comparison

`MarketReturns.py` now reads `crsp.indmthseriesdata`, the CIZ monthly index
series in the stock database, rather than legacy `crsp.msi`. WRDS metadata
checked on 2026-10-07 found no `msi_v2`; it confirmed `indmthseriesdata` and
`indmthseriesdata_ind` have `indno`, `mthcaldt`, `mthtotret`, and `mthusdval`.
The `_ind` table is the larger Index database counterpart. The [WRDS index
overview](https://wrds-www.wharton.upenn.edu/pages/support/manuals-and-overviews/crsp/stocks-and-indices/siz-to-ciz-wrds-overview-of-index/)
and local `SIZ to CIZ WRDS Transition FAQ.md` identify 1000200 and 1000201 as
the NYSE/NYSEMKT/Nasdaq/Arca value- and equal-weighted market indexes. Both
have 1,201 monthly observations from 1925-12 through 2025-12 in the stock
database. Some *other* monthly CIZ series require daily `IndNo + 400`; these
two retain 1000200 and 1000201. The [CRSP cross-reference guide]
(/yolobox/cellar/Manuals-and-Reference/CRSP-v2/CRSP_Cross_Reference_Guide_1.0_to_2.0.pdf)
maps legacy monthly index total return and used value to `MthTotRet` and
`MthUsdVal`. `MthUsdVal` is in thousands of dollars. The value-weighted series'
1926-01 value is 27,412,916, matching legacy `usdval` 27,412,916.2 after
rounding; the equal-weighted series has a different used value.

| Output column | Mapping | Source and rule | Downstream use |
|---|---|---|---|
| `vwretd` | exact | `MthTotRet` for `IndNo=1000200`, renamed; CIZ total return including distributions. | `ZZ1_betaRR_betaCC_betaRC_betaCR_betaNet.py` uses it as the market return. |
| `ewretd` | exact | `MthTotRet` for `IndNo=1000201`, renamed. | `Beta.py` and `BetaSquared.py` use it to form the equal-weighted market excess return. |
| `usdval` | exact | `MthUsdVal` for `IndNo=1000200`, renamed; CIZ used market value in thousands, with no unit conversion. | `ZZ1_betaRR_betaCC_betaRC_betaCR_betaNet.py` normalizes it by July 1962 to form `MarketCapitalization`. |
| `time_avail_m` | derived | Month-start timestamp from `MthCalDt` for each series, then one-to-one matched across series. | All three consumers join by month. |

No output field is redefined. “Exact” means the native CIZ source field is
carried directly; it does not imply equal values across the two CRSP versions.
The script rejects missing or duplicate index-month keys and mismatched month
calendars before writing. It selects no row from a tie. The output has the same
column order and dtypes as v1.

## Stage 1 result

Ran with `DEBUG_MODE=True` set in memory, `OPENAP_DATA_ROOT=Signals/pyData-v2`,
and `/opt/venv/projects/openap/bin/python3`. The standard
`Signals/tests/crsp_v2/compare.py monthlyMarket` report found 1,189 common
months, no v1-only months, and 12 CIZ-only months (all of 2025). There are no
duplicate/null month keys, schema or dtype differences, or missingness
transitions on common months. Both versions have all three values missing in
1925-12 and present in the other 1,188 common months. All 12 added months have
all three values present.

| Field | Matched-month differences | Breakdown | Largest absolute difference |
|---|---:|---|---:|
| `vwretd` | 51 | 48 differ by 0.000001; one each by 0.000002, 0.000004, and 0.000007. | 0.000007 (2018-08) |
| `ewretd` | 47 | 41 differ by 0.000001; four by 0.000002; one by 0.000007; one by 0.000038. | 0.000038 (2014-04) |
| `usdval` | 1,003 | 271 differ by at most 0.5 thousand dollars, consistent with CIZ's integer values; 732 differ by more than 0.5. Of the latter, 723 are at most 100,000 and nine exceed 100,000. | 7,377,924 thousand dollars, 0.00966% of v1 (2024-12) |

The current WRDS `crsp.msi` has exactly the frozen baseline's 1,189 months and
all three values match the frozen output exactly. Thus none of these differences
comes from a changed legacy extract or from the script's join. The return
differences are native CIZ versus legacy index values; 89 of the 98 changed
return cells differ by only the final reported decimal, consistent with
precision or rounding. The other nine return cells and the 732 `usdval` cells
beyond integer rounding are CIZ source-series differences. The local CRSP
cross-reference guide warns that index values passed from the legacy system to
CIZ may not precisely match values calculated from new files, but it does not
identify the mechanism for these individual months. The largest `usdval`
changes cluster in 2024-07 through 2024-12. July 1962, the downstream scaling
denominator, changes from 287,198,521 to 287,198,542 (thousands; +21).

These are observed CIZ data differences, not evidence of a field mapping or
unit error. The exact underlying cause of the nine larger return changes and
732 used-value changes remains open. Further source-level investigation could
distinguish revised index constituents, calculation changes, and source
precision. The comparison artifacts are under
`Signals/pyData-v2/Logs/crsp_v2/monthlyMarket_*`.

## Sample decision (2026-10-07)

Keep all 12 CIZ months in 2025; do not truncate to v1's 2024-12 cutoff, per the
project's simple-code principle. Common-month keys and missingness do not
change, so their sample membership is unchanged; their market-return and
market-value inputs may change calculated signals negligibly.
