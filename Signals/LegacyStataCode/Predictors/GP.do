* --------------
// DATA LOAD
use gvkey permno time_avail_m revt cogs at sic datadate using "$pathDataIntermediate/m_aCompustat", clear

destring sic, replace
keep if (sic < 6000 | sic >= 7000) 

// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen GP = (revt-cogs)/at

label var GP "Gross profitability"

// SAVE
do "$pathCode/savepredictor" GP

