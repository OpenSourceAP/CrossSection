* --------------
// DATA LOAD
use permno time_avail_m ret sicCRSP mve_c using "$pathDataIntermediate/SignalMasterTable", clear

* CHECKPOINT 1: Initial data load
count
di "Initial observations after data load: " r(N)
list permno time_avail_m ret sicCRSP mve_c if permno == 10006 & time_avail_m == tm(2007m4), ab(20)
list permno time_avail_m ret sicCRSP mve_c if permno == 11406 & time_avail_m == tm(2007m4), ab(20)

// SIGNAL CONSTRUCTION
tostring sicCRSP, replace
gen sic2D = substr(sicCRSP,1,2)

* CHECKPOINT 2: After SIC2D creation
count if !mi(sic2D)
di "Observations with non-missing sic2D: " r(N)
list permno time_avail_m sicCRSP sic2D if permno == 10006 & time_avail_m == tm(2007m4), ab(20)
list permno time_avail_m sicCRSP sic2D if permno == 11406 & time_avail_m == tm(2007m4), ab(20)

replace ret = 0 if mi(ret)

* CHECKPOINT 3: After return cleaning
count if !mi(ret)
di "Observations with non-missing ret after cleaning: " r(N)
list permno time_avail_m ret if permno == 10006 & inrange(time_avail_m, tm(2007m1), tm(2007m6)), ab(20)
list permno time_avail_m ret if permno == 11406 & inrange(time_avail_m, tm(2007m1), tm(2007m6)), ab(20)

gen Mom6m = ( (1+l.ret)*(1+l2.ret)*(1+l3.ret)*(1+l4.ret)*(1+l5.ret)) - 1

* CHECKPOINT 4: After Mom6m calculation
count if !mi(Mom6m)
di "Observations with non-missing Mom6m: " r(N)
list permno time_avail_m l.ret l2.ret l3.ret l4.ret l5.ret Mom6m if permno == 10006 & time_avail_m == tm(2007m4), ab(20)
list permno time_avail_m l.ret l2.ret l3.ret l4.ret l5.ret Mom6m if permno == 11406 & time_avail_m == tm(2007m4), ab(20)
list permno time_avail_m l.ret l2.ret l3.ret l4.ret l5.ret Mom6m if permno == 12473 & time_avail_m == tm(2007m4), ab(20)

egen IndMom = wtmean(Mom6m), by(sic2D time_avail_m) weight(mve_c)

* CHECKPOINT 5: After IndMom calculation
count if !mi(IndMom)
di "Observations with non-missing IndMom: " r(N)
list permno time_avail_m sic2D Mom6m mve_c IndMom if permno == 10006 & time_avail_m == tm(2007m4), ab(20)
list permno time_avail_m sic2D Mom6m mve_c IndMom if permno == 11406 & time_avail_m == tm(2007m4), ab(20)
list permno time_avail_m sic2D Mom6m mve_c IndMom if permno == 12473 & time_avail_m == tm(2007m4), ab(20)

* CHECKPOINT 6: Industry group analysis for 2007m4
di "Industry groups in 2007m4:"
bysort sic2D: egen temp_count = count(Mom6m) if time_avail_m == tm(2007m4) & !mi(Mom6m) & !mi(mve_c)
list sic2D temp_count if time_avail_m == tm(2007m4) & !mi(temp_count), clean noobs
drop temp_count

label var IndMom "Industry momentum"

// SAVE
do "$pathCode/savepredictor" IndMom
