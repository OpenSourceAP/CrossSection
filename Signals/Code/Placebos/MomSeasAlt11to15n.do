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
gen retLagTemp = l120.ret
asrol retLagTemp, by(permno) window(time_avail_m 59) stat(sum count) minimum(36)  
gen MomSeasAlt11to15n = (sum59_retLagTemp - retTemp1)/(count59_retLagTemp - retTemp2)
label var MomSeasAlt11to15n "Non-seasonal return (years 11-15)"
// SAVE
do "$pathCode/saveplacebo" MomSeasAlt11to15n