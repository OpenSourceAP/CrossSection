* --------------
// DATA LOAD
use permno time_avail_m ret mve_c sicCRSP using "$pathDataIntermediate/SignalMasterTable", clear
// SIGNAL CONSTRUCTION
ffind sicCRSP, newvar(tempFF48) type(48)
bys tempFF48 time_avail_m: relrank mve_c, gen(tempRK) ref(mve_c)
preserve
    keep if tempRK >=.7 & !mi(tempRK)
    gcollapse (mean) ret, by(tempFF48 time_avail_m)
    rename ret IndRetBig

save "$pathtemp/temp",replace
restore
merge m:1 tempFF48 time_avail_m using "$pathtemp/temp", nogenerate
replace IndRetBig = . if tempRK >= .7
label var IndRetBig "Industry return big companies"
// SAVE
do "$pathCode/savepredictor" IndRetBig