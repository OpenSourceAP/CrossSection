* CFq
* --------------

// DATA LOAD
use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)

merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(ibq dpq) nogenerate keep(match)

// SIGNAL CONSTRUCTION
gen CFq 		= (ibq + dpq)/mve_c

label var CFq "Cash-flow to market (quarterly)"

// SAVE
do "$pathCode/saveplacebo" CFq