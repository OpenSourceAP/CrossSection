* OP is mostly theory, really old, and pretty vague about what it does.
* So we combine their guidelines with our knowledge of the data
* to get results similar to their regression.

// PREP DISTRIBUTIONS DATA
use permno cd* divamt exdt using "$pathDataIntermediate/CRSPdistributions", clear

keep if cd1 == 1 & cd2 == 2
keep if cd3 == 3 | cd3 == 4 | cd3 == 5 // these are quarterly, semi-ann, and ann respectively

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
use permno time_avail_m prc using "$pathDataIntermediate/SignalMasterTable", clear
merge 1:1 permno time_avail_m using "$pathtemp/tempdivamt", keep(master match) nogenerate keepusing(cd3 divamt) 
merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keep(master match) nogenerate keepusing(ret retx) 

replace cd3 = l1.cd3 if cd3 == .
replace divamt = 0 if divamt == .

* keep only dividend payers
bys permno: asrol divamt, window(time_avail_m 12) stat(sum) gen(div12)
drop if div12 == 0 | div12 == .
	
gen Ediv1 = l2.divamt if (cd3 == 3 | cd3 == 0 | cd3 == 1)
replace Ediv1 = l5.divamt if cd3 == 4
replace Ediv1 = l11.divamt if cd3 == 5

gen Edy1 = Ediv1/abs(prc)

* this is super janky, but we try to imitate their regression with ports
* 0.008 is the median among positive Eyields, but time series behavior is complicated
gen DivYieldST = 0 if Edy1 == 0
replace DivYieldST = 1 if Edy1 > 0     & Edy1 <= 0.005
replace DivYieldST = 2 if Edy1 > 0.005 & Edy1 <= 0.010
replace DivYieldST = 3 if Edy1 > 0.010 & Edy1 != .

label var DivYieldST "Predicted dividend yield next month"

// SAVE
do "$pathCode/savepredictor" DivYieldST


