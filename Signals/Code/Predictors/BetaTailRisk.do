* BetaTailRisk
* --------------

// DATA LOAD

* Daily data to estimate tail risk

use permno time_d ret using "$pathDataIntermediate/dailyCRSP.dta", clear

gen time_avail_m = mofd(time_d)
format time_avail_m %tm

preserve
	gcollapse (p5) ret, by(time_avail_m) fast
	rename ret retp5
	save "$pathtemp/temp", replace
restore

merge m:1 time_avail_m using "$pathtemp/temp", nogenerate

keep if ret <= retp5

gen tailex = log(ret/retp5)
gcollapse (mean) tailex, by(time_avail_m) 

save "$pathDataIntermediate/TailRisk", replace


* Load monthly returns for tailrisk regression
use permno time_avail_m ret shrcd using "$pathDataIntermediate/monthlyCRSP", clear

* Add monthly tail risk for tail risk beta regressions
merge m:1 time_avail_m using "$pathDataIntermediate/TailRisk", keep(master match) nogenerate

// SIGNAL CONSTRUCTION

asreg ret tailex, window(time_avail_m 120) min(72) by(permno)

rename _b_tailex BetaTailRisk
drop _*
replace BetaTailRisk = . if shrcd > 11

label var BetaTailRisk "Tail risk beta"


// SAVE
do "$pathCode/savepredictor" BetaTailRisk