* --------------
// DATA LOAD
use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(revtq cogsq atq) nogenerate keep(match)
// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen GPlag_q =   (revtq - cogsq)/l3.atq

label var GPlag_q "Gross profitability (quarterly)"
// SAVE
do "$pathCode/saveplacebo" GPlag_q