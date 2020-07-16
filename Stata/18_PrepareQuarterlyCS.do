** Pre-processing quarterly Compustat data items

import delimited "$pathProject/DataRaw/CompustatQuarterly.csv", clear
gen tempTime = date(datadate, "YMD")
drop if mi(tempTime)
gen time_avail_m = mofd(tempTime) + 3  // Assume data available with a 3 month lag
format time_avail_m %tm
bys gvkey time_avail_m: keep if _n == 1  // A few obervation have two rows in the same quarter (probably change in fiscal year end)

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
drop datadate fyearq fqtr datacqtr datafqtr rdq
expand 3
gen tempTimeAvailM = time_avail_m
bysort gvkey tempTimeAvailM: replace time_avail_m = time_avail_m + _n - 1  if _n > 1

// SAVE
drop temp*
bysort gvkey time_avail_m: keep if _n == 1  // A few obervation have two rows in the same month (probably change in fiscal year end)

compress
save "$pathProject/DataClean/m_QCompustat", replace

