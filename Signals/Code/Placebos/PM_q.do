* --------------
// DATA LOAD
use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(niq revtq) nogenerate keep(match)
// SIGNAL CONSTRUCTION
gen PM_q = niq/revtq
label var PM_q "Profit Margin (quarterly)"
// SAVE
do "$pathCode/saveplacebo" PM_q