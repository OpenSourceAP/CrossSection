# Plan for standardizing lags and rolling windows (again)
2025-08-28

It's true that Stata's lag and rolling functions naturally handle calendar gaps. But we don't need to make ours so complicated.

All we need to do is fill in the date gaps before doing standard row-based lags. 

## Current status:
- `utils/stata_replication.py`
    - `fill_date_gaps`: a clean wrapper
    - `stata_multi_lag`: a clean wrapper
- `utils/asrol.py`
    - `asrol`: a wrapper that cleanly uses fill_date_gaps and then just does row based lagging.
- `utils/asreg.py`: TBC

## Tasks

1. Build out a robust `fill_date_gaps` function that can handle all the different cases.
    - Build on `fill_date_gaps_pl`
    - Make a pandas version ✅
    - Add a wrapper for both ✅
    - Test on ✅
        - PS.py ✅
        - RDcap.py ✅
        - ZZ2_AbnormalAccruals_AbnormalAccrualsPercent.py ✅
2. Build out a simple and robust `stata_multi_lag` function
    - The idea is to just make sure we don't make mistakes by forgetting to fill in the date gaps.
    - It should just call `fill_date_gaps` by default and then do standard pandas or polars groupby lags.
    - There should be an option to not fill in the date gaps for speed. But default should be to fill in the date gaps.
    - Test on the following
        CitationsRD.py ✅
        CompEquIss.py ✅
        EarningsConsistency.py ✅
        FirmAgeMom.py ✅
        Mom12m.py ✅
        Mom6m.py ✅
        MomOffSeason.py ✅
        MomOffSeason06YrPlus.py ✅
        MomOffSeason11YrPlus.py ✅
        MomOffSeason16YrPlus.py ✅
        MomRev.py ✅
        MomSeason.py ✅
        MomSeason06YrPlus.py ✅
        MomSeason11YrPlus.py ✅
        MomSeason16YrPlus.py ✅
        MomSeasonShort.py ✅
        MomVol.py ✅
        PS.py ✅
        RDcap.py ✅
3. Build a simple and robust `asrol` function
    - Start with `asrol_pl`, a polars-only version. ✅
        - This version should just call `fill_date_gaps` by default and then do standard polars .rolling_STATNAME, e.g. 
            df.group_by('group').agg(
                pl.col('value').rolling_mean(window_size=3)
            )
    - Build a wrapper `asrol` that either just calls `asrol_pl` directly, or first transforms the data to polars if the data is pandas (and then transforms back). ✅
    - Test on the following    
        CitationsRD.py ✅
        DivInit.py ✅
        DivOmit.py ✅
        DivSeason.py ✅
        Herf.py ✅
        HerfAsset.py ✅
        HerfBE.py ✅
        Investment.py ✅
        Mom12mOffSeason.py ✅
        MomOffSeason.py ✅
        MomOffSeason06YrPlus.py ✅
        MomOffSeason11YrPlus.py ✅
        MomOffSeason16YrPlus.py ✅
        MomVol.py ✅
        MS.py: failing for some reason
        RDAbility.py: failing for some reason
        Recomm_ShortInterest.py ✅
        TrendFactor.py ✅
        VarCF.py ✅
        ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility.py ✅
    - Delete unnecessary asrol functions

    