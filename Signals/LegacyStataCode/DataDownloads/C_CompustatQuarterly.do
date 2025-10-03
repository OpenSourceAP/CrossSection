* 3. Compustat Quarterly -------------------------------------------------------

// Prepare query
#delimit ;
local sql_statement
    SELECT a.gvkey, a.datadate, a.fyearq, a.fqtr, a.datacqtr, a.datafqtr, a.acoq,
	a.actq,a.ajexq,a.apq,a.atq,a.ceqq,a.cheq,a.cogsq,a.cshoq,a.cshprq,
	a.dlcq,a.dlttq,a.dpq,a.drcq,a.drltq,a.dvpsxq,a.dvpq,a.dvy,a.epspiq,a.epspxq,a.fopty,
	a.gdwlq,a.ibq,a.invtq,a.intanq,a.ivaoq,a.lcoq,a.lctq,a.loq,a.ltq,a.mibq,
	a.niq,a.oancfy,a.oiadpq,a.oibdpq,a.piq,a.ppentq,a.ppegtq,a.prstkcy,a.prccq,
	a.pstkq,a.rdq,a.req,a.rectq,a.revtq,a.saleq,a.seqq,a.sstky,a.txdiq,
	a.txditcq,a.txpq,a.txtq,a.xaccq,a.xintq,a.xsgaq,a.xrdq, a.capxy
    FROM COMP.FUNDQ as a
	WHERE a.consol = 'C'
	AND a.popsrc = 'D'
	AND a.datafmt = 'STD'
	AND a.curcdq = 'USD'
	AND a.indfmt = 'INDL';
#delimit cr

odbc load, exec("`sql_statement'") dsn($wrdsConnection) clear

bys gvkey fyearq fqtr (datadate): keep if _n == _N // Keep only the most recent data for each fiscal quarter

// Data availability assumed as discussed in https://github.com/OpenSourceAP/CrossSection/issues/50
gen time_avail_m = mofd(datadate) + 3  // Assume data available with a 3 month lag
replace time_avail_m = mofd(rdq) if !mi(rdq) & mofd(rdq) > time_avail_m  // Patch cases with earlier data availability
drop if mofd(rdq) - mofd(datadate) > 6 & !mi(rdq) // Drop cases with very late release

format time_avail_m %tm
bys gvkey time_avail_m (datadate): keep if _n == _N  // A few obervation have two rows in the same quarter (probably change in fiscal year end), keep more recent info

// For these variables, missing is assumed to be 0
foreach v of varlist acoq actq apq cheq dpq drcq invtq intanq ivaoq ///
                       gdwlq lcoq lctq loq mibq prstkcy rectq sstky txditcq {
				
	replace `v' = 0 if `v' ==.
	
}

// Prepare year-to-date items
sort gvkey fyearq fqtr
foreach v of varlist sstky prstkcy oancfy fopty {
    gen `v'q = `v' if fqtr == 1
	by gvkey fyearq: replace `v'q = `v' - `v'[_n-1] if fqtr !=1
}

* To monthly
* drop fyearq fqtr datacqtr datafqtr // 2021 02 ac: these guys might be useful...
expand 3
gen tempTimeAvailM = time_avail_m
bysort gvkey tempTimeAvailM: replace time_avail_m = time_avail_m + _n - 1  if _n > 1

// SAVE
bysort gvkey time_avail_m (datadate): keep if _n == _N  // A few obervation have two rows in the same month after expanding, keep the most recent info (fiscal year changes)
drop temp* 
rename datadate datadateq

destring gvkey, replace
compress
save "$pathDataIntermediate/m_QCompustat", replace
