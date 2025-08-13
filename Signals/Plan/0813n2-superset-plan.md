# Plan: Fixing Major Superset Failures

## Context
**Important: Before you start, read these doc(s)**: 
- DocsForClaude/leg3-Predictors.md for the big picture

## Mission
Fix the Superset failures for the predictors described in the Initial Test Results below.
- Strategy: rewrite the Python code from scratch.
  - Read the Stata do file
  - Read DocsForClaude/traps.md
  - Given this information, think about how to translate the Stata code to Python.
  - Rewrite the Python code from scratch.
  - Test the Python code with `python3 utils/test_predictors.py --predictors [predictor_name]`

## Initial Test Results: 
August 13, 2025 1:00 PM

| Predictor                 | Python CSV | Columns  | Superset  | Precision1   | Precision2              |
|---------------------------|------------|----------|-----------|--------------|-------------------------|
| Recomm_ShortInterest      | ✅         | ✅       | ❌ (55.76%)  | ✅ (0.00%)    | ✅ (99th diff 0.0E+00)   |
| PatentsRD                 | ✅         | ✅       | ❌ (21.05%)  | ✅ (0.02%)    | ✅ (99th diff 0.0E+00)   |
| Mom6mJunk                 | ✅         | ✅       | ❌ (18.09%)  | ✅ (0.28%)    | ✅ (99th diff 1.0E-07)   |
| ShareVol                  | ✅         | ✅       | ❌ (17.95%)  | ✅ (0.00%)    | ✅ (99th diff 0.0E+00)   |
| sinAlgo                   | ✅         | ✅       | ❌ (15.87%)  | ✅ (0.01%)    | ✅ (99th diff 0.0E+00)   |
| RDAbility                 | ✅         | ✅       | ❌ (4.95%)   | ✅ (9.52%)    | ✅ (99th diff 9.5E-01)   |
| RIO_Volatility            | ✅         | ✅       | ❌ (4.44%)   | ✅ (4.32%)    | ✅ (99th diff 7.5E-01)   |

# Status Update

## Group 1: 
- Recomm_ShortInterest: TBC
- PatentsRD: TBC
- Mom6mJunk: TBC

## Group 2: 
- ShareVol: TBC
- sinAlgo: TBC
- RDAbility: TBC
- RIO_Volatility: TBC