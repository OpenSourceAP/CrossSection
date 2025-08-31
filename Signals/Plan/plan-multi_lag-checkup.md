# Plan for multi_lag checkup

We changed stata_multi_lag to use fill_gaps = True by default. Some of the test results changed:

Numbers report the **FAILURE** rate. ❌ (100.00%) is BAD.

| Predictor                 | Python CSV | Superset   | NumRows       | Precision1   | Precision2              | T-stat     |
|---------------------------|------------|------------|---------------|--------------|-------------------------|------------|
| Mom6mJunk*                | ✅         | ❌ (12.76%) | ✅ (-11.8%)  | ✅ (0.0%)     | ✅ (2.6E-07)             | ✅ (+0.11)  |
| CompEquIss*               | ✅         | ✅ (0.73%) | ❌ (+17.9%)  | ✅ (0.0%)     | ✅ (2.1E-06)             | ❌ (+2.80)  |
| MomOffSeason06YrPlus      | ✅         | ✅ (0.00%) | ✅ (+1.9%)   | ❌ (1.3%)     | ❌ (3.5E+00)             | ❌ (+0.39)  |
| MomOffSeason              | ✅         | ✅ (0.00%) | ✅ (+1.2%)   | ✅ (0.9%)     | ❌ (2.2E+00)             | ❌ (+2.72)  |
| MomVol                    | ✅         | ✅ (0.00%) | ✅ (+0.1%)   | ✅ (0.2%)     | ❌ (3.5E-01)             | ❌ (-0.94)  |
| RDcap                     | ✅         | ✅ (0.02%) | ✅ (+3.9%)   | ✅ (0.0%)     | ✅ (3.7E-07)             | ✅ (-0.14)  |
| EarningsConsistency       | ✅         | ✅ (0.00%) | ✅ (+0.1%)   | ✅ (0.0%)     | ✅ (3.2E-07)             | ❌ (-3.53)  |
| MomSeason                 | ✅         | ✅ (0.00%) | ✅ (+1.1%)   | ✅ (0.0%)     | ✅ (3.0E-07)             | ❌ (-1.19)  |
| FirmAgeMom                | ✅         | ✅ (0.00%) | ✅ (+3.4%)   | ✅ (0.0%)     | ✅ (2.7E-07)             | ❌ (-1.83)  |
| Mom6m                     | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (2.6E-07)             | ✅ (+0.01)  |
| Mom12m                    | ✅         | ✅ (0.00%) | ✅ (+0.0%)   | ✅ (0.0%)     | ✅ (2.5E-07)             | ✅ (-0.03)  |
| MomSeasonShort            | ✅         | ✅ (0.00%) | ✅ (+0.3%)   | ✅ (0.0%)     | ✅ (1.7E-07)             | ❌ (-1.83)  |
| MomRev                    | ✅         | ✅ (0.46%) | ✅ (-0.2%)   | ✅ (0.0%)     | ✅ (0.0E+00)             | ✅ (-0.14)  |
| PS                        | ✅         | ✅ (0.00%) | ✅ (+0.1%)   | ✅ (0.0%)     | ✅ (0.0E+00)             | ✅ (+0.03)  |

## good examples of utils/ module implementations
- stata_multi_lag: CompEquIss.py
- asrol: TrendFactor.py
    - 