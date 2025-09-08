# Quarterly Placebo Missing Data Analysis Framework

**Date**: 2025-09-04  
**Purpose**: Rigorous analysis of why quarterly placebos are failing superset tests

## Overview Framework

For each failing quarterly placebo, follow this structure:

### Part 1: Overall Coverage Analysis
1. **Total missing placebo observations**: X (observations that exist in Stata's {placebo}.csv but NOT in Python's {placebo}.csv)
2. **Y cases**: Missing placebo observations caused by Python missing intermediate {variables} data entirely ({var}_python = null, {var}_stata has values)
3. **Z cases**: Missing placebo observations that occur even though BOTH datasets have identical intermediate {variables} data ({var}_python = {var}_stata = same_value)

### Part 2: Rigorous Verification of Non-Intermediate Issues
For the Z cases where intermediate data matches:

1. **Extract specific combinations**: Take those Z specific gvkey+time_avail_m combinations where both datasets show matching {variable} values
2. **Verify existence**: Confirm these combinations actually exist in both intermediate m_QCompustat datasets
3. **Trace placebo logic**: Follow the placebo calculation step-by-step to identify why these observations fail to produce output despite having required input data
   - Check SignalMasterTable merging
   - Verify lag operations (stata_multi_lag vs Stata's lag syntax)
   - Examine filtering conditions
   - Review any other processing steps

## Complete Placebo List to Analyze

Full list of quarterly placebos failing superset tests:

1. **KZ_q**
2. **OperProfRDLagAT_q**
3. **EntMult_q** 
4. **PS_q**
5. **NetDebtPrice_q**
6. **Tax_q**
7. **Leverage_q**
8. **OPLeverage_q**
9. **EBM_q**
10. **AssetGrowth_q**
11. **AssetLiquidityMarketQuart**
12. **AssetTurnover_q**
13. **CapTurnover_q**
14. **EPq**
15. **sgr_q**
16. **WW_Q**
17. **AssetLiquidityBookQuart**
18. **SP_q**

**Analysis Order**: Start with placebos already analyzed (AssetGrowth_q, OperProfRDLagAT_q, EPq, sgr_q) then proceed systematically through the remaining 14.

## Implementation Steps

1. **Modify check-missing.py**: Update script to follow this framework exactly
2. **Create detailed reports**: Generate complete analysis for each placebo
3. **Document findings**: Store results in Debug/quarterly_placebos.md following the two-part structure
4. **Focus on actionable insights**: Prioritize cases where we can fix Python processing logic

## Expected Outcomes

- **Clear categorization**: Separate intermediate data issues from placebo logic issues  
- **Actionable fixes**: Identify specific code changes needed in Python placebos
- **Root cause analysis**: Understand whether issues are in data processing or calculation logic