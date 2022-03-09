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

asrol ireccd, gen(ireccd12) by(tempID) stat(first) window(time_avail_m 12) min(1) 

* collapse down to firm-month
gcollapse (mean) ireccd12, by(tickerIBES time_avail_m)  

save tempRec, replace

// DATA LOAD
use permno gvkey tickerIBES time_avail_m bh1m using "$pathDataIntermediate/SignalMasterTable", clear
drop if mi(gvkey) | mi(tickerIBES)
merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keep(match) nogenerate keepusing(shrout)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/monthlyShortInterest", keep(match) nogenerate keepusing(shortint)
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
