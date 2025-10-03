* --------------
// DATA LOAD
use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(dlttq dlcq pstkq cheq atq ibq ceqq) nogenerate keep(master match)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_aCompustat", keep(match) nogenerate keepusing(sic ceq csho prcc_f) 
// SIGNAL CONSTRUCTION
destring sic, replace
gen NetDebtPrice_q = ((dlttq + dlcq + pstkq) - cheq)/mve_c
replace NetDebtPrice_q = . if sic >= 6000 & sic <= 6999
replace NetDebtPrice_q = . if mi(atq) | mi(ibq) | mi(csho) | mi(ceqq) | mi(prcc_f)
* keep constant B/M, as in Table 4
gen BM = log(ceq/mve_c)
egen tempsort = fastxtile(BM), by(time_avail_m) n(5)
replace NetDebtPrice_q = . if tempsort <= 2
label var NetDebtPrice_q "Net debt to price ratio (quarterly)"
// SAVE
do "$pathCode/saveplacebo" NetDebtPrice_q