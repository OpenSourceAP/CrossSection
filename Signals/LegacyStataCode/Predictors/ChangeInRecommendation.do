* ChangeInRecommendation
* --------------

// PREP IBES DATA
use tickerIBES amaskcd anndats time_avail_m ireccd using "$pathDataIntermediate/IBES_Recommendations", clear

* collapse down to firm-month
gcollapse (lastnm) ireccd, by(tickerIBES amaskcd time_avail_m) // drops only 3/80
gcollapse (mean) ireccd, by(tickerIBES time_avail_m)  // drops about 1/2

* reverse score following OP
gen opscore = 6 - ireccd
bys tickerIBES (time_avail_m): ///
	gen ChangeInRecommendation = opscore - opscore[_n-1] if opscore[_n-1] != .

* add permno
merge 1:m tickerIBES time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(match) nogenerate keepusing(permno)


// SAVE
do "$pathCode/savepredictor" ChangeInRecommendation
