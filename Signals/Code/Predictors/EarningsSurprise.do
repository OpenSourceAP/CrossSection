* --------------
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
label var EarningsSurprise "Earnings Surprise"

// SAVE
do "$pathCode/savepredictor" EarningsSurprise