* --------------
// DATA LOAD
use permno gvkey time_avail_m prc using "$pathDataIntermediate/SignalMasterTable", clear
drop if mi(gvkey)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(cshprq epspxq) nogenerate keep(match)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_aCompustat", keepusing(at) nogenerate keep(match)

// SIGNAL CONSTRUCTION
gen Profitability = (cshprq*epspxq)/at
label var Profitability "Profitability"

// SAVE
do "$pathCode/savepredictor" Profitability