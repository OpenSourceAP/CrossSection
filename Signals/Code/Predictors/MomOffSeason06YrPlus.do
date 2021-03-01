* --------------
// DATA LOAD
use permno time_avail_m ret using "$pathDataIntermediate/SignalMasterTable", clear

// SIGNAL CONSTRUCTION
replace ret = 0 if mi(ret)
foreach n of numlist 71(12)119 {

gen temp`n' = l`n'.ret
}
egen retTemp1 = rowtotal(temp*), missing  
egen retTemp2 = rownonmiss(temp*)

gen retLagTemp = l60.ret
asrol retLagTemp, by(permno) window(time_avail_m 60) stat(sum count) minimum(1)  
gen MomOffSeason06YrPlus = (sum60_retLagTemp - retTemp1)/(count60_retLagTemp - retTemp2)

label var MomOffSeason06YrPlus "Off-season reversal years 6 to 10"

// SAVE
do "$pathCode/savepredictor" MomOffSeason06YrPlus

