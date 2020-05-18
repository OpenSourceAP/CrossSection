** Pre-processing quarterly Compustat data items

import delimited "$pathProject/DataRaw/CompustatQuarterly.csv", clear
gen time_q = quarterly(datacqtr, "YQ")
drop if mi(time_q)
format time_q %tq
bys gvkey time_q: keep if _n == 1  // One obervation has two rows in same quarter (probably change in fiscal year end)

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



* TIMING: Assume data available with one quarter lag
replace time_q = time_q + 1
gen time_avail_m = mofd(dofq(time_q))
format time_avail_m %tm

* To monthly
drop datadate fyearq fqtr datacqtr datafqtr rdq
expand 3
bysort gvkey time_q: replace time_avail_m = time_avail_m + _n - 1  if _n > 1

// SAVE
drop time_q
compress
save "$pathProject/DataClean/m_QCompustat", replace
