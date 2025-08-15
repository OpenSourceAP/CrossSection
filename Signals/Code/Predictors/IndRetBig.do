* --------------
// DATA LOAD
use permno time_avail_m ret mve_c sicCRSP using "$pathDataIntermediate/SignalMasterTable", clear

* CHECKPOINT 1: Initial data load
di "CHECKPOINT 1: Loaded " _N " observations"
list permno time_avail_m ret mve_c sicCRSP if permno == 10006 & time_avail_m == tm(2007m4)
list permno time_avail_m ret mve_c sicCRSP if permno == 11406 & time_avail_m == tm(2007m4)

// SIGNAL CONSTRUCTION
sicff sicCRSP, generate(tempFF48) industry(48)

* CHECKPOINT 2: After FF48 industry classification
di "CHECKPOINT 2: FF48 classification complete"
list permno time_avail_m sicCRSP tempFF48 if permno == 10006 & time_avail_m == tm(2007m4)
list permno time_avail_m sicCRSP tempFF48 if permno == 11406 & time_avail_m == tm(2007m4)
di "Missing FF48 observations: " _N - e(N_not_missing)

drop if mi(tempFF48)

* CHECKPOINT 3: After dropping missing FF48
di "CHECKPOINT 3: After dropping missing FF48, " _N " observations remain"
list permno time_avail_m sicCRSP tempFF48 if permno == 10006 & time_avail_m == tm(2007m4)
list permno time_avail_m sicCRSP tempFF48 if permno == 11406 & time_avail_m == tm(2007m4)

bys tempFF48 time_avail_m: relrank mve_c, gen(tempRK) ref(mve_c)

* CHECKPOINT 4: After relrank calculation
di "CHECKPOINT 4: Relrank calculation complete"
list permno time_avail_m mve_c tempRK if permno == 10006 & time_avail_m == tm(2007m4)
list permno time_avail_m mve_c tempRK if permno == 11406 & time_avail_m == tm(2007m4)
sum tempRK, detail

preserve

* CHECKPOINT 5: Before filtering for large companies
di "CHECKPOINT 5: Before preserve, " _N " observations"
list permno time_avail_m tempRK if permno == 10006 & time_avail_m == tm(2007m4)
list permno time_avail_m tempRK if permno == 11406 & time_avail_m == tm(2007m4)

    keep if tempRK >=.7 & !mi(tempRK)
    
* CHECKPOINT 6: After filtering for large companies  
di "CHECKPOINT 6: Large companies (tempRK >= 0.7): " _N " observations"
list permno time_avail_m tempRK ret if permno == 10006 & time_avail_m == tm(2007m4)
list permno time_avail_m tempRK ret if permno == 11406 & time_avail_m == tm(2007m4)
    
    gcollapse (mean) ret, by(tempFF48 time_avail_m)
    rename ret IndRetBig

* CHECKPOINT 7: After industry return calculation
di "CHECKPOINT 7: Industry returns calculated for " _N " industry-month groups"
list tempFF48 time_avail_m IndRetBig if time_avail_m == tm(2007m4)

save "$pathtemp/temp",replace
restore

* CHECKPOINT 8: After restore
di "CHECKPOINT 8: After restore, " _N " observations"
list permno time_avail_m tempRK if permno == 10006 & time_avail_m == tm(2007m4)
list permno time_avail_m tempRK if permno == 11406 & time_avail_m == tm(2007m4)

merge m:1 tempFF48 time_avail_m using "$pathtemp/temp", nogenerate

* CHECKPOINT 9: After merge with industry returns
di "CHECKPOINT 9: After merge, " _N " observations"
list permno time_avail_m tempRK IndRetBig if permno == 10006 & time_avail_m == tm(2007m4)
list permno time_avail_m tempRK IndRetBig if permno == 11406 & time_avail_m == tm(2007m4)
count if !mi(IndRetBig)

replace IndRetBig = . if tempRK >= .7

* CHECKPOINT 10: Final result
di "CHECKPOINT 10: Final dataset"
list permno time_avail_m tempRK IndRetBig if permno == 10006 & time_avail_m == tm(2007m4)
list permno time_avail_m tempRK IndRetBig if permno == 11406 & time_avail_m == tm(2007m4)
count if !mi(IndRetBig)
di "Total observations: " _N ", Non-missing IndRetBig: " r(N)

label var IndRetBig "Industry return big companies"
// SAVE
do "$pathCode/savepredictor" IndRetBig