# CRSP v2 migration comparisons

The v1 baseline is frozen at commit `ff623e3` in `Signals/pyData-v1/`.
`FROZEN.json` records the committed source and verified data/source checksums.
Source release identifiers were not obtained. The v1 stock calendar ends in
December 2024; link-table intervals may extend later. Never overwrite this root.

Candidate downloads go to `Signals/pyData-v2/`. Reuse the baseline's explicit
Compustat raw extract. Pull a separate v2 keys-only calendar for IBES. The default
production root remains `Signals/pyData/`. Production output is Stage 2 work.

Run with the project environment:

```sh
/opt/venv/projects/openap/bin/python3 Signals/tests/crsp_v2/compare.py monthlyCRSP
```

`compare.py` selects each side independently, verifies key uniqueness, and
outer-joins their key union. Null event-date components match explicitly.
It saves complete key inventories, unmatched keys, schemas, missingness
transitions, value mismatch percentages, p99/max absolute differences, and
up to 100 examples per mismatching column under the candidate's Logs/crsp_v2.
Producing a report does not mean its discrepancies are accepted.

| Output | Selection | Comparison key |
|---|---|---|
| monthlyCRSP | 1981 stock months, all securities | permno, time_avail_m |
| dailyCRSP, dailyCRSPprc | January 1981, all securities | permno, time_d |
| CRSPdistributions | 1981 ex-dates, all events | permno, rcrddt, exdt, paydt, distcd |
| m_CRSPAcquisitions | 1981 source ex-dates, existing distinct-child logic | permno |
| monthlyMarket | Full history; later coverage reported separately | time_avail_m |
| CCMLinkingTable | Full link history | gvkey, permno, permco, liid, linktype, linkprim, timeLinkStart_d |
| CompustatAnnual.csv | 1981 datadate, shared fundamentals extract | gvkey, datadate |
| a_aCompustat | 1981 datadate, all linked firms | gvkey, permno, datadate |
| m_aCompustat | 1981 availability months, built solely from 1981 reports | permno, time_avail_m |
| IBESCRSPLinkingTable | Full links and full stock calendar for each version | permno, time_avail_m |
| OPTIONMETRICSCRSPLinkingTable | Full link history | secid, permno, sdate |

Distribution and acquisition field mappings, code crosswalk, collision rule,
and 1981 coverage: `Signals/tests/crsp_v2/distribution_mapping.md`.

Tolerances were fixed before the comparisons: returns use absolute and relative
1e-7; prices use absolute 1e-6 / relative 1e-8; share/price factors use absolute
1e-7 / relative 1e-8; volume uses absolute 1e-6 / relative 1e-8; shares use
absolute and relative 1e-8; market equities use absolute 1e-6 / relative 1e-8.
Identifiers, classifications, dates, strings, and unspecified numeric fields
require exact equality. Derived columns need independent expected-value checks;
this label does not exempt them from v1 comparison. Report definition changes,
evidenced source revisions, migration errors and unresolved differences explicitly.

## Monthly mapping research

Schema inspection confirms `crsp.msf_v2` contains monthly cumulative factors;
`crsp.stksecurityinfohist` contains `shareclass`; `crsp.stkdelists` contains
`delret`. Earlier plan statements implying those inputs were absent were
incorrect. Monthly returns already incorporate delisting returns, and prices
use a separate price flag rather than a negative sign. Mapping decisions must
be finalized before replacing the monthly script.

Primary references:

- [WRDS CIZ-to-SIZ conversion guide](https://wrds-www.wharton.upenn.edu/pages/wrds-research/macros/crsp-ciztosiz-macro/)
- [WRDS CRSP transition notice](https://wrds-www.wharton.upenn.edu/pages/data-announcements/changes-to-crsp-data/)
- WRDS `crsp.metaiteminfo` and `crsp.metaflaginfo`, queried in the authorized session.

The agreed monthly sample contains 323 company-months with multiple securities;
it also contains delistings and multiple share classes. Cases outside the windows
remain untested. Monthly Compustat covers only July–December 1981 by agreement.

## Factor comparisons across vintages

Cumulative factors are normalized to the endpoint of each source vintage, so
raw factor-level differences alone do not establish a migration error. Keep
raw differences as diagnostics, but assess split adjustment using factor ratios
between common dates or factors rebased to a shared date within each PERMNO.
Report missingness and nonconstant within-security scaling separately. Never
normalize away missing observations or claim every difference is vintage-related.

Relevant repository discussions:

- [Closed issue #152: proper usage of cfacshr](https://github.com/OpenSourceAP/CrossSection/issues/152)
- [Closed issue #95: cfacpr vintage normalization](https://github.com/OpenSourceAP/CrossSection/issues/95)

Predictor work remains outside this migration checklist. Consumer inspection
only establishes the compatibility requirements for downloaded output columns.
