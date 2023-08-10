* -------------------------
* follows Appendix and Table 8 caption
* we used to download NYSE CRSP only for this predictor to be super
* careful but it doesn't make much difference.  Updated 2022 03
* Our notes say it works better with standard CRSP VW index, but t-stat
* is closer to OP using NYSE CRSP

timer clear
timer on 1

// DATA LOAD
use permno time_d ret using "$pathDataIntermediate/dailyCRSP.dta", clear
	keep if time_d >= date("19620702","YMD")	

merge m:1 time_d using "$pathDataIntermediate/dailyFF", nogenerate keep(match) keepusing(mktrf rf) 
gen mkt = mktrf + rf
	

* convert to cts compounded exret "in place"
replace mkt = log(1+mkt) - log(1+rf) 
replace ret = log(1+ret) - log(1+rf) 
drop rf

* set up for 12-month "periods"
gen temptime = -time_d
sort permno temptime
drop temptime

// set up for looping over Jan - Dec
save "$pathtemp/tempdailymerge", replace

local cdir "`c(pwd)'"
cd $pathtemp
local list : dir . files "tempcoskew*.dta"
foreach f of local list {
	display "erasing `f'"
	erase "`f'"
}
cd `cdir'

forvalues m=1/12 {
		
	use "$pathtemp/tempdailymerge", clear	
	
	* pretend we're in end of month m, and we're looking back over the 12 months	
	* (dataset is sorted in reverse time)
	display `m'	
	gen time_avail_m = mofd(time_d) if month(time_d) == `m'
	format time_avail_m %tm
	by permno: replace time_avail_m = time_avail_m[_n-1] if time_avail_m == .
	drop if time_avail_m == .
	drop time_d

	* demean returns within each 12-month period
	gcollapse (mean) E_ret = ret E_mkt = mkt, by(permno time_avail_m) merge
	replace ret = ret - E_ret // called \tilde{r}_{it} in ACX appendix
	replace mkt = mkt - E_mkt // called \tilde{r}_{mt} in ACX appendix
	drop E_ret E_mkt

	* calculate coskewness with sample moments
	gen ret2 = ret^2
	gen mkt2 = mkt^2
	gen ret_mkt2 = ret*mkt2
	gcollapse (mean) E_ret_mkt2=ret_mkt2 E_ret2=ret2 E_mkt2=mkt2 ///
		(count) nobs=ret ///
		, by(permno time_avail_m)
	gen CoskewACX = E_ret_mkt2 / (sqrt(E_ret2) * E_mkt2)	// eq B-9	
	
	
	* exclude of more than five missing obs (just above eq B-7)	
	gcollapse (max) max_nobs = nobs, by (time_avail_m) merge
	drop if max_nobs - nobs > 5	
	
	* save
	save "$pathtemp/tempcoskew`m'", replace

} // forvalues m

// append Jan-Dec
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

timer off 1
timer list 1


label var CoskewACX "Coskewness following Ang, Chen, Xing 2006"

// SAVE
do "$pathCode/savepredictor" CoskewACX

