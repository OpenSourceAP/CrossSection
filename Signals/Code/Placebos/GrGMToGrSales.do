* --------------
// DATA LOAD
use gvkey permno time_avail_m sale cogs using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m
gen tempGM = sale-cogs
gen GrGMToGrSales = ((tempGM- (.5*(l12.tempGM + l24.tempGM)))/(.5*(l12.tempGM + l24.tempGM))) ///
    - ((sale- (.5*(l12.sale + l24.sale)))/(.5*(l12.sale + l24.sale)))
replace GrGMToGrSales =  ((tempGM-l12.tempGM)/l12.tempGM)- ((sale-l12.sale)/l12.sale) if mi(GrGMToGrSales)
drop tempGM
label var GrGMToGrSales "Gross Margin growth over sales growth"
// SAVE
do "$pathCode/saveplacebo" GrGMToGrSales