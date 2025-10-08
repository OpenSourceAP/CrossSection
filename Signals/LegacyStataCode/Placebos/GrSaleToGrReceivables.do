* --------------
// DATA LOAD
use gvkey permno time_avail_m sale rect using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m
gen GrSaleToGrReceivables = ((sale- (.5*(l12.sale + l24.sale)))/(.5*(l12.sale + l24.sale))) ///
    -((rect- (.5*(l12.rect + l24.rect)))/(.5*(l12.rect + l24.rect)))
replace GrSaleToGrReceivables =  ((sale-l12.sale)/l12.sale)-((rect-l12.rect)/l12.rect) if mi(GrSaleToGrReceivables)
label var GrSaleToGrReceivables "Sales growth over receivables growth"
// SAVE
do "$pathCode/saveplacebo" GrSaleToGrReceivables