* --------------
// DATA LOAD
use permno time_avail_m ret using "$pathDataIntermediate/SignalMasterTable", clear

// SIGNAL CONSTRUCTION
replace ret = 0 if mi(ret)

* CHECKPOINT 1: After replacing missing returns with 0
list permno time_avail_m ret if permno == 89169 & time_avail_m == tm(2021m5)

foreach n of numlist 23(12)59 {

gen temp`n' = l`n'.ret
}

* CHECKPOINT 2: After creating seasonal lag variables
list permno time_avail_m temp23 temp35 temp47 temp59 if permno == 89169 & time_avail_m == tm(2021m5)

egen retTemp1 = rowtotal(temp*), missing  // Quick way to take mean only over non-missing values
egen retTemp2 = rownonmiss(temp*)

* CHECKPOINT 3: After calculating seasonal totals
list permno time_avail_m retTemp1 retTemp2 if permno == 89169 & time_avail_m == tm(2021m5)

* We compute this with a trick: Use asrol to compute rolling sum and non-missing obs
* in specified window, then subtract seasonal part of returns from above and adjust denominator accordingly
gen retLagTemp = l12.ret

* CHECKPOINT 4: After creating 12-month lag
list permno time_avail_m retLagTemp if permno == 89169 & time_avail_m == tm(2021m5)

asrol retLagTemp, by(permno) window(time_avail_m 48) stat(sum) minimum(1) gen(retLagTemp_sum48)
asrol retLagTemp, by(permno) window(time_avail_m 48) stat(count) minimum(1) gen(retLagTemp_count48)

* CHECKPOINT 5: After rolling calculations
list permno time_avail_m retLagTemp_sum48 retLagTemp_count48 if permno == 89169 & time_avail_m == tm(2021m5)

gen MomOffSeason = (retLagTemp_sum48 - retTemp1)/(retLagTemp_count48 - retTemp2)

* CHECKPOINT 6: After final calculation
list permno time_avail_m MomOffSeason retLagTemp_sum48 retTemp1 retLagTemp_count48 retTemp2 if permno == 89169 & time_avail_m == tm(2021m5)
label var MomOffSeason "Off-season long-term reversal"

// SAVE
do "$pathCode/savepredictor" MomOffSeason

