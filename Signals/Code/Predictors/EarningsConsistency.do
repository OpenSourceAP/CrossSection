* --------------
// DATA LOAD
use permno time_avail_m epspx using "$pathDataIntermediate/m_aCompustat", clear
// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen temp = (epspx - l12.epspx)/(.5*(abs(l12.epspx) + abs(l24.epspx)))
foreach n of numlist 12(12)48 {

gen temp`n' = l`n'.temp

}
egen EarningsConsistency = rowmean(temp*)
replace EarningsConsistency = . if abs(epspx/l12.epspx) > 6 | ///
    (temp > 0 & l12.temp < 0 & !mi(temp)) | (temp < 0 & l12.temp > 0 & !mi(temp))
    
label var EarningsConsistency "Earnings Consistency"
// SAVE
do "$pathCode/savepredictor" EarningsConsistency