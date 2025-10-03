* AM
* --------------

// DATA LOAD
use permno time_avail_m at using "$pathDataIntermediate/m_aCompustat", clear
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations

merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(match) nogenerate keepusing(mve_c) 

// SIGNAL CONSTRUCTION
gen AM = at/mve_c

label var AM "Total assets to market"

// SAVE
do "$pathCode/savepredictor" AM