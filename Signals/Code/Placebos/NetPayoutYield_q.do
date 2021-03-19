* --------------
// DATA LOAD
use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(dvpsxq cshoq ajexq prstkcyq pstkq sstkyq) nogenerate keep(match)
// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen tempDiv = dvpsxq*cshoq*ajexq 
gen tempTotalPayout = tempDiv + prstkcyq + (pstkq - l3.pstkq) // See 1_PrepareQuarterlyCS for treatment of year-to-date variables
gen NetPayoutYield_q = (tempTotalPayout - sstkyq - (pstkq - l3.pstkq))/mve_c
label var NetPayoutYield_q "Net Payout Yield (quarterly)"
// SAVE
do "$pathCode/saveplacebo" NetPayoutYield_q