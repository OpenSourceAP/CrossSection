* --------
// DATA LOAD
use "$pathDataIntermediate/dailyCRSP.dta", clear
// SIGNAL CONSTRUCTION
gen time_avail_m = mofd(time_d)
format time_avail_m %tm
gen prcadj = abs(prc)/cfacshr
gcollapse (max) maxpr = prcadj (lastnm) prcadj, by(permno time_avail_m)
xtset permno time_avail_m
gen temp = max(l1.maxpr, l2.maxpr, l3.maxpr, l4.maxpr, l5.maxpr, l6.maxpr, ///
    l7.maxpr, l8.maxpr, l9.maxpr, l10.maxpr, l11.maxpr, l12.maxpr)
    
gen High52 = prcadj / temp
drop temp*
label var High52 "52-week High"
// SAVE
do "$pathCode/savepredictor" High52