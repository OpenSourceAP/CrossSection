* 11. CRSP Acquisitions ---------------------------------------------------------

// Prepare query
#delimit ;
local sql_statement
    SELECT a.permno, a.distcd, a.exdt, a.acperm
	FROM crsp.msedist as a;
#delimit cr

odbc load, exec("`sql_statement'") dsn($wrdsConnection) clear

keep if acperm >999 & acperm <.
rename exdt time_d
drop if missing(time_d)
format time_d %td
gen time_avail_m = mofd(time_d)
format time_avail_m %tm
drop time_d 

* According to 
* http://www.crsp.com/products/documentation/distribution-codes
* distcd identifies true spinoffs using keep if distcd >= 3762 & distcd <= 3764
* But MP don't use it, and it results in a large share of months with no 
* spinoffs.

* turn into list of permnos which were created in spinoffs
gen SpinoffCo = 1
drop permno
rename acperm permno
keep permno SpinoffCo

* remove spinoffs which had multi-stock parents
duplicates drop

// Save file
compress
save "$pathDataIntermediate/m_CRSPAcquisitions.dta", replace