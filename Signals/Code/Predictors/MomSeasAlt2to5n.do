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
* We compute this with a trick: Use asrol to compute rolling sum and non-missing obs
* in specified window, then subtract seasonal part of returns from above and adjust denominator accordingly
gen retLagTemp = ret
asrol retLagTemp, by(permno) window(time_avail_m 59) stat(sum count) minimum(36)  // 59 because current obs is also part of calculations (predictions for t+1)
gen MomSeasAlt2to5n = (sum59_retLagTemp - retTemp1)/(count59_retLagTemp - retTemp2)
label var MomSeasAlt2to5n "Non-seasonal return (years 2-5)"
// SAVE
do "$pathCode/savepredictor" MomSeasAlt2to5n