# CRSP distribution and acquisition mapping

Stage 1 selection: every `crsp.stkdistributions` row with
`1981-01-01 <= DisExDt < 1982-01-01`. Record and payment dates are unrestricted.
The source has zero missing ex-dates. The frozen v1 baseline is
`Signals/pyData-v1/Intermediate/`; candidate outputs are in
`Signals/pyData-v2/Intermediate/`.

## Distribution output

| Output | CIZ input | Rule |
|---|---|---|
| `permno` | `PERMNO` | Exact security identifier. |
| `divamt` | `DisDivAmt` | Same event amount; fill CIZ null with zero to match SIZ's noncash-event convention. Retain CIZ precision. |
| `distcd` | Seven CIZ code fields | Derived by the bundled official 3,473-row crosswalk; fail on an unknown combination. |
| `facshr` | `DisFacShr` | Same share adjustment factor; retain CIZ precision. |
| `rcrddt` | `DisRecordDt` | Exact record date. |
| `exdt` | `DisExDt` | Exact ex-date. |
| `paydt` | `DisPayDt` | Exact payment date. |
| `cd1`–`cd4` | `distcd` | Derived digits of the four-digit legacy code. |

The crosswalk keys are `DisType`, `DisFreqType`, `DisPaymentType`,
`DisDetailType`, `DisTaxType`, `DisOrigCurType`, and `DisAmountSourceType`.
The CSV at `Signals/pyCode/utils/crsp_distribution_code_map.csv` is a
code-only projection of
`/yolobox/cellar/Manuals-and-Reference/CRSP-v2/CRSP_DistributionCode_SIZ_to_CIZ_Mapping.html`.
The original HTML has a unique `distcd` for every complete code tuple. Literal
`N/A` is a code value. Special cash dividends 1272 map from `DisType=SD`;
spinoffs 3762–3764 map from `DisType=SP` and differ in `DisTaxType`.

The original output key is `(permno, rcrddt, exdt, paydt, distcd)`. CIZ's
`DisSeqNbr` identifies distinct events when that key collides, but the legacy
schema has no sequence field. The script sorts by the output key and then by
`DisSeqNbr`, logs the removed count, and retains the lowest sequence. Six CIZ
rows are dropped in 1981; one retained amount differs materially from v1
because v1 retained the other event. Details: `Docs/CRSP-v2-Migration.md`.

Consumers: `DivInit` and `DivOmit` use `cd2`, ex-date and amount; `DivSeason`
and `DivYieldST` also use `cd1` and `cd3`; the `DivYield` and `DivYieldAnn`
placebos use every event's amount and ex-date. No inspected consumer uses
`facshr`, `rcrddt`, or `paydt` directly.

## Acquisition output

| Output | CIZ input | Rule |
|---|---|---|
| `permno` | `DisPERMNO` | Keep identifiers above 999 and distinct them; source ex-date must be present. |
| `SpinoffCo` | None | Set to integer one for every retained child. |

The v1 script used all distribution types, despite its spinoff output name.
Filtering on spinoff codes 3762–3764 would change the sample, so the CIZ script
retains the original all-event rule. `Spinoff.py` is the sole downstream
consumer. The only v1-only child in 1981 is identifier 3679, recoded as `-5`
in CIZ; it is absent from the frozen monthly stock panel.

## Verification

Run the two scripts with `DEBUG_MODE=True` in memory and
`OPENAP_DATA_ROOT=Signals/pyData-v2`, then run:

```sh
/opt/venv/projects/openap/bin/python3 Signals/tests/crsp_v2/compare.py CRSPdistributions
/opt/venv/projects/openap/bin/python3 Signals/tests/crsp_v2/compare.py m_CRSPAcquisitions
```

The comparison reports are in `Signals/pyData-v2/Logs/crsp_v2/`. Candidate
files match baseline schema and dtypes. Distribution coverage is 12,910 common
keys, four v1-only, zero v2-only. Acquisition coverage is 62 common children,
one v1-only, zero v2-only.
