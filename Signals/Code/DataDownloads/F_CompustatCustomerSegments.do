* 6. Compustat Customer segments --------------------------------------------------

// Prepare query
#delimit ;
local sql_statement
    SELECT a.*
    FROM compseg.wrds_seg_customer as a;
#delimit cr

odbc load, exec("`sql_statement'") dsn($wrdsConnection) clear

rename srcdate datadate

compress
export delimited "$pathDataIntermediate/CompustatSegmentDataCustomers.csv", replace  // to create customer momentum in R