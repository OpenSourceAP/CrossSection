# CRSP v2 (CIZ) migration: known output differences

This file records how the downloads were migrated from legacy CRSP (v1, SIZ) to
CRSP v2 (CIZ), the differences found, and the decisions taken. Comparisons use the
frozen v1 baseline (code revision `ff623e3`) and the Stage 1
selections in `Signals/tests/crsp_v2/README.md`.

Status (2026-10-11): migration review is complete for all nine scripts. Stage 1
and Stage 2 comparisons are approved, including the documented differences and
known limitations. The sections below record the evidence and decisions.

### Guiding principle: simple code over exact reproduction

The project trades off simplicity of code against exact reproduction of v1
output, and generally favors simplicity. Use CIZ data and coverage as they come
rather than adding filters or backfills to reproduce v1 samples. Accept a
difference when it follows from v2 data or coverage and the code stays simple;
fix it when it is a migration error. Selections must still be deterministic:
whenever a rule picks one row from several, sort on a stable identifier after the
substantive criterion.

### Lessons from the migration

- Check WRDS metadata (`crsp.metaiteminfo`, `crsp.metaflaginfo`) and CRSP
  documentation before assuming a v1 field has no v2 equivalent. Earlier
  planning wrongly listed `cfacshr` and the `ret_b4_dl` inputs as unavailable.
- Expect the same two definition changes elsewhere: delisting months and
  partial-period returns. In `dsf_v2`, delisting returns are separate rows
  (`dlydelflg = 'Y'`); the daily download excludes them to match v1 `dsf` keys.
- v1 numeric fields are often rounded (factors to 6 decimals, volume to hundreds
  of shares), so tight tolerances flag many harmless differences. Attribute
  groups rather than relying on tolerance pass rates.
- Saving small v2 extracts locally made iteration fast and avoided repeated
  WRDS sessions.

### Stage 2: market, link tables and Compustat (full history) — shared comparison scope

Reports: `s2_report.py` for `monthlyMarket`, `CCMLinkingTable`,
`OPTIONMETRICSCRSPLinkingTable`, `IBESCRSPLinkingTable`, `CompustatAnnual`,
`a_aCompustat` and `m_aCompustat`, each restricted to the baseline's coverage.

`monthlyMarket`, `CCMLinkingTable`, `OPTIONMETRICSCRSPLinkingTable` and
`IBESCRSPLinkingTable` are identical to their Stage 1 outputs, which were
full-history comparisons against the frozen current-vintage v1. Their
differences from the older v1 baseline are therefore source-vintage changes.

Decision (2026-10-07): accepted. Stage 2 is complete for all nine scripts.

A ✅ in a script heading indicates approval of its consolidated findings.

### PrepScripts follow-up: corwin_schultz_edit.sas

