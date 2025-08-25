// DATA LOAD
use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
gen year = yofd(dofm(time_avail_m))

merge m:1 permno time_avail_m using "$pathDataIntermediate/pin_monthly", keep(master match) nogen

// SIGNAL CONSTRUCTION
* Use Hvidkjaer measure if available, use Hu measure otherwise
* the two measures are highly correlated when both are available
* reg pinHvidkjaer pinHu has intercept of .01 and slope of .96

gen pinHu = (a*u) / (a*u + es + eb)
gen pin = pinHvidkjaer if !mi(pinHvidkjaer)
replace pin = pinHu if mi(pin)

egen tempsize = fastxtile(mve_c), by(time_avail_m) n(2)
replace pin = . if tempsize == 2
rename pin ProbInformedTrading
label var ProbInformedTrading "Probablity of Informed Trading"

// SAVE
do "$pathCode/savepredictor" ProbInformedTrading
