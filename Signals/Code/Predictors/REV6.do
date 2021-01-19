* --------------
// DATA LOAD
use permno tickerIBES time_avail_m prc using "$pathDataIntermediate/SignalMasterTable", clear
merge m:1 tickerIBES time_avail_m using "$pathDataIntermediate/IBES_EPS", keep(master match) nogenerate keepusing(meanest)

// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen tempRev = (meanest - l.meanest)/abs(l.prc)
gen REV6 = tempRev + l.tempRev + l2.tempRev + l3.tempRev + l4.tempRev + l5.tempRev + l6.tempRev
label var REV6 "Earnings forecast revision"

// SAVE
do "$pathCode/savepredictor" REV6