# Plan for standardizing lags and rolling windows (again)
2025-08-28

It's true that Stata's lag and rolling functions naturally handle calendar gaps. But we don't need to make ours so complicated.

All we need to do is fill in the date gaps before doing standard row-based lags. 

## Current status:
- `utils/stata_replication.py`
    - `fill_date_gaps_pl` function is good. But could do with more testing.
    - `fill_date_gaps` function is the pandas version. It could be improved (needs at least a period argument).
    - `stata_multi_lag_pl`: not used anywhere. needs testing. Maybe not needed.
    - `stata_multi_lag`: (pandas) used a lot but not needed. Wayyy too complicated. **SIMPLIFY**
- `utils/asrol.py`
    - `asrol_fast`: row based lags for either polars or pandas.
    - `asrol_calendar`: calendar based lags for polars. It's not that complicated but it's still really not needed. **SIMPLIFY**
    - `asrol_calendar_pd`: pandas wrapper for `asrol_calendar`. Once again needlessly complicated. *SIMPLIFY*
- `utils/asreg.py`: TBC

## Tasks

1. Build out a robust `fill_date_gaps` function that can handle all the different cases.
    - Build on `fill_date_gaps_pl`
    - Make a pandas version ✅
    - Add a wrapper for both ✅
    - Test on ✅
        - PS.py ✅
        - RDcap.py ✅
        - ZZ2_AbnormalAccruals_AbnormalAccrualsPercent.py 
2. Build out a simple and robust `stata_multi_lag` function
    - The idea is to just make sure we don't make mistakes by forgetting to fill in the date gaps.
    - It should just call `fill_date_gaps` by default and then do standard pandas or polars groupby lags.
    - There should be an option to not fill in the date gaps for speed. But default should be to fill in the date gaps.
    - Test on the following
        CitationsRD.py
        CompEquIss.py
        EarningsConsistency.py
        FirmAgeMom.py
        Mom12m.py
        Mom6m.py
        MomOffSeason.py
        MomOffSeason06YrPlus.py
        MomOffSeason11YrPlus.py
        MomOffSeason16YrPlus.py
        MomRev.py
        MomSeason.py
        MomSeason06YrPlus.py
        MomSeason11YrPlus.py
        MomSeason16YrPlus.py
        MomSeasonShort.py
        MomVol.py
        PS.py
        RDcap.py    
3. Add a 