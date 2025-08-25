* 7. Compustat short interest -----------------------------------------------------

// Prepare query
#delimit ;
local sql_statement
    SELECT a.gvkey, a.iid, a.shortint, a.shortintadj, a.datadate
    FROM comp.sec_shortint as a;
#delimit cr

odbc load, exec("`sql_statement'") dsn($wrdsConnection) clear

gen time_avail_m = mofd(datadate)
format time_avail_m %tm

gcollapse (firstnm) shortint shortintadj, by(gvkey time_avail_m)  // Data reported bi-weekly and made available with a four day lag (according to
			        	                                         // Rapach et al. (2016). As they do, we use the mid-month observation to make sure 
                                                                 // Data would be available in real time

replace shortint = shortint/10^6  // for consistency as we also use shares outstanding in millions of shares (see I_CRSPmonthly.do)
replace shortintadj = shortintadj/10^6																 
																 
destring gvkey, replace
compress
save "$pathDataIntermediate/monthlyShortInterest", replace
