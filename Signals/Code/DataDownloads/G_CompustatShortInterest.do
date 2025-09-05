* 7. Compustat short interest -----------------------------------------------------

* In 2025, S&P replaced the short interest data (starting in 1973) with a different
* data source that only starts in 2006. We combine both files and keep the legacy
* data when both are available for consistency with previous publications

* Legacy file (1973-2024)

// Prepare query
#delimit ;
local sql_statement
    SELECT a.gvkey, a.iid, a.shortint, a.shortintadj, a.datadate
    FROM comp.sec_shortint_legacy as a;
#delimit cr

odbc load, exec("`sql_statement'") dsn($wrdsConnection) clear

gen time_avail_m = mofd(datadate)
format time_avail_m %tm

sort gvkey iid time_avail_m datadate
gcollapse (firstnm) shortint shortintadj datadate, by(gvkey iid time_avail_m)  // Data reported bi-weekly and made available with a four day lag (according to
			        	                                         // Rapach et al. (2016). As they do, we use the mid-month observation to make sure 
                                                                 // Data would be available in real time

* Add permno
rename iid liid
joinby gvkey liid using "$pathDataIntermediate/CCMLinkingTable", update unmatched(none)

* Use only if data date is within the validity period of the link
gen temp = (timeLinkStart_d <= datadate  & datadate <= timeLinkEnd_d)
tab temp
keep if temp == 1
drop temp conm tic cusip cik sic naics linkprim linktype lpermco timeLinkStart_d timeLinkEnd_d
rename liid iid

bys permno time_avail_m: gen tmp = _N
tab tmp  // There are 12 edge cases where the permno-(gvkey-iid) link shifts within months and I keep the mid-month observation
sort permno time_avail_m datadate
bys permno time_avail_m: drop if tmp == 2 & _n == _N
drop tmp datadate

gen legacyFile = 1
save tmp, replace
																 

* New file (2006-)

// Prepare query
#delimit ;
local sql_statement
    SELECT a.gvkey, a.iid, a.shortint, a.shortintadj, a.datadate
    FROM comp.sec_shortint as a;
#delimit cr

odbc load, exec("`sql_statement'") dsn($wrdsConnection) clear

gen time_avail_m = mofd(datadate)
format time_avail_m %tm

* Use only if data date is within the validity period of the link
sort gvkey iid time_avail_m datadate
gcollapse (firstnm) shortint shortintadj datadate, by(gvkey iid time_avail_m)  // Data reported bi-weekly and made available with a four day lag (according to
			        	                                         // Rapach et al. (2016). As they do, we use the mid-month observation to make sure 
                                                                 // Data would be available in real time

* Add permno
rename iid liid
joinby gvkey liid using "$pathDataIntermediate/CCMLinkingTable", update unmatched(none)

gen temp = (timeLinkStart_d <= datadate  & datadate <= timeLinkEnd_d)
tab temp
keep if temp == 1
drop temp conm tic cusip cik sic naics linkprim linktype lpermco timeLinkStart_d timeLinkEnd_d
rename liid iid

bys permno time_avail_m: gen tmp = _N
tab tmp  // There are 310 edge cases (0.02%) where the permno-(gvkey-iid) link shifts within months and I keep the mid-month observation
sort permno time_avail_m datadate
bys permno time_avail_m: drop if tmp == 2 & _n == _N
drop tmp datadate

* Combine
append using tmp
* Keep legacy data if two observations for same firm in same month
bys gvkey permno iid time_avail_m: gen nobs = _N
drop if nobs >1 & legacy !=1
drop nobs legacyFile

* There are 16 observations where the same permno shows up with different short interest in the same month
* I drop those observations
bys permno time_avail_m: gen tmp = _N
tab tmp
drop if tmp == 2
drop tmp

* check whether no repeated observations 
bys gvkey permno iid time_avail_m: assert _N == 1
bys permno time_avail_m: assert _N == 1

* Wrap up
replace shortint = shortint/10^6  // for consistency as we also use shares outstanding in millions of shares (see I_CRSPmonthly.do)
replace shortintadj = shortintadj/10^6																 
																 
destring gvkey, replace
compress

save "$pathDataIntermediate/monthlyShortInterest", replace

* Housekeeping
erase tmp.dta