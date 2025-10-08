* --------------
// DATA LOAD
use gvkey permno time_avail_m revt using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m
gen temp = log(revt) - log(l12.revt)
gsort time_avail_m -temp
by time_avail_m: gen tempRank = _n if temp !=.
xtset permno time_avail_m
 
gen MeanRankRevGrowth = (5*l12.tempRank + 4* l24.tempRank + 3*l36.tempRank + ///
    2*l48.tempRank  + l60.tempRank)/15

drop temp*
label var MeanRankRevGrowth "Average Revenue Growth"
// SAVE
do "$pathCode/savepredictor" MeanRankRevGrowth