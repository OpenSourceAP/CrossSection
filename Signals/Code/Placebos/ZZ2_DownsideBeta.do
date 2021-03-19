* --------------
// DATA LOAD
* Rolling averages of market excess return
use "$pathDataIntermediate/dailyFF"
sort time_d
gen time_temp = _n
asrol mktrf, window(time_temp 252) stat(mean) gen(mu_market) min(252)
keep if mktrf < mu_market  // Keep only if return less than mean of market over previous year
keep time_d mktrf rf
save "$pathtemp/tempPlacebo", replace
use permno time_d ret using "$pathDataIntermediate/dailyCRSP.dta", clear
merge m:1 time_d using "$pathtemp/tempPlacebo", nogenerate keep(master match)
replace ret = ret - rf
drop rf 
// SIGNAL CONSTRUCTION
* Compute downside beta
bys permno (time_d): gen time_temp = _n
xtset permno time_temp
asreg ret mktrf, window(time_temp 252) min(50) by(permno)
rename _b_mktrf DownsideBeta
gen time_avail_m = mofd(time_d)
format time_avail_m %tm
sort permno time_avail_m time_d
gcollapse (lastnm) DownsideBeta, by(permno time_avail_m)
label var DownsideBeta "Downside beta"

// SAVE
do "$pathCode/saveplacebo" DownsideBeta