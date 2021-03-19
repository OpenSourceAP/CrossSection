* 14. IBES Unadjusted Actuals --------------------------------------------------

// Prepare query
// #delimit ;
// local sql_statement
//     SELECT a.ticker, a.statpers, a.int0a, a.shout, a.fy0a, a.fy0edats, 
// 	a.price, a.curr_price
//     FROM ibes.actpsumu_epsus as a
// 	WHERE a.measure = 'EPS';
// #delimit cr

// newer: download everything (it's not that much )
#delimit ;
local sql_statement
    SELECT a.*
    FROM ibes.actpsumu_epsus as a
	WHERE a.measure = 'EPS';
#delimit cr

odbc load, exec("`sql_statement'") dsn($wrdsConnection) clear

rename shout shoutIBESUnadj

* Set up in monthly time and fill gaps
gen time_avail_m = mofd(statpers)
format time_avail %tm

egen id = group(ticker)
bys id time_av: keep if _n == 1

xtset id time_av
tsfill 

foreach v of varlist int0a fy0a shoutIBESUnadj ticker {
	replace `v' = `v'[_n-1] if id == id[_n-1] & mi(`v') 
}

drop id statpers

* Prepare for match with other files
rename ticker tickerIBES

compress
save "$pathDataIntermediate/IBES_UnadjustedActuals", replace
