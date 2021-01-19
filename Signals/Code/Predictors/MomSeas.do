* --------------
// DATA LOAD
use permno time_avail_m ret using "$pathDataIntermediate/SignalMasterTable", clear
// SIGNAL CONSTRUCTION
replace ret = 0 if mi(ret)
foreach n of numlist 11(12)60 {

gen temp`n' = l`n'.ret
}
egen retTemp1 = rowtotal(temp*), missing  // Quick way to take mean only over non-missing values
egen retTemp2 = rownonmiss(temp*)
gen MomSeas = retTemp1/retTemp2
label var MomSeas "Return Seasonality"
// SAVE
do "$pathCode/savepredictor" MomSeas