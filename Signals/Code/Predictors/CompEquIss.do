* CompEquIss
* --------------

// DATA LOAD
use permno time_avail_m ret mve_c using "$pathDataIntermediate/SignalMasterTable", clear

// SIGNAL CONSTRUCTION
bys permno (time_avail): gen tempIdx = 1 if _n == 1
bys permno (time_avail): replace tempIdx = (1 + ret)*l.tempIdx if _n > 1
gen tempBH = (tempIdx - l60.tempIdx)/l60.tempIdx

gen CompEquIss = log(mve_c/l60.mve_c) - tempBH

label var CompEquIss "Composite Equity Issuance"

// SAVE
do "$pathCode/savepredictor" CompEquIss