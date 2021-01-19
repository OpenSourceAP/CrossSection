* ConsRecomm
* --------------

// DATA LOAD
use permno tickerIBES time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
merge m:1 tickerIBES time_avail_m using "$pathDataIntermediate/IBES_Recommendations", keep(master match) nogenerate keepusing(MeanRecomm)

// SIGNAL CONSTRUCTION
gen ConsRecomm = 1 if MeanRecomm >3 & MeanRecomm < .
replace ConsRecomm = 0 if MeanRecomm <= 1.5

label var ConsRecomm "Consensus Recommendation"

// SAVE
do "$pathCode/savepredictor" ConsRecomm