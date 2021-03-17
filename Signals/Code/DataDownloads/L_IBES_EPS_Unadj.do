* 12. IBES EPS ------------------------------------------------------------------
* doc: https://wrds-www.wharton.upenn.edu/pages/support/manuals-and-overviews/i-b-e-s/ibes-estimates/general/wrds-overview-ibes/
// For example, if December 2007 is the last reported annual 
// (assume the calendar year = the fiscal year), 
// the FPI=1, FPI=2 and FPI=3 estimates are for the periods ending December 2008, 2009 and 2010, respectively. 
// Please note FPI=0 is for long term growth.

// https://wrds-web.wharton.upenn.edu/wrds//ds/ibes/statsumu/index.cfm
// FPI=6 is current quarter

// statsum_epsus is adjusted for splits, statsumu_epsus is not.  
// We typically scale forecasts by crsp prc, which is also not split adjusted

// Prepare query
#delimit ;
local sql_statement
    SELECT a.ticker, a.statpers, a.measure, a.fpi, a.numest, a.medest,
	    a.meanest, a.stdev, a.fpedats
	FROM ibes.statsumu_epsus as a
	WHERE a.fpi = '0' or a.fpi = '1' or a.fpi = '2' or a.fpi = '6'
	;
#delimit cr

odbc load, exec("`sql_statement'") dsn($wrdsConnection) clear

* Set up linking variables
gen time_avail_m = mofd(statpers)
format time_avail_m %tm
rename ticker tickerIBES

drop measure

* Keep last obs each month
drop if meanest == . // just for sanity
sort tickerIBES fpi time_avail_m statpers
by tickerIBES fpi time_avail_m: keep if _n == _N


compress
save "$pathDataIntermediate/IBES_EPS_Unadj", replace
