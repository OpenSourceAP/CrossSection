* --------------
// DATA LOAD
use permno gvkey time_avail_m sicCRSP using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(atq ibq dpq dvpsxq dlttq saleq) nogenerate keep(match)
// SIGNAL CONSTRUCTION
xtset permno time_avail_m
tostring sicCRSP, replace
gen tempSIC3 = substr(sicCRSP, 1, 3)
egen tempIndSales = total(saleq), by(tempSIC3 time_avail_m)
gen WW_Q = -.091* (ibq+dpq)/atq -.062*(dvpsxq>0 & !mi(dvpsxq)) + .021*dlttq/atq ///
         -.044*log(atq) + .102*(tempIndSales/l3.tempIndSales - 1) - .035*(saleq/l.saleq - 1)
label var WW_Q "Whited-Wu index (quarterly)"
// SAVE
do "$pathCode/saveplacebo" WW_Q