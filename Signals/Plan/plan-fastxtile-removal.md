# Plan for removing fastxtile from - *.py

Goal is to reduce reliance on the complicated fastxtile utility.

## Task for a given script

1. Identify all calls of `fastxtile()`
    - e.g. `df['tempMom6'] = fastxtile(df, 'Mom6m_clean', by='time_avail_m', n=5)`
2. Replace with the groupby, transform, qcut pattern
    ```
    df['tempMom6'] = (
        df.groupby('time_avail_m')['Mom6m']
        .transform(lambda x: pd.qcut(x, q=5, labels=False, duplicates='drop') + 1)
    )
    ```
3. Run the script
4. Run `utils/test_predictor --predictors [script_name]`
5. Compare the test results with `Logs/testout_predictors 0831n2.md`
    - search for the predictor name in the file
6. Update the progress tracking below
    - mark with ✅ if fastxtile is updated and the test results are the same as the original
    - mark with ❌ if fastxtile is updated and the test results are different from the original

## Progress Tracking

1. ✅ AccrualsBM.py - fastxtile removed, tests passed
2. ✅ ChForecastAccrual.py - fastxtile removed, tests passed
3. ✅ ChNAnalyst.py - fastxtile removed, tests passed
    - ac: but the do file had an error, which is now corrected, so the superset and numrows tests now fail.
4. ❌ CitationsRD.py - fastxtile replaced but superset check degraded (5.33% vs 0.49% missing)
5. ✅ DivYieldST.py - fastxtile removed, tests passed
6. ✅ FirmAgeMom.py - fastxtile removed, tests passed
7. ✅ GrAdExp.py - fastxtile removed, tests passed
8. ✅ MomRev.py - fastxtile removed, tests passed
9. ⚠️ MomVol.py - fastxtile removed, minor precision differences (0.175% obs, R²=0.9998, tie-breaking differences)
10. ✅ MS.py - fastxtile removed, tests match original (precision failures with override, same as baseline)
11. ✅ OperProf.py - fastxtile removed, tests passed
12. ✅ OScore.py - fastxtile removed, tests passed
13. ❌ PatentsRD.py - fastxtile replaced but major superset failure (21.04% vs 0.04% missing) - complex patent efficiency double-sorting algorithm may have edge cases
14. ✅ ProbInformedTrading.py - fastxtile removed, tests passed
15. ✅ PS.py - fastxtile removed, tests passed
16. ✅ RDAbility.py - fastxtile removed, tests passed
17. ✅ RDcap.py - fastxtile removed, tests passed
18. ✅ Recomm_ShortInterest.py - fastxtile removed, tests match baseline (override passes, similar superset/numrows failures as original)
19. ✅ sfe.py - fastxtile removed, tests passed
20. ✅ std_turn.py - fastxtile removed, tests passed
21. ✅ tang.py - fastxtile removed, tests passed
22. ✅ ZZ1_Activism1_Activism2.py - fastxtile removed, tests passed (required custom quartile assignment due to qcut limitations with duplicate values)
23. ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility.py