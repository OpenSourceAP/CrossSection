* --------------
// DATA LOAD
use permno time_avail_m ret using "$pathDataIntermediate/SignalMasterTable", clear

// SIGNAL CONSTRUCTION
replace ret = 0 if mi(ret)
foreach n of numlist 191(12)239 {

gen temp`n' = l`n'.ret
}
egen retTemp1 = rowtotal(temp*), missing  
egen retTemp2 = rownonmiss(temp*)

gen retLagTemp = l180.ret
asrol retLagTemp, by(permno) window(time_avail_m 60) stat(sum count) minimum(36)  

gen MomOffSeason16YrPlus = (sum60_retLagTemp - retTemp1)/(count60_retLagTemp - retTemp2)
label var MomOffSeason16YrPlus "Off season reversal years 16 to 20"

// SAVE
do "$pathCode/savepredictor" MomOffSeason16YrPlus
