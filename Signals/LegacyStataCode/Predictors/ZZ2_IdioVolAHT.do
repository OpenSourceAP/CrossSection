* -------------
// DATA LOAD
use permno time_d ret using "$pathDataIntermediate/dailyCRSP.dta", clear
merge m:1 time_d using "$pathDataIntermediate/dailyFF", nogenerate keep(match) keepusing(rf mktrf)
replace ret = ret - rf
drop rf 
// SIGNAL CONSTRUCTION
* IdioVol as in HXZ citing Ali et al (2003)
bys permno (time_d): gen time_temp = _n
xtset permno time_temp
asreg ret mktrf, window(time_temp 252) min(100) by(permno) rmse
rename _rmse IdioVolAHT
gen time_avail_m = mofd(time_d)
format time_avail_m %tm
sort permno time_avail_m time_d
gcollapse (lastnm) IdioVolAHT, by(permno time_avail_m)
label var IdioVolAHT "Idiosyncratic Risk (AHT)"

// SAVE 
do "$pathCode/savepredictor" IdioVolAHT