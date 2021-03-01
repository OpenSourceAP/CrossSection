* --------------
// DATA LOAD
use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(atq ibq) nogenerate keep(match)

// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen roaq = ibq/l3.atq
label var roaq "Return on Assets"

// SAVE
do "$pathCode/savepredictor" roaq
