* 16. Monthly Fama-French factors ----------------------------------------------

// Prepare query
#delimit ;
local sql_statement
    SELECT date, mktrf, smb, hml, rf, umd
    FROM ff.factors_monthly;
#delimit cr

odbc load, exec("`sql_statement'") dsn($wrdsConnection) clear

gen time_avail_m = mofd(date)
format time_avail_m %tm
drop date

compress
save "$pathDataIntermediate/monthlyFF", replace