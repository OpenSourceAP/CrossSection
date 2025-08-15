* --------------
* make earnings surprise (copied from EarningsSurprise.do)
// DATA LOAD
use permno gvkey time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(epspxq) nogenerate keep(match)

// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen GrTemp = (epspxq - l12.epspxq)

* CHECKPOINT 1 - After calculating GrTemp (12-month lag)
di "CHECKPOINT 1: GrTemp calculated"
list permno time_avail_m epspxq GrTemp if permno == 10613 & time_avail_m == tm(1973m8)
list permno time_avail_m epspxq GrTemp if permno == 10100 & time_avail_m == tm(2001m5)
foreach n of numlist 3(3)24 {

gen temp`n' = l`n'.GrTemp

}
egen Drift = rowmean(temp*)

* CHECKPOINT 2 - After calculating Drift
di "CHECKPOINT 2: Drift calculated"
list permno time_avail_m GrTemp Drift if permno == 10613 & time_avail_m == tm(1973m8)
list permno time_avail_m GrTemp Drift if permno == 10100 & time_avail_m == tm(2001m5)

gen EarningsSurprise = epspxq - l12.epspxq - Drift

* CHECKPOINT 3 - After calculating raw EarningsSurprise (before standardization)
di "CHECKPOINT 3: Raw EarningsSurprise calculated"
list permno time_avail_m epspxq Drift EarningsSurprise if permno == 10613 & time_avail_m == tm(1973m8)
list permno time_avail_m epspxq Drift EarningsSurprise if permno == 10100 & time_avail_m == tm(2001m5)
cap drop temp*
foreach n of numlist 3(3)24 {

gen temp`n' = l`n'.EarningsSurprise

}
egen SD = rowsd(temp*)

* CHECKPOINT 4 - After calculating SD (critical for standardization)
di "CHECKPOINT 4: SD calculated"
list permno time_avail_m SD EarningsSurprise if permno == 10613 & time_avail_m == tm(1973m8)
list permno time_avail_m SD EarningsSurprise if permno == 10100 & time_avail_m == tm(2001m5)
* Check for very small SD values that could cause extreme results
list permno time_avail_m SD EarningsSurprise if SD < 0.001 & SD > 0 & !mi(SD) & !mi(EarningsSurprise)

replace EarningsSurprise = EarningsSurprise/SD

* CHECKPOINT 5 - After standardization (CRITICAL STEP)
di "CHECKPOINT 5: EarningsSurprise standardized"
list permno time_avail_m SD EarningsSurprise if permno == 10613 & time_avail_m == tm(1973m8)
list permno time_avail_m SD EarningsSurprise if permno == 10100 & time_avail_m == tm(2001m5)
* Check for extreme values after standardization
list permno time_avail_m SD EarningsSurprise if abs(EarningsSurprise) > 1000 & !mi(EarningsSurprise)

save "$pathtemp/temp", replace

* --------------
* actually make EarnSupBig
// DATA LOAD
use permno time_avail_m mve_c sicCRSP using "$pathDataIntermediate/SignalMasterTable", clear
merge 1:1 permno time_avail_m using "$pathtemp/temp", keep(master match) nogenerate

// SIGNAL CONSTRUCTION
sicff sicCRSP, generate(tempFF48) industry(48)
drop if mi(tempFF48)

bys tempFF48 time_avail_m: relrank mve_c, gen(tempRK) ref(mve_c)

* CHECKPOINT 6 - After calculating relrank
di "CHECKPOINT 6: Relrank calculated"
list permno time_avail_m tempFF48 mve_c tempRK EarningsSurprise if permno == 10613 & time_avail_m == tm(1973m8)
list permno time_avail_m tempFF48 mve_c tempRK EarningsSurprise if permno == 10100 & time_avail_m == tm(2001m5)
preserve
    keep if tempRK >=.7 & !mi(tempRK)
    gcollapse (mean) EarningsSurprise, by(tempFF48 time_avail_m)
    rename EarningsSurprise EarnSupBig
    
    * CHECKPOINT 7 - Industry averages for large companies
    di "CHECKPOINT 7: Industry averages calculated"
    list tempFF48 time_avail_m EarnSupBig if time_avail_m == tm(1973m8)
    list tempFF48 time_avail_m EarnSupBig if time_avail_m == tm(2001m5)

save "$pathtemp/temp",replace
restore
merge m:1 tempFF48 time_avail_m using "$pathtemp/temp", nogenerate

* CHECKPOINT 8 - After merging industry averages and final result
di "CHECKPOINT 8: Final EarnSupBig values"
list permno time_avail_m tempFF48 tempRK EarnSupBig if permno == 10613 & time_avail_m == tm(1973m8)
list permno time_avail_m tempFF48 tempRK EarnSupBig if permno == 10100 & time_avail_m == tm(2001m5)

replace EarnSupBig = . if tempRK >= .7
label var EarnSupBig "Industry Earnings surprise big companies"

* CHECKPOINT 9 - Final values after setting large companies to missing
di "CHECKPOINT 9: Final EarnSupBig after excluding large companies"
list permno time_avail_m tempFF48 tempRK EarnSupBig if permno == 10613 & time_avail_m == tm(1973m8)
list permno time_avail_m tempFF48 tempRK EarnSupBig if permno == 10100 & time_avail_m == tm(2001m5)

// SAVE 
do "$pathCode/savepredictor" EarnSupBig
