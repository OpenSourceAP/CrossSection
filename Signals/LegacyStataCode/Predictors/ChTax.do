* ChTax
* --------------

// DATA LOAD
use permno gvkey time_avail_m at using "$pathDataIntermediate/m_aCompustat", clear

merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(txtq) nogenerate keep(match)

// SIGNAL CONSTRUCTION
xtset gvkey time_avail_m
gen ChTax = (txtq - l12.txtq)/l12.at

label var ChTax "Change in taxes"

// SAVE
do "$pathCode/savepredictor" ChTax