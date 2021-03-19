* 9. CRSP monthly --------------------------------------------------------------
* raw version omits delisting return adjustments for testing
// Prepare query
#delimit ;
local sql_statement
    SELECT a.permno, a.permco, a.date, a.ret, a.retx, a.vol, a.shrout, a.prc, a.cfacshr, a.bidlo, a.askhi,
                     b.shrcd, b.exchcd, b.siccd, b.ticker, b.shrcls, 
                     c.dlstcd, c.dlret                               
    FROM crsp.msf as a
	LEFT JOIN crsp.msenames as b
    ON a.permno=b.permno AND b.namedt<=a.date AND a.date<=b.nameendt
	LEFT JOIN crsp.msedelist as c
	ON a.permno=c.permno AND date_trunc('month', a.date) = date_trunc('month', c.dlstdt)
	;
#delimit cr
odbc load, exec("`sql_statement'") dsn($wrdsConnection) clear

* Make 2 digit SIC
rename siccd sicCRSP
tostring sicCRSP, replace
gen sic2D = substr(sicCRSP,1,2)
destring sic*, replace

*create monthly date
gen time_avail_m = mofd(date)
format time_avail_m %tm
drop date

* Compute market value of equity (used all the time)

* Converting units
replace shrout = shrout/1000
replace vol =  vol/10^4

gen mve_c = (shrout * abs(prc)) // Common shares outstanding * Price

** Housekeeping
drop dlret dlstcd permco
compress
save "$pathDataIntermediate/monthlyCRSPraw", replace
