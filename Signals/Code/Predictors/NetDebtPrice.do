* --------------
// DATA LOAD
use permno time_avail_m at dltt dlc pstk dvpa tstkp che sic ib csho ceq prcc_f using "$pathDataIntermediate/m_aCompustat", clear
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(match) nogenerate keepusing(mve_c) 
// SIGNAL CONSTRUCTION
destring sic, replace
gen NetDebtPrice = ((dltt + dlc + pstk + dvpa - tstkp) - che)/mve_c
replace NetDebtPrice = . if sic >= 6000 & sic <= 6999
replace NetDebtPrice = . if mi(at) | mi(ib) | mi(csho) | mi(ceq) | mi(prcc_f)
* keep constant B/M, as i nTable 4
gen BM = log(ceq/mve_c)
egen tempsort = fastxtile(BM), by(time_avail_m) n(5)
replace NetDebtPrice = . if tempsort <= 2
label var NetDebtPrice "Net debt to price ratio"
// SAVE
do "$pathCode/savepredictor" NetDebtPrice