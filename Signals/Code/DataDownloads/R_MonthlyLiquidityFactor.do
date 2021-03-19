* 18. Monthly liquidity factor -----------------------------------------------------

// Prepare query
#delimit ;
local sql_statement
    SELECT date, ps_innov
    FROM ff.liq_ps;
#delimit cr

odbc load, exec("`sql_statement'") dsn($wrdsConnection) clear

gen time_avail_m = mofd(date)
format time_avail_m %tm
drop date 

compress
save "$pathDataIntermediate/monthlyLiquidity", replace