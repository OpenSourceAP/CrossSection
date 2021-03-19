* --------------
// DATA LOAD
use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(saleq) nogenerate keep(match)
// SIGNAL CONSTRUCTION
gen SP_q = saleq/mve_c
label var SP_q "Sales-to-price ratio (quarterly)"
// SAVE
do "$pathCode/saveplacebo" SP_q