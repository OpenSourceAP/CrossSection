* TrendFactor
* ------------
* See sections 2.1 and 2.2 of the paper for a detailed description

* 1. Compute moving averages
use permno time_d prc cfacpr using "$pathDataIntermediate/dailyCRSP", clear

* Adjust prices for splits etc
gen P = abs(prc)/cfacpr // I guess they just take the absolute value of prc but it does not say in the paper
drop cfacpr prc

* Generate time variable without trading day gaps for simplicity and generate month variable for sorting
bys permno (time_d): gen time_temp = _n
gen time_avail_m = mofd(time_d)
format time_avail_m %tm

* Calculate moving average prices for various lag lengths
xtset permno time_temp
foreach L of numlist 3 5 10 20 50 100 200 400 600 800 1000 {

    asrol P, window(time_temp `L') stat(mean) by(permno) gen(A_`L')  // Do they require a minimum number of obs? Not discussed in the paper
	
}

* Keep only last observation each month
bys permno time_avail_m (time_d): keep if _n == _N
drop time_d time_temp 
* Normalize by closing price at end of month
foreach L of numlist 3 5 10 20 50 100 200 400 600 800 1000 {

    replace A_`L' = A_`L'/P
	
}

keep permno time_avail_m A_*
save tempMA, replace

** 2. Run cross-sectional regressions on monthly data
use permno time_avail_m ret prc exchcd shrcd mve_c using "$pathDataIntermediate/SignalMasterTable", clear

* Calculate size deciles based on NYSE stocks only
preserve
    keep if exchcd == 1
	gcollapse (p10) qu10 = mve_c, by(time_avail_m)
	save tempQU, replace
restore

merge m:1 time_avail_m using tempQU, nogenerate

* Filters need to be imposed here rather than at portfolio stage in order to run cross-sectional regressions on the filtered sample
keep if exchcd == 1 | exchcd == 2 | exchcd == 3
keep if shrcd == 10 | shrcd == 11
keep if abs(prc)>=5
keep if mve_c >= qu10

drop exchcd shrcd qu10 mve_c prc

* Merge moving averages
merge 1:1 permno time_avail_m using tempMA, keep(match) nogenerate

* Cross-sectional regression of returns on trend signals in month t-1
xtset permno time_avail_m
gen fRet = f.ret  // Instead of lagging all moving averages, I lead the return (and adjust the rolling sums below accordingly)
bys time_avail_m: asreg fRet A_*

* Take 12-month rolling average of MA beta coefficients (leaving out most recent one to not use future information from fRet)
asrol _b_A*, window(time_avail_m -13 -1) stat(mean) by(permno) 
	
* Calculate expected return E[r] = \sum E[\beta_i]A_L_i
gen TrendFactor = _b_A_3_mean_13__1    * A_3 +   ///
                  _b_A_5_mean_13__1    * A_5 +   ///
                  _b_A_10_mean_13__1   * A_10 +  ///
				  _b_A_20_mean_13__1   * A_20 +  ///
                  _b_A_50_mean_13__1   * A_50 +  ///
				  _b_A_100_mean_13__1  * A_100 + ///
                  _b_A_200_mean_13__1  * A_200 + ///
				  _b_A_400_mean_13__1  * A_400 + ///
                  _b_A_600_mean_13__1  * A_600 + ///
				  _b_A_800_mean_13__1  * A_800 + ///
				  _b_A_1000_mean_13__1 * A_1000
				  
label var TrendFactor "Trend Factor"


// SAVE
do "$pathCode/savepredictor" TrendFactor

* Housekeeping		  
erase tempMA.dta
erase tempQU.dta
