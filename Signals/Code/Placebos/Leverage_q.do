* --------------
// DATA LOAD
use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(ltq) nogenerate keep(match)
// SIGNAL CONSTRUCTION
gen Leverage_q = ltq/mve_c
label var Leverage_q "Market leverage (quarterly)"
// SAVE
do "$pathCode/saveplacebo" Leverage_q