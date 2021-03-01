* --------------------------------------
// DATA LOAD
use permno time_d ret using "$pathDataIntermediate/dailyCRSP.dta", clear
merge m:1 time_d using "$pathDataIntermediate/dailyFF", nogenerate keep(match) keepusing(rf mktrf)
replace ret = ret - rf
drop rf 
// SIGNAL CONSTRUCTION
* Set up CAPM to estimate idiovol
bys permno (time_d): gen time_temp = _n
xtset permno time_temp
* CAPM 
asreg ret mktrf, window(time_temp 20) min(15) by(permno) rmse
rename _rmse IdioRisk
gen epsReturnCAPM = ret - _b_cons - _b_mktrf*mktrf  // This is idiosyncratic return, skew computed below
drop if mi(IdioRisk)
gen time_avail_m = mofd(time_d)
format time_avail_m %tm
sort permno time_avail_m time_d
gcollapse (lastnm) IdioRisk (sd) IdioVolCAPM = epsReturnCAPM, by(permno time_avail_m)
label var IdioRisk "Idiosyncratic Risk"
label var IdioVolCAPM "Idiosyncratic Risk (CAPM)"

// SAVE 
do "$pathCode/savepredictor" IdioRisk
do "$pathCode/saveplacebo" IdioVolCAPM
