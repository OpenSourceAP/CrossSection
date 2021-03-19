* --------------
// DATA LOAD
use gvkey permno time_avail_m ib dp using "$pathDataIntermediate/m_aCompustat", clear
merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(using match) nogenerate 
xtset permno time_avail_m

// SIGNAL CONSTRUCTION
* works better without MP's screens (original lacks screens)
gen tempCF = (ib + dp)/mve_c
asrol tempCF, gen(sigma) stat(sd) window(time_avail_m 60) min(24) by(permno)
gen VarCF = sigma^2
label var VarCF "Cash-flow variance"

// SAVE
do "$pathCode/savepredictor" VarCF
