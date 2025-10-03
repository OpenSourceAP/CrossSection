* --------------
// DATA LOAD
use permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
merge m:1 permno using "$pathDataIntermediate/IPODates", keep(master match) nogenerate 

// SIGNAL CONSTRUCTION
gen IndIPO = (time_avail_m - IPOdate <= 36) & (time_avail_m - IPOdate >= 3)
replace IndIPO = 0 if IPOdate == .
label var IndIPO "IPO 3 months to 3 years ago"

// SAVE
do "$pathCode/savepredictor" IndIPO
