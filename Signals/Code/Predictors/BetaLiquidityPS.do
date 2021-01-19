* BetaLiquidityPS
* --------------

// DATA LOAD
use permno time_avail_m ret using "$pathDataIntermediate/monthlyCRSP", clear
merge m:1 time_avail_m using "$pathDataIntermediate/monthlyFF", nogenerate keep(match) keepusing(rf mktrf hml smb)
merge m:1 time_avail_m using "$pathDataIntermediate/monthlyLiquidity", nogenerate keep(master match)

// SIGNAL CONSTRUCTION
gen retrf = ret - rf

bys permno (time_avail_m): gen time_temp = _n
xtset permno time_temp

asreg retrf ps_innov mktrf hml smb, window(time_temp 60) min(36) by(permno)

rename _b_ps_innov BetaLiquidityPS

label var BetaLiquidityPS "Pastor-Stambaugh liquidity beta"

// SAVE
do "$pathCode/savepredictor" BetaLiquidityPS