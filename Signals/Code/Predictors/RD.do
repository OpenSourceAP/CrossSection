* --------------
// DATA LOAD
use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
drop if mi(gvkey)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_aCompustat", keepusing(xrd) nogenerate keep(match)
// SIGNAL CONSTRUCTION
gen RD = xrd/mve_c

label var RD "R&D-to-market cap"
// SAVE
do "$pathCode/savepredictor" RD