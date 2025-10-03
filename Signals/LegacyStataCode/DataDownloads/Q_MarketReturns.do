* 17. Monthly equal- and value-weighted market returns ---------------------------

// Prepare query
#delimit ;
local sql_statement
    SELECT date, vwretd, ewretd, usdval
    FROM crsp.msi;
#delimit cr

odbc load, exec("`sql_statement'") dsn($wrdsConnection) clear

gen time_avail_m = mofd(date)
format time_avail_m %tm
drop date

compress
save "$pathDataIntermediate/monthlyMarket", replace

