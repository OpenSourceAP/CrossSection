* 15. Daily Fama-French factors ------------------------------------------------

// Prepare query
#delimit ;
local sql_statement
    SELECT date, mktrf, smb, hml, rf, umd
    FROM ff.factors_daily;
#delimit cr

odbc load, exec("`sql_statement'") dsn($wrdsConnection) clear

rename date time_d 

// Save file
compress
save "$pathDataIntermediate/dailyFF.dta", replace