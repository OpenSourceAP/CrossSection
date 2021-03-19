* --------------
// DATA LOAD
use permno gvkey time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(ibq atq) nogenerate keep(match)
// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen roaq = ibq/l3.atq
bys permno: asrol roaq, gen(roavol) stat(sd) window(time_avail_m 48) min(24) 
label var roavol "RoA volatility"
// SAVE
do "$pathCode/saveplacebo" roavol