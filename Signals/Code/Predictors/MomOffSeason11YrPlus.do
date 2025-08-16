* --------------
// DATA LOAD
use permno time_avail_m ret using "$pathDataIntermediate/SignalMasterTable", clear

// SIGNAL CONSTRUCTION
replace ret = 0 if mi(ret)

* CHECKPOINT 1: After data load and ret replacement
list permno time_avail_m ret if permno == 75302 & time_avail_m == tm(1993m12)

foreach n of numlist 131(12)179 {

gen temp`n' = l`n'.ret
}

* CHECKPOINT 2: After seasonal lag creation  
list permno time_avail_m temp131 temp143 temp155 temp167 temp179 if permno == 75302 & time_avail_m == tm(1993m12)

egen retTemp1 = rowtotal(temp*), missing  
egen retTemp2 = rownonmiss(temp*)

* CHECKPOINT 3: After seasonal calculations
list permno time_avail_m retTemp1 retTemp2 if permno == 75302 & time_avail_m == tm(1993m12)

gen retLagTemp = l120.ret
asrol retLagTemp, by(permno) window(time_avail_m 60) stat(sum) minimum(1) gen(retLagTemp_sum60)
asrol retLagTemp, by(permno) window(time_avail_m 60) stat(count) minimum(1) gen(retLagTemp_count60)

* CHECKPOINT 4: After 60-month rolling calculations
list permno time_avail_m retLagTemp retLagTemp_sum60 retLagTemp_count60 if permno == 75302 & time_avail_m == tm(1993m12)

gen MomOffSeason11YrPlus = (retLagTemp_sum60 - retTemp1)/(retLagTemp_count60 - retTemp2)

* CHECKPOINT 5: After final calculation
list permno time_avail_m MomOffSeason11YrPlus retLagTemp_sum60 retTemp1 retLagTemp_count60 retTemp2 if permno == 75302 & time_avail_m == tm(1993m12)

label var MomOffSeason11YrPlus "Off season reversal years 11 to 15"

// SAVE
do "$pathCode/savepredictor" MomOffSeason11YrPlus
