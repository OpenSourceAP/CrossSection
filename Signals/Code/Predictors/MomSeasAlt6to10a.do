* --------------
// DATA LOAD
use permno time_avail_m ret using "$pathDataIntermediate/SignalMasterTable", clear
// SIGNAL CONSTRUCTION
replace ret = 0 if mi(ret)
foreach n of numlist 71(12)120 {

gen temp`n' = l`n'.ret
}
egen retTemp1 = rowtotal(temp*), missing  
egen retTemp2 = rownonmiss(temp*)
gen MomSeasAlt6to10a = retTemp1/retTemp2
label var MomSeasAlt6to10a "Return Seasonality (6-10)"
// SAVE
do "$pathCode/savepredictor" MomSeasAlt6to10a