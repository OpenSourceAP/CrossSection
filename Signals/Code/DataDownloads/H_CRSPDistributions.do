* 8. CRSP Distributions --------------------------------------------------------
* http://www.crsp.org/products/documentation/distribution-codes

// Prepare query
#delimit ;
local sql_statement
    SELECT d.permno, d.divamt, d.distcd, d.facshr, d.rcrddt, d.exdt, d.paydt
    FROM crsp.msedist as d;
#delimit cr

odbc load, exec("`sql_statement'") dsn($wrdsConnection) clear

* remove duplicates
* seems like these are data errors, e.g. see permno 93338 or 93223
bysort permno distcd paydt: keep if _n == 1

* for convenience, extract components of distribution code
tostring distcd, replace
gen cd1 = real(substr(distcd,1,1))
gen cd2 = real(substr(distcd,2,1))
gen cd3 = real(substr(distcd,3,1))
gen cd4 = real(substr(distcd,4,1))

save "$pathDataIntermediate/CRSPdistributions", replace
