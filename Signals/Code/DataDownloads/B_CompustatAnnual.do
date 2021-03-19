* 2. Compustat annual ----------------------------------------------------------

// Prepare query
#delimit ;
local sql_statement
    SELECT a.gvkey, a.datadate, a.conm, a.fyear, a.tic, a.cusip, a.naicsh, a.sich, 
	       a.aco,a.act,a.ajex,a.am,a.ao,a.ap,a.at,a.capx,a.ceq,a.che,a.cogs,
		   a.csho,a.cshrc,a.dcpstk,a.dcvt,a.dlc,a.dlcch,a.dltis,a.dltr,
		   a.dltt,a.dm,a.dp,a.drc,a.drlt,a.dv,a.dvc,a.dvp,a.dvpa,a.dvpd,
		   a.dvpsx_c,a.dvt,a.ebit,a.ebitda,a.emp,a.epspi,a.epspx,a.fatb,a.fatl,
		   a.ffo,a.fincf,a.fopt,a.gdwl,a.gdwlia,a.gdwlip,a.gwo,a.ib,a.ibcom,
		   a.intan,a.invt,a.ivao,a.ivncf,a.ivst,a.lco,a.lct,a.lo,a.lt,a.mib,
		   a.msa,a.ni,a.nopi,a.oancf,a.ob,a.oiadp,a.oibdp,a.pi,a.ppenb,a.ppegt,
		   a.ppenls,
		   a.ppent,a.prcc_c,a.prcc_f,a.prstkc,a.prstkcc,a.pstk,a.pstkl,a.pstkrv,
		   a.re,a.rect,a.recta,a.revt,a.sale,a.scstkc,a.seq,a.spi,a.sstk,
		   a.tstkp,a.txdb,a.txdi,a.txditc,a.txfo,a.txfed,a.txp,a.txt,
		   a.wcap,a.wcapch,a.xacc,a.xad,a.xint,a.xrd,a.xpp,a.xsga
    FROM COMP.FUNDA as a
	WHERE a.consol = 'C'
	AND a.popsrc = 'D'
	AND a.datafmt = 'STD'
	AND a.curcd = 'USD'
	AND a.indfmt = 'INDL'
	;
#delimit cr

odbc load, exec("`sql_statement'") dsn($wrdsConnection) clear

export delimited "$pathDataIntermediate/CompustatAnnual.csv", replace  // For processing of IO-Momentum in R

* Require some reasonable amount of information
drop if at ==. | prcc_c ==. | ni ==.

* 6 digit CUSIP
gen cnum = substr(cusip,1,6)

* ----------------------------------------------------------------------------
* Replace missing values if reasonable
* ----------------------------------------------------------------------

gen dr = . // Deferred revenue
replace dr = drc + drlt if drc !=. & drlt !=.    // drc  = deferred revenue current 
replace dr = drc 		if drc !=. & drlt ==.  // drlt = deferred revenue long-term
replace dr = drlt 		if drc ==. & drlt !=.

// dcpstk = convertible debt and preferred stock, pstk = preferred stock, dcvt = convertible debt
gen dc 		= dcpstk - pstk if dcpstk > pstk & pstk !=. & dcpstk !=. & dcvt ==. // convertible debt
replace dc	= dcpstk 		if pstk ==. & dcpstk !=. & dcvt ==.
replace dc 	= dcvt 			if dc ==.

// xint = interest and related expense - Total
gen xint0 		= 0
replace xint0 	= xint if xint !=.
// xsga = Selling, general and administrative expenses
gen xsga0		= 0
replace xsga0 	= xsga if xsga !=.

gen xad0 = xad
replace xad0 = 0 if mi(xad) 

// For these variables, missing is assumed to be 0
foreach v of varlist nopi dvt ob dm dc aco ap intan ao lco lo rect ///
				invt drc spi gdwl che dp act lct tstk dvpa scstkc sstk mib ///
				ivao prstkc prstkcc txditc ivst {
				
	replace `v' = 0 if `v' ==.
	
}

// Add identifiers for merging
joinby gvkey using "$pathDataIntermediate/CCMLinkingTable", update unmatched(none)

* Use only if data date is within the validity period of the link
gen temp = (timeLinkStart_d <= datadate  & datadate <= timeLinkEnd_d)
tab temp
keep if temp == 1
drop temp

// Create two versions: Annual and monthly (monthly makes matching to monthly CRSP easier)

* Annual version
drop timeLinkStart_d timeLinkEnd_d linkprim liid linktype
destring gvkey, replace
compress

gen time_avail_m = mofd(datadate) + 6  // Assuming 6 month reporting lag
format time_avail_m %tm

save "$pathDataIntermediate/a_aCompustat", replace

* Monthly version
gen temp = 12
expand temp
drop temp

gen tempTime = time_avail_m
bysort gvkey tempTime: replace time_avail_m = time_avail_m + _n - 1 

drop tempTime
bysort gvkey time_avail_m (datadate): keep if _n == _N  // This affects .14% of observations that had changes of fiscal year ends. In that case, we keep the more recent info
bysort permno time_avail_m (datadate): keep if _n == _N  // This affects an additional 89/3m observations

save "$pathDataIntermediate/m_aCompustat", replace

