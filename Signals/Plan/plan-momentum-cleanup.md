# Plan for momentum cleanup

The goal is to make sure all momentum scripts are nice and clean. They should use these functions from utils/*.py:
- stata_multi_lag for lag operations
- asrol for rolling operations
- save_predictor for saving the results

If the script is already nice and clean, mark it with ✅.
If it is not, fix it, and then mark it with ✅.
For scripts that are messy, translate it from the Stata do file from scratch, line by line.
- Omit the main() function. Keep everything linear.

## Progress Tracking

Group 1
- Mom12m.py ✅
- Mom12mOffSeason.py ✅
- Mom6m.py ✅
- Mom6mJunk.py ✅
- MomRev.py ✅
- MomVol.py ✅

Group 2
- MomOffSeason.py ✅
- MomOffSeason06YrPlus.py ✅
- MomOffSeason11YrPlus.py ✅
- MomOffSeason16YrPlus.py ✅

Group 3
- MomSeason.py ✅
- MomSeason06YrPlus.py ✅
- MomSeason11YrPlus.py ✅
- MomSeason16YrPlus.py ✅
- MomSeasonShort.py ✅

