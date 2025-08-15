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

* DEBUG: Analyze data before tsfill
di "=== DEBUG: Pre-tsfill Analysis ==="
count
di "Total observations before tsfill: " r(N)

* Check HGR specifically
preserve
keep if tickerIBES == "HGR"
tab amaskcd
di "HGR analysts before tsfill:"
list amaskcd time_avail_m ireccd if time_avail_m >= tm(2006m1) & time_avail_m <= tm(2007m12), sepby(amaskcd)
restore

xtset tempID time
tsfill   // Fill in missing time points for each firm

* DEBUG: Analyze effect of tsfill
di "=== DEBUG: Post-tsfill Analysis ==="
count
di "Total observations after tsfill: " r(N)

* Check what tsfill did for HGR
preserve
keep if tickerIBES == "HGR" | mi(tickerIBES)
gen has_ireccd = !mi(ireccd)
bys tempID: egen n_actual = sum(has_ireccd)
bys tempID: gen n_total = _N
keep if time_avail_m == tm(2007m4)
list tempID tickerIBES amaskcd n_actual n_total if tickerIBES == "HGR"
restore

* Forward-fill tickerIBES after tsfill
bys tempID (time_avail_m): replace tickerIBES = tickerIBES[_n-1] if mi(tickerIBES) & _n >1

* Get most recent recommendation within past 12 months
asrol ireccd, gen(ireccd12) by(tempID) stat(first) window(time_avail_m 12) min(1)

* DEBUG: Analyze asrol results for HGR
di "=== DEBUG: asrol Results for HGR ==="
preserve
keep if tickerIBES == "HGR" & time_avail_m == tm(2007m4)
list tempID amaskcd ireccd ireccd12
restore

