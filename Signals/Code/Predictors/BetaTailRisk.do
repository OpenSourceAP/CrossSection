* BetaTailRisk
* --------------

// DATA LOAD

* Daily data to estimate tail risk

use permno time_d ret using "$pathDataIntermediate/dailyCRSP.dta", clear

gen time_avail_m = mofd(time_d)
format time_avail_m %tm

* CHECKPOINT 1
list permno time_d ret time_avail_m if permno == 78050 & time_avail_m >= tm(1998m11) & time_avail_m <= tm(1999m2), sepby(time_avail_m)

preserve
	gcollapse (p5) ret, by(time_avail_m) fast
	rename ret retp5
	* CHECKPOINT 2
	list time_avail_m retp5 if time_avail_m >= tm(1998m11) & time_avail_m <= tm(1999m2)
	save "$pathtemp/temp", replace
restore

merge m:1 time_avail_m using "$pathtemp/temp", nogenerate

keep if ret <= retp5

* CHECKPOINT 3
count if permno == 78050 & time_avail_m >= tm(1998m11) & time_avail_m <= tm(1999m2)
list permno time_d ret retp5 time_avail_m if permno == 78050 & time_avail_m >= tm(1998m11) & time_avail_m <= tm(1999m2)

gen tailex = log(ret/retp5)

* CHECKPOINT 4
list permno time_d ret retp5 tailex time_avail_m if permno == 78050 & time_avail_m >= tm(1998m11) & time_avail_m <= tm(1999m2)

gcollapse (mean) tailex, by(time_avail_m) 

save "$pathDataIntermediate/TailRisk", replace


* Load monthly returns for tailrisk regression
use permno time_avail_m ret shrcd using "$pathDataIntermediate/monthlyCRSP", clear

* Add monthly tail risk for tail risk beta regressions
merge m:1 time_avail_m using "$pathDataIntermediate/TailRisk", keep(master match) nogenerate

* CHECKPOINT 5
list permno time_avail_m ret tailex if permno == 78050 & time_avail_m >= tm(1990m1) & time_avail_m <= tm(2000m12)

// SIGNAL CONSTRUCTION

asreg ret tailex, window(time_avail_m 120) min(72) by(permno)

rename _b_tailex BetaTailRisk
drop _*
replace BetaTailRisk = . if shrcd > 11

* CHECKPOINT 6
list permno time_avail_m ret tailex BetaTailRisk if permno == 78050 & time_avail_m >= tm(1998m1) & time_avail_m <= tm(2000m12)

label var BetaTailRisk "Tail risk beta"


// SAVE
do "$pathCode/savepredictor" BetaTailRisk