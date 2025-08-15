* --------------
// DATA LOAD
use permno time_avail_m ret sicCRSP mve_c using "$pathDataIntermediate/SignalMasterTable", clear

* CHECKPOINT 1
display "CHECKPOINT 1: Initial observations after data load: " _N
list permno time_avail_m ret sicCRSP mve_c if permno == 16086 & time_avail_m == tm(2021m11)
list permno time_avail_m ret sicCRSP mve_c if permno == 11406 & time_avail_m == tm(2007m4)

// SIGNAL CONSTRUCTION
tostring sicCRSP, replace
gen sic2D = substr(sicCRSP,1,2)

* CHECKPOINT 2
display "CHECKPOINT 2: After sic2D creation"
list permno time_avail_m sicCRSP sic2D if inlist(permno, 16086, 16338, 21359) & time_avail_m == tm(2021m11)
list permno time_avail_m sicCRSP sic2D if permno == 11406 & time_avail_m == tm(2007m4)

replace ret = 0 if mi(ret)

* CHECKPOINT 3
display "CHECKPOINT 3: After return cleaning"
list permno time_avail_m ret if inlist(permno, 16086, 16338, 21359) & inrange(time_avail_m, tm(2021m6), tm(2021m11))

gen Mom6m = ( (1+l.ret)*(1+l2.ret)*(1+l3.ret)*(1+l4.ret)*(1+l5.ret)) - 1

* CHECKPOINT 4
display "CHECKPOINT 4: After Mom6m calculation"
list permno time_avail_m l.ret l2.ret l3.ret l4.ret l5.ret Mom6m if inlist(permno, 16086, 16338, 21359) & time_avail_m == tm(2021m11)
list permno time_avail_m l.ret l2.ret l3.ret l4.ret l5.ret Mom6m if permno == 11406 & time_avail_m == tm(2007m4)

* CHECKPOINT 5
display "CHECKPOINT 5: Before IndMom calculation - Industry groups in 2021m11"
tab sic2D if time_avail_m == tm(2021m11) & !mi(Mom6m) & !mi(mve_c), missing
egen temp_IndMom = wtmean(Mom6m), by(sic2D time_avail_m) weight(mve_c)
list sic2D temp_IndMom if inlist(permno, 16086, 16338, 21359) & time_avail_m == tm(2021m11)
drop temp_IndMom

egen IndMom = wtmean(Mom6m), by(sic2D time_avail_m) weight(mve_c)
label var IndMom "Industry momentum"

* CHECKPOINT 6
display "CHECKPOINT 6: After IndMom calculation"
list permno time_avail_m sic2D Mom6m mve_c IndMom if inlist(permno, 16086, 16338, 21359) & time_avail_m == tm(2021m11)
list permno time_avail_m sic2D Mom6m mve_c IndMom if inlist(permno, 16086, 16338, 21359) & time_avail_m == tm(2022m2)
list permno time_avail_m sic2D Mom6m mve_c IndMom if permno == 11406 & time_avail_m == tm(2007m4)

// SAVE
do "$pathCode/savepredictor" IndMom
