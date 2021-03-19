* --------------
// DATA LOAD
use gvkey permno time_avail_m prstkc using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
gen ShareRepurchase = (prstkc > 0 & !mi(prstkc))
replace ShareRepurchase = . if mi(prstkc)
label var ShareRepurchase "Share Repurchase"
// SAVE
do "$pathCode/savepredictor" ShareRepurchase