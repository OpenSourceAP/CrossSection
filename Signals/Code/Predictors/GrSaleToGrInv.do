* --------------
// DATA LOAD
use gvkey permno time_avail_m sale invt using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m
gen GrSaleToGrInv = ((sale- (.5*(l12.sale + l24.sale)))/(.5*(l12.sale + l24.sale))) ///
    -((invt- (.5*(l12.invt + l24.invt)))/(.5*(l12.invt + l24.invt)))
replace GrSaleToGrInv =  ((sale-l12.sale)/l12.sale)-((invt-l12.invt)/l12.invt) if mi(GrSaleToGrInv)
label var GrSaleToGrInv "Sales growth over inventory growth"
// SAVE
do "$pathCode/savepredictor" GrSaleToGrInv