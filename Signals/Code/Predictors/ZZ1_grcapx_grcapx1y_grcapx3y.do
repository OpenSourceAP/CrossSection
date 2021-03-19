* --------------
// DATA LOAD
use gvkey permno time_avail_m capx ppent at using "$pathDataIntermediate/m_aCompustat", clear
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(using match) nogenerate keepusing(exchcd)
// SIGNAL CONSTRUCTION
* Need Firm Age
bys permno (time_avail_m): gen FirmAge = _n
* remove stuff we started with (don't have age for)
gen tempcrsptime = time_avail_m - mofd(mdy(7,1,1926)) + 1
replace FirmAge = . if tempcrsptime == FirmAge
*replace FirmAge = . if exchcd != 1   // Restriction for FirmAge but not for grcapx1y?
replace capx = ppent - l12.ppent if capx ==. & FirmAge >=24

gen grcapx = (capx-l24.capx)/l24.capx 
gen grcapx1y = (l12.capx-l24.capx)/l24.capx 
gen grcapx3y = capx/(l12.capx + l24.capx + l36.capx )*3

label var grcapx "Change in capex (two years)" 
label var grcapx1y "Change in capex (one year)" 
label var grcapx3y "Change in capex (three years)" 

// SAVE 
do "$pathCode/savepredictor" grcapx
do "$pathCode/saveplacebo" grcapx1y
do "$pathCode/savepredictor" grcapx3y
