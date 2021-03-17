* 9. CRSP monthly --------------------------------------------------------------

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
export delimited "$pathDataIntermediate/mCRSP.csv", replace  // For processing of IO-Momentum in R


* Make 2 digit SIC
rename siccd sicCRSP
tostring sicCRSP, replace
gen sic2D = substr(sicCRSP,1,2)
destring sic*, replace

*create monthly date
gen time_avail_m = mofd(date)
format time_avail_m %tm
drop date

* Incorporate delisting return
replace dlret = -.35 if dlret==. & (dlstcd == 500 | (dlstcd >=520 & dlstcd <=584)) ///
	& (exchcd == 1 | exchcd == 2)

replace dlret = -.55 if dlret==. & (dlstcd == 500 | (dlstcd >=520 & dlstcd <=584)) ///
	& exchcd == 3  // GHZ cite Johnson and Zhao (2007), Shumway and Warther (1999)

replace dlret = -1 if dlret < -1 & dlret !=.

replace dlret = 0 if dlret ==.

replace ret = ret + dlret

replace ret = dlret if ret ==. & dlret !=0

* Compute market value of equity (used all the time)

* Converting units
replace shrout = shrout/1000
replace vol =  vol/10^4

gen mve_c = (shrout * abs(prc)) // Common shares outstanding * Price

** Housekeeping
drop dlret dlstcd permco
compress
save "$pathDataIntermediate/monthlyCRSP", replace
