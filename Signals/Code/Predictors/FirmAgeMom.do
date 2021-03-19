* --------------
// DATA LOAD
use permno time_avail_m ret prc using "$pathDataIntermediate/SignalMasterTable", clear
// SIGNAL CONSTRUCTION
replace ret = 0 if mi(ret)
bys permno (time_avail_m): gen tempage = _n
gen FirmAgeMom = ( (1+l.ret)*(1+l2.ret)*(1+l3.ret)*(1+l4.ret)*(1+l5.ret)) - 1
replace FirmAgeMom = . if abs(prc) < 5 | tempage < 12
egen temp = fastxtile(tempage), by(time_avail_m) n(5)  // Find bottom age quintile
replace FirmAgeMom =. if temp > 1 & temp !=.
label var FirmAgeMom "Firm Age - Momentum"
// SAVE
do "$pathCode/savepredictor" FirmAgeMom