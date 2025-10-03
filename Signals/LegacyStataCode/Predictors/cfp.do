* cfp
* --------------

// DATA LOAD
use gvkey permno time_avail_m act che lct dlc txp dp ib oancf using "$pathDataIntermediate/m_aCompustat", clear
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(using match) nogenerate keepusing(mve_c)

// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen accrual_level = (act-l12.act - (che-l12.che)) - ( (lct-l12.lct)- ///
                (dlc-l12.dlc)-(txp-l12.txp)-dp )  
gen cfp =(ib - accrual_level )/ mve_c       
replace cfp = oancf/mve_c if oancf !=.

label var cfp "Cash flow to price"

// SAVE
do "$pathCode/savepredictor" cfp