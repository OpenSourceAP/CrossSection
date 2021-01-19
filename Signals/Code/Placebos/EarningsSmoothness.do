* --------------
// DATA LOAD
use gvkey permno time_avail_m fyear ib at act lct che dlc dp at datadate using "$pathDataIntermediate/a_aCompustat", clear
// SIGNAL CONSTRUCTION
xtset gvkey fyear
gen tempEarnings = ib/l.at
gen tempCF       = (ib - ( (act - l.act) - (lct - l.lct) - (che - l.che) + (dlc - l.dlc) - dp))/l.at
asrol temp*, window(fyear 10) min(10) by(gvkey) stat(sd)
gen EarningsSmoothness = sd10_tempEarnings/sd10_tempCF
label var EarningsSmoothness "Earnings Smoothness"
* Expand to monthly
gen temp = 12
expand temp
drop temp
gen tempTime = time_avail_m
bysort gvkey tempTime: replace time_avail_m = time_avail_m + _n - 1 
drop tempTime
bysort gvkey time_avail_m (datadate): keep if _n == _N 
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
// SAVE
do "$pathCode/saveplacebo" EarningsSmoothness