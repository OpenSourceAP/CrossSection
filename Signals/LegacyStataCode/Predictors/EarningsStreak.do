// PROCESS ACTUALS
use "$pathDataIntermediate/IBES_EPS_Adj", clear
keep if fpi == "6"

drop if actual == . | meanest == . | price == .

// use actual release date as date of availability
drop time_avail_m 
gen time_avail_m = mofd(anndats_act)
format time_avail_m %tm

// keep the last forecast before the actual release
sort tickerIBES time_avail_m anndats_act statpers
by tickerIBES time_avail_m: keep if _n == _N

// Define Surp (positive / negative surprise) and Streak (consistent Surp)
gen surp = (actual - meanest)/price 
sort tickerIBES anndats_act
by tickerIBES: gen streak = sign(surp) == sign(surp[_n-1])

// Convert to Postitive Streak vs Negative Streak
keep if streak == 1 

save "$pathtemp/tempibes", replace

// FILL TO MONTHLY AND ADD PERMNOS
use permno time_avail_m tickerIBES using "$pathDataIntermediate/SignalMasterTable", clear
merge m:1 tickerIBES time_avail_m using "$pathtemp/tempibes", keep(master match) nogenerate 

drop fpi tickerIBES

xtset permno time_avail_m

// drop stale or empty
replace anndats_act = l1.anndats_act if anndats_act == .
drop if anndats_act == .
drop if time_avail_m - mofd(anndats_act) > 6 // drop if stale

// the signal is just surp among streak == 1, but we've already kept only streak == 1
gen EarningsStreak = surp
replace EarningsStreak = l1.EarningsStreak if EarningsStreak == .

label var EarningsStreak "Earnings surprise among earnings streaks"

// SAVE
do "$pathCode/savepredictor" EarningsStreak

