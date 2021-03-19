* CredRatDG
* --------------

// DATA LOAD
use gvkey time_avail_m credrat using "$pathDataIntermediate/m_SP_creditratings", clear

xtset gvkey time_avail_m

gen credrat_dwn = 1 if credrat - l.credrat < 0
bys gvkey: replace credrat_dwn = . if _n == 1

save "$pathtemp/temp", replace

use gvkey permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
drop if gvkey ==.

merge 1:1 gvkey time_avail_m using "$pathtemp/temp", keep(master match) nogenerate keepusing(credrat_dwn)

// SIGNAL CONSTRUCTION
xtset permno time_avail_m

gen CredRatDG = 0
replace CredRatDG = 1 if (credrat_dwn == 1 | l.credrat_dwn == 1 | l2.credrat_dwn == 1 | l3.credrat_dwn == 1 | l4.credrat_dwn == 1 | l5.credrat_dwn == 1  ) 

gen year = yofd(dofm(time_avail_m))
replace CredRatDG = . if year < 1979 | year > 2016  // No data before or after that

label var CredRatDG "Credit Rating Downgrade"

// SAVE
do "$pathCode/savepredictor" CredRatDG