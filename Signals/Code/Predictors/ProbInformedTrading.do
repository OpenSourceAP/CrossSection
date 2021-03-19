* --------------
// DATA LOAD
use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
gen year = yofd(dofm(time_avail_m))
merge m:1 permno year using "$pathDataIntermediate/aInformedTrading", keep(master match) nogenerate
// SIGNAL CONSTRUCTION
rename pin ProbInformedTrading
egen tempsize = fastxtile(mve_c), by(time_avail_m) n(2)
replace ProbInformedTrading = . if tempsize == 2
label var ProbInformedTrading "Probability of Informed Trading"
// SAVE
do "$pathCode/savepredictor" ProbInformedTrading