* --------------
// DATA LOAD
use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(dvpsxq cshoq ajexq prstkcyq pstkq) nogenerate keep(match)
// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen tempDiv = dvpsxq*cshoq*ajexq 
gen tempTotalPayout = tempDiv + prstkcyq + (pstkq - l3.pstkq) // See 1_PrepareQuarterlyCS for treatment of year-to-date variables
gen PayoutYield_q = tempTotalPayout/l6.mve_c
replace PayoutYield_q = . if PayoutYield_q <= 0
label var PayoutYield_q "Payout Yield (quarterly)"
// SAVE
do "$pathCode/saveplacebo" PayoutYield_q
