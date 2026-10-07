# Monthly CRSP mapping and compatibility decisions

Scope: CRSPMonthly.py output only. Preserve the existing twenty columns and types;
no predictor code or predictor-output tests are part of this work.

| Output column | Status | V2 source / rule |
|---|---|---|
| permno, permco | exact | msf_v2 identifiers, nullable Int64 |
| time_avail_m | derived | month start from mthcaldt |
| ret | derived | mthret directly, including applicable delisting; no second adjustment or legacy missing-delisting imputation |
| retx | derived | mthretx; CIZ compounding and delisting conventions replace legacy monthly conventions |
| ret_b4_dl | derived | mthret for N; for A/P/V months with a month-end price, (1+mthret)/(1+delret)-1 using the PERMNO's stkdelists event (missing if delret=-1); G/M with month-end price keep mthret; any delisting month without a month-end price is missing, as in v1. Accepted differences: Docs/CRSP-v2-Migration.md |
| vol | derived | mthvol / 1,000,000, millions of shares; CIZ raw volume is shares while v1 monthly volume was hundreds of shares |
| shrout | derived | shrout / 1,000, millions of shares |
| prc | derived | mthprc, negated only when mthprcflg=BA |
| cfacshr | exact | mthcumfacshr; assess within-security factor ratios across vintages, preserving missingness separately |
| bidlo, askhi | derived | extrema of regular daily closing dlyprc; rank positive magnitudes, retain chosen observation's BA sign; earliest date breaks equal-price ties |
| shrcd | derived | five-field share/issuer tuple mapped to WRDS's CIZ-to-SIZ conversion codes; default75 for remaining combinations |
| exchcd | derived | primaryexch, conditionaltype and tradingstatusflg mapped to WRDS's conversion codes; default99 for unresolved combinations |
| ticker | exact | monthly ticker, missing becomes empty string |
| shrcls | derived | effective-dated shareclass; NCS/missing become empty string |
| sicCRSP | exact | effective-dated SICCD; CIZ issuer-wide SIC revisions are possible |
| sic2D | derived | first two digits of sicCRSP using existing conversion |
| mve_c | derived | shrout in millions times absolute prc |
| mve_permco | derived | sum mve_c over all securities of each company-month, min_count=1 |

The effective-date information join uses mthprcdt, falling back to mthcaldt when
no price date exists. CIZ descriptors belong to the period price date. This keeps
name history available for within-month delistings and no-price stock months.
Duplicate monthly keys after the join cause failure rather than deduplication.

Compatibility decisions: keep ret_b4_dl as a return excluding delisting events;
its dividend reinvestment follows native CIZ monthly returns. Keep ret as the
native CIZ total return, without reproducing legacy exchange-specific imputation.
Both are explicitly changed return definitions, to be compared and reported.
Keep legacy numeric share/exchange fields through documented WRDS mappings (verified against the macro and Appendix B; see Docs/CRSP-v2-Migration.md);
unknown combinations remain visible through fallback codes and mismatch reports.
The other seven in-scope scripts are untouched until the monthly comparison is
reviewed. The frozen v1 files remain unchanged.

Sources: cellar/Manuals-and-Reference/CRSP-v2/ user guide (daily flag/return/volume
items, monthly return and price-date definitions), cross-reference guide and
executive summary (reinvestment and return-definition differences), WRDS stock
overview and event reconstruction notes (shareclass, delisting and name history).
The older CRSP Data Descriptions Guide and the 1981 input probe confirm that the
existing monthly bidlo/askhi are signed daily closing-price extrema; substituting
intraday high/low does not reproduce this output.
WRDS's published CIZ-to-SIZ macro supplies share/exchange reverse mappings:
https://wrds-www.wharton.upenn.edu/pages/wrds-research/macros/crsp-ciztosiz-macro/
