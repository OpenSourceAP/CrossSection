# Plan for updating predictors to use mve_permco instead of mve_c

Due to data structure changes, we need to update predictors that currently use `mve_c` to use `mve_permco` instead. This ensures consistency with the new market value calculation methodology.

## Task 

Work on only one script at a time.

For the script you are working on:

- Search for all instances of `mve_c` in the file
- Replace `mve_c` with `mve_permco` 
- Ensure the script still runs without errors
- Run `python utils/test_predictor.py <predictor_name>` to verify the changes
- Update the progress tracking below
    - Mark with ✅ if the script is updated and tests pass

## Progress Tracking

1. AccrualsBM.py
2. AdExp.py
3. AM.py
4. BM.py
5. CashProd.py
6. CBOperProf.py
7. CF.py
8. cfp.py
9. ChNAnalyst.py
10. CitationsRD.py
11. CompEquIss.py
12. DebtIssuance.py
13. DelBreadth.py
14. EarnSupBig.py
15. EntMult.py
16. EP.py
17. Frontier.py
18. Governance.py
19. GrAdExp.py
20. IndMom.py
21. IndRetBig.py
22. Leverage.py
23. MS.py
24. NetDebtPrice.py
25. NetPayoutYield.py
26. OperProf.py
27. OperProfRD.py
28. PatentsRD.py
29. PayoutYield.py
30. ProbInformedTrading.py
31. PS.py
32. RD.py
33. RDcap.py
34. RevenueSurprise.py
35. roaq.py
36. sfe.py
37. Size.py
38. SP.py
39. std_turn.py
40. TrendFactor.py
41. VarCF.py
42. VolMkt.py
43. ZZ1_Activism1_Activism2.py
44. ZZ1_AnalystValue_AOP_PredictedFE_IntrinsicValue.py
45. ZZ1_EBM_BPEBM.py
46. ZZ1_FR_FRbook.py
47. ZZ1_IntanBM_IntanSP_IntanCFP_IntanEP.py
48. ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility.py