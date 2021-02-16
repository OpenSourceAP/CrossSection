* UpRecomm 
* --------------

// PREP IBES DATA
use tickerIBES amaskcd anndats time_avail_m ireccd using "$pathDataIntermediate/IBES_Recommendations", clear

* collapse down to firm-month
gcollapse (lastnm) ireccd, by(tickerIBES amaskcd time_avail_m) // drops only 3/80
gcollapse (mean) ireccd, by(tickerIBES time_avail_m)  // drops about 1/2

bys tickerIBES (time_avail_m): ///
	gen UpRecomm = ireccd < ireccd[_n-1] & ireccd[_n-1] != .

* add permno
merge 1:m tickerIBES time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(match) nogenerate keepusing(permno)


// SAVE
label var UpRecomm "Recommendation Upgrade"
do "$pathCode/savepredictor" UpRecomm

