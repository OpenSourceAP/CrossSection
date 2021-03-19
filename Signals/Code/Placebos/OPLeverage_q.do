* --------------
// DATA LOAD
use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(xsga cogsq atq) nogenerate keep(match)
// SIGNAL CONSTRUCTION
gen tempxsga = 0
replace tempxsga = xsgaq if xsgaq !=.
gen OPLeverage_q = (tempxsga + cogsq)/atq
label var OPLeverage_q "Operating Leverage (quarterly)"
// SAVE
do "$pathCode/saveplacebo" OPLeverage_q