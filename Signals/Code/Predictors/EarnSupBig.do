* --------------
* make earnings surprise (copied from EarningsSurprise.do)
// DATA LOAD
use permno gvkey time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(epspxq) nogenerate keep(match)

// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen GrTemp = (epspxq - l12.epspxq)
foreach n of numlist 3(3)24 {

gen temp`n' = l`n'.GrTemp

}
egen Drift = rowmean(temp*)
gen EarningsSurprise = epspxq - l12.epspxq - Drift
cap drop temp*
foreach n of numlist 3(3)24 {

gen temp`n' = l`n'.EarningsSurprise

}
egen SD = rowsd(temp*)
replace EarningsSurprise = EarningsSurprise/SD

save "$pathtemp/temp", replace

* --------------
* actually make EarnSupBig
// DATA LOAD
use permno time_avail_m mve_c sicCRSP using "$pathDataIntermediate/SignalMasterTable", clear
merge 1:1 permno time_avail_m using "$pathtemp/temp", keep(master match) nogenerate

// SIGNAL CONSTRUCTION
ffind sicCRSP, newvar(tempFF48) type(48)
bys tempFF48 time_avail_m: relrank mve_c, gen(tempRK) ref(mve_c)
preserve
    keep if tempRK >=.7 & !mi(tempRK)
    gcollapse (mean) EarningsSurprise, by(tempFF48 time_avail_m)
    rename EarningsSurprise EarnSupBig

save "$pathtemp/temp",replace
restore
merge m:1 tempFF48 time_avail_m using "$pathtemp/temp", nogenerate
replace EarnSupBig = . if tempRK >= .7
label var EarnSupBig "Industry Earnings surprise big companies"

// SAVE 
do "$pathCode/savepredictor" EarnSupBig
