* --------------
// DATA LOAD
use gvkey permno time_avail_m sic sale ib dp at dvpsx_c dltt at using "$pathDataIntermediate/m_aCompustat", clear
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(match) nogenerate keepusing(sicCRSP)
// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
xtset permno time_avail_m
gen tempSIC = sicCRSP
tostring tempSIC, replace
gen tempSIC3 = substr(tempSIC, 1, 3)
egen tempIndSales = total(sale), by(tempSIC3 time_avail_m)
* Divide CF and growth rates by 4 to approximate quarterly rates
gen WW = -.091* (ib+dp)/(4*at) -.062*(dvpsx_c>0 & !mi(dvpsx_c)) + .021*dltt/at ///
         -.044*log(at) + .102*(tempIndSales/l12.tempIndSales - 1)/4 - .035*(sale/l.sale - 1)/4


 
label var WW "Whited-Wu index (annual)"
// SAVE
do "$pathCode/saveplacebo" WW