Implementation (2026-10-15, issue #215 / PR #214): replaced `crspa.dsf` with
`crsp.dsf_v2`, mapping daily dates, prices, trade highs/lows, and volume in
shares. Regular rows (`dlydelflg='N'`) exclude the separate delisting events.
The adapter negates `dlyprc` when `dlyprcflg='BA'` so the existing screen and
retained-range replacement still handle bid/ask-average days. It does not
filter those days out or substitute closing quotes for trading ranges.

The script now sorts by security/month/date and aborts on missing or duplicate
security-date keys. The estimator calculations, 12-valid-day monthly minimum,
and `PERMNO,month,hlspread` CSV interface are unchanged. No cumulative-factor
price adjustment or additional universe filter was introduced.

Validated 2026-10-15 on the WRDS prep run; see "PrepScripts validation" below.

### PrepScripts follow-up: TAQ–Chen–Velikov links

Implementation (2026-10-15, issue #215 / PR #214): made the minimal CRSP input
change in `taq-chen-velikov/add_permnos.sas` and `macro_tclink.sas`. The direct
ticker/class match reads `crsp.stksecurityinfohist` and uses the native
`secinfostartdt`, `secinfoenddt`, and `shareclass` names directly.
`NCS` is normalized to blank; missing classes remain blank in SAS. Both macro
reads also use native CIZ `cusip`, `issuernm`, `tradingsymbol`, and history-date
names throughout the intermediate steps. The macro's output retains `comnam`
via a final rename of `issuernm`; its other output names are preserved as well.
Header identifiers are not used. The macro include is relative to the project's
prep directory.

The existing direct-match endpoint rounding (dates after the 15th move to the
next month; end month excluded), TCLINK CUSIP/name scoring and ticker-date
envelopes, 1993–2010 macro window, link precedence, spread calculations,
duplicate cleanup, and CSV interface are retained. No new universe or trading
status filter is applied. The proposed `wrdsapps.taqmclink` replacement and
CIZ midpoint fallback were deferred at the user's direction.

Known limitation: finer CIZ history intervals, including separate delisting
records, can alter monthly matches under the retained endpoint rule. For
example, splitting June 1–30 into June 1–15 and June 16–30 turns a valid June
interval into two empty rounded intervals. This update does not redesign that
rule or the macro's existing name/tie selection. The measured effect is small;
see "PrepScripts validation" below.

The first WRDS run of `add_permnos.sas` stalled in the ticker join because CIZ
has many more blank-ticker rows than `msenames`; blank tickers are now dropped
before the join (they could never match).

### PrepScripts validation

WRDS prep run 2026-10-15 (`run_all_prep.sh`, all three CRSP-dependent outputs
regenerated). Compared with the 2025 prep outputs (`temp/pyData25/Prep/`), the
only baseline. Differences may mix the migration with source revisions since
2025; that is accepted.

| Output | Duplicate keys | Coverage | Overlap through 2024 |
|---|---|---|---|
| `corwin_schultz_spread.csv` | 0 (PERMNO, month) | through 202512 (was 202412) | 4,481,621 common; 1 only in 2025; 0 values differ by more than 1e-6 |
| `hf_monthly.csv` | 0 (permno, yearm) | through 202512 (was 202412) | 3,262,441 common; 486 only in 2025; 17 only in new; 14 symbol-months changed permno |
| `tr_13f.csv` | 0 (PERMNO, rdate) | through 2025Q4 (was 2024Q4) | 865,654 common; 63 only in 2025; 464 only in new; `numinstown` differs in 1 row, `instown_perc` in 1,941 (0.2%) |

CSV headers and formats are unchanged (`rdate` remains SAS `date9.`;
`numinstown` keeps its quoted thousands separators). The `hf_monthly.csv`
link losses are consistent with the interval-rounding limitation above. The
13F `instown_perc` differences go through shares outstanding, so they likely
reflect CIZ share/factor revisions or the CIZ common-stock filter; they were
not investigated row by row.

Decision: pending approval.

## Portfolios/Code (issue 216)

The portfolio code no longer downloads CRSP. `10_DownloadCRSP.R` (legacy
`crsp.msf`/`msenames`/`msedelist` and `crsp.dsf`) and
`12_CreateCRSPPredictors.R` are removed. `11_ProcessCRSP.R` reads
`Signals/pyData/Intermediate/monthlyCRSP.parquet` and `dailyCRSP.parquet`
(the CIZ outputs of `CRSPMonthly.py` and `CRSPDaily.py`) and writes the same
`crspmret.fst`, `crspminfo.fst` and `crspdret.fst` as before, so scripts `20_`
to `50_` are unchanged. `Signals/pyCode/crsp_only.py` runs only the CRSP
downloads and the three CRSP predictors, for users who start from downloaded
signals.

Differences from the legacy portfolio inputs:

- Delisting returns: `ret` is native `mthret`, which includes the delisting
  return for `mthdelflg` A, P and V. The legacy portfolio code compounded
  `msf.ret` with `msedelist.dlret` and imputed −35% (NYSE/AMEX) or −55%
  (NASDAQ) for performance-related delistings (codes 500, 520–584) without a
  delisting return. Neither step is applied now, matching `Signals/`. Months
  with `mthdelflg` G or M have no delisting return in CIZ and none is imputed.
- Mid-month delistings: `mthret` is missing when there is no month-end price,
  so these months drop out of `crspmret` as they did in v1 when `msf.ret` was
  missing; in v1 the delisting return could still enter through `dlret`.
- `shrcd` and `exchcd` are the legacy codes recovered in `CRSPMonthly.py`
  (see "Share and exchange codes"). The portfolio code uses only
  `exchcd == 1` (NYSE breakpoints and the NYSE-only alternative) and
  `shrcd %in% c(10, 11)` (2x3 sorts).
- `me` is `mve_c` (`|prc| * shrout`, millions), the same definition as before.
- `Price`, `Size` and `STreversal` are now built by `Signals/pyCode/Predictors/`
  for everyone. They read `monthlyCRSP.parquet` directly with the
  `SignalMasterTable.py` screen (`shrcd` 10–12, `exchcd` 1–3), so the full
  pipeline output is unchanged and no Compustat is needed. The legacy R
  versions did not apply this screen and used the imputed delisting returns in
  `STreversal`.
- Daily: `dailyCRSP.parquet` excludes CIZ's separate delisting-event rows
  (`dlydelflg = 'Y'`), matching legacy `dsf` keys. `passgain` and `melag` are
  computed as before.

- `date` in `crspmret` is `mthcaldt` (the month's last trading date), kept in
  `monthlyCRSP.parquet` from 2026-10-23 so portfolio output stays month-end
  dated like legacy `msf.date`. For older parquet files without the column,
  `11_ProcessCRSP.R` uses the last calendar day of the month. Checked on
  WRDS 2026-10-23: through 2024-12, `mthcaldt` equals legacy `msf.date` on
  all 5,117,046 security-months present in both tables, and each of the 1,189
  months has a single date in both tables. After rerunning `CRSPMonthly.py`,
  `crspmret.fst` dates equal the legacy dates on all 5,033,554 matched rows.
- `me` in `crspminfo` is in millions of dollars (`mve_c`); the legacy portfolio
  code had it in thousands (legacy `shrout` was in thousands). The portfolio
  code uses `me` only relatively (NYSE breakpoints, `me > me_nyse20`, value
  weights), so nothing downstream changes.

#### Validation (2026-10-23, legacy `crsp.msf` pulled from WRDS, compared through 2024-12)

The legacy monthly tables were pulled with the old `10_DownloadCRSP.R` query
and processed with the old `11_ProcessCRSP.R` monthly block; the result was
compared with the new intermediates (legacy `me` rescaled to millions).

`crspmret` (security-months with a return): 4,987,378 legacy vs 5,033,581 new.

- 72 keys only in legacy (9 delisting months where `msf.ret` was missing but
  `dlret` was present and became the return). 46,275 keys only in new, mostly
  first months of a listing (1972 alone 3,236) where CIZ reports a
  partial-period return and legacy `ret` was missing.
- On the 4,987,306 common keys, `ret` differs by more than 1e-4 pct in 18% of
  rows and by more than 0.01 pct in 11% (CIZ dividend reinvestment; matches the
  Stage 2 finding and the 10% in Schwarz, Walter and Weiss). 7,400 rows differ
  by more than 1 pct: 2,041 are delisting months (legacy −35%/−55% imputation
  or `dlret` compounding), the rest are source revisions concentrated in the
  1930s and 1970s.
- `melag` differs by more than 1e-4 relative in 4,041 rows; 3,158 legacy-missing
  values are now present and 2,736 the reverse.

`crspminfo`: 5,153,763 legacy vs 5,117,616 new rows.

- 36,717 keys only in legacy: one empty month per PERMNO (no price, no name
  match), the same rows as in Stage 2. 570 keys only in new (40 PERMNOs).
- NYSE status (`exchcd == 1`) never differs. `exchcd` in 1–3 status differs in
  24,194 rows and `shrcd` in 10–11 status in 20,167 rows, almost all because
  the legacy `msenames` join left `shrcd`/`exchcd` missing in 25,761 rows
  that CIZ classifies.
- `prc`: no sign differences; 2,664 rows differ by more than 1e-4 relative.
  `me`: 6,743 rows differ by more than 1e-4 relative, 1,742 by more than 1e-2.
  `me_nyse20` differs by more than 1% in 189 of 1,189 months (max 6%).

Baseline long-short portfolios (same signal CSVs, legacy vs new CRSP):

| Signal     | Months | Corr  | Mean LS legacy | Mean LS new | t legacy | t new | Max abs diff (pct) |
| ---------- | ------ | ----- | -------------- | ----------- | -------- | ----- | ------------------ |
| Price      | 1,188  | 0.999 | 0.67           | 0.72        | 2.68     | 2.90  | 3.4                |
| Size       | 1,182  | 0.999 | 0.32           | 0.34        | 2.76     | 2.95  | 1.3                |
| STreversal | 1,187  | 0.997 | 2.72           | 2.83        | 13.60    | 14.03 | 7.7                |

The largest monthly differences are STreversal months in 1930–1942, where CIZ
revised a handful of extreme small-stock returns. Daily intermediates were
not compared against legacy `dsf` here; `dailyCRSP.parquet` was validated in
the Signals migration (see `CRSPDaily.py` below).

Decision (2026-10-23): accepted; the differences are the documented CIZ
definition changes plus the removal of the legacy delisting imputation.

## CRSPMonthly.py: ✅

PR #214 follow-up: removed the daily CRSP aggregation and the unused monthly
`bidlo`/`askhi` columns. No predictor or placebo reads those columns. The output
now has 18 columns; the other columns and return calculations are unchanged.
The comparison results below describe the previously approved 20-column output,
including the two columns subsequently removed. New comparison reports should
list only `bidlo` and `askhi` as baseline-only monthly columns.

### Stage 1 summary (1981, WRDS run 2026-10-07)

Rows: v1 65,652; v2 65,042. Keys: 65,039 matched, 613 v1-only, 3 v2-only.
Schema: the same 20 columns and dtypes.

| Column       | Mismatches | %      | v1 missing → v2 present | v1 present → v2 missing |
| ------------ | ---------- | ------ | ----------------------- | ----------------------- |
| `askhi`      | 791        | 1.22%  | 0                       | 0                       |
| `bidlo`      | 872        | 1.34%  | 0                       | 0                       |
| `cfacshr`    | 4,834      | 7.43%  | 0                       | 244                     |
| `exchcd`     | 439        | 0.67%  | 244                     | 0                       |
| `mve_c`      | 1,313      | 2.02%  | 452                     | 14                      |
| `mve_permco` | 1,315      | 2.02%  | 451                     | 14                      |
| `permco`     | 0          | 0.00%  | 0                       | 0                       |
| `prc`        | 1,303      | 2.00%  | 456                     | 0                       |
| `ret`        | 10,563     | 16.24% | 906                     | 3                       |
| `ret_b4_dl`  | 10,504     | 16.15% | 882                     | 3                       |
| `retx`       | 1,379      | 2.12%  | 1,126                   | 2                       |
| `shrcd`      | 256        | 0.39%  | 244                     | 0                       |
| `shrcls`     | 6          | 0.01%  | 0                       | 0                       |
| `shrout`     | 19         | 0.03%  | 0                       | 19                      |
| `sic2D`      | 246        | 0.38%  | 244                     | 0                       |
| `sicCRSP`    | 246        | 0.38%  | 244                     | 0                       |
| `ticker`     | 234        | 0.36%  | 0                       | 0                       |
| `vol`        | 30         | 0.05%  | 0                       | 0                       |

Mismatch counts include missingness transitions. The sections below attribute
each group. In short:
- dividend reinvestment: `ret`, `ret_b4_dl`;
- mid-month delisting months: the 244-row blocks;
- partial-period returns: most other missing-to-present rows;
- cumulative-factor vintage scaling and rounding: `cfacshr`;
- rounding: price and volume.

### Stage 1 details

#### How comparisons were run

- Candidate: `CRSPMonthly.py` run with `DEBUG_MODE = True` set in memory (not
  in `config.py`). The debug selection is
  all securities in calendar 1981.
- Comparison: `Signals/tests/crsp_v2/compare.py monthlyCRSP` produces
  a JSON comparison report, key inventories and up to 100 examples per mismatching column.
- Diagnostics: ad hoc probes on saved 1981 v2 monthly, delisting, daily,
  name-history, and flag extracts reproduced the WRDS run exactly.
- Tolerances (fixed before comparing) are in the test README. Most "mismatches"
  in the summary above are rounding or documented definition changes; the counts
  are diagnostics, not acceptance criteria.

#### Implementation: `CRSPMonthly.py`

Sources:

| v2 table                   | Used for                                                                                                                                          |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `crsp.msf_v2`              | identifiers, `mthret`, `mthretx`, `mthprc`/`mthprcflg`/`mthprcdt`, `mthvol`, `shrout`, `mthcumfacshr`, `mthdelflg`, ticker, classification fields |
| `crsp.stksecurityinfohist` | `shareclass`, `siccd` (effective-dated)                                                                                                           |
| `crsp.stkdelists`          | `delret`; full history, one event per PERMNO                                                                                                      |

Column rules (full table in `Signals/tests/crsp_v2/monthly_mapping.md`):

- `ret`, `retx`: native `mthret`, `mthretx`. No legacy −35%/−55% delisting
  imputation and no second delisting adjustment.
- `ret_b4_dl`: rebuilt; see the next sections.
- `prc`: `mthprc`, negated when `mthprcflg = 'BA'` (bid/ask average) to keep v1's
  sign convention.
- `vol`: `mthvol / 1e6`. CIZ volume is in shares; v1 monthly volume was in
  hundreds and divided by 1e4. The output unit (millions of shares) is unchanged.
- `shrout`: `shrout / 1e3` (millions), unchanged.
- `cfacshr`: `mthcumfacshr`.
- `shrcd`, `exchcd`: `Signals/pyCode/DataDownloads/CRSPMonthly.py`; see "Share and
  exchange codes".
- `shrcls`: `shareclass`, with `NCS` (no class) and missing mapped to `''`.
- `sicCRSP`, `sic2D`: effective-dated `siccd`.
- Security information is joined on `COALESCE(mthprcdt, mthcaldt)`, the date of
  the month's last price. CIZ descriptors belong to that date, so name history
  stays available in delisting and no-price months.

Safety checks: the script raises an error on duplicate `(permno, time_avail_m)`
after the join, duplicate PERMNOs in `stkdelists`, more than one
delisting-inclusive month per PERMNO, a delisting-inclusive month without
`delret`, or an unknown `mthdelflg`. Nothing is silently deduplicated.

#### Reference: CIZ flags used here

`mthdelflg` (flag type DE):

| Flag | Meaning                 | Delisting return in `mthret`? |
| ---- | ----------------------- | ----------------------------- |
| N    | Not applicable (active) | —                             |
| A    | Amount (distributions)  | included                      |
| P    | Price (next available)  | included                      |
| V    | Value partial           | included                      |
| G    | Gap                     | excluded                      |
| M    | Missing                 | excluded                      |

`mthretflg` (aggregate return flag, type AR). 1981 counts: CR 61,017, NT 1,862,
MP 856, NS 577, IP 369, DE 262, GP 99. Meanings follow the matching codes in the
AV and PC flag types: NS new security, IP incomplete period, GP gap during period,
DE delisting, MP missing price, NT not tracked. CR is presumably the regular
complete return; the AR value list was not retrieved.

`mthprcflg` (type PC): TR closing trade price, BA bid/ask average, MP missing price.

In CIZ daily data, the delisting return is a separate `dsf_v2` row
(`dlydelflg = 'Y'`) dated `deldlydt`, the trading day after the delisting date. It
can therefore fall in the month after `delistingdt`.

#### `ret_b4_dl` (return before delisting)

##### Definition

CIZ has no monthly return-before-delisting field: `mthret` already includes the
delisting return. `CRSPMonthly.py` rebuilds `ret_b4_dl` from monthly data:

| `mthdelflg`                         | Last price at month end? | `ret_b4_dl`                                                 |
| ----------------------------------- | ------------------------ | ----------------------------------------------------------- |
| N (active)                          | any                      | `mthret`                                                    |
| A, P, V (delisting return included) | yes                      | `(1 + mthret) / (1 + delret) - 1`; missing if `delret = -1` |
| G, M (delisting return excluded)    | yes                      | `mthret`                                                    |
| A, P, V, G, M                       | no (mid-month delisting) | missing                                                     |

`delret` comes from `crsp.stkdelists` (one event per PERMNO). The mid-month rule
reproduces v1. There, `msf.ret` is missing in a delisting month whenever the last
price comes before month end; all 196 such A/P/V months in 1981 follow this rule.
G and M months behave the same way: v1 is missing in 44 of 49 M and 8 of 9 G
months.

Events are matched to the flagged month by PERMNO, not by the `delistingdt`
month. In 1981 the two always coincide (all 283 flagged months), but CIZ can
place the delisting return in a later month. The full delisting table is
downloaded, because a 1981 window on `delistingdt` could miss an event whose
flagged month differs.

Rejected alternative: an earlier draft fell back to compounding regular daily
returns (`dlydelflg = 'N'`) within the month when the inversion failed. It was
dropped for three reasons:
- it was inconsistent with the mapping doc;
- it covered only one 1981 case (`delret = -1`);
- it did not reproduce v1, which is missing in mid-month delisting months.

The monthly script no longer queries `dsf_v2`; `bidlo`/`askhi` were unused and removed.

##### Match to v1 (1981, all securities)

|     | Rows   | `ret_b4_dl` missing |
| --- | ------ | ------------------- |
| v1  | 65,652 | 3,599 (5.48%)       |
| v2  | 65,042 | 2,110 (3.24%)       |

- Keys: 65,039 matched; 613 v1-only, all with missing `ret_b4_dl`; 3 v2-only.
- Missingness on matched keys: 2,104 both missing; 882 v1 missing → v2
  present, all in non-delisting (`N`) months; 3 v1 present → v2 missing.
- Values on the 62,050 rows where both are present:

| Absolute difference | Share of rows |
| ------------------- | ------------- |
| ≤ 1e-7              | 84.5%         |
| ≤ 1e-4              | 86.9%         |
| ≤ 1e-3              | 97.1%         |
| ≤ 1e-2              | 99.8%         |

  The median difference is 0, the 90th percentile 0.00023, the 99th percentile
  0.0019, and the maximum 1.74.
- Delisting months: all 39 P and all 49 M months match. 160 of 181 A months
  are within tolerance; most of the rest are within about 1e-6, and the largest
  is 8e-5.
- The rule leaves two delisting months unmatched:
  - one A month with `delret = -1` (PERMNO 52330, September 1981), which cannot
    be inverted (v2 missing, v1 −0.33);
  - one G month (PERMNO 57525, July 1981) that differs by 0.011.
- Compared with the first candidate (daily fallback, `delistingdt` matching),
  the rule changed 245 values and cut v1-missing → v2-present rows from 1,126 to
  882.

##### Interpretation

The small differences in returns fit CIZ's change in dividend reinvestment
convention. The CRSP v2 paper ("Rewriting CRSP History", JFQA)
finds that 9.6% of monthly returns change by more than 1bp. WRDS's transition FAQ
reports over 3,000 stock-months with return changes above 5% across the full
history; its largest examples carry partial-period flags (GP, IP, DE). Neither has
been confirmed row by row here. The 882 returns that v2 adds in active months
are partial-period returns; see "Partial-period prices and returns" below.

Decision (2026-10-06): accepted as close enough. The only downstream consumer
is `Signals/pyCode/Predictors/CustomerMomentum.py`, which drops missing values.

#### Mid-month delisting months

In v1, the name-history record (`msenames`) ends on the last trading day. In a
month where a security delists before month end, the name join therefore fails:
`shrcd`, `exchcd`, `sicCRSP`, `sic2D`, `ticker`, `shrcls`, `prc`, `retx` and
`mve_c` are missing, `cfacshr` is 0, and the row drops out of
`SignalMasterTable` (`shrcd ∈ {10,11,12}`, `exchcd ∈ {1,2,3}`). v1 `ret`, which
includes the delisting return, is still present in 220 of these rows.

`CRSPMonthly.py` joins CIZ security information on the month's last price date
(`mthprcdt`), so these rows keep their descriptors, last price and market equity.
`cfacshr` is missing rather than 0.

In 1981, this affects 244 security-months, all in delisting months (154 A,
43 M, 38 P, 8 G, 1 V). Of these, 235 would pass the `SignalMasterTable` filter,
so the master table gains roughly that many final-month rows per year relative to
v1. This group accounts for:
- the 244-row blocks in the `shrcd`, `exchcd`, `sicCRSP`, `sic2D` and `cfacshr`
  comparisons;
- all 234 `ticker` and 6 `shrcls` mismatches;
- 244 of the 456 `prc` and 452 `mve_c` missing-to-present rows.

Pre-delisting returns in these months stay missing (see above).

Alternative considered: blank the descriptors and price in these months to
replicate v1 exactly. Rejected in favor of keeping the information.

Decision (2026-10-07): keep the v2 values.

#### Share and exchange codes

`Signals/pyCode/DataDownloads/CRSPMonthly.py` rebuilds `shrcd` and `exchcd` from CIZ
classifications. It matches the WRDS CIZ-to-SIZ macro exactly, and its share
codes match Appendix B of the CRSP cross-reference guide (July 2026). Appendix B's
extra row (75 for non-US ETV units) is covered by the default code 75.

- `shrcd` maps the tuple (`sharetype`, `securitytype`, `securitysubtype`,
  `usincflg`, `issuertype`) to 22 legacy codes; anything else is 75.
- `exchcd` maps `primaryexch` and the trading flags:
  - `primaryexch` N/A/Q/R/B/I → 1–6, for regular-way (`conditionaltype = RW`),
    active (`tradingstatusflg = A`) securities;
  - halted (H) and suspended (S) NYSE/AMEX/NASDAQ securities → −2 and −1;
  - when-issued securities → 31–33;
  - `primaryexch = X` with `conditionaltype = NT` → 0;
  - anything else → 99.

  The macro's conditions do not overlap, so assignment order does not matter.
- Legacy codes that CIZ cannot recover, such as regional exchanges, become 0
  or 99.

Apart from the delisting months above, 1981 differences are:

- `shrcd` 10 → 11 (12 rows): CIZ classifies the issuer as `CORP` rather than
  `ACOR`. Both codes pass every downstream share-code filter.
- `exchcd` 10, 16, 17, 20 → 0 (195 rows): CIZ has no legacy regional and OTC
  exchange codes; the macro maps them (`primaryexch = X`, `conditionaltype = NT`)
  to 0. Both are excluded by downstream filters, which use only codes 1–3.

#### Partial-period prices and returns

v1 monthly prices and returns are missing when there is no valid month-end price,
or no valid previous month-end price to compound from. CIZ instead uses the last
price within the month and flags partial periods in `mthretflg`. In 1981
non-delisting months, v2 adds:

| Case                                              | `mthretflg` | Rows | v2 adds               |
| ------------------------------------------------- | ----------- | ---- | --------------------- |
| Last price before month end (1–28 days, median 4) | mostly IP   | 212  | `prc`, `mve_c`, `ret` |
| First month of a new security                     | NS          | 577  | `ret`                 |
| Incomplete period                                 | IP          | 56   | `ret`                 |
| Gap during period                                 | GP          | 43   | `ret`                 |

In the first case, 184 of the 212 prices are bid/ask averages (BA) and 166 are
NASDAQ (v1 `exchcd = 3`). v1 has no `ret` in any of the 212.

These account for all 882 `ret_b4_dl` missing-to-present rows, and for the
non-delisting `prc` and `mve_c` missing-to-present rows. The remaining
missing-to-present rows are the mid-month delisting months above.

Decision (2026-10-07): keep the v2 values, consistent with the delisting-month
decision. To restore v1 behavior, blank returns with these `mthretflg` values and
prices dated before month end.

#### Other column differences (1981)

- `ret`: Of the 65,039 matched stock months, 9,654 (14.8%) matched values differ. Of the matched values that differ, 9,486 of them (98%) fall in dividend months
  (v1 `ret ≠ retx`), consistent with CIZ reinvesting dividends on the ex-date;
  85% of dividend months differ. Of the other 168, 127 carry partial-period
  flags (IP 61, GP 35, DE 30, MP 1) and 41 are regular (CR) months; 33 of the
  168 are delisting months.
- `retx`: 251 matched values differ (0.4%), even though prices are identical
  in all but 3 of these rows.
  - 148 are partial-period months (IP, GP, DE, MP), where CIZ compounds from a
    different base price.
  - 103 are regular months with no price-factor change (median relative
    difference 1.1e-4). These are probably non-ordinary distributions, which
    `retx` includes, affected by the reinvestment change. This has not been
    confirmed.
  - Regular months with a price-factor change (917 in 1981) match except for 2.
  - The 1,126 missing-to-present `retx` rows are the delisting and
    partial-period cases above.
- `cfacshr`: cumulative factors are normalized to the end of each source
  vintage, so raw levels differ by a constant within each PERMNO when a later
  split occurred.
  - 4,177 of the 4,834 raw mismatches are consistent with this scaling.
  - After rebasing each PERMNO to its first common date (5,813 PERMNOs; 79 have
    only one comparable date), 632 rows differ. v1 stores factors to exactly 6
    decimal places and v2 at full precision. 625 rows differ by a relative 1e-7
    to 1e-6. The other 7 belong to PERMNO 18148, whose factor (1.9e-5) loses
    about 5% to 6-decimal rounding.
  - The 244 present-to-missing rows are delisting months (v1 0, v2 missing).
- `vol`: 30 rows differ by at most 5e-5 million shares; v1 monthly volume is in
  hundreds of shares, while v2 reports exact shares.
- `shrout`: 19 rows are 0 in v1 and missing in v2 (CIZ has no shares
  outstanding there), so `mve_c` is 0 in v1 and missing in v2 (14 rows).
- `sicCRSP`: 2 rows have SIC 0 (unknown) in v1 and a real code in v2.
- `mve_c`, `mve_permco`: differences follow from `prc` and `shrout`. The largest
  `mve_permco` difference (281, PERMCO 21926 in April 1981) comes from a second
  share class (PERMNO 59475) in its mid-month delisting month, which v2 includes
  and v1 did not.
- `prc`, `bidlo`, `askhi`: value differences are at most 5e-6, which is rounding.
- Coverage: the 613 v1-only rows are one empty month per PERMNO, with every
  value missing. 590 fall in the month before the security's first v2 month;
  the other 23 PERMNOs have no v2 month in 1981, presumably because their first
  month is in 1982 (not checked). No data are lost. The 3 v2-only rows (PERMNO
  18383 and 80550 in January, 31377 in April) have not been investigated.

#### Downstream effects

- `SignalMasterTable.py:49` keeps `shrcd ∈ {10,11,12}` and `exchcd ∈ {1,2,3}`.
  `ExchSwitch.py` and other predictors test only exchange codes 1–3. Share-code
  filters use `<= 11`, `> 11`, `{10,11}` or `{10,11,12}`. So the 10 → 11 share
  codes and regional-exchange → 0 codes have no effect.
- The master table gains final-month rows for mid-month delistings (about 235
  in 1981) and rows with partial-period prices.
- Missing codes behave differently by language. In pandas, `shrcd > 11` is
  False for a missing `shrcd`, so a "drop if > 11" filter keeps the row. In
  Stata, missing is greater than any number, so the row is dropped. v2 fills
  codes where v1 had them missing, which reduces this ambiguity.
- `ret_b4_dl` is read only by `CustomerMomentum.py`.

#### Caveats for the full-history (Stage 2) run

- One delisting event per PERMNO, and at most one delisting-inclusive month per
  PERMNO, hold in 1981. Over full history they are assumptions; the script
  raises an error, rather than guessing, if they fail.
- 1981 cannot test cases that are absent or rare in that year, such as ETFs and
  other later security types, or classification changes after 1981.
- CIZ is updated continuously, while v1 stopped at December 2024. Stage 2
  differences against the older v1 baseline will mix definition changes with a year
  of revisions.

### Stage 2 summary (full history vs the older v1 baseline)

Report: `Signals/tests/crsp_v2/s2_report.py monthlyCRSP`.
Compared through the baseline's last month,
2024-12; the 122,990 candidate rows in 2025 are excluded.

- Keys: 5,117,046 matched; 36,717 baseline-only (one empty month per PERMNO,
  every value missing, as in Stage 1); 570 candidate-only across 40 PERMNOs,
  95% with missing `ret`.
- Means by decade of `ret`, `shrout`, `prc` and `mve_c` agree closely. The lower
  candidate `retx` mean in recent decades comes entirely from newly present
  delisting and partial-period months; on rows present in both, means agree to
  the fifth decimal.
- Matched values: `ret`/`ret_b4_dl` differ in 18% of rows (dividend
  reinvestment; 16% in 1981). `vol` differs in 48%, all but 8 within one hundred
  shares (v1 units). `cfacshr` 6.6% (vintage normalization and rounding).
  `retx`, `prc`, `mve_c` 1-2%, mostly newly present values. Two `permco` values
  in 2024-12 are source revisions.
- SIC: about 189k stock-months coded 9999 (unclassified) in v1 carry a real SIC
  in v2, almost all from 2010 on (most common: 2834, 6799, 8731, 7389); about 25k
  more are reclassified. This changes samples for predictors that exclude
  financials (`CBOperProf`, `OperProfRD`, `CitationsRD`, `PatentsRD`) and for
  industry-based signals. See "SIC codes" below.

Decision (2026-10-07): accepted, using v2 SIC codes as they come.

### SIC codes (issue 212, checked 2026-10-21)

The v2 codes are a correction of a defect in the legacy tape, not a change in
definition.

- Schwarz, Walter and Weiss (JFQA 2026, "Rewriting CRSP's History", Table B.1)
  compare SIZ and CIZ item by item for common stocks on NYSE/AMEX/NASDAQ,
  July 1926 to December 2023, on a WRDS vintage from July 2024. They find only
  7 differing SIC observations out of 3.76 million. So the differences above were
  introduced by CRSP after mid-2024 and show up only in CIZ because the SIZ
  export ended with the December 2024 data.
- Root cause: from about 2008 the legacy tape stopped classifying new listings.
  First `msenames` record per PERMNO (share codes 10-12, exchanges 1-3), by
  listing year, share with SIC 9999 on the first record / on the last record:
  2007 2% / 1%; 2008 16% / 12%; 2009 32% / 31%; 2012 46% / 45%; 2015 64% / 63%;
  2018 69% / 69%; 2021 71% / 70%; 2024 72% / 72%. The codes were never filled in
  later. In `SignalMasterTable` the share of stock-months with `sicCRSP == 9999`
  under v1 is 0.3% in 2008, 14% in 2015 and 39% in 2024; under v2 it is below 1%
  throughout. Of the 2022-2024 rows whose code changed, 73% are stocks first
  listed in 2015 or later; they carry 25% of total market capitalization.
- What `sicCRSP` is in v2: CIZ carries `siccd` in three places. The column on
  `msf_v2` is the header code (identical to `stksecurityinfohdr` in every month
  of an 819-PERMNO sample, never varying within a PERMNO). `stksecurityinfohist`
  holds effective-dated spells and differs from the header in 37% of
  stock-months. `CRSPMonthly.py` joins the history table on the month's last
  price date, the same point-in-time idea as the legacy `msenames` join and the
  choice Tidy Finance recommends.
- Where the new codes come from: 99.6% of the changed stock-months equal the
  issuer-level code in `stkissuerinfohist`, so CRSP assigned one code per company
  and applied it through the security's history. They are not copied from
  Compustat: for changed stock-months with a Compustat match, v2 equals `sich`
  in 22% of cases (57% at two digits), against 38% (75%) for unchanged
  stock-months. About 28% of the changed stock-months have no Compustat match.
  Caveat: a firm that changed industries since listing may carry its current
  code back to its first month, the usual mild look-ahead of a vendor cleanup.
- Effect on predictors: `SignalMasterTable` was built twice from the same v2
  `monthlyCRSP.parquet`, once with `msenames` SIC codes and once with v2 codes,
  the SIC-dependent predictors were rerun on each, and long-short returns were
  computed with each predictor's SignalDoc settings (Python port of
  `Portfolios/Code/01_PortfolioFunction.R`), sample through 2024-12. Only
  `sicCRSP` differs between the runs. `OrgCap` was not run (no FRED key).

  | Predictor | Full: mean LS %/mo v1 / v2 | t v1 / v2 | corr | 2010+: mean v1 / v2 | t v1 / v2 | 2010+ mean abs diff (bp) |
  |---|---|---|---|---|---|---|
  | CBOperProf | 0.51 / 0.50 | 3.5 / 3.5 | 1.00 | 0.50 / 0.48 | 1.4 / 1.3 | 21 |
  | OperProfRD | 0.44 / 0.43 | 2.6 / 2.6 | 1.00 | 0.77 / 0.72 | 2.1 / 2.0 | 23 |
  | ShareVol | 0.15 / 0.15 | 0.8 / 0.8 | 1.00 | 0.18 / 0.18 | 0.6 / 0.6 | 0 |
  | IndMom | 0.35 / 0.36 | 3.7 / 3.9 | 0.98 | -0.03 / 0.01 | -0.2 / 0.1 | 122 |
  | IndRetBig | 1.37 / 1.40 | 12.1 / 12.4 | 0.99 | 0.52 / 0.71 | 2.2 / 3.0 | 114 |
  | Frontier | 1.27 / 1.27 | 6.2 / 6.3 | 0.98 | 0.49 / 0.48 | 1.1 / 1.1 | 126 |
  | ChInvIA | 0.30 / 0.32 | 5.3 / 5.6 | 0.96 | -0.19 / -0.12 | -1.2 / -0.8 | 70 |
  | realestate | 0.21 / 0.22 | 1.8 / 1.9 | 0.99 | 0.07 / 0.11 | 0.3 / 0.5 | 60 |
  | Herf | 0.01 / 0.04 | 0.2 / 0.7 | 0.89 | -0.33 / -0.16 | -1.6 / -1.2 | 143 |
  | HerfAsset | -0.02 / -0.02 | -0.2 / -0.3 | 0.92 | -0.30 / -0.30 | -1.4 / -1.8 | 127 |
  | HerfBE | 0.02 / 0.03 | 0.3 / 0.4 | 0.93 | -0.30 / -0.25 | -1.5 / -1.6 | 117 |

  Full-sample premia and t-statistics are unchanged for every predictor (largest
  change in a mean: 3 bp per month). Post-2010 monthly long-short returns of the
  industry-grouping signals differ by 60-140 bp in absolute terms, because v2
  places stocks that v1 left unclassified into real industries. Financial-screen
  predictors differ by about 20 bp; roughly 44k stock-months newly fall into
  6000-6999, mostly 6799 and SPAC-like issuers.

Decision (2026-10-21): keep the v2 codes from `stksecurityinfohist`. Do not
patch 9999 codes with Compustat (mixes classification sources) or with the
header code (look-ahead). Release notes should warn that industry-based
predictors differ from the 2025 release after about 2015, with `Herf`,
`HerfAsset`, `HerfBE`, `IndMom`, `IndRetBig`, `Frontier` and `ChInvIA` most
affected.

## CRSPDaily.py: ✅

### dailyCRSP and dailyCRSPprc (January 1981)

`CRSPDaily.py` reads native `crsp.dsf_v2` stock days with `dlydelflg = 'N'`.
The 29 separate delisting-event rows in January (`Y`) are excluded because v1
`dsf` has no corresponding stock-day rows. The script keeps native `dlyret`,
`dlyvol` (shares), `dlycumfacpr`, and `shrout` (thousands), and negates `dlyprc`
when `dlyprcflg = 'BA'`. WRDS metadata and the CRSP v2 transition FAQ confirm
those field meanings. The full column mapping is in
`Signals/tests/crsp_v2/daily_mapping.md`.

The debug run produced both outputs. Each has 108,923 rows,
the same schema and keys as the frozen v1 baseline; missingness is identical.
`dailyCRSPprc` equals the corresponding five columns of `dailyCRSP` exactly.
Under the predeclared tolerances, `vol` and `shrout` match exactly. The remaining
differences are:

| Column   | Beyond tolerance | Attribution                                                                                                                                                                                                                                                                                                                       |
| -------- | ---------------: | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `prc`    |              912 | Every case is a negative bid/ask price and differs by exactly 0.000005, the last decimal of the v1 stored price.                                                                                                                                                                                                                  |
| `ret`    |               60 | Every case differs by exactly 0.000001; only four pairs of v1/v2 values occur. These are precision-level differences, with no missingness transition. The upstream rounding rule is unverified.                                                                                                                                   |
| `cfacpr` |       15,884 raw | 15,745 pass after rebasing to each security's first common date. The other 139 raw mismatches and 42 rebased-only mismatches fit v1's six-decimal factor rounding. A fixed positive scale per PERMNO can put *every* v2 factor within half a unit of its v1 value's sixth decimal; all 5,224 PERMNOs satisfy this interval check. |

Decision (2026-10-07): keep the native v2 values and exclude the separate
delisting-event rows. No January sample membership or missingness changes. The
constant-scale factor result is consistent with vintage normalization and
rounding, but does not identify each security's endpoint normalization. Stage 2
must check later periods, where return definitions or delisting handling may
produce larger changes.

### Stage 2: dailyCRSP and dailyCRSPprc (full history vs the older v1 baseline)

Reports: `s2_report.py dailyCRSP` and `dailyCRSPprc` (value section on January
1981). A separate full-history value check on matched keys used polars.
Compared through 2024-12; 2,541,089 candidate rows in 2025 are excluded.
`dailyCRSPprc` equals the matching columns of `dailyCRSP`.

- Keys: 107,662,848 matched (every key before 2010). 11,470 candidate-only rows
  (15 PERMNOs, 2011-2024) and 113 baseline-only rows (one PERMNO, 2024-07 to
  2024-12) all have missing `ret` and `prc`.
- Means by decade of `ret`, `prc`, `vol` and `shrout` agree to about four
  significant digits.
- `ret`: all but 115 differences are 1e-6; the 115 are scattered days from 2000
  on, probably source revisions. `prc`: stored precision (5e-6 before 2000,
  typically 1e-5 after; maximum 0.05 on a $607k price); no sign changes. `vol`:
  identical. `shrout`: 58,140 days are 0 in v1 and missing in v2; about 41k
  values changed, 30k of them in 2024 across about 2,500 PERMNOs (median 0.9%),
  consistent with share updates after the baseline vintage. `cfacpr`: vintage
  scaling, as in Stage 1.

Decision (2026-10-07): accepted.

## CRSPDistributions.py: ✅

### Shared source and code mapping

Both scripts now read `crsp.stkdistributions`. WRDS `information_schema` confirmed
the field names. The 3,473-row code-only projection of CRSP's
`CRSP_DistributionCode_SIZ_to_CIZ_Mapping.html` is bundled as
`Signals/pyCode/utils/crsp_distribution_code_map.csv`. Its seven CIZ code fields
uniquely determine `distcd`; `DisOrdinaryFlg` is not in the published crosswalk.
All 65 CIZ code combinations observed in 1981 map, including special dividends
(1272) and spinoffs (3762–3763). Unknown combinations raise an error. Full
field rules and consumers: `Signals/tests/crsp_v2/distribution_mapping.md`.

### CRSPdistributions (1981 ex-dates)

The 1981 run found 12,916 CIZ source events and zero CIZ events with missing
ex-dates (counted outside the selected window). The distributions script removes
six records sharing another record's legacy event key, keeping the lowest CIZ
`DisSeqNbr` deterministically. Its output has 12,910 rows versus 12,914 v1;
12,910 keys match, four are v1-only, and none is v2-only. Schemas, dtypes,
missingness, and all four derived code digits match on common keys. The four
missing v1 rows are `distcd` 7111 (three bankruptcy filings) and 7181 (one
exchange-requirement failure), all with zero amount. These are legacy
information records, absent from `stkdistributions` for their PERMNOs and dates.

On matched distribution keys, `divamt` differs in 283 rows. In 282, the
absolute difference is at most 0.000005, consistent with the v1 stored amount
being rounded to five decimals. The exception is PERMNO 19430 on 1981-03-10,
`distcd` 3723: two CIZ events share the legacy output key but have different
`DisSeqNbr`, child identifiers, and amounts (11.5285 and 30.875). The frozen
v1 output retained 30.875; the deterministic lowest-sequence CIZ rule retains
11.5285. The old script selected an unspecified first row after sorting only
the legacy key, so this cannot be resolved from that key. This changes the
March 1981 amount consumed by the two DivYield placebos; it does not change
event or stock-month membership. The six discarded CIZ rows have distinct
sequence numbers.

`facshr` differs in 15 matched rows, each by at most 0.000003; the v1 stored
factor has five decimals and CIZ has six. CIZ has 1,022 null `DisDivAmt` source
values in 1981, mainly stock splits and stock dividends. These become zero to
reproduce the v1 `divamt` convention; the corresponding output has no amount
missingness difference.

### Shared distributions and acquisitions decision (Stage 1)

Decision (2026-10-07): retain CIZ events, native numeric precision, the
deterministic first-sequence rule for duplicate legacy keys, and the distinct
child rule. Do not backfill records or identifiers from v1. The collision on
PERMNO 19430 is documented as an output-key limitation and should be revisited
if the downstream DivYield amount is material. Stage 2 must check whether new
CIZ code combinations appear and whether full-history duplicate-key collisions
require a richer output key.

### Stage 2: CRSPdistributions (full history)

Reports: `s2_report.py CRSPdistributions` and `m_CRSPAcquisitions`. Attribution
used one read-only pull of `crsp.stkdistributions` and current `crsp.msedist`.
Distributions are compared through 2024-12 (37,001 events in 2025 excluded).

- Distribution keys: 1,060,784 matched. 3,115 baseline-only/candidate-only pairs
  are the same event with a changed `paydt` (almost always v1 date to v2
  missing); `paydt` has no downstream consumer. Unpaired: 186 baseline-only
  (mostly legacy information codes 7111/7181 absent from CIZ, as in Stage 1,
  plus about 100 small dividends), 18 baseline events without ex-date, and 67
  candidate-only. No new `distcd` values.
- `divamt` on matched keys: 85,768 differences are rounding (v1 five decimals;
  CIZ four for some large amounts). 175 are real and all occur where CIZ has
  several events for the same PERMNO and ex-date; the lowest-`DisSeqNbr` rule
  (715 duplicates removed in full history) picks a different event than v1. In
  156, v1's amount is one of the CIZ events; about 19 may be a dividend split
  across CIZ events that v1 recorded as one amount (e.g. PERMNO 81774).

### Shared distributions and acquisitions decision (Stage 2)

Decision (2026-10-07): accepted. The duplicate-key amount picks (0.02% of
events, feeding the DivYield placebos) are a known limitation; summing amounts
over duplicate keys was considered and not adopted.

## CRSPAcquisitions.py: ✅

### Shared source and code mapping

Both scripts now read `crsp.stkdistributions`. WRDS `information_schema` confirmed
the field names. The 3,473-row code-only projection of CRSP's
`CRSP_DistributionCode_SIZ_to_CIZ_Mapping.html` is bundled as
`Signals/pyCode/utils/crsp_distribution_code_map.csv`. Its seven CIZ code fields
uniquely determine `distcd`; `DisOrdinaryFlg` is not in the published crosswalk.
All 65 CIZ code combinations observed in 1981 map, including special dividends
(1272) and spinoffs (3762–3763). Unknown combinations raise an error. Full
field rules and consumers: `Signals/tests/crsp_v2/distribution_mapping.md`.

### m_CRSPAcquisitions (1981 ex-dates)

The acquisition script preserves its legacy rule: any source event with
`DisPERMNO > 999` contributes that distinct child PERMNO, regardless of the
distribution code. It finds 70 qualifying CIZ events and 62 children versus
63 v1 children. The 62 common children and their `SpinoffCo` values match.
The sole v1-only child is PERMNO 3679. In the same parent event (PERMNO 46252,
1981-08-13, amount 33.3025, code 3823), legacy `ACPERM=3679` became CIZ
`DisPERMNO=-5`; no CIZ event references 3679. This is a source identifier
change, not a code-mapping or filter error. PERMNO 3679 does not occur in the
frozen monthly stock panel, so it cannot affect the downstream Spinoff join.

### Shared distributions and acquisitions decision (Stage 1)

Decision (2026-10-07): retain CIZ events, native numeric precision, the
deterministic first-sequence rule for duplicate legacy keys, and the distinct
child rule. Do not backfill records or identifiers from v1. The collision on
PERMNO 19430 is documented as an output-key limitation and should be revisited
if the downstream DivYield amount is material. Stage 2 must check whether new
CIZ code combinations appear and whether full-history duplicate-key collisions
require a richer output key.

### Stage 2: m_CRSPAcquisitions (full history)

Reports: `s2_report.py CRSPdistributions` and `m_CRSPAcquisitions`. Attribution
used one read-only pull of `crsp.stkdistributions` and current `crsp.msedist`.
Distributions are compared through 2024-12 (37,001 events in 2025 excluded).

- Acquisitions: with CIZ events cut at 2024-12, 5,291 children vs 5,632 in the
  baseline (115 more children come from 2025 events). All 342 baseline-only
  children still have their parent event in CIZ, which records the child as
  -5 (264), a different child (55), or a zero/small code (23). None of the 342
  is in the monthly stock panel, so the Spinoff join is unaffected. One new
  pre-2025 child is in the v2 panel. Current `msedist` reproduces the baseline's
  5,632 children, so the changes come from CIZ.

### Shared distributions and acquisitions decision (Stage 2)

Decision (2026-10-07): accepted. The duplicate-key amount picks (0.02% of
events, feeding the DivYield placebos) are a known limitation; summing amounts
over duplicate keys was considered and not adopted.

## CompustatAnnual.py: ✅

### CompustatAnnual.py: CCM source unchanged

The script's CRSP dependency is `crsp.ccmxpf_lnkhist`. WRDS's CIZ sample
programs `ccm_ciz_merge.ipynb` and `ccm_link_collapse.ipynb` still use this table. WRDS metadata confirms the
current names and types of `gvkey`, `linkprim`, `linktype`, `liid`, `lpermno`,
`lpermco`, `linkdt`, and `linkenddt`. Its existing `LC`/`LU` and `P`/`C`
filters, inclusive interval test, and output schema therefore need no CIZ field
substitution. The code now checks that the interval match resolves each
`(gvkey, datadate)` to one link before producing annual data.

Column mapping for this script:

| Output fields                                                                                                                                                                                                                      | Classification and rule                                                                                                                                                             |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| All 110 `CompustatAnnual.csv` fields                                                                                                                                                                                               | Exact values from the shared `comp.funda` extract; `datadate` is formatted as a Stata date string. No CRSP fields.                                                                  |
| Original annual fields, except the zero-filled fields below                                                                                                                                                                        | Carried from the extract; `gvkey` is converted to numeric and `datadate` to a timestamp.                                                                                            |
| `permno`, `permco`                                                                                                                                                                                                                 | Exact `ccmxpf_lnkhist.lpermno`, `.lpermco`, renamed and converted to nullable integers.                                                                                             |
| `cik`, `sic`, `naics`                                                                                                                                                                                                              | Exact `comp.names` fields, with missing `naics` represented as an empty string.                                                                                                     |
| `nopi`, `dvt`, `ob`, `dm`, `dc`, `aco`, `ap`, `intan`, `ao`, `lco`, `lo`, `rect`, `invt`, `drc`, `spi`, `gdwl`, `che`, `dp`, `act`, `lct`, `tstkp`, `dvpa`, `scstkc`, `sstk`, `mib`, `ivao`, `prstkc`, `prstkcc`, `txditc`, `ivst` | Derived by filling missing values with zero.                                                                                                                                        |
| `cnum`, `dr`, `dc`, `xint0`, `xsga0`, `xad0`, `time_avail_m`                                                                                                                                                                       | Derived: six-character CUSIP prefix; sum of available deferred-revenue components; convertible-debt fallback rule then zero fill; expense zero fills; report month plus six months. |
| Monthly output                                                                                                                                                                                                                     | Annual fields carried through, except `time_avail_m` advances by 0–11 months; existing month-key deduplication applies.                                                             |

No field was redefined for CIZ and no downstream consumer needs a new rule.
`ccmxpf_lnkhist` is joined by `gvkey` across historical intervals and then
filtered by report date. The 1981 run had 6,486 rows before this interval filter
and 4,493 after it; the latter had no repeated `(gvkey, datadate)` or
`(gvkey, permno, datadate)` keys. Monthly output had no repeated
`(permno, time_avail_m)` keys. The older full-history v1 baseline annual and
monthly files also have no repeated keys on these respective output keys.

Stage 1 reused the frozen v1 baseline's raw Compustat annual extract and set
`DEBUG_MODE=True` in memory. The three
`compare.py` reports have identical schemas and dtypes, zero unmatched keys, and
zero column mismatches: 6,744 `CompustatAnnual.csv` rows, 4,493
`a_aCompustat` rows, and 3,692 `m_aCompustat` rows. The CSV files are also byte
identical (SHA-256 `b59af83af4f9521f92ddfee0faac669513f1dfdcc9ab930a20d2aec00dd1ef1e`).
There is no Stage 1 sample or value change to approve.

### Stage 2: full history

- Compustat: the only CRSP input is `ccmxpf_lnkhist`, so all differences are
  Compustat revisions and new filings. `CompustatAnnual.csv` matches 517,119
  `(gvkey, datadate)` keys (156 baseline-only, 887 candidate-only, mostly in the
  2020s); every value column differs in at most 0.15% of matched rows apart
  from identifier text (`conm`, `tic`, `cusip`) and `ajex` (about 1.5%). Means by
  decade agree to four digits before 2020. `a_aCompustat` follows the same
  pattern (302,333 matched, 107/47 unmatched). `m_aCompustat` adds 27,697
  stock-months inside the baseline window, almost all from fiscal 2025 reports
  filed after the baseline was pulled.

## IBESCRSPLink.py: ✅

### IBESCRSPLinkingTable

`IBESCRSPLink.py` uses `wrdsapps_link_crsp_ibes.ibcrsphist`. WRDS metadata and
bidirectional `EXCEPT ALL` show that it is row-for-row identical to
`wrdsapps.ibcrsphist`; no distinct CIZ link table was found in the inspected
schemas. A separate full keys-only `crsp.msf_v2` calendar has 5,240,606 unique
stock-months through 2025-12. The existing debug `monthlyCRSP` covers only 1981
and cannot serve as this calendar.

The Stage 1 output has 2,684,399 keys matching v1 exactly, no v1-only keys, and
50,529 v2-only keys. Ticker, score, schema, dtypes, and missingness match on every
common key. All added keys are absent from the v1 calendar: 50,240 are in 2025,
and 289 are historical months for seven CIZ-only PERMNOs. The existing interval
and lowest-score rules were retained; 46 stock-months have overlapping link
candidates.

Decisions (2026-10-07): the 289 historical CIZ-only months and the 2025 months
enter downstream samples; the link follows the v2 calendar without filtering.
Equal-score overlaps now go to the first IBES ticker (sort on `score`, then
`ticker`). A rerun with this tie rule leaves every common key unchanged.
Details: `Signals/tests/crsp_v2/ibes_mapping.md`.

### Stage 2: full history

IBES has 422 baseline-only and 3,255 candidate-only stock-months, identical tickers
on matched keys, and 240 changed scores.

## OptionMetricsCRSPLink.py: ✅

### OptionMetrics–CRSP link

WRDS catalog inspection on 2026-10-07 found no CIZ or `_v2` counterpart to
`wrdsapps_link_crsp_optionm.opcrsphist`. All five output columns remain direct
mappings. The full-history candidate equals the frozen v1 output: 34,881 common
keys; zero unmatched, null, or duplicate `(secid, permno, sdate)` keys; and zero
value, schema, or missingness differences. Both files have 1,515 intervals
starting and 13,807 ending after the 2024-12-31 stock calendar cutoff. Stage 2
should check how this unchanged link joins to the full CIZ stock calendar.
Details: `Signals/tests/crsp_v2/optionmetrics_mapping.md`.

### Stage 2: full history

OptionMetrics has 75 baseline-only and 1,041
candidate-only links (1,006 in the 2020s) and extended `edate`s.

## MarketReturns.py: ✅

### monthlyMarket

`MarketReturns.py` now reads `crsp.indmthseriesdata`: `MthTotRet` from
IndNo 1000200 and 1000201 supplies `vwretd` and `ewretd`; `MthUsdVal`
from 1000200 supplies `usdval` in thousands of dollars. `time_avail_m`
is derived from `MthCalDt`. The output schema is unchanged. See
`Signals/tests/crsp_v2/market_mapping.md` for the full mapping.

The full-history comparison has 1,189 common months, no v1-only months,
and 12 CIZ-only months in 2025. Common-month mismatches are 51 `vwretd`,
47 `ewretd`, and 1,003 `usdval`; there are no missingness, schema, or
dtype changes. Of the return differences, 89 are one unit in the sixth
decimal; the largest is 0.000038. Of the used-value differences, 271 are
at most 0.5 thousand dollars and 732 are larger; the maximum is 7,377,924
thousand dollars (0.00966%) in 2024-12. Current `crsp.msi` exactly
matches the frozen v1 values, so these are CIZ series differences. Their
underlying cause is not identified; they are accepted as negligible.

Decision (2026-10-07): keep native CIZ coverage, including 2025, per the
guiding principle.

### Stage 2: full history

`monthlyMarket` repeats the Stage 1 CIZ index differences (51 `vwretd`, 47
`ewretd`, 1,003 `usdval` months).

## CCMLinkingTable.py: ✅

### CCMLinkingTable.py

WRDS's CIZ examples continue to use `crsp.ccmxpf_lnkhist`; catalog
inspection found no separate CIZ CCM link history. The script retains the
same query and conversions as `CompustatAnnual.py` and now checks for null
or duplicate link keys. Full-history comparison found 32,306 matching keys,
no unmatched keys, and no link-field, interval, schema, or missingness
differences. Current `comp.names` descriptors differ on 10 rows across seven
GVKEYs: `conm` 4, `tic` 7, `cusip` 2, and `sic`/`naics` 1 each, with
overlaps. These are Compustat source revisions, not migration effects; the
`conm` changes can touch `CustomerMomentum.py` name matches.

Decision (2026-10-07): keep current source values without backfills, per the
guiding principle. Details: `Signals/tests/crsp_v2/ccm_mapping.md`.

### Stage 2: full history

CCM has 95 baseline-only and 137
candidate-only link keys, 370 links that have since ended, and `comp.names`
descriptor revisions.
