* --------------
// DATA LOAD
use gvkey permno time_avail_m at che ivao dlc dltt mib pstk oiadp ceq using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m
gen tempOA = at - che - ivao
replace tempOA = at - che if mi(ivao)
foreach v of varlist dlc dltt mib pstk {
gen temp`v' = `v'
replace temp`v' = 0 if mi(`v')
}
gen tempOL = at - tempdlc - tempdltt - tempmib - temppstk - ceq
gen RetNOA = l12.oiadp/(l24.tempOA - l24.tempOL)
cap drop temp*
label var RetNOA "Return on Net Operating Assets"
// SAVE
do "$pathCode/saveplacebo" RetNOA