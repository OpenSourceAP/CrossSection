* 10. CRSP daily ----------------------------------------------------------------

// Prepare query
#delimit ;
local sql_statement
    SELECT a.permno, a.date, a.ret, a.vol, a.shrout, a.prc, a.cfacshr
    FROM crsp.dsf as a;
#delimit cr

odbc load, exec("`sql_statement'") dsn(wrds-stata) clear

rename date time_d 

// Save file
compress
save "$pathDataIntermediate/dailyCRSP.dta", replace