* --------------
// DATA LOAD
use permno time_avail_m at xrd using "$pathDataIntermediate/m_aCompustat", clear
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(master match) nogenerate keepusing(mve_c) 
// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen year = yofd(dofm(time_avail_m))
gen tempXRD = xrd
replace tempXRD = 0 if mi(tempXRD)
gen RDcap = (tempXRD + .8*l12.tempXRD + .6*l24.tempXRD + .4*l36.tempXRD + .2*l48.tempXRD)/at
replace RDcap = . if year < 1980
egen tempsizeq = fastxtile(mve_c), by(time_avail_m) n(3) // OP: only works in small firms
replace RDcap = . if tempsizeq >= 2
label var RDcap "R&D capital to assets (for constrained only)"
// SAVE
do "$pathCode/savepredictor" RDcap