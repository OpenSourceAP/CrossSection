* --------------
// DATA LOAD
use permno time_avail_m ceq dltis using "$pathDataIntermediate/m_aCompustat", clear
merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(match) nogenerate keepusing(mve_c shrcd) 
// SIGNAL CONSTRUCTION
gen BM = log(ceq/mve_c)
gen DebtIssuance = (dltis > 0 & dltis !=.)
replace DebtIssuance = . if shrcd > 11 | mi(BM)
label var DebtIssuance "Debt Issuance"
// SAVE
do "$pathCode/savepredictor" DebtIssuance