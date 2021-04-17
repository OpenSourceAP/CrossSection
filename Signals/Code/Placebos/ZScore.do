* --------------
// DATA LOAD
use gvkey permno time_avail_m act lct at lt re ni xint txt revt sic using "$pathDataIntermediate/m_aCompustat", clear
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(match) nogenerate keepusing(mve_c) 

// SIGNAL CONSTRUCTION
gen ZScore = 1.2*(act - lct)/at + 1.4*(re/at) + 3.3*(ni + xint + txt)/at + ///
    .6*(mve_c/lt) + revt/at

destring sic, replace
replace ZScore = . if (sic >3999 & sic < 5000) | sic > 5999


label var ZScore "Altman Z-Score"

// SAVE
do "$pathCode/saveplacebo" ZScore

