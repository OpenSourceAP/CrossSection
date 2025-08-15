* --------------
* make earnings surprise (copied from EarningsSurprise.do)
// DATA LOAD
use permno gvkey time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear

* CHECKPOINT 1: Initial data load
count
di "CHECKPOINT 1: Loaded " r(N) " observations from SignalMasterTable"
if time_avail_m == tm(2007m4) {
    list permno gvkey time_avail_m if inlist(permno, 10006, 11406, 12473, 10051)
}

keep if !mi(gvkey)

* CHECKPOINT 2: After removing missing gvkey
count
di "CHECKPOINT 2: After dropping missing gvkey: " r(N) " observations"
if time_avail_m == tm(2007m4) {
    list permno gvkey time_avail_m if inlist(permno, 10006, 11406, 12473, 10051)
}

merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(epspxq) nogenerate keep(match)

* CHECKPOINT 3: After merge with m_QCompustat
count
di "CHECKPOINT 3: After merge with m_QCompustat: " r(N) " observations"
if time_avail_m == tm(2007m4) {
    list permno gvkey time_avail_m epspxq if inlist(permno, 10006, 11406, 12473, 10051)
}

// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen GrTemp = (epspxq - l12.epspxq)

* CHECKPOINT 4: After calculating GrTemp (12-month lag)
count if !mi(GrTemp)
di "CHECKPOINT 4: GrTemp calculated for " r(N) " observations"
if time_avail_m == tm(2007m4) {
    list permno time_avail_m epspxq GrTemp if inlist(permno, 10006, 11406, 12473, 10051)
}

foreach n of numlist 3(3)24 {

gen temp`n' = l`n'.GrTemp

}
egen Drift = rowmean(temp*)
gen EarningsSurprise = epspxq - l12.epspxq - Drift

* CHECKPOINT 5: After calculating EarningsSurprise
count if !mi(EarningsSurprise)
di "CHECKPOINT 5: EarningsSurprise calculated for " r(N) " observations"
if time_avail_m == tm(2007m4) {
    list permno time_avail_m epspxq Drift EarningsSurprise if inlist(permno, 10006, 11406, 12473, 10051)
}

cap drop temp*
foreach n of numlist 3(3)24 {

gen temp`n' = l`n'.EarningsSurprise

}
egen SD = rowsd(temp*)
replace EarningsSurprise = EarningsSurprise/SD

* CHECKPOINT 6: After standardizing EarningsSurprise
count if !mi(EarningsSurprise)
di "CHECKPOINT 6: Standardized EarningsSurprise for " r(N) " observations"
if time_avail_m == tm(2007m4) {
    list permno time_avail_m SD EarningsSurprise if inlist(permno, 10006, 11406, 12473, 10051)
}

save "$pathtemp/temp", replace

* --------------
* actually make EarnSupBig
// DATA LOAD
use permno time_avail_m mve_c sicCRSP using "$pathDataIntermediate/SignalMasterTable", clear

* CHECKPOINT 7: Second data load for EarnSupBig
count
di "CHECKPOINT 7: Loaded " r(N) " observations from SignalMasterTable for EarnSupBig"
if time_avail_m == tm(2007m4) {
    list permno time_avail_m mve_c sicCRSP if inlist(permno, 10006, 11406, 12473, 10051)
}

merge 1:1 permno time_avail_m using "$pathtemp/temp", keep(master match) nogenerate

* CHECKPOINT 8: After merge with earnings surprise data
count
di "CHECKPOINT 8: After merge with earnings data: " r(N) " observations"
count if !mi(EarningsSurprise)
di "CHECKPOINT 8: With non-missing EarningsSurprise: " r(N) " observations"
if time_avail_m == tm(2007m4) {
    list permno time_avail_m mve_c sicCRSP EarningsSurprise if inlist(permno, 10006, 11406, 12473, 10051)
}

// SIGNAL CONSTRUCTION
sicff sicCRSP, generate(tempFF48) industry(48)

* CHECKPOINT 9: After FF48 industry classification
count if !mi(tempFF48)
di "CHECKPOINT 9: FF48 industries assigned to " r(N) " observations"
if time_avail_m == tm(2007m4) {
    list permno time_avail_m sicCRSP tempFF48 if inlist(permno, 10006, 11406, 12473, 10051)
}

drop if mi(tempFF48)

* CHECKPOINT 10: After dropping missing FF48 industries
count
di "CHECKPOINT 10: After dropping missing FF48: " r(N) " observations"
if time_avail_m == tm(2007m4) {
    list permno time_avail_m tempFF48 mve_c if inlist(permno, 10006, 11406, 12473, 10051)
}

bys tempFF48 time_avail_m: relrank mve_c, gen(tempRK) ref(mve_c)

* CHECKPOINT 11: After calculating relrank
count if !mi(tempRK)
di "CHECKPOINT 11: Relrank calculated for " r(N) " observations"
if time_avail_m == tm(2007m4) {
    list permno time_avail_m tempFF48 mve_c tempRK if inlist(permno, 10006, 11406, 12473, 10051)
}
preserve
    keep if tempRK >=.7 & !mi(tempRK)
    
    * CHECKPOINT 12: Large companies only (tempRK >= 0.7)
    count
    di "CHECKPOINT 12: Large companies (tempRK >= 0.7): " r(N) " observations"
    if time_avail_m == tm(2007m4) {
        list permno time_avail_m tempFF48 tempRK EarningsSurprise if inlist(permno, 10006, 11406, 12473, 10051)
    }
    
    gcollapse (mean) EarningsSurprise, by(tempFF48 time_avail_m)
    rename EarningsSurprise EarnSupBig
    
    * CHECKPOINT 13: Industry-month averages for large companies
    count
    di "CHECKPOINT 13: Industry-month groups with EarnSupBig: " r(N) " groups"
    if time_avail_m == tm(2007m4) {
        list tempFF48 time_avail_m EarnSupBig
    }

save "$pathtemp/temp",replace
restore
merge m:1 tempFF48 time_avail_m using "$pathtemp/temp", nogenerate

* CHECKPOINT 14: After merging industry averages back
count
di "CHECKPOINT 14: After merging industry averages: " r(N) " observations"
count if !mi(EarnSupBig)
di "CHECKPOINT 14: With non-missing EarnSupBig: " r(N) " observations"
if time_avail_m == tm(2007m4) {
    list permno time_avail_m tempFF48 tempRK EarnSupBig if inlist(permno, 10006, 11406, 12473, 10051)
}

replace EarnSupBig = . if tempRK >= .7

* CHECKPOINT 15: Final result after setting large companies to missing
count if !mi(EarnSupBig)
di "CHECKPOINT 15: Final EarnSupBig (excluding large companies): " r(N) " observations"
if time_avail_m == tm(2007m4) {
    list permno time_avail_m tempFF48 tempRK EarnSupBig if inlist(permno, 10006, 11406, 12473, 10051)
}
label var EarnSupBig "Industry Earnings surprise big companies"

// SAVE 
do "$pathCode/savepredictor" EarnSupBig
