* --------------
// DATA LOAD
use permno gvkey time_avail_m sale ib dp ni ceq using "$pathDataIntermediate/m_aCompustat", clear
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keepusing(ret mve_c) nogenerate keep(match)
// SIGNAL CONSTRUCTION
gen tempAccBM = log(ceq/mve_c)
gen tempAccSP = sale/mve_c
gen tempAccCFP = (ib + dp)/mve_c
gen tempAccEP = ni/mve_c
// Cumulative return (based on return adjusted for splits and dividends)
xtset permno time_avail_m
replace ret = 0 if mi(ret)
bys permno: gen tempCumRet = exp(sum(log(1+ ret)))  
gen tempRet60 = (tempCumRet - l60.tempCumRet)/l60.tempCumRet
winsor2 tempRet60, replace cut(1 99) trim
foreach v of varlist tempAcc* {  // Loop over four measures

gen `v'Ret = `v' - l60.`v' + tempRet60

gen tempU_`v' = .


levelsof time_avail_m  // Loop over cross-sectional regressions

foreach t of numlist `r(levels)' {


cap reg tempRet60 l60.`v' `v'Ret if time_avail_m == `t'


cap predict tempResid, resid


cap replace tempU_`v' = tempResid if time_avail_m == `t'


cap drop tempResid

}
}
rename tempU_tempAccBM IntanBM
label var IntanBM "Intangible return (BM)"
rename tempU_tempAccSP IntanSP
label var IntanSP "Intangible return (SP)"
rename tempU_tempAccCFP IntanCFP
label var IntanCFP "Intangible return (CFP)"
rename tempU_tempAccEP IntanEP
label var IntanEP "Intangible return (EP)"

// SAVE 
do "$pathCode/savepredictor" IntanBM
do "$pathCode/savepredictor" IntanSP
do "$pathCode/savepredictor" IntanCFP
do "$pathCode/savepredictor" IntanEP