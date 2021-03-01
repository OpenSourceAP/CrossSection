* --------------
// DATA LOAD
use permno time_avail_m ret using "$pathDataIntermediate/SignalMasterTable", clear
// SIGNAL CONSTRUCTION
replace ret = 0 if mi(ret)
foreach n of numlist 191(12)240 {

gen temp`n' = l`n'.ret
}
egen retTemp1 = rowtotal(temp*), missing  
egen retTemp2 = rownonmiss(temp*)
gen MomSeason16YrPlus = retTemp1/retTemp2
label var MomSeason16YrPlus "Return Seasonality (16-20)"
// SAVE
do "$pathCode/savepredictor" MomSeason16YrPlus
