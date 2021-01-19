* --------------
// DATA LOAD
use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(cheq rectq invtq ppegtq atq) nogenerate keep(match)
// SIGNAL CONSTRUCTION
gen tang_q = (cheq + .715*rectq + .547*invtq + .535*ppegtq)/atq 
label var tang_q "Tangibility (quarterly)"
// SAVE
do "$pathCode/saveplacebo" tang_q