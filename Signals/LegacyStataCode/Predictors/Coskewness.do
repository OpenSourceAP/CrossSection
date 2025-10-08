* Coskewness
* --------------

* 2022 03 moved to simple ff mkt instead of special NYSE only index

* notes:
* smaller minimum obs helps, 12 minimum works pretty well
* choice of msia, msic, or msix actually doesn't matter much
* using NYSE only in ports helps a bit
* using simple demeaning (following ACX) works somewhat better
* real trick is to not use asrol 

timer clear
timer on 1

// DATA LOAD
* doc: see DataSet List here:
*	https://wrds-web.wharton.upenn.edu/wrds//ds/crsp/stock_a/stkmktix.cfm
* msia = NYSE 
* msic = NYSE/AMEX
* msix = NYSE/AMEX/NASDAQ
* doc for tfz*: http://www.crsp.org/products/documentation/crsp-risk-free-rates-file

use permno time_avail_m ret using "$pathDataIntermediate/monthlyCRSP.dta", clear
merge m:1 time_avail_m using "$pathDataIntermediate/monthlyFF", nogenerate keep(match) keepusing(mktrf rf)

* convert to exret "in place"
replace mkt = mktrf
replace ret = ret - rf
drop rf

// set up for looping over 60-month window sets
gen temptime = -time_avail_m
sort permno temptime
drop temptime


gen time_m = time_avail_m
format time_m %tm	
gen m60 = mod(time_avail_m,60) // month in a 60 month per year calender


save "$pathtemp/tempmerge", replace

local cdir "`c(pwd)'"
cd $pathtemp
local list : dir . files "tempcoskew*.dta"
foreach f of local list {
	display "erasing `f'"
	erase "`f'"
}
cd `cdir'

forvalues m=0/59 {
		
	display `m'	
	
	use "$pathtemp/tempmerge", clear	
		
	replace time_avail_m = . if m60 != `m'
	by permno: replace time_avail_m = time_avail_m[_n-1] if time_avail_m == .
	drop if time_avail_m == .
	drop time_m
	
	* convert to ret residuals using capm
// 	bys permno time_avail_m: asreg ret mkt, fitted
// 	replace ret = _residuals
// 	drop _*	
	
	* simple de-meaning following ACX works somewhat better
	gcollapse (mean) E_ret = ret, by(permno time_avail_m) merge
	replace ret = ret - E_ret 
	drop E_ret	

	* convert mkt to residuals by demeaning	
	gcollapse (mean) E_mkt = mkt, by(permno time_avail_m) merge
	replace mkt = mkt - E_mkt 
	drop E_mkt

	* calculate coskewness with sample moments
	gen ret2 = ret^2
	gen mkt2 = mkt^2
	gen ret_mkt2 = ret*mkt2
	gcollapse (mean) E_ret_mkt2=ret_mkt2 E_ret2=ret2 E_mkt2=mkt2 ///
		(count) nobs=ret ///
		, by(permno time_avail_m)
	gen Coskewness = E_ret_mkt2 / (sqrt(E_ret2) * E_mkt2)	// eq B-9
		
	* OP does not state the required number of obs
	keep if nobs >= 12
	
	* save
	save "$pathtemp/tempcoskew`m'", replace

} // forvalues m


// append all m60 
local cdir "`c(pwd)'"
cd $pathtemp
local files : dir "" files "tempcoskew*.dta"
display `files'
clear
foreach file in `files' {
	display "appending `file'"
	append using `file'
}
cd `cdir'

sort permno time_avail_m

timer off 1
timer list 1


label var Coskewness "Coskewness of stock return wrt market return"

// SAVE
do "$pathCode/savepredictor" Coskewness
