* --------------
// DATA LOAD
use permno time_avail_m at che dltt dlc mib pstk ceq using "$pathDataIntermediate/m_aCompustat", clear
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen tempOA = at - che
foreach v of varlist dltt dlc mib pstk {
    gen temp`v' = `v'
    replace temp`v' = 0 if mi(temp`v')
}
gen tempOL = at - tempdltt - tempmib - tempdlc - temppstk - ceq
gen tempNOA = tempOA - tempOL
gen dNoa = (tempNOA - l12.tempNOA)/l12.at
label var dNoa "Change in Net Operating Assets"
// SAVE
do "$pathCode/savepredictor" dNoa