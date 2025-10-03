* ChangeRoE
* --------------

// DATA LOAD
use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)

merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(ibq ceqq) nogenerate keep(match)

// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen tempRoe = ibq/ceqq
gen ChangeRoE = tempRoe - l12.tempRoe

label var ChangeRoE "Change in return on equity"

// SAVE
do "$pathCode/saveplacebo" ChangeRoE