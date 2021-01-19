* --------------
// DATA LOAD
use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(saleq) nogenerate keep(match)
// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen sgr_q = (saleq/l12.saleq)-1
label var sgr_q "Quarterly sales growth"
// SAVE
do "$pathCode/saveplacebo" sgr_q