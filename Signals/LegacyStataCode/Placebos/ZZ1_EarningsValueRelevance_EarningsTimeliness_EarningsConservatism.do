* --------------
// DATA LOAD
* Compute 15 month return (with 12 month past returns and 3 months future return)
* This will be matched to end of fiscal year, and then lagged to make sure
* data are actually available
use permno time_avail_m ret prc shrout using "$pathDataIntermediate/monthlyCRSP", clear
rename time_avail_m time_m
xtset permno time_m
replace ret = 0 if mi(ret)
gen tempMom15m = ( (1+f2.ret)*(1+f.ret)*(1+ret)*(1+l.ret)*(1+l2.ret)* ///
(1+l3.ret)*(1+l4.ret)*(1+l5.ret)*(1+l6.ret)*(1+l7.ret)* ///
(1+ l8.ret)*(1+l9.ret)*(1+l10.ret)*(1+l11.ret) ) - 1

gen tempmktcap = abs(prc)*shrout
keep permno time_m temp*
save "$pathtemp/tempPlacebo", replace
**
use gvkey permno datadate fyear ib using "$pathDataIntermediate/a_aCompustat", clear
* Monthly date to match to monthly returns
gen time_m = mofd(datadate)
format time_m %tm
merge 1:1 permno time_m using "$pathtemp/tempPlacebo", keep(master match) nogenerate
// SIGNAL CONSTRUCTION
xtset gvkey fyear
gen tempEarn  = ib/tempmktcap
gen tempDEarn = (ib - l.ib)/tempmktcap
* Regression for value relevance of earnings
asreg tempMom15m tempEarn tempDEarn, window(fyear 10) min(10) by(gvkey)
rename _R2 EarningsValueRelevance
drop _*
* Regression for earnings timeliness and earnings conservatism
gen tempNeg = (tempMom15m < 0)
replace tempNeg = . if mi(tempMom15m)
gen tempInter = tempNeg*tempMom15m
asreg tempEarn tempNeg tempMom15m tempInter,  window(fyear 10) min(10) by(gvkey)
rename _R2 EarningsTimeliness
gen EarningsConservatism = (_b_tempMom15m + _b_tempInter)/_b_tempMom15m
drop _* temp*
label var EarningsValueRelevance "Value relevance of earnings"
label var EarningsConservatism "Earnings conservatism"
label var EarningsTimeliness "Earnings timeliness"
* Expand to monthly
gen time_avail_m = mofd(datadate) + 6
gen temp = 12
expand temp
drop temp
gen tempTime = time_avail_m
bysort gvkey tempTime: replace time_avail_m = time_avail_m + _n - 1 
drop tempTime
bysort gvkey time_avail_m (datadate): keep if _n == _N 
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations

// SAVE
do "$pathCode/saveplacebo" EarningsValueRelevance
do "$pathCode/saveplacebo" EarningsTimeliness
do "$pathCode/saveplacebo" EarningsConservatism