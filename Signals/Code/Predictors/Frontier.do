* --------------
// DATA LOAD
use permno time_avail_m mve_c sicCRSP using "$pathDataIntermediate/SignalMasterTable", clear
merge 1:1 permno time_avail_m using "$pathDataIntermediate/m_aCompustat", nogenerate keepusing(at ceq dltt at capx sale xrd xad ppent ebitda) keep(master match)
// SIGNAL CONSTRUCTION
replace xad = 0 if mi(xad) 
gen YtempBM = log(mve_c)
gen tempBook = log(ceq)
gen tempLTDebt = dltt/at
gen tempCapx = capx/sale
gen tempRD   = xrd/sale
gen tempAdv  = xad/sale
gen tempPPE = ppent/at
gen tempEBIT = ebitda/at
ffind sicCRSP, newvar(tempFF48) type(48)
gen logmefit_NS = .
levelsof time_avail_m
foreach t of numlist `r(levels)' {

cap drop tempY

cap reg YtempBM temp* i.tempFF48 if time_avail <= `t' & time_avail_m > `t' - 60

cap predict tempY

cap replace logmefit_NS = tempY if time_avail_m == `t'
}
cap drop temp*

gen Frontier = YtempBM - logmefit_NS
replace Frontier = -1*Frontier

// filters
drop if ceq == . | ceq < 0

label var Frontier "Efficient Frontier index"
// SAVE
do "$pathCode/savepredictor" Frontier
