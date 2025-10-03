* --------------
// DATA LOAD
use gvkey permno time_avail_m che dltt dlc dc dvpa tstkp ceq using "$pathDataIntermediate/m_aCompustat", clear
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(using match) nogenerate keepusing(mve_c)
xtset permno time_avail_m
// SIGNAL CONSTRUCTION
gen temp = che - dltt - dlc - dc - dvpa + tstkp
gen EBM = (ceq + temp)/(mve_c + temp)
gen BP = (ceq + tstkp - dvpa)/mve_c
gen BPEBM = BP - EBM
label var EBM "Enterprise component of EBM"
label var BPEBM "Leverage component of BM"

// SAVE
do "$pathCode/savepredictor" EBM 
do "$pathCode/savepredictor" BPEBM