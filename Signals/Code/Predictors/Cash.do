* Cash
* --------------

// DATA LOAD
* 2020 01 Andrew
* use rdq instead of time_avail_m following OP
* Note: time_avail_m is datadate + 3 months but rdq is unchanged from 
* WRDS download
use gvkey rdq cheq atq using "$pathDataIntermediate/m_QCompustat", clear

* drop duplicates: there are a lot since m_QCompustat is a monthly version 
sort gvkey rdq
quietly by gvkey rdq:  gen dup = cond(_N==1,0,_n)
keep if !mi(gvkey) & dup == 1 & !mi(atq)
drop dup

* define time avail
gen time_avail_m = mofd(rdq)
format time_avail_m %tm

* expand back to monthly (seems redudant, but safely deals with non-quarterly rdq)
* (based on m_QCompustat code)
sort gvkey time_avail_m
expand 3
gen tempTimeAvailM = time_avail_m
bysort gvkey tempTimeAvailM: replace time_avail_m = time_avail_m + _n - 1  if _n > 1

* remove dups: happens if announcements occur within 3 months
* keep newest rdq (most updated announcement)
gsort gvkey time_avail_m -rdq
quietly by gvkey time_avail_m:  gen dup = cond(_N==1,0,_n)
keep if dup == 0

save "$pathtemp/tempCash", replace

* merge
use permno gvkey time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)

merge 1:1 gvkey time_avail_m using "$pathtemp/tempCash", keepusing(atq cheq rdq) nogenerate keep(match)

// // SIGNAL CONSTRUCTION
gen Cash = cheq/atq 

// SIGNAL CONSTRUCTION NEW
label var Cash "Cash to assets"

// SAVE
do "$pathCode/savepredictor" Cash
