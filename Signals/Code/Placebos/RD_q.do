* --------------
// DATA LOAD
use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
drop if mi(gvkey)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(xrdq) nogenerate keep(match)
// SIGNAL CONSTRUCTION
gen RD_q = xrdq/mve_c

label var RD_q "R&D-to-market cap (quarterly)"
// SAVE
do "$pathCode/saveplacebo" RD_q