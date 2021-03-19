* --------------
// DATA LOAD
use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(revtq cshprq) nogenerate keep(match)
// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen revps = revtq/cshprq
gen GrTemp = (revps - l12.revps)
foreach n of numlist 3(3)24 {

gen temp`n' = l`n'.GrTemp

}
egen Drift = rowmean(temp*)
gen RevenueSurprise = revps - l12.revps - Drift
cap drop temp*
foreach n of numlist 3(3)24 {

gen temp`n' = l`n'.RevenueSurprise

}
egen SD = rowsd(temp*)
replace RevenueSurprise = RevenueSurprise/SD
label var RevenueSurprise "Revenue Surprise"
// SAVE
do "$pathCode/savepredictor" RevenueSurprise