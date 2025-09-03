# Plan for patching Option Metrics Implied Vol signals

In 2024-08, we found that Option Metrics had significantly revised their implied vol calculations, leading to a sharp drop in predictor performance.
See https://github.com/OpenSourceAP/CrossSection/issues/156.

Eventually, we hope to re-do the implied vol calculations ourselves to replicate the original papers. But for now, we'll continue to patch by using the 2023-08 vintage of the data.

## Task 

Work on only one script at a time.

For the script you are working on:

- At the beginning of add a check for whether `pyCode/config.py` `PATCH_OPTIONM_IV == True`. 
- If true, use the `openassetpricing` package to download the 2023 vintage and stop the script there.
```python
print("WARNING: PATCH_OPTIONM_IV is True, using 2023 vintage from openassetpricing")
print("See https://github.com/OpenSourceAP/CrossSection/issues/156")
from openassetpricing import OpenAP
openap = OpenAP(2023)
df = openap.dl_signal('polars', ['dVolCall'])
df = df.rename({'yyyymm': 'time_avail_m'})
save_predictor(df, 'dVolCall')
sys.exit()
```
- try running the script.
- fix errors
    - unlike other tasks, do **not** run `utils/test_predictor.py`. It won't match by construction.
- update the progress tracking below
    - mark with ✅ if the script is patched and the script runs
    

## Progress Tracking

1. CPVolSpread.py ✅
2. dVolCall.py ✅
3. dVolPut.py ✅
4. dCPVolSpread.py ✅
5. RIVolSpread.py ✅
6. SmileSlope.py ✅
7. skew1.py ✅