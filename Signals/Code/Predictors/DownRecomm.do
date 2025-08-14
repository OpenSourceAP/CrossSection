* DownRecomm 
* --------------

// PREP IBES DATA
use tickerIBES amaskcd anndats time_avail_m ireccd using "$pathDataIntermediate/IBES_Recommendations", clear

* collapse down to firm-month
gcollapse (lastnm) ireccd, by(tickerIBES amaskcd time_avail_m) // drops only 3/80
* CHECKPOINT 1: After first gcollapse
list tickerIBES time_avail_m ireccd if tickerIBES == "AAPL" & time_avail_m == tm(1993m11), noobs
gcollapse (mean) ireccd, by(tickerIBES time_avail_m)  // drops about 1/2
* CHECKPOINT 2: After second gcollapse
list tickerIBES time_avail_m ireccd if tickerIBES == "AAPL" & time_avail_m == tm(1993m11), noobs

bys tickerIBES (time_avail_m): ///
	gen DownRecomm = ireccd > ireccd[_n-1] & ireccd[_n-1] != .
* CHECKPOINT 3: After creating DownRecomm variable
list tickerIBES time_avail_m ireccd DownRecomm if tickerIBES == "AAPL" & time_avail_m == tm(1993m11), noobs

* add permno
merge 1:m tickerIBES time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(match) nogenerate keepusing(permno)
* CHECKPOINT 4: After merge with SignalMasterTable
list permno time_avail_m DownRecomm if permno == 10001 & time_avail_m == tm(1993m11), noobs

// SAVE
label var DownRecomm "Recommendation Downgrade"
do "$pathCode/savepredictor" DownRecomm

