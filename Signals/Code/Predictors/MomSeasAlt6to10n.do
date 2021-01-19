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
gen retLagTemp = l60.ret
asrol retLagTemp, by(permno) window(time_avail_m 59) stat(sum count) minimum(36)  
gen MomSeasAlt6to10n = (sum59_retLagTemp - retTemp1)/(count59_retLagTemp - retTemp2)
label var MomSeasAlt6to10n "Non-seasonal return (years 6-10)"
// SAVE
do "$pathCode/savepredictor" MomSeasAlt6to10n