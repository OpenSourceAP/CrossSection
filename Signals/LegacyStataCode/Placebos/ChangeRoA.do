* ChangeRoA
* --------------

// DATA LOAD
use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)

merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(atq ibq) nogenerate keep(match)

// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen tempRoa = ibq/atq
gen ChangeRoA = tempRoa - l12.tempRoa

label var ChangeRoA "Change in return on assets"

// SAVE
do "$pathCode/saveplacebo" ChangeRoA