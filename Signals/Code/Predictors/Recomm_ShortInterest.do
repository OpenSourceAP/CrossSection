* Recomm_ShortInterest

* Prepare consensus recommendation
use tickerIBES amaskcd anndats time_avail_m ireccd using "$pathDataIntermediate/IBES_Recommendations", clear
bys tickerIBES amaskcd time_avail_m (anndats): keep if _n==_N  // Drop if more than one recommendation per month

* Use latest analyst recommendation at most 12 months prior to month t
egen tempID = group(tickerIBES amaskcd)
xtset tempID time
tsfill

* fill tickerIBES
bys tempID (time_avail_m): replace tickerIBES = tickerIBES[_n-1] if mi(tickerIBES) & _n >1

bysort tempID (time_avail_m): gen _last_time     = time_avail_m if !mi(ireccd)
bysort tempID (time_avail_m): replace _last_time = _last_time[_n-1] if missing(_last_time)

bysort tempID (time_avail_m): gen _last_val      = ireccd if !mi(ireccd) 
bysort tempID (time_avail_m): replace _last_val  = _last_val[_n-1]  if missing(_last_val)

* Compute how far back that last non-missing value is
gen _lag_len = time_avail_m - _last_time

* Use the carried value only if it's ≤ 12 periods old
gen ireccd12     = ireccd
replace ireccd12 = _last_val if missing(ireccd12) & _lag_len <= 12

* collapse down to firm-month
gcollapse (mean) ireccd12, by(tickerIBES time_avail_m)  

save tempRec, replace

// DATA LOAD
use gvkey permno iid time_avail_m shortint using "$pathDataIntermediate/monthlyShortInterest", clear
merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keep(match) nogenerate keepusing(shrout)
merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(match) nogenerate keepusing(tickerIBES)
merge m:1 tickerIBES time_avail_m using tempRec, keep(match) nogenerate

// SIGNAL CONSTRUCTION
gen ShortInterest = shortint/shrout
gen ConsRecomm = 6 - ireccd12  // To align with coding in Drake, Rees, Swanson (2011)

egen QuintShortInterest = xtile(ShortInterest), n(5) by(time_avail_m)
egen QuintConsRecomm    = xtile(ConsRecomm), n(5) by(time_avail_m)

cap drop Recomm_ShortInterest
gen Recomm_ShortInterest = .
replace Recomm_ShortInterest = 1 if QuintShortInterest == 1 & QuintConsRecomm ==1
replace Recomm_ShortInterest = 0 if QuintShortInterest == 5 & QuintConsRecomm ==5

keep if !mi(Recomm_ShortInterest)	

// SAVE
label var Recomm_ShortInterest "Recommendation and Short Interest"
do "$pathCode/savepredictor" Recomm_ShortInterest


* 
erase tempRec.dta
