// 2021 01 ac: 
// added sic and ceq filter, changed to deciles following tab 3b
// It seems like delisting returns make a big difference for the high yield portfolio!
// Overall, not a super robust predictor, but it still has some power
// things that help: all stock breaks, deciles, short port period, 
// basically this is stronger in small stocks
* --------------
// DATA LOAD
use permno time_avail_m dvc prstkc pstkrv sic ceq datadate using "$pathDataIntermediate/m_aCompustat", clear
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(match) nogenerate keepusing(mve_c) 

destring sic, replace
keep if (sic < 6000 | sic >= 7000) & ceq > 0 // OP p 5: each of these filters helps
sort permno time_avail_m
bysort permno: keep if _n >= 24

// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen PayoutYield = (dvc + prstkc + max(pstkrv,0))/l6.mve_c
replace PayoutYield = . if PayoutYield <= 0 // critical
label var PayoutYield "Payout Yield"


// SAVE
do "$pathCode/savepredictor" PayoutYield


// check cts
preserve	

	xtset permno time_avail_m
	gen signallag = l1.PayoutYield
	
	*replace signallag = . if month(dofm(time_avail_m)) == 7
	*bys permno: replace signallag = signallag[_n-1] if missing(signallag)
	
	merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keepusing(ret mve_c exchcd prc) nogenerate keep(master match)
	replace ret = ret*100
	xtset permno time_avail_m
	gen melag = l1.mve_c

	local nport 5
	egen port = fastxtile(signallag), by(time_avail_m) n(`nport')
	*bys time_avail_m: astile port = signallag, qc(exchcd == 1) nq(`nport')
	*gen port = signallag
	
	keep time_avail_m port ret signallag melag
	drop if mi(port)
	keep if year(dofm(time_avail_m)) >= 1984
	keep if year(dofm(time_avail_m)) <= 2003
	
	tabstat signallag ret, by(port) stat(mean n)
	
	// SELECT ONE
	collapse (mean) ret, by(time_avail_m port)	
	*collapse (mean) ret [iweight = melag], by(time_avail_m port)				

	reshape wide ret, i(time_avail_m) j(port)
	gen retLS = ret`nport'-ret1
	*gen retLS = ret1-ret0
	summarize
	reg retLS
	
restore



// check in detail

	xtset permno time_avail_m
	gen signallag = l1.PayoutYield
	
	*replace signallag = . if month(dofm(time_avail_m)) == 7
	*bys permno: replace signallag = signallag[_n-1] if missing(signallag)
	
	merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keepusing(ret mve_c exchcd prc) nogenerate keep(master match)
	replace ret = ret*100
	xtset permno time_avail_m
	gen melag = l1.mve_c

	local nport 5
	egen port = fastxtile(signallag), by(time_avail_m) n(`nport')
	*bys time_avail_m: astile port = signallag, qc(exchcd == 1) nq(`nport')
	*gen port = signallag
	
	keep time_avail_m port ret signallag melag
	drop if mi(port)
	keep if year(dofm(time_avail_m)) >= 1984
	keep if year(dofm(time_avail_m)) <= 2003
	
	tabstat signallag ret, by(port) stat(mean n)
	
preserve 
	// SELECT ONE
	collapse (mean) signallag, by(time_avail_m port)	
	reshape wide signallag, i(time_avail_m) j(port)
	summarize	
restore
