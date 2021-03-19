* BookLeverage
* --------------

// DATA LOAD
use permno time_avail_m at lt txditc pstk pstkrv pstkl seq ceq using "$pathDataIntermediate/m_aCompustat", clear
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations

// SIGNAL CONSTRUCTION
replace txditc = 0 if mi(txditc)
gen tempPS = pstk
replace tempPS = pstkrv if mi(tempPS)
replace tempPS = pstkl if mi(tempPS)

gen tempSE = seq
replace tempSE = ceq + tempPS if mi(tempSE)
replace tempSE = at - lt if mi(tempSE)

gen BookLeverage = at/(tempSE + txditc - tempPS)

label var BookLeverage "Book leverage (annual)"

// SAVE
do "$pathCode/savepredictor" BookLeverage