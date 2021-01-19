* CapTurnover_q
* --------------

// DATA LOAD
use permno gvkey time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)

merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(atq saleq) nogenerate keep(match)

// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen CapTurnover_q = saleq/l3.atq

label var CapTurnover_q "Capital turnover (quarterly)"

// SAVE
do "$pathCode/saveplacebo" CapTurnover_q