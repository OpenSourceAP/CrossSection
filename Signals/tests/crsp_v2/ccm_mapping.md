# CCM link mapping and Stage 1 comparison

`CCMLinkingTable.py` exports the full primary CRSP–Compustat link history to
`CCMLinkingTable.parquet`. Its comparison key is `(gvkey, permno, permco, liid,
linktype, linkprim, timeLinkStart_d)`. `DEBUG_MODE=True` retains full history.

## Source and column mapping

WRDS's CIZ examples `ccm_ciz_merge.ipynb` and `ccm_link_collapse.ipynb` in
`/yolobox/cellar/Manuals-and-Reference/CRSP-v2/` use
`crsp.ccmxpf_lnkhist`. A WRDS catalog check on 2026-10-07 found the active
`crsp.ccmxpf_lnkhist` view and CCM tables in `crsp_a_ccm`, `crsp_m_ccm`, and
`crsp_q_ccm`, but no separate `_v2` or CIZ-specific CCM link history in those
schemas. WRDS metadata confirms the eight link fields and types: `gvkey`,
`linkprim`, `liid`, and `linktype` are strings; `lpermno` and `lpermco` are
double precision; `linkdt` and `linkenddt` are dates. Keep the active
`crsp.ccmxpf_lnkhist` view. `CompustatAnnual.py` uses the same query, join,
`LC`/`LU` and `P`/`C` filters, and conversions. No change to that script is
needed for consistency.

| Output column | Status | Source and rule |
|---|---|---|
| `gvkey` | exact | `comp.names.gvkey`; inner join to the link history by `gvkey`. |
| `conm`, `tic`, `cusip`, `sic` | exact | Current `comp.names` descriptors, with no historical dating or transformation. |
| `cik`, `naics` | derived | `comp.names` values; missing values become an empty string. |
| `linkprim`, `linktype`, `liid` | exact | `ccmxpf_lnkhist` fields; keep only link types `LC`/`LU` and primary codes `P`/`C`. |
| `permno`, `permco` | exact | `lpermno`, `lpermco`, renamed and converted to nullable integers. |
| `timeLinkStart_d`, `timeLinkEnd_d` | exact | `linkdt`, `linkenddt`, renamed and converted to timestamps; null end dates remain open. |

No column is redefined for CIZ. `CustomerMomentum.py` uses link identifiers,
dates, and `conm` for customer-name matching. `retConglomerate.py` and
`ZZ2_AnnouncementReturn.py` use link identifiers and dates. The standalone
export and `CompustatAnnual.py` do not read each other's output.

The script keeps its query and filters, closes the WRDS engine even if the read
fails, and rejects null or duplicate comparison keys before writing. It does
not collapse links or change interval rules. All 32,306 candidate keys are
nonnull and unique.

## Stage 1 result

Ran with `DEBUG_MODE=True` set in memory, `OPENAP_DATA_ROOT=Signals/pyData-v2`,
and `/opt/venv/projects/openap/bin/python3`, then ran
`Signals/tests/crsp_v2/compare.py CCMLinkingTable` over full history.

| Comparison | Result |
|---|---:|
| v1 / candidate rows | 32,306 / 32,306 |
| Common / v1-only / candidate-only keys | 32,306 / 0 / 0 |
| Link identifier, code, or interval-end mismatches | 0 |
| Schema, dtype, or missingness transitions | 0 |
| `comp.names` descriptor rows with any change | 10, across 7 GVKEYs |

The same SQL and transformations read a later `comp.names` snapshot. All
differences are source descriptor revisions, with no rounding or CCM-link
definition difference:

| Descriptor | Changed rows | Detail |
|---|---:|---|
| `conm` | 4 | GVKEY 013714: `PARAMOUNT SKYDANCE CORP` → `SKYDANCE CORP` on four historical links. |
| `tic` | 7 | Four rows for GVKEY 013714 (`PSKY` → `SKYD`), plus one each for 009729 (`SLVI` → `SLVI.1`), 024779 (`CPU` → `CPU.1`), and 037284 (`LESL` → `LESLQ`). |
| `cusip` | 2 | GVKEY 031994 (`38741L107` → `38741L404`) and 043756 (`G71399102` → `G71399110`). |
| `sic` and `naics` | 1 each | Same link, GVKEY 050260: `4731` → `5122` and `488510` → `424210`. |
| `cik`, `timeLinkEnd_d` | 0 | No changes. |

The 10 changed rows overlap across columns. Both versions have 6,054 open
interval ends, 347 links starting after the 2024-12-31 stock calendar cutoff,
and 380 ending after it. Those later intervals are identical in both versions.

## Sample decision (2026-10-07)

Use current `comp.names` values without backfilling old names or industry codes,
per the project's simple-code principle. The four `conm` changes for GVKEY
013714 can change the customer-name match in `CustomerMomentum.py`, and the one
`sic`/`naics` revision is also read by `CompustatAnnual.py` in full history.
These are Compustat source revisions, not migration effects. None changes link
membership or date coverage. Stage 2 should measure the effect of joining this
unchanged link history to the full CIZ stock calendar.
