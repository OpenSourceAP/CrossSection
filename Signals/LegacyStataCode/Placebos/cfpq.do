* cfpq
* --------------

// DATA LOAD
use gvkey permno time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)

merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keep(match) nogenerate keepusing(actq cheq lctq dlcq txpq dpq ibq oancfyq)

// SIGNAL CONSTRUCTION
xtset permno time_avail_m

gen tempaccrual_level = (actq-l12.actq - (cheq-l12.cheq)) - ( (lctq-l12.lctq)- ///
                (dlcq-l12.dlcq)-(txpq-l12.txpq)-dpq )  
gen cfpq =(ibq - tempaccrual_level )/ mve_c       
replace cfpq = oancfyq/mve_c if oancfyq !=.

label var cfpq "Cash flow to price (quarterly)"

// SAVE
do "$pathCode/saveplacebo" cfpq