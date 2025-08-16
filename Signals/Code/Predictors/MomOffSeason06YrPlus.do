* --------------
// DATA LOAD
use permno time_avail_m ret using "$pathDataIntermediate/SignalMasterTable", clear

// SIGNAL CONSTRUCTION
replace ret = 0 if mi(ret)

* CHECKPOINT 1: After ret replacement
list permno time_avail_m ret if permno == 83382 & time_avail_m == tm(2005m10)
list permno time_avail_m ret if permno == 33268 & time_avail_m == tm(1983m11)

foreach n of numlist 71(12)119 {

gen temp`n' = l`n'.ret
}

* CHECKPOINT 2: After seasonal lag creation
list permno time_avail_m temp71 temp83 temp95 temp107 temp119 if permno == 83382 & time_avail_m == tm(2005m10)
list permno time_avail_m temp71 temp83 temp95 temp107 temp119 if permno == 33268 & time_avail_m == tm(1983m11)

egen retTemp1 = rowtotal(temp*), missing  
egen retTemp2 = rownonmiss(temp*)

* CHECKPOINT 3: After seasonal aggregation
list permno time_avail_m retTemp1 retTemp2 if permno == 83382 & time_avail_m == tm(2005m10)
list permno time_avail_m retTemp1 retTemp2 if permno == 33268 & time_avail_m == tm(1983m11)

gen retLagTemp = l60.ret
asrol retLagTemp, by(permno) window(time_avail_m 60) stat(sum) minimum(1) gen(retLagTemp_sum60)
asrol retLagTemp, by(permno) window(time_avail_m 60) stat(count) minimum(1) gen(retLagTemp_count60)

* CHECKPOINT 4: After rolling momentum calculation
list permno time_avail_m retLagTemp retLagTemp_sum60 retLagTemp_count60 if permno == 83382 & time_avail_m == tm(2005m10)
list permno time_avail_m retLagTemp retLagTemp_sum60 retLagTemp_count60 if permno == 33268 & time_avail_m == tm(1983m11)

gen MomOffSeason06YrPlus = (retLagTemp_sum60 - retTemp1)/(retLagTemp_count60 - retTemp2)

* CHECKPOINT 5: After final calculation
list permno time_avail_m MomOffSeason06YrPlus retLagTemp_sum60 retTemp1 retLagTemp_count60 retTemp2 if permno == 83382 & time_avail_m == tm(2005m10)
list permno time_avail_m MomOffSeason06YrPlus retLagTemp_sum60 retTemp1 retLagTemp_count60 retTemp2 if permno == 33268 & time_avail_m == tm(1983m11)

label var MomOffSeason06YrPlus "Off-season reversal years 6 to 10"

// SAVE
do "$pathCode/savepredictor" MomOffSeason06YrPlus

