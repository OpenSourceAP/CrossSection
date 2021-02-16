// // # 2021 01 ac: new portfolio code had a problem with conversion of monthly data 
// to annual rebalancing.  Looking closer at OP: OP actually used quarterly data with 
// a 3-month lag, then selected only close-to-december fiscal years, then 
// converted to annual.  This is more aggressive than our annual data with a 6 month lag
// , so to try to get close I added an annual smoothing / conversion at the end of 
// the MS computation.

* --------------
// DATA LOAD
use permno gvkey time_avail_m datadate at ceq ni oancf fopt wcapch ib dp xrd capx xad revt using "$pathDataIntermediate/m_aCompustat", clear
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
merge 1:1 permno gvkey time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(match) nogenerate keepusing(mve_c sicCRSP) 
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keep(master match) nogenerate keepusing(niq atq saleq oancfy capxy) 

// prep variables
xtset permno time_avail_m
replace xad = 0 if mi(xad) 

* aggregate quarterly
gen oancfq = oancfy - l3.oancfy // see "locating oancfq" on wrds
replace oancfq = oancfy if l3.oancfy == .
gen capxq = capxy - l3.capxy // see "locating oancfq" on wrds
replace capxq = capxy if l3.capxy == .
bys permno: asrol niq, gen(niqsum) stat(sum) window(time_avail_m 4) min(4)
bys permno: asrol oancfq, gen(oancfqsum) stat(sum) window(time_avail_m 4) min(4)
replace oancfqsum = fopt - wcapch if year(datadate) <= 1988 // endnote 3

// SAMPLE SELECTION
* Limit sample to firms in the lowest BM quintile (see p 8 OP)
* (has to be done first!, see also MP)
gen BM = log(ceq/mve_c)
egen temp = fastxtile(BM), by(time_avail_m) n(5) 
keep if temp == 1 & ceq > 0
drop temp

* keep if at least 3 firms in sic2D (p 8)
tostring sicCRSP, replace
gen sic2D = substr(sicCRSP,1,2)
egen tempN = count(at), by(sic2D time_avail_m)
keep if tempN >= 3
drop tempN

save "$pathtemp/debug", replace

use "$pathtemp/debug", clear

// SIGNAL CONSTRUCTION
* profitability and cash flow signals 
* OP uses annualized financials, but shouldn't much difference...
gen atdenom = (atq+l3.atq)/2 // OP p 6, needs to be done later?

gen roa = niqsum/atdenom
gen cfroa = oancfqsum/atdenom
foreach v of varlist roa cfroa {
	egen md_`v' = median(`v'), by(sic2D time_avail_m)
}
gen m1 = 0
replace m1 = 1 if roa > md_roa
gen m2 = 0
replace m2 = 1 if cfroa > md_cfroa
gen m3 = 0 
replace m3 = 1 if oancfqsum > niqsum

* "naive extrapolation" according to OP
* quarterly is used here
gen roaq = niq/atq
gen sg = saleq / l3.saleq
bys permno: asrol roaq, gen(niVol) stat(sd) window(time_avail_m 48) min(18)
bys permno: asrol sg, gen(revVol) stat(sd) window(time_avail_m 48) min(18)

foreach v of varlist niVol revVol {
	egen md_`v' = median(`v'), by(sic2D time_avail_m)
}
gen m4 = 0
replace m4 = 1 if niVol < md_niVol
gen m5 = 0
replace m5 = 1 if revVol < md_revVol


* "Conservatism" according to OP
* OP also uses annualized financials here
gen atdenom2 = l3.atq  // (OP p5)
gen xrdint = xrd/atdenom2
gen capxint = capx/atdenom2
gen xadint = xad/atdenom2
foreach v of varlist xrdint capxint xadint {
	egen md_`v' = median(`v'), by(sic2D time_avail_m)
}
gen m6 = 0
replace m6 = 1 if xrdint > md_xrdint
gen m7 = 0
replace m7 = 1 if capxint > md_capxint
gen m8 = 0
replace m8 = 1 if xadint > md_xadint

gen tempMS = m1 + m2 + m3 + m4 + m5 + m6 + m7 + m8

* fix tempMS at most recent data release for entire yer
foreach v of varlist tempMS {
	replace `v' = . if month(dofm(time_avail_m)) != mod(month(datadate)+6,12)
	bysort permno: replace `v'= `v'[_n-1] if missing(`v') & _n > 1
}

gen MS = tempMS
replace MS = 6 if tempMS >= 6 & tempMS <= 8
replace MS = 1 if tempMS <= 1


label var MS "Mohanram G-score"

// SAVE
do "$pathCode/savepredictor" MS





// custom
preserve	
	replace time_avail_m = time_avail_m + 1
	gen signallag = MS
	keep permno time_avail_m signallag	
	
	merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keepusing(ret mve_c exchcd prc) nogenerate keep(master match)
	replace ret = ret*100			

	*local nport 4
	*egen port = fastxtile(signallag), by(time_avail_m) n(`nport')
	gen port = signallag
	
	cap sum port 
	local maxport `r(max)'
	local minport `r(min)'	

	drop if mi(port)
	keep if year(dofm(time_avail_m)) >= 1979
	keep if year(dofm(time_avail_m)) <= 2001
	
	*tabstat signallag ret, by(port) stat(mean min max n)
	
	// SELECT ONE
	collapse (mean) ret, by(time_avail_m port)	
	*gen melag = l1.mve_c
	*collapse (mean) ret [iweight = melag], by(time_avail_m port)				

	cap reshape wide ret, i(time_avail_m) j(port)
	gen retLS = ret`maxport' - ret`minport'
	summarize
	reg retLS
	
restore

