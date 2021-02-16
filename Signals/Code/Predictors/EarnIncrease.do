* --------------
// DATA LOAD
use permno gvkey time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(ibq) nogenerate keep(match)

// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen temp = ibq - l12.ibq
gen EarnIncrease = 1 if temp > 0 & l3.temp > 0 & l6.temp > 0 & l9.temp > 0 & l12.temp > 0 ///
               & !mi(temp) & !mi(l3.temp) & !mi(l6.temp) & !mi(l9.temp) & !mi(l12.temp)
replace EarnIncrease = 0 if temp < 0 & l3.temp < 0 & l6.temp < 0 & l9.temp < 0 & l12.temp < 0 ///
               & !mi(temp) & !mi(l3.temp) & !mi(l6.temp) & !mi(l9.temp) & !mi(l12.temp)                     
label var EarnIncrease "Consistent Earnings Increase (quarterly)"

// SAVE
*do "$pathCode/savepredictor" EarnIncrease
