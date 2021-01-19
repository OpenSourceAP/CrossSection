* --------------
// DATA LOAD
use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(ibq) nogenerate keep(match)
// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen EPq = ibq/l6.mve_c
replace EPq  = . if EPq < 0
label var EPq "Earnings-to-price ratio (quarterly)"
// SAVE
do "$pathCode/saveplacebo" EPq