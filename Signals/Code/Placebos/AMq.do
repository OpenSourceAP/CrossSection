* AMq
* --------------

// DATA LOAD
use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)

merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(atq) nogenerate keep(match)

// SIGNAL CONSTRUCTION
gen AMq = atq/mve_c
label var AMq "Total assets to market (quarterly)"

// SAVE
do "$pathCode/saveplacebo" AMq