* DEBUG: Show individual analyst lookback windows
preserve
keep if tickerIBES == "HGR"
* Find tempIDs for HGR
levelsof tempID if time_avail_m == tm(2007m4), local(hgr_tempids)
foreach tid of local hgr_tempids {
    di "=== TempID `tid' lookback window ==="
    list time_avail_m ireccd if tempID == `tid' & time_avail_m >= tm(2006m5) & time_avail_m <= tm(2007m4), sepby(tempID)
}
restore 

* DEBUG: Show all analyst contributions before collapse
di "=== DEBUG: Pre-collapse HGR Analysts for 2007m4 ==="
preserve
keep if tickerIBES == "HGR" & time_avail_m == tm(2007m4)
list tempID amaskcd ireccd12
di "Number of HGR analysts contributing: " _N
su ireccd12, detail
restore

* Collapse to firm-month level
gcollapse (mean) ireccd12, by(tickerIBES time_avail_m)

* DEBUG: Verify consensus calculation
di "=== DEBUG: Post-collapse Consensus for HGR ==="
list tickerIBES time_avail_m ireccd12 if tickerIBES == "HGR" & time_avail_m == tm(2007m4)  

* CHECKPOINT 1: Check if sample missing observations exist in recommendations
di "=== CHECKPOINT 1: IBES Recommendations ==="
list tickerIBES time_avail_m ireccd12 if tickerIBES == "IBM" & time_avail_m == tm(2007m4), noobs
list tickerIBES time_avail_m ireccd12 if tickerIBES == "ACE" & (time_avail_m == tm(2006m7) | time_avail_m == tm(2008m7) | time_avail_m == tm(2009m3)), noobs

save tempRec, replace


* ---------------------------------------------------------------
* STEP 2: MERGE RECOMMENDATIONS AND SHORT INTEREST ONTO SIGNALMASTER
* ---------------------------------------------------------------
// DATA LOAD
use permno gvkey tickerIBES time_avail_m bh1m using "$pathDataIntermediate/SignalMasterTable", clear
drop if mi(gvkey) | mi(tickerIBES)

* Merge with monthly CRSP data (shares outstanding)
merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keep(match) nogenerate keepusing(shrout)

* CHECKPOINT 2: Check if sample missing observations survive CRSP merge
di "=== CHECKPOINT 2: After CRSP merge ==="
count if permno == 10051 & time_avail_m == tm(2007m4)
list permno time_avail_m gvkey tickerIBES shrout if permno == 10051 & time_avail_m == tm(2007m4), noobs
count if permno == 10104 & (time_avail_m == tm(2006m7) | time_avail_m == tm(2008m7) | time_avail_m == tm(2009m3))
list permno time_avail_m gvkey tickerIBES shrout if permno == 10104 & (time_avail_m == tm(2006m7) | time_avail_m == tm(2008m7) | time_avail_m == tm(2009m3)), noobs

* Merge with monthly short interest data
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/monthlyShortInterest", keep(match) nogenerate keepusing(shortint)

* CHECKPOINT 3: Check if sample missing observations survive short interest merge
di "=== CHECKPOINT 3: After Short Interest merge ==="
count if permno == 10051 & time_avail_m == tm(2007m4)
list permno time_avail_m gvkey tickerIBES shrout shortint if permno == 10051 & time_avail_m == tm(2007m4), noobs
count if permno == 10104 & (time_avail_m == tm(2006m7) | time_avail_m == tm(2008m7) | time_avail_m == tm(2009m3))
list permno time_avail_m gvkey tickerIBES shrout shortint if permno == 10104 & (time_avail_m == tm(2006m7) | time_avail_m == tm(2008m7) | time_avail_m == tm(2009m3)), noobs

* Merge with prepared recommendation dataset
merge m:1 tickerIBES time_avail_m using tempRec, keep(match) nogenerate

* CHECKPOINT 4: Check if sample missing observations survive recommendation merge
di "=== CHECKPOINT 4: After Recommendation merge ==="
count if permno == 10051 & time_avail_m == tm(2007m4)
list permno time_avail_m gvkey tickerIBES shrout shortint ireccd12 if permno == 10051 & time_avail_m == tm(2007m4), noobs
count if permno == 10104 & (time_avail_m == tm(2006m7) | time_avail_m == tm(2008m7) | time_avail_m == tm(2009m3))
list permno time_avail_m gvkey tickerIBES shrout shortint ireccd12 if permno == 10104 & (time_avail_m == tm(2006m7) | time_avail_m == tm(2008m7) | time_avail_m == tm(2009m3)), noobs


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

* CHECKPOINT 5: Check quintile assignments for sample missing observations
di "=== CHECKPOINT 5: After quintile creation ==="
count if permno == 10051 & time_avail_m == tm(2007m4)
list permno time_avail_m ShortInterest ConsRecomm QuintShortInterest QuintConsRecomm if permno == 10051 & time_avail_m == tm(2007m4), noobs
count if permno == 10104 & (time_avail_m == tm(2006m7) | time_avail_m == tm(2008m7) | time_avail_m == tm(2009m3))
list permno time_avail_m ShortInterest ConsRecomm QuintShortInterest QuintConsRecomm if permno == 10104 & (time_avail_m == tm(2006m7) | time_avail_m == tm(2008m7) | time_avail_m == tm(2009m3)), noobs

* Show quintile cutoffs for these dates
di "--- Quintile cutoffs for 2007m4 ---"
tabstat ShortInterest if time_avail_m == tm(2007m4), by(QuintShortInterest) stat(min max count)
tabstat ConsRecomm if time_avail_m == tm(2007m4), by(QuintConsRecomm) stat(min max count)

* Define binary signal: pessimistic vs optimistic cases
cap drop Recomm_ShortInterest
gen Recomm_ShortInterest = .
replace Recomm_ShortInterest = 1 if QuintShortInterest == 1 & QuintConsRecomm ==1
replace Recomm_ShortInterest = 0 if QuintShortInterest == 5 & QuintConsRecomm ==5

* CHECKPOINT 6: Check final signal values for sample missing observations
di "=== CHECKPOINT 6: Before final filter (keep if !mi(Recomm_ShortInterest)) ==="
count if permno == 10051 & time_avail_m == tm(2007m4)
list permno time_avail_m QuintShortInterest QuintConsRecomm Recomm_ShortInterest if permno == 10051 & time_avail_m == tm(2007m4), noobs
count if permno == 10104 & (time_avail_m == tm(2006m7) | time_avail_m == tm(2008m7) | time_avail_m == tm(2009m3))
list permno time_avail_m QuintShortInterest QuintConsRecomm Recomm_ShortInterest if permno == 10104 & (time_avail_m == tm(2006m7) | time_avail_m == tm(2008m7) | time_avail_m == tm(2009m3)), noobs

* Show distribution of signal assignments
di "--- Signal assignment counts ---"
tab Recomm_ShortInterest, missing

* Keep only defined signal observations
keep if !mi(Recomm_ShortInterest)

* CHECKPOINT 7: Final counts after filter
di "=== CHECKPOINT 7: After final filter ==="
count if permno == 10051 & time_avail_m == tm(2007m4)
count if permno == 10104 & (time_avail_m == tm(2006m7) | time_avail_m == tm(2008m7) | time_avail_m == tm(2009m3))
di "Total observations in final dataset: " _N	


* ---------------------------------------------------------------
* STEP 4: SAVE OUTPUT
* ---------------------------------------------------------------
// SAVE
label var Recomm_ShortInterest "Recommendation and Short Interest"
do "$pathCode/savepredictor" Recomm_ShortInterest

* Remove temporary recommendation file
erase tempRec.dta
