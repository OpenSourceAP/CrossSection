* --------------
// DATA LOAD
use permno time_avail_m ret using "$pathDataIntermediate/SignalMasterTable", clear

// SIGNAL CONSTRUCTION
replace ret = 0 if mi(ret)
foreach n of numlist 131(12)179 {

gen temp`n' = l`n'.ret
}
egen retTemp1 = rowtotal(temp*), missing  
egen retTemp2 = rownonmiss(temp*)

gen retLagTemp = l120.ret
asrol retLagTemp, by(permno) window(time_avail_m 60) stat(sum count) minimum(1)  
gen MomOffSeason11YrPlus = (sum60_retLagTemp - retTemp1)/(count60_retLagTemp - retTemp2)

label var MomOffSeason11YrPlus "Off season reversal years 11 to 15"

// SAVE
do "$pathCode/savepredictor" MomOffSeason11YrPlus
