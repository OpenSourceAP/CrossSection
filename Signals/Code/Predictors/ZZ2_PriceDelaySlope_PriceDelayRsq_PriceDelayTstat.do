* -----------------------------------------
* Takes about 10 min

* works best with nlag 4 weightscale 1 so far.  
global nlag 4
global weightscale 1

// DATA LOAD

* Prep mkt lag data
use "$pathDataIntermediate/dailyFF", clear
drop smb hml umd
sort time_d
foreach n of numlist 1/$nlag {
	gen mktLag`n' = mktrf[_n-`n']
}
save "$pathtemp/tempdailyff", replace

* load daily crsp
use permno time_d ret using "$pathDataIntermediate/dailyCRSP.dta", clear
merge m:1 time_d using "$pathtemp/tempdailyff", nogenerate keep(match) 
replace ret = ret - rf
drop rf 

* set up for Regressions in each June
* time_avail_m is the most next June after the obs (or is just the current month)
gen time_m = mofd(time_d) 
format time_m %tm
gen time_avail_m = mofd(mdy(6,30,year(dofm(time_m+6))))
format time_avail_m %tm
drop time_m

// REGRESSIONS

* restricted (lag slopes = 0)
* takes about 5 min.  Barfs out if there are memory limitations
sort time_avail_m permno
by time_avail_m permno: asreg ret mktrf, min(26) // Cannot entirely control that observations are the same as above
rename _R2 R2Restricted
drop _*

* unrestricted
by time_avail_m permno: asreg ret mktrf mktLag*, min(26) se
cap drop _adjR2 _Nobs _b_cons
foreach n of numlist 1/$nlag {
	gen _t_mktLag`n' = _b_mktLag`n'/_se_mktLag`n'
}

// CONSTRUCT DELAY SIGNALS

* collapse to monthly 
drop if _R2 == .
keep if month(time_d) == 6 // drop if last obs is not June
bys permno time_avail_m: keep if _n == 1

* Construct D1
gen PriceDelayRsq = 1 - R2Restricted/_R2

* Construct D2
foreach n of numlist 1/$nlag  {
	gen tempweighted`n' = (`n'/$weightscale)*_b_mktLag`n'
}
egen tempSum1 = rowtotal(tempweighted*)
egen tempSum2 = rowtotal(_b_mktLag*)
gen PriceDelaySlope = tempSum1/(_b_mktrf + tempSum2)
drop temp*


* Construct D3
foreach n of numlist 1/$nlag {
	gen tempweighted`n' = (`n'/$weightscale)*_t_mktLag`n'
}
egen tempSum1 = rowtotal(tempweighted*)
egen tempSum2 = rowtotal(_t_mktLag*)
gen PriceDelayTstat = tempSum1/(_b_mktrf + tempSum2)
drop temp*

replace time_avail_m = time_avail_m + 1 // Hou and Moskowitz skip one month

label var PriceDelaySlope "Price delay (slope)"
label var PriceDelayRsq "Price delay (R2 based)"
label var PriceDelayTstat "Price delay (SE adjusted)"

gstats winsor PriceDelayTstat, by(time_avail_m) trim cuts(10 90) replace  // Trim very aggressively because coefficient/se not very well-behaved

* Fill to monthly
keep permno time_avail_m PriceDelay* 
xtset permno time_avail_m
tsfill
foreach v of varlist PriceDelay* {
    bys permno (time_avail_m): replace `v' = `v'[_n-1] if mi(`v')    
}

// SAVE 
do "$pathCode/savepredictor" PriceDelaySlope
do "$pathCode/savepredictor" PriceDelayRsq
do "$pathCode/savepredictor" PriceDelayTstat
