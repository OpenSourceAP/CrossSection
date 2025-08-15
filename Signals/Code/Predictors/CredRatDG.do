* CredRatDG
* --------------

// Define signal for Compustat SP ratings data
use gvkey time_avail_m credrat using "$pathDataIntermediate/m_SP_creditratings", clear

xtset gvkey time_avail_m

gen credrat_dwn = 1 if credrat - l.credrat < 0
bys gvkey: replace credrat_dwn = . if _n == 1

* CHECKPOINT 1: Check credrat_dwn creation for problem observations
list gvkey time_avail_m credrat l.credrat credrat_dwn if gvkey == 1013 & inrange(year(dofm(time_avail_m)), 1983, 1984)
list gvkey time_avail_m credrat l.credrat credrat_dwn if gvkey == 1175 & time_avail_m == tm(2024m12)

save "$pathtemp/temp_comp_rat", replace

// Define signal for CIQ SP ratings data
use "$pathDataIntermediate/m_CIQ_creditratings.dta", clear

* let's try it the easy way for now, using CIQ's ratingaction
keep if !missing(gvkey) & ratingaction == "Downgrade"
gen ciq_dg = 1 
order gvkey time_avail_m ciq_dg
collapse (max) ciq_dg, by(gvkey time_avail_m) // handle dups within month by looking for any downgrades

save "$pathtemp/temp_ciq_rat", replace

// merge on to permnos
use gvkey permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
drop if gvkey ==.

merge 1:1 gvkey time_avail_m using "$pathtemp/temp_comp_rat", keep(master match) nogenerate keepusing(credrat_dwn)
merge 1:1 gvkey time_avail_m using "$pathtemp/temp_ciq_rat", keep(master match) nogenerate keepusing(ciq_dg)

* use ciq of compustat data is missing
replace credrat_dwn = ciq_dg if credrat_dwn == .

* CHECKPOINT 2: Check credrat_dwn after CIQ merge for problem observations  
list permno gvkey time_avail_m credrat_dwn ciq_dg if permno == 10006 & inrange(year(dofm(time_avail_m)), 1983, 1984)
list permno gvkey time_avail_m credrat_dwn ciq_dg if permno == 11990 & time_avail_m == tm(2024m12)

// SIGNAL CONSTRUCTION
xtset permno time_avail_m

gen CredRatDG = 0
replace CredRatDG = 1 if (credrat_dwn == 1 | l.credrat_dwn == 1 | l2.credrat_dwn == 1 | l3.credrat_dwn == 1 | l4.credrat_dwn == 1 | l5.credrat_dwn == 1  )

* CHECKPOINT 3: Check CredRatDG signal creation with lags for problem observations
list permno time_avail_m credrat_dwn l.credrat_dwn l2.credrat_dwn l3.credrat_dwn l4.credrat_dwn l5.credrat_dwn CredRatDG if permno == 10006 & inrange(year(dofm(time_avail_m)), 1983, 1984)
list permno time_avail_m credrat_dwn l.credrat_dwn l2.credrat_dwn l3.credrat_dwn l4.credrat_dwn l5.credrat_dwn CredRatDG if permno == 11990 & time_avail_m == tm(2024m12) 

gen year = yofd(dofm(time_avail_m))
replace CredRatDG = . if year < 1979 // No data before that

* CHECKPOINT 4: Check final CredRatDG signal after year filter for problem observations
list permno time_avail_m year CredRatDG if permno == 10006 & inrange(year(dofm(time_avail_m)), 1983, 1984)
list permno time_avail_m year CredRatDG if permno == 11990 & time_avail_m == tm(2024m12)

label var CredRatDG "Credit Rating Downgrade"

// SAVE
do "$pathCode/savepredictor" CredRatDG
