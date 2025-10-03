* --------------------------------------
// DATA LOAD
use permno time_d ret using "$pathDataIntermediate/dailyCRSP.dta", clear
merge m:1 time_d using "$pathDataIntermediate/dailyFF", nogenerate keep(match) keepusing(rf mktrf)
replace ret = ret - rf
drop rf 

// SIGNAL CONSTRUCTION
sort permno time_d 

* create time_avail_m that is just the year-month of each year-day
gen time_avail_m = mofd(time_d)
format time_avail_m %tm

* get CAPM residuals within each month
bys permno time_avail_m: asreg ret mktrf, fit

* collapse into second and third moments
gcollapse (sd) IdioVolCAPM = _residuals (skewness) ReturnSkewCAPM = _residuals, ///
	by(permno time_avail_m)

label var IdioVolCAPM "Idiosyncratic Risk (CAPM)"
label var ReturnSkewCAPM "Skewness of daily idiosyncratic returns (CAPM)"

// SAVE
do "$pathCode/saveplacebo" IdioVolCAPM
do "$pathCode/saveplacebo" ReturnSkewCAPM
