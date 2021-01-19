* 12. IBES EPS ------------------------------------------------------------------

// Prepare query
#delimit ;
local sql_statement
    SELECT a.ticker, a.statpers, a.measure, a.fpi, a.numest, a.medest,
	       a.meanest, a.stdev, a.fpedats, a.actual, a.anndats_act
	FROM ibes.statsum_epsus as a
	WHERE a.fpi = '0' or a.fpi = '1' or a.fpi = '6';
#delimit cr

odbc load, exec("`sql_statement'") dsn(wrds-stata) clear

* Fiscal year earnings estimate
preserve

	keep if fpi == "1"  // Use fiscal year earnings estimates only

	keep if statpers < anndats_act

	rename actual EPSactualIBES
	drop anndats_act measure fpi fpedats
	duplicates drop

	* Set up in monthly time and fill gaps
	gen time_avail_m = mofd(statpers)
	format time_avail %tm

	egen id = group(ticker)
	bys id time_avail_m: keep if _n == 1

	xtset id time_av
	tsfill  // THIS INTRODUCES SOME STALENESS IF NO ESTIMATES ARE AVAILABLE. IS THIS WHAT WE WANT?

	foreach v of varlist ticker numest medest meanest stdev EPSactualIBES {
		replace `v' = `v'[_n-1] if id == id[_n-1] & mi(`v') 
	}

	drop id 

	* Prepare for match with other files
	rename ticker tickerIBES
	rename stdev stdev_est
	compress
	save "$pathDataIntermediate/IBES_EPS", replace

restore


* Long-run growth expectations
keep if fpi == "0"

keep ticker meanest stdev numest statpers
duplicates drop

* Set up in monthly time and fill gaps
gen time_avail_m = mofd(statpers)
format time_avail %tm

egen id = group(ticker)

xtset id time_avail_m
tsfill
 
foreach v of varlist ticker meanest stdev numest {
	replace `v' = `v'[_n-1] if id == id[_n-1] & mi(`v') 
}

drop id

* Prepare for match with other files
rename ticker tickerIBES
rename meanest fgr5yr
rename stdev stdev5yr
rename numest numest5yr

compress
save "$pathDataIntermediate/IBES_EPSLongRun", replace
