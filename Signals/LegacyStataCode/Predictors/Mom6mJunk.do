* --------------
/*
Updated 2024 08 to 
1. include post -2016 data from CIQ
2. Be consistent across CIQ and old Comp samples
3. Be closer in a sense to Tab III of Avramov Hordia Jostova Philipov 2007

*/

// Clean CIQ ratings
use "$pathDataIntermediate/m_CIQ_creditratings.dta", clear

* remove suffixes
replace currentratingsymbol = subinstr(currentratingsymbol, "pi", "", .)
replace currentratingsymbol = subinstr(currentratingsymbol, "q", "", .)
replace currentratingsymbol = subinstr(currentratingsymbol, " prelim", "", .)

* Create numerical rating (for ease of comparison with CredRatDG)
gen credratciq 	= 0 
replace credratciq = 1 if currentratingsymbol == "D"
replace credratciq = 2 if currentratingsymbol == "C"
replace credratciq = 3 if currentratingsymbol == "CC"
replace credratciq = 4 if currentratingsymbol == "CCC-"
replace credratciq = 5 if currentratingsymbol == "CCC"
replace credratciq = 6 if currentratingsymbol == "CCC+"
replace credratciq = 7 if currentratingsymbol == "B-"
replace credratciq = 8 if currentratingsymbol == "B"
replace credratciq = 9 if currentratingsymbol == "B+"
replace credratciq = 10 if currentratingsymbol == "BB-"
replace credratciq = 11 if currentratingsymbol == "BB"
replace credratciq = 12 if currentratingsymbol == "BB+"
replace credratciq = 13 if currentratingsymbol == "BBB-"
replace credratciq = 14 if currentratingsymbol == "BBB"
replace credratciq = 15 if currentratingsymbol == "BBB+"
replace credratciq = 16 if currentratingsymbol == "A-"
replace credratciq = 17 if currentratingsymbol == "A"
replace credratciq = 18 if currentratingsymbol == "A+"
replace credratciq = 19 if currentratingsymbol == "AA-"
replace credratciq = 20 if currentratingsymbol == "AA"
replace credratciq = 21 if currentratingsymbol == "AA+"
replace credratciq = 22 if currentratingsymbol == "AAA"

keep gvkey time_avail_m credratciq

save "$pathtemp/temp_ciq_rat", replace

// DATA LOAD
use gvkey permno time_avail_m ret using "$pathDataIntermediate/SignalMasterTable", clear
drop if gvkey ==.
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_SP_creditratings", keep(master match) nogenerate
merge 1:1 gvkey time_avail_m using "$pathtemp/temp_ciq_rat", keep(master match) nogenerate

* fill missing credratciq with most recent 
xtset permno time_avail_m
tsfill
sort permno time_avail_m
foreach v of varlist credratciq {
	replace `v' = `v'[_n-1] if permno == permno[_n-1] & mi(`v') 
}

* coalecse credit ratings
replace credrat = credratciq if credrat == .

// SIGNAL CONSTRUCTION
xtset permno time_avail_m
replace ret = 0 if mi(ret)
gen Mom6m = ( (1+l.ret)*(1+l2.ret)*(1+l3.ret)*(1+l4.ret)*(1+l5.ret)) - 1
gen Mom6mJunk = Mom6m if ( credrat <= 14 & credrat > 0 )
label var Mom6mJunk "Junk stock momentum"

// SAVE
do "$pathCode/savepredictor" Mom6mJunk

