// DATA LOAD
use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
gen year = yofd(dofm(time_avail_m))

merge m:1 permno time_avail_m using "$pathDataIntermediate/pin_monthly", keep(master match) nogen

// SIGNAL CONSTRUCTION
* generate yearly PIN measure from Easley et al
gen pin = (a*u) / (a*u + es + eb)
egen tempsize = fastxtile(mve_c), by(time_avail_m) n(2)
replace pin = . if tempsize == 2
rename pin ProbInformedTrading
label var ProbInformedTrading "Probablity of Informed Trading"

// SAVE
do "$pathCode/savepredictor" ProbInformedTrading
