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

* We compute this with a trick: Use asrol to compute rolling sum and non-missing obs
* in specified window, then subtract seasonal part of returns from above and adjust denominator accordingly
gen retLagTemp = l12.ret
asrol retLagTemp, by(permno) window(time_avail_m 48) stat(sum) minimum(1) gen(retLagTemp_sum48)
asrol retLagTemp, by(permno) window(time_avail_m 48) stat(count) minimum(1) gen(retLagTemp_count48)

gen MomOffSeason = (retLagTemp_sum48 - retTemp1)/(retLagTemp_count48 - retTemp2)
label var MomOffSeason "Off-season long-term reversal"

// SAVE
do "$pathCode/savepredictor" MomOffSeason

