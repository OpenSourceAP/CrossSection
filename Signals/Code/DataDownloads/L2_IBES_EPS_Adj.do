* ------------------------------------------------------------------
* doc: https://wrds-www.wharton.upenn.edu/pages/support/manuals-and-overviews/i-b-e-s/ibes-estimates/general/wrds-overview-ibes/
* I could only find anndats_act on statsum_epsus, so I use this for Earnings Streak

// Prepare query
#delimit ;
local sql_statement
    SELECT a.fpi, a.ticker, a.statpers, a.fpedats, a.anndats_act
		, a.meanest, a.actual, a.medest, a.stdev, a.numest
		, b.prdays, b.price, b.shout
	FROM ibes.statsum_epsus as a left join ibes.actpsum_epsus as b
	on a.ticker = b.ticker and a.statpers = b.statpers
	;
#delimit cr

odbc load, exec("`sql_statement'") dsn($wrdsConnection) clear

* Set up linking variables
gen time_avail_m = mofd(statpers)
format time_avail_m %tm
rename ticker tickerIBES

* Keep last obs each month
drop if meanest == . // just for sanity
sort tickerIBES fpi time_avail_m statpers
by tickerIBES fpi time_avail_m: keep if _n == _N

compress
save "$pathDataIntermediate/IBES_EPS_Adj", replace
