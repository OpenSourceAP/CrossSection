* 24. Credit ratings ------------------------------------------------------------

// Prepare query
#delimit ;
local sql_statement
    SELECT gvkey, datadate, splticrm
    FROM comp.adsprate;
#delimit cr

odbc load, exec("`sql_statement'") dsn($wrdsConnection) clear

gen time_avail_m = mofd(datadate)
format time_avail_m %tm
drop datadate

* Create numerical rating
gen credrat 	= 0
replace credrat = 1 if sp == "D"
replace credrat = 2 if sp == "C"
replace credrat = 3 if sp == "CC"
replace credrat = 4 if sp == "CCC-"
replace credrat = 5 if sp == "CCC"
replace credrat = 6 if sp == "CCC+"
replace credrat = 7 if sp == "B-"
replace credrat = 8 if sp == "B"
replace credrat = 9 if sp == "B+"
replace credrat = 10 if sp == "BB-"
replace credrat = 11 if sp == "BB"
replace credrat = 12 if sp == "BB+"
replace credrat = 13 if sp == "BBB-"
replace credrat = 14 if sp == "BBB"
replace credrat = 15 if sp == "BBB+"
replace credrat = 16 if sp == "A-"
replace credrat = 17 if sp == "A"
replace credrat = 18 if sp == "A+"
replace credrat = 19 if sp == "AA-"
replace credrat = 20 if sp == "AA"
replace credrat = 21 if sp == "AA+"
replace credrat = 22 if sp == "AAA"
drop sp


// Save file
destring gvkey, replace
compress
save "$pathDataIntermediate/m_SP_creditratings.dta", replace
