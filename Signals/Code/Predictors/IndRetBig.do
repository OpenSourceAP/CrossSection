* --------------
// DATA LOAD
use permno time_avail_m ret mve_c sicCRSP using "$pathDataIntermediate/SignalMasterTable", clear

* CHECKPOINT 1: Initial data load
display "CHECKPOINT 1: Initial data load"
count
list permno time_avail_m ret mve_c sicCRSP if permno == 13784 & time_avail_m == tm(1932m7), noobs
list permno time_avail_m ret mve_c sicCRSP if permno == 10886 & time_avail_m == tm(2002m4), noobs

// SIGNAL CONSTRUCTION
sicff sicCRSP, generate(tempFF48) industry(48)

* CHECKPOINT 2: After FF48 industry classification  
display "CHECKPOINT 2: After FF48 industry classification"
count if mi(tempFF48)
list permno time_avail_m sicCRSP tempFF48 if permno == 13784 & time_avail_m == tm(1932m7), noobs
list permno time_avail_m sicCRSP tempFF48 if permno == 10886 & time_avail_m == tm(2002m4), noobs

drop if mi(tempFF48)

* CHECKPOINT 3: After dropping missing FF48
display "CHECKPOINT 3: After dropping missing FF48"
count
list permno time_avail_m sicCRSP tempFF48 if permno == 13784 & time_avail_m == tm(1932m7), noobs
list permno time_avail_m sicCRSP tempFF48 if permno == 10886 & time_avail_m == tm(2002m4), noobs

bys tempFF48 time_avail_m: relrank mve_c, gen(tempRK) ref(mve_c)

* CHECKPOINT 4: After relrank calculation
display "CHECKPOINT 4: After relrank calculation"
list permno time_avail_m mve_c tempRK if permno == 13784 & time_avail_m == tm(1932m7), noobs
list permno time_avail_m mve_c tempRK if permno == 10886 & time_avail_m == tm(2002m4), noobs
summarize tempRK

preserve

* CHECKPOINT 5: Before filtering for large companies
display "CHECKPOINT 5: Before preserve"
count
list permno time_avail_m tempRK if permno == 13784 & time_avail_m == tm(1932m7), noobs
list permno time_avail_m tempRK if permno == 10886 & time_avail_m == tm(2002m4), noobs

    keep if tempRK >=.7 & !mi(tempRK)
    
* CHECKPOINT 6: After filtering for large companies
display "CHECKPOINT 6: Large companies (tempRK >= 0.7)"
count
list permno time_avail_m tempRK ret if permno == 13784 & time_avail_m == tm(1932m7), noobs
list permno time_avail_m tempRK ret if permno == 10886 & time_avail_m == tm(2002m4), noobs
    
    gcollapse (mean) ret, by(tempFF48 time_avail_m)
    rename ret IndRetBig

* CHECKPOINT 7: After industry return calculation
display "CHECKPOINT 7: Industry returns calculated"
count
list tempFF48 time_avail_m IndRetBig if time_avail_m == tm(1932m7), noobs
list tempFF48 time_avail_m IndRetBig if time_avail_m == tm(2002m4), noobs

save "$pathtemp/temp",replace
restore

* CHECKPOINT 8: After restore
display "CHECKPOINT 8: After restore"
count
list permno time_avail_m tempRK if permno == 13784 & time_avail_m == tm(1932m7), noobs
list permno time_avail_m tempRK if permno == 10886 & time_avail_m == tm(2002m4), noobs

merge m:1 tempFF48 time_avail_m using "$pathtemp/temp", nogenerate

* CHECKPOINT 9: After merge with industry returns
display "CHECKPOINT 9: After merge"
count
list permno time_avail_m tempRK IndRetBig if permno == 13784 & time_avail_m == tm(1932m7), noobs
list permno time_avail_m tempRK IndRetBig if permno == 10886 & time_avail_m == tm(2002m4), noobs

replace IndRetBig = . if tempRK >= .7

* CHECKPOINT 10: Final result
display "CHECKPOINT 10: Final dataset"
list permno time_avail_m tempRK IndRetBig if permno == 13784 & time_avail_m == tm(1932m7), noobs
list permno time_avail_m tempRK IndRetBig if permno == 10886 & time_avail_m == tm(2002m4), noobs
count if !mi(IndRetBig)
label var IndRetBig "Industry return big companies"
// SAVE
do "$pathCode/savepredictor" IndRetBig