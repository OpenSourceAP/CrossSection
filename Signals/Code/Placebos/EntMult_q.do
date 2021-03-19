* --------------
// DATA LOAD
use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(dlttq dlcq pstkq che oibdpq ceqq) nogenerate keep(match)
// SIGNAL CONSTRUCTION
gen EntMult_q = (mve_c + dlttq + dlcq + pstkq - cheq)/oibdpq
replace EntMult_q = . if ceqq < 0 | oibdpq < 0  // This screen come from Loughran and Wellman's paper, MP don't mention them.
label var EntMult_q "Enterprise Multiple (quarterly)"
// SAVE
do "$pathCode/saveplacebo" EntMult_q