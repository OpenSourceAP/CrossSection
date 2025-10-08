* --------------
// DATA LOAD
use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(piq niq) nogenerate keep(match)
// SIGNAL CONSTRUCTION
gen Tax_q = piq/niq if piq >0 & niq >0
label var Tax_q "Taxable income to income"
// SAVE
do "$pathCode/saveplacebo" Tax_q