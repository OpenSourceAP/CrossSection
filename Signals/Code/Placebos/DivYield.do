// PREP DISTRIBUTIONS DATA
use "$pathDataIntermediate/CRSPdistributions", clear

* collapse by exdt: this date tends to come first
gen time_avail_m = mofd(exdt)
format time_avail_m %tm
drop if time_avail_m == . | divamt == .

* sum dividends
gcollapse (sum) divamt, by(permno time_avail_m)

save "$pathtemp/tempdivamt", replace

* --------------
// DATA LOAD
use permno time_avail_m mve_c prc using "$pathDataIntermediate/SignalMasterTable", clear
merge 1:1 permno time_avail_m using "$pathtemp/tempdivamt", keep(master match) nogenerate keepusing(divamt) 

// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen temp = divamt
replace temp = 0 if divamt ==.
gen tempdy = 4*max(temp, l1.temp, l2.temp)/abs(prc)
gen tempdypos = tempdy 
replace tempdypos = . if (temp <=0 & l1.temp<=0 & l2.temp<=0) | ///
    (l3.temp <=0 & l4.temp <= 0 & l5.temp <=0) | ///
    (l6.temp<=0 & l7.temp<=0 & l8.temp<=0) | ///
    (l9.temp<=0 & l10.temp<=0 & l11.temp <=0)
gen DivYield = tempdypos

egen tempsize = fastxtile(mve_c), by(time_avail_m) n(4)
replace DivYield = . if tempsize >= 3


// see table 1B
label var DivYield "Dividend Yield (Current)"

// SAVE
do "$pathCode/saveplacebo" DivYield


