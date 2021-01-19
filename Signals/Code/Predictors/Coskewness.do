* Coskewness
* --------------

// DATA LOAD
use permno time_avail_m ret using "$pathDataIntermediate/monthlyCRSP", clear
merge m:1 time_avail_m using "$pathDataIntermediate/monthlyFF", nogenerate keep(match) keepusing(rf mktrf hml smb)
merge m:1 time_avail_m using "$pathDataIntermediate/monthlyMarket",  nogenerate keep(match) keepusing(vwretd)

// SIGNAL CONSTRUCTION
gen retrf = ret - rf
gen vwmktrf = vwretd - rf

bys permno (time_avail_m): gen time_temp = _n
xtset permno time_temp

asreg retrf vwmktrf, window(time_temp 60) min(20) by(permno)
gen tempResid = retrf - _b_cons - _b_vwmktrf*vwmktrf

* Compute various moving averages
drop _N*
asrol vwmktrf, gen(meanX) stat(mean) window(time_temp 60) min(20) by(permno)
gen tempResidMkt = vwmktrf - meanX
drop meanX

gen tempNum1 = tempResid*(tempResidMkt^2)
asrol tempNum1, gen(tempNumerator) stat(mean) window(time_temp 60) min(20) by(permno)

gen tempResid2 = tempResid^2
asrol tempResid2, gen(tempDenom1) stat(mean) window(time_temp 60) min(20) by(permno)

gen tempResidMkt2 = tempResidMkt^2
asrol tempResidMkt2, gen(tempDenom2) stat(mean) window(time_temp 60) min(20) by(permno)

* Finally, calculate coskewness
gen Coskewness = tempNumerator/(sqrt(tempResid2)*tempResidMkt2)

label var Coskewness "Coskewness"

// SAVE
do "$pathCode/savepredictor" Coskewness