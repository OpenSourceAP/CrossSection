* --------------
// DATA LOAD
use gvkey permno time_avail_m exchcd using "$pathDataIntermediate/SignalMasterTable", clear
xtset permno time_avail_m
// SIGNAL CONSTRUCTION
bys permno (time_avail_m): gen FirmAge = _n
* remove stuff we started with (don't have age for)
gen tempcrsptime = time_avail_m - mofd(mdy(7,1,1926)) + 1
replace FirmAge = . if tempcrsptime == FirmAge
replace FirmAge = . if exchcd != 1 
label var FirmAge "Firm Age"
// SAVE
do "$pathCode/savepredictor" FirmAge