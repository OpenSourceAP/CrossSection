* --------------
// DATA LOAD
use permno time_avail_m ret using "$pathDataIntermediate/SignalMasterTable", clear
// SIGNAL CONSTRUCTION
replace ret = 0 if mi(ret)
foreach n of numlist 131(12)180 {

gen temp`n' = l`n'.ret
}
egen retTemp1 = rowtotal(temp*), missing  
egen retTemp2 = rownonmiss(temp*)
gen MomSeasAlt11to15a = retTemp1/retTemp2
label var MomSeasAlt11to15a "Return Seasonality (11-15)"
// SAVE
do "$pathCode/savepredictor" MomSeasAlt11to15a