* --------------
// DATA LOAD
use permno time_avail_m ret using "$pathDataIntermediate/SignalMasterTable", clear

// SIGNAL CONSTRUCTION
replace ret = 0 if mi(ret)
foreach n of numlist 23(12)59 {
	gen temp`n' = l`n'.ret
}

egen retTemp1 = rowtotal(temp*), missing  // Quick way to take mean only over non-missing values
egen retTemp2 = rownonmiss(temp*)

gen MomSeason = retTemp1/retTemp2
label var MomSeason "Return Seasonality (years 2 to 5)"

// SAVE
do "$pathCode/savepredictor" MomSeason

