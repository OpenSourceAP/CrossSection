* --------------
// DATA LOAD
use permno gvkey time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(ibq) nogenerate keep(match)
// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen chearn = ibq - l12.ibq

* CHECKPOINT 1
list permno time_avail_m ibq chearn l3.chearn l6.chearn l9.chearn l12.chearn if permno == 10056 & time_avail_m >= tm(2001m3) & time_avail_m <= tm(2001m5), abbrev(10)

gen nincr = 0
replace nincr = 1 if chearn > 0 & l3.chearn <=0
replace nincr = 2 if chearn > 0 & l3.chearn >0 & l6.chearn <=0
replace nincr = 3 if chearn > 0 & l3.chearn >0 & l6.chearn >0 & l9.chearn <=0
replace nincr = 4 if chearn > 0 & l3.chearn >0 & l6.chearn >0 & l9.chearn >0 & l12.chearn <=0
replace nincr = 5 if chearn > 0 & l3.chearn >0 & l6.chearn >0 & l9.chearn >0 & l12.chearn >0 & l15.chearn <=0
replace nincr = 6 if chearn > 0 & l3.chearn >0 & l6.chearn >0 & l9.chearn >0 & l12.chearn >0 & l15.chearn >0 & l18.chearn <=0
replace nincr = 7 if chearn > 0 & l3.chearn >0 & l6.chearn >0 & l9.chearn >0 & l12.chearn >0 & l15.chearn >0 & l18.chearn >0 & l21.chearn <=0
replace nincr = 8 if chearn > 0 & l3.chearn >0 & l6.chearn >0 & l9.chearn >0 & l12.chearn >0 & l15.chearn >0 & l18.chearn >0 & l21.chearn >0 & l24.chearn <=0

* CHECKPOINT 2
list permno time_avail_m chearn nincr if permno == 10056 & time_avail_m >= tm(2001m3) & time_avail_m <= tm(2001m5), abbrev(10)
rename nincr NumEarnIncrease
label var NumEarnIncrease "Number of consecutive earnings increases"
// SAVE
do "$pathCode/savepredictor" NumEarnIncrease