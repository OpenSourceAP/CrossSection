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
gen retLagTemp = l180.ret
asrol retLagTemp, by(permno) window(time_avail_m 59) stat(sum count) minimum(36)  
gen MomSeasAlt16to20n = (sum59_retLagTemp - retTemp1)/(count59_retLagTemp - retTemp2)
label var MomSeasAlt16to20n "Non-seasonal return (years 16-20)"
// SAVE
do "$pathCode/savepredictor" MomSeasAlt16to20n