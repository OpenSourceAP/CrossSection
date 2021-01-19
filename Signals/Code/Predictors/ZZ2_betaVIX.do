* betaVIX
* -----------------------

// DATA LOAD
use permno time_d ret using "$pathDataIntermediate/dailyCRSP.dta", clear

merge m:1 time_d using "$pathDataIntermediate/dailyFF", nogenerate keep(match) keepusing(rf mktrf)
replace ret = ret - rf
drop rf 

merge m:1 time_d using "$pathDataIntermediate/d_vix", nogenerate keep(match) keepusing(dVIX)

// SIGNAL CONSTRUCTION

* Set up CAPM to estimate systematic volatility
bys permno (time_d): gen time_temp = _n
xtset permno time_temp

asreg ret mktrf dVIX, window(time_temp 20) min(15) by(permno)
rename _b_dVIX betaVIX

gen time_avail_m = mofd(time_d)
format time_avail_m %tm

sort permno time_avail_m time_d
gcollapse (lastnm) betaVIX , by(permno time_avail_m)

label var betaVIX "Systematic volatility"

// SAVE 
do "$pathCode/savepredictor" betaVIX