* 5. Compustat Segments --------------------------------------------------------

// Prepare query
#delimit ;
local sql_statement
    SELECT a.gvkey, a.datadate, a.stype, a.sid, a.sales, a.srcdate, a.naicsh, a.sics1, a.snms
    FROM compseg.wrds_segmerged as a;
#delimit cr

odbc load, exec("`sql_statement'") dsn($wrdsConnection) clear

destring gvkey sics1 naicsh, replace

compress
save "$pathDataIntermediate/CompustatSegments", replace
