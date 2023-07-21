* -------------------------
// DATA LOAD
use permno time_d ret using "$pathDataIntermediate/dailyCRSP.dta", clear
merge m:1 time_d using "$pathDataIntermediate/d_qfactor", nogenerate keep(master match)
replace ret = ret - r_f_qfac
drop r_f_qfac

// SIGNAL CONSTRUCTION
sort permno time_d 

* create time_avail_m that is just the year-month of each year-day
gen time_avail_m = mofd(time_d)
format time_avail_m %tm

* get qfac residuals within each month
bys permno time_avail_m: asreg ret r_mkt_qfac r_me_qfac r_ia_qfac r_roe_qfac, fit

* collapse into second and third moments
gcollapse (sd) IdioVolQF = _residuals (skewness) ReturnSkewQF = _residuals, ///
	by(permno time_avail_m)


label var IdioVolQF "Idiosyncratic Risk (Q factor)"
label var ReturnSkewQF "Skewness of daily idiosyncratic returns (QF model)"

// SAVE
do "$pathCode/saveplacebo" IdioVolQF
do "$pathCode/saveplacebo" ReturnSkewQF
