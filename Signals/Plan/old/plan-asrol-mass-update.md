# Plan: update asrol everywhere to use GPT5 solution

Aug 15: the GPT5 solution handles edge cases that cause rare precision failures.
- implemented in `utils/asrol.py`
- `DivSeason.py` is the first script to use it.

## Task: update asrol everywhere to use GPT5 solution

Make sure the other asrol-related scripts use `asrol.py`. Make sure they do NOT use their own in-line implementations.

If the user requests a script, work on that one. Otherwise, work on the first TBC script in the list below.

## Progress Tracking
- CitationsRD.py
  - ✅ COMPLETED: Updated to use utils/asrol.py GPT5 solution
- DivInit.py
  - ✅ COMPLETED: Updated to use utils/asrol.py GPT5 solution via legacy wrapper
- DivOmit.py
  - ✅ COMPLETED: Updated to use utils/asrol.py GPT5 solution via legacy wrapper
- Herf.py
  - ✅ COMPLETED: Updated to use utils/asrol.py GPT5 solution via legacy wrapper
- HerfAsset.py
  - ✅ COMPLETED: Updated to use utils/asrol.py GPT5 solution via legacy wrapper
- HerfBE.py
  - ✅ COMPLETED: Updated to use utils/asrol.py GPT5 solution via legacy wrapper
- Investment.py
  - ✅ COMPLETED: Updated to use utils/asrol.py GPT5 solution via legacy wrapper
- MomOffSeason.py
  - ✅ COMPLETED: Updated to use utils/asrol.py GPT5 solution via legacy wrapper
- MomOffSeason06YrPlus.py
  - ✅ COMPLETED: Updated to use utils/asrol.py GPT5 solution via legacy wrapper
- MomOffSeason11YrPlus.py
  - ✅ COMPLETED: Updated to use utils/asrol.py GPT5 solution via legacy wrapper
- MomOffSeason16YrPlus.py
  - ✅ COMPLETED: Updated to use utils/asrol.py GPT5 solution via legacy wrapper
- MomVol.py
  - ✅ COMPLETED: Updated to use utils/asrol.py GPT5 solution via legacy wrapper
- RDAbility.py
  - ✅ COMPLETED: Updated to use utils/asrol.py GPT5 solution via legacy wrapper
- Recomm_ShortInterest.py
  - ✅ COMPLETED: Updated to use utils/asrol.py GPT5 solution via legacy wrapper
- TrendFactor.py
  - ✅ COMPLETED: Updated to use utils/asrol.py GPT5 solution via legacy wrapper
- VarCF.py
  - ✅ COMPLETED: Replaced inline implementation with utils/asrol.py GPT5 solution via legacy wrapper
- ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility.py
  - ✅ COMPLETED: Updated to use utils/asrol.py GPT5 solution via legacy wrapper
