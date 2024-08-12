* CredRatDG
* --------------

// Define signal for Compustat SP ratings data
use gvkey time_avail_m credrat using "$pathDataIntermediate/m_SP_creditratings", clear

xtset gvkey time_avail_m

gen credrat_dwn = 1 if credrat - l.credrat < 0
bys gvkey: replace credrat_dwn = . if _n == 1

save "$pathtemp/temp_comp_rat", replace

// Define signal for CIQ SP ratings data
use "$pathDataIntermediate/m_CIQ_creditratings.dta", clear
gen time_avail_m = mofd(ratingdate)
format time_avail_m %tm

* let's try it the easy way for now, using CIQ's ratingaction
keep if !missing(gvkey) & ratingaction == "Downgrade"
gen ciq_dg = 1 
order gvkey time_avail_m ciq_dg
collapse (max) ciq_dg, by(gvkey time_avail_m) // handle dups within month

save "$pathtemp/temp_ciq_rat", replace

// merge on to permnos
use gvkey permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
drop if gvkey ==.

merge 1:1 gvkey time_avail_m using "$pathtemp/temp_comp_rat", keep(master match) nogenerate keepusing(credrat_dwn)
merge 1:1 gvkey time_avail_m using "$pathtemp/temp_ciq_rat", keep(master match) nogenerate keepusing(ciq_dg)

* use ciq of compustat data is missing
replace credrat_dwn = ciq_dg if credrat_dwn == .

// SIGNAL CONSTRUCTION
xtset permno time_avail_m

gen CredRatDG = 0
replace CredRatDG = 1 if (credrat_dwn == 1 | l.credrat_dwn == 1 | l2.credrat_dwn == 1 | l3.credrat_dwn == 1 | l4.credrat_dwn == 1 | l5.credrat_dwn == 1  ) 

gen year = yofd(dofm(time_avail_m))
replace CredRatDG = . if year < 1979 // No data before that

label var CredRatDG "Credit Rating Downgrade"

// SAVE
do "$pathCode/savepredictor" CredRatDG
