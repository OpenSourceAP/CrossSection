* ===============================================================
* Recomm_ShortInterest
* Construct a binary signal from analyst recommendations & short interest
* ===============================================================


* ---------------------------------------------------------------
* STEP 1: PREPARE CONSENSUS RECOMMENDATION DATA
* ---------------------------------------------------------------
use tickerIBES amaskcd anndats time_avail_m ireccd using "$pathDataIntermediate/IBES_Recommendations", clear
bys tickerIBES amaskcd time_avail_m (anndats): keep if _n==_N  // Keep only latest recommendation per firm-month

* Create firm ID and set panel for time-series filling
egen tempID = group(tickerIBES amaskcd)
xtset tempID time
tsfill   // Fill in missing time points for each firm

* Forward-fill tickerIBES after tsfill
bys tempID (time_avail_m): replace tickerIBES = tickerIBES[_n-1] if mi(tickerIBES) & _n >1

* Get most recent recommendation within past 12 months
asrol ireccd, gen(ireccd12) by(tempID) stat(first) window(time_avail_m 12) min(1) 

* Collapse to firm-month level
gcollapse (mean) ireccd12, by(tickerIBES time_avail_m)  

save tempRec, replace


* ---------------------------------------------------------------
* STEP 2: MERGE RECOMMENDATIONS AND SHORT INTEREST ONTO SIGNALMASTER
* ---------------------------------------------------------------
// DATA LOAD
use permno gvkey tickerIBES time_avail_m bh1m using "$pathDataIntermediate/SignalMasterTable", clear
drop if mi(gvkey) | mi(tickerIBES)

* Merge with monthly CRSP data (shares outstanding)
merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keep(match) nogenerate keepusing(shrout)

* Merge with monthly short interest data
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/monthlyShortInterest", keep(match) nogenerate keepusing(shortint)

* Merge with prepared recommendation dataset
merge m:1 tickerIBES time_avail_m using tempRec, keep(match) nogenerate


* ---------------------------------------------------------------
* STEP 3: SIGNAL CONSTRUCTION
* ---------------------------------------------------------------
* Short interest as proportion of shares outstanding
gen ShortInterest = shortint/shrout

* Reverse recommendation coding so higher is more positive
gen ConsRecomm = 6 - ireccd12  // Matches Drake, Rees, Swanson (2011) coding

* Create quintiles by month
egen QuintShortInterest = xtile(ShortInterest), n(5) by(time_avail_m)
egen QuintConsRecomm    = xtile(ConsRecomm), n(5) by(time_avail_m)

* Define binary signal: pessimistic vs optimistic cases
cap drop Recomm_ShortInterest
gen Recomm_ShortInterest = .
replace Recomm_ShortInterest = 1 if QuintShortInterest == 1 & QuintConsRecomm ==1
replace Recomm_ShortInterest = 0 if QuintShortInterest == 5 & QuintConsRecomm ==5

* Keep only defined signal observations
keep if !mi(Recomm_ShortInterest)	


* ---------------------------------------------------------------
* STEP 4: SAVE OUTPUT
* ---------------------------------------------------------------
// SAVE
label var Recomm_ShortInterest "Recommendation and Short Interest"
do "$pathCode/savepredictor" Recomm_ShortInterest

* Remove temporary recommendation file
erase tempRec.dta
