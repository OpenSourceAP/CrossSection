* ConsRecomm
* --------------

// PREP IBES DATA
use tickerIBES amaskcd anndats time_avail_m ireccd using "$pathDataIntermediate/IBES_Recommendations", clear

* collapse down to firm-month
gcollapse (lastnm) ireccd, by(tickerIBES amaskcd time_avail_m) // drops only 3/80
gcollapse (mean) ireccd, by(tickerIBES time_avail_m)  // drops about 1/2

* define signal
gen ConsRecomm = 1 if ireccd > 3 & ireccd < .
replace ConsRecomm = 0 if ireccd <= 1.5

* add permno
merge 1:m tickerIBES time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(match) nogenerate keepusing(permno)

// SAVE
label var ConsRecomm "Consensus Recommendation"
do "$pathCode/savepredictor" ConsRecomm




// check
preserve	

	xtset permno time_avail_m
	gen signallag = l1.ConsRecomm
	
*	replace signallag = . if month(dofm(time_avail_m)) == 7
*	bys permno: replace signallag = signallag[_n-1] if missing(signallag)
	
	merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keepusing(ret mve_c exchcd prc) nogenerate keep(master match)
	replace ret = ret*100
	xtset permno time_avail_m
	gen melag = l1.mve_c

*	local nport 3
*	egen port = fastxtile(signallag), by(time_avail_m) n(`nport')
	gen port = signallag
	
	keep time_avail_m port ret signallag melag
	drop if mi(port)
	keep if year(dofm(time_avail_m)) >= 1994
	keep if year(dofm(time_avail_m)) <= 2004
	
	*tabstat signallag ret, by(port) stat(mean min max n)
	
	// SELECT ONE
	collapse (mean) ret, by(time_avail_m port)	
	*collapse (mean) ret [iweight = melag], by(time_avail_m port)				

	reshape wide ret, i(time_avail_m) j(port)
	*gen retLS = ret`nport'-ret1
	gen retLS = ret1-ret0
	summarize
	reg retLS
	
restore


