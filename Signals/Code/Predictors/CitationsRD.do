* CitationsRD
* --------------

// DATA LOAD
use permno gvkey time_avail_m mve_c sicCRSP exchcd using "$pathDataIntermediate/SignalMasterTable", clear
gen year = yofd(dofm(time_avail_m))
merge 1:1 permno time_avail_m using "$pathDataIntermediate/m_aCompustat", nogenerate keep(master match) keepusing(xrd sich datadate ceq)
drop if gvkey == .

// patent citation dataset
* compustat is already lagged (time_avail_m = June uses at from Dec)
* so we need to lag patent data to match 
merge m:1 gvkey year using "$pathDataIntermediate/PatentDataProcessed", keep(master match) nogenerate keepusing(ncitscale)

xtset permno time_avail_m
gen temp = l6.ncitscale // year t is matched with July t+1
replace temp = 0 if mi(temp)
replace ncitscale = temp
drop temp

// SIGNAL CONSTRUCTION
* form portfolios only in june
drop if time_avail_m < ym(1975,1)  // Takes into account that xrd data standardized after 1975
keep if month(dofm(time_avail_m)) == 6

xtset permno time_avail_m
gen xrd_lag = l24.xrd
replace xrd_lag = 0 if xrd_lag == .
bys permno: asrol xrd_lag, window(time_avail_m 48) stat(sum) gen(sum_xrd)
bys permno: asrol ncitscale, window(time_avail_m 48) stat(sum) gen(sum_ncit)

gen tempCitationsRD  = sum_ncit/sum_xrd if sum_xrd > 0

// Filter
bysort gvkey (time_avail_m): drop if _n <= 2
drop if sicCRSP >= 6000 & sicCRSP <= 6999
drop if ceq < 0

// double indep sort (can't just drop high mve_c, need indep)
bys time_avail_m: astile sizecat = mve_c, qc(exchcd == 1) nq(2)
egen maincat = fastxtile(tempCitationsRD), by(time_avail_m) n(3)

// * following FF1993, others, first digit is S or B, second digit is L,M,or H
// * i.e. 13 = S/H, then VW before compbining
// * too difficult to implement in spreadsheet
// * just do simple binary VW for ease
gen CitationsRD = 1 if sizecat == 1 & maincat == 3
replace CitationsRD = 0 if sizecat == 1 & maincat == 1
	
// expand back to monthly
gen temp = 12
expand temp
drop temp

gen tempTime = time_avail_m
bysort gvkey tempTime: replace time_avail_m = time_avail_m + _n - 1 
drop tempTime

label var CitationsRD "Citations to RD expenses"

// SAVE
do "$pathCode/savepredictor" CitationsRD


// binary
preserve	

	xtset permno time_avail_m
	gen signallag = l1.CitationsRD
	
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
	keep if year(dofm(time_avail_m)) >= 1982
	keep if year(dofm(time_avail_m)) <= 2008
	
	*tabstat signallag ret, by(port) stat(mean min max n)
	
	// SELECT ONE
	*collapse (mean) ret, by(time_avail_m port)	
	collapse (mean) ret [iweight = melag], by(time_avail_m port)				

	reshape wide ret, i(time_avail_m) j(port)
	*gen retLS = ret`nport'-ret1
	gen retLS = ret1-ret0
	summarize
	reg retLS
	
restore


