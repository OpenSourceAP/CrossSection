* --------------
// DATA LOAD
use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(atq ceqq cheq ivaoq dlcq dlttq mibq pstkq oiadpq) nogenerate keep(match)
// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen tempOA = atq - cheq - ivaoq
replace tempOA = atq - cheq if mi(ivaoq)
foreach v of varlist dlcq dlttq mibq pstkq {
    gen temp`v' = `v'
    replace temp`v' = 0 if mi(`v')
}
gen tempOL = atq - tempdlcq - tempdlttq - tempmibq - temppstkq - ceqq
gen RetNOA_q = oiadpq/(l3.tempOA - l3.tempOL)
label var RetNOA_q "Return on Net Operating Assets (quarterly)"
// SAVE
do "$pathCode/saveplacebo" RetNOA_q