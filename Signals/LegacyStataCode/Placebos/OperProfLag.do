* --------------
// DATA LOAD
use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
drop if mi(gvkey)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_aCompustat", keepusing(revt cogs xsga xint ceq) nogenerate keep(match)
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
gen tempprof = (revt - cogs - xsga - xint)/l12.ceq
egen tempsizeq = fastxtile(mve_c), by(time_avail_m) n(3)
replace tempprof = . if tempsizeq == 1
gen OperProfLag = tempprof
label var OperProfLag "Operating Profits to lagged equity"
// SAVE
do "$pathCode/saveplacebo" OperProfLag