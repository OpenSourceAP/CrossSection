# OptionMetrics–CRSP link mapping and Stage 1 comparison

`OptionMetricsCRSPLink.py` still reads
`wrdsapps_link_crsp_optionm.opcrsphist`. The WRDS PostgreSQL catalog inspection
on 2026-10-07 found that base table, a `wrdsapps.opcrsphist` view, and an
`wrdsapps_link_crsp_optionm_old.opcrsphist` backup, but no `_v2` or CIZ-specific
OptionMetrics–CRSP link. The active table's description says “Option Metrics
CRSP History Link (Updated 2026-02-16).” Its five fields are `secid` (double
precision), `sdate` and `edate` (date), `permno` (integer), and `score` (double
precision). The local WRDS transition FAQ at
`/yolobox/cellar/Manuals-and-Reference/CRSP-v2/SIZ to CIZ WRDS Transition FAQ.md`
describes `_v2` replacements for CRSP stock tables in the `crsp` schema; the
two local CRSP cross-reference guides do not mention OptionMetrics or
`opcrsphist`. Together with the exact output comparison below, this confirms
that the downloaded link is unchanged for this migration. It does not establish
how WRDS internally built the link.

| Output column | Mapping | Rule / downstream use |
|---|---|---|
| `secid` | exact | Raw OptionMetrics security identifier; `SignalMasterTable.py` carries the selected identifier into option predictors. |
| `sdate` | exact | Raw link start date; `SignalMasterTable.py` turns it into the first month of a candidate interval. |
| `edate` | exact | Raw link end date; `SignalMasterTable.py` turns it into the last eligible month under its existing rule. |
| `permno` | exact | Raw CRSP security identifier; joins the link to stock months. |
| `score` | exact | Raw match score; `SignalMasterTable.py` sorts ascending to choose a link for a stock month. |

There are no derived or redefined output columns. The existing
`WHERE permno IS NOT NULL` row filter and column order are unchanged. The
script now closes its WRDS engine immediately after the read and fails before
writing if `(secid, permno, sdate)` contains nulls or duplicate rows. It does
not collapse ties or alter identifiers.

## Stage 1 verification

Ran the script with `DEBUG_MODE=True` set in memory and
`OPENAP_DATA_ROOT=Signals/pyData-v2`, then ran:

```sh
/opt/venv/projects/openap/bin/python3 Signals/tests/crsp_v2/compare.py OPTIONMETRICSCRSPLinkingTable
```

Both versions contain the full 34,881-row
history, with five columns and identical dtypes. The complete dataframes also
compare equal in original row order. Key uniqueness: zero null keys and zero
duplicate `(secid, permno, sdate)` keys on each side.

| Comparison | Count |
|---|---:|
| Matched identifier/start-date keys | 34,881 |
| v1-only / candidate-only keys | 0 / 0 |
| `edate` mismatches or missingness transitions | 0 |
| `score` mismatches or missingness transitions | 0 |
| Schema or dtype differences | 0 |

Thus identifier assignments, interval start and end dates, scores, and
missingness have zero differences. There is no migration error, definition
change, source revision, or rounding discrepancy in this output. The candidate
and baseline have the same 1,515 intervals starting after the v1 stock
calendar's 2024-12-31 cutoff and the same 13,807 intervals ending after it;
these groups overlap. Neither file has an interval date after 2025-12-31.
Those later intervals do not represent candidate-only coverage.

## Open item

The link itself needs no sample-changing decision. Stage 2 should measure how
the unchanged link attaches to the full CIZ stock calendar. If CIZ changes
stock-month membership, deciding whether to rebuild or filter this link to
that calendar would change downstream option samples and belongs to the user.
