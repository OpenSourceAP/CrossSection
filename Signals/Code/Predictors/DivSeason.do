// PREP DISTRIBUTIONS DATA
use permno cd* divamt exdt using "$pathDataIntermediate/CRSPdistributions", clear

keep if cd1 == 1 & cd2 == 2

* select timing variable and convert to monthly
* (p5 says exdt is used)
gen time_avail_m = mofd(exdt)
format time_avail_m %tm
drop if time_avail_m == . | divamt == .

* sum across all frequency codes
gcollapse (sum) divamt, by(permno cd3 time_avail_m)

* clean up a handful of odd two-frequency permno-months
* by keeping the quarterly code
sort permno time_avail_m cd3
by permno time_avail_m: keep if _n == 1

save "$pathtemp/tempdivamt", replace

// DATA LOAD
use permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
merge 1:1 permno time_avail_m using "$pathtemp/tempdivamt", keep(master match) nogenerate keepusing(cd3 divamt) 

replace cd3 = l1.cd3 if cd3 == .
replace divamt = 0 if divamt == .
gen divpaid = divamt > 0
drop if cd3 == 2 // OP drops monly div unless otherwise noted (p5)
keep if cd3 < 6 // Tab 2 note


* short all other with a div in last 12 months
bys permno: asrol divpaid, window(time_avail_m 12) stat(sum) gen(div12)
gen DivSeason = 0 if div12 > 0 

* long if div month is predicted
* OP page 5: "unkown and missing frequency are assumed quarterly"
gen temp3 = (cd3 == 3 | cd3 == 0 | cd3 == 1) ///
	& (l2.divpaid | l5.divpaid | l8.divpaid | l11.divpaid ) 
gen temp4 = cd3 == 4 & (l5.divpaid | l11.divpaid )
gen temp5 = cd3 == 5 & (l11.divpaid )

replace DivSeason = 1 if temp3 | temp4 | temp5


label var DivSeason "Predicted Dividend Month"

// SAVE
do "$pathCode/savepredictor" DivSeason
