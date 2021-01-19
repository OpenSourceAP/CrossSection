* ConvDebt
* --------------

// DATA LOAD
use gvkey permno time_avail_m dc cshrc using "$pathDataIntermediate/m_aCompustat", clear

// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m

gen ConvDebt 	 = 0
replace ConvDebt = 1 	if (dc !=. & dc !=0) | (cshrc !=. & cshrc !=0)

label var ConvDebt "Convertible debt indicator"

// SAVE
do "$pathCode/savepredictor" ConvDebt