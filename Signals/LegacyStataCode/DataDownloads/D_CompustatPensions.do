* 4. Compustat Pensions --------------------------------------------------------

// Prepare query
#delimit ;
local sql_statement
    SELECT a.gvkey, a.datadate, a.paddml, a.pbnaa, a.pbnvv, a.pbpro, 
	       a.pbpru, a.pcupsu, a.pplao, a.pplau
    FROM COMP.ACO_PNFNDA as a
	WHERE a.consol = 'C'
	AND a.popsrc = 'D'
	AND a.datafmt = 'STD'
	AND a.indfmt = 'INDL';
#delimit cr

odbc load, exec("`sql_statement'") dsn($wrdsConnection) clear

gen year = year(datadate)
replace year = year + 1  // Assume data available with a lag of one year
bysort gvkey year (datadate): keep if _n == 1

drop datadate
mdesc  // Missing data for about 80% of firm-years in all but two variables

destring gvkey, replace
compress
save "$pathDataIntermediate/CompustatPensions", replace

