* AdExp
* --------------

// DATA LOAD
use permno time_avail_m xad using "$pathDataIntermediate/m_aCompustat", clear

merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(using match) nogenerate keepusing(mve_c)

// SIGNAL CONSTRUCTION
gen AdExp 	= xad/mve_c
replace AdExp = . if xad <= 0 // Following Table VII

label var AdExp "Advertising Expenses"

// SAVE
do "$pathCode/savepredictor" AdExp