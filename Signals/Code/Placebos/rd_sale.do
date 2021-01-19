* --------------
// DATA LOAD
use gvkey permno time_avail_m xrd sale using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen rd_sale     =   l12.xrd/l12.sale  // Returns seem to be strongest in the second year after portfolio formation (table IV of Chan et al paper)
replace rd_sale = . if rd_sale == 0
label var rd_sale "R&D-to-sales ratio"
// SAVE
do "$pathCode/saveplacebo" rd_sale