* --------
// DATA LOAD
use "$pathDataIntermediate/dailyCRSP.dta", clear

// SIGNAL CONSTRUCTION
gen time_avail_m = mofd(time_d)
format time_avail_m %tm

*gen prcadj = abs(prc)/cfacpr  
*OP does not appear to adjust prices for splits and cfacpr has look-ahead bias. 
*See discussion here: https://github.com/OpenSourceAP/CrossSection/issues/95#issuecomment-2286803178
gen prcadj = abs(prc)  

gcollapse (max) maxpr = prcadj (lastnm) prcadj, by(permno time_avail_m)
xtset permno time_avail_m
gen temp = max(l1.maxpr, l2.maxpr, l3.maxpr, l4.maxpr, l5.maxpr, l6.maxpr, ///
    l7.maxpr, l8.maxpr, l9.maxpr, l10.maxpr, l11.maxpr, l12.maxpr)
    
gen High52 = prcadj / temp
drop temp*
label var High52 "52-week High"

// SAVE
do "$pathCode/savepredictor" High52