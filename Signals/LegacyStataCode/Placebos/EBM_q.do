* --------------
// DATA LOAD
use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(cheq dlttq dlcq pstkq ceqq) nogenerate keep(match)
// SIGNAL CONSTRUCTION
gen temp = cheq - dlttq - dlcq - pstkq
gen EBM_q = (ceqq + temp)/(mve_c + temp)
label var EBM_q "Enterprise component of BM (quarterly)"
// SAVE
do "$pathCode/saveplacebo" EBM_q