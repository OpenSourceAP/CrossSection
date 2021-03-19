* --------
// DATA LOAD
use "$pathDataIntermediate/dailyCRSP.dta", clear

// SIGNAL CONSTRUCTION
gen time_avail_m = mofd(time_d)
format time_avail_m %tm

gen prcadj = abs(prc)/cfacpr
gcollapse (max) maxpr = prcadj (lastnm) prcadj, by(permno time_avail_m)
xtset permno time_avail_m
gen temp = max(l1.maxpr, l2.maxpr, l3.maxpr, l4.maxpr, l5.maxpr, l6.maxpr, ///
    l7.maxpr, l8.maxpr, l9.maxpr, l10.maxpr, l11.maxpr, l12.maxpr)
    
gen High52 = prcadj / temp
drop temp*
label var High52 "52-week High"
// SAVE
do "$pathCode/savepredictor" High52

// check
preserve	
	xtset permno time_avail_m
	gen signallag = l1.High52
	
	merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keepusing(ret mve_c exchcd prc) nogenerate keep(master match)
	replace ret = ret*100
	xtset permno time_avail_m
		
	//drop if exchcd != 1
	//drop if abs(prclag) < 5

	local nport 3
	egen port = fastxtile(signallag), by(time_avail_m) n(`nport')
	//gen port = signallag
	
	keep time_avail_m port ret signallag 
	drop if mi(port)
	keep if year(dofm(time_avail_m)) >= 1964
	keep if year(dofm(time_avail_m)) <= 2000
	
	// SELECT ONE
	collapse (mean) ret, by(time_avail_m port)	
*	collapse (mean) ret [iweight = melag], by(time_avail_m port)				

	reshape wide ret, i(time_avail_m) j(port)
	gen retLS = ret`nport'-ret1
	//gen retLS = ret1-ret0
	summarize
	reg retLS
	
restore
