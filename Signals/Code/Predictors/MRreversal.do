* --------------
// DATA LOAD
use permno time_avail_m ret using "$pathDataIntermediate/SignalMasterTable", clear
// SIGNAL CONSTRUCTION
replace ret = 0 if mi(ret)

* CHECKPOINT 1: After ret cleanup, before lag calculation
list permno time_avail_m ret if permno == 15017 & time_avail_m == tm(2018m6)
list permno time_avail_m ret if permno == 91201 & time_avail_m == tm(2019m10)

gen MRreversal = ( (1+l13.ret)*(1+l14.ret)*(1+l15.ret)*(1+l16.ret)*(1+l17.ret)*(1+l18.ret) ) - 1

* CHECKPOINT 2: After MRreversal calculation
list permno time_avail_m ret l13.ret l14.ret l15.ret l16.ret l17.ret l18.ret MRreversal if permno == 15017 & time_avail_m == tm(2018m6)
list permno time_avail_m ret l13.ret l14.ret l15.ret l16.ret l17.ret l18.ret MRreversal if permno == 91201 & time_avail_m == tm(2019m10)

label var MRreversal "Momentum-Reversal"

* CHECKPOINT 3: Before save
list permno time_avail_m MRreversal if permno == 15017 & time_avail_m == tm(2018m6)
list permno time_avail_m MRreversal if permno == 91201 & time_avail_m == tm(2019m10)

// SAVE
do "$pathCode/savepredictor" MRreversal

