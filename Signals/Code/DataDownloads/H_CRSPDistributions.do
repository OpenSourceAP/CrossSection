* 8. CRSP Distributions --------------------------------------------------------

// Prepare query
#delimit ;
local sql_statement
    SELECT d.permno, d.divamt, d.distcd, d.facshr, d.rcrddt
    FROM crsp.msedist as d;
#delimit cr

odbc load, exec("`sql_statement'") dsn(wrds-stata) clear

*create monthly date
gen time_avail_m = mofd(rcrddt)
format time_avail_m %tm

gcollapse (sum) divamt, by(permno time_avail_m)
save "$pathDataIntermediate/mCRSPdistributions", replace