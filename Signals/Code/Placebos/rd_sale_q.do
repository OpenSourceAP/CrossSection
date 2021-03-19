* --------------
// DATA LOAD
use permno gvkey time_avail_m prc using "$pathDataIntermediate/SignalMasterTable", clear
drop if mi(gvkey)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(xrdq saleq) nogenerate keep(match)
// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen rd_sale_q =  l12.xrdq/l12.saleq  
replace rd_sale_q = . if rd_sale_q == 0
label var rd_sale_q "R&D-to-sales ratio (quarterly)"
// SAVE
do "$pathCode/saveplacebo" rd_sale_q