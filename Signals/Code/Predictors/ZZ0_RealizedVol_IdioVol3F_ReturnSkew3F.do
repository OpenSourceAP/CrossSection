* -------------------------
* Realized Vol is used in one other predictor so this is run before other ZZ stuff
// DATA LOAD
use permno time_d ret using "$pathDataIntermediate/dailyCRSP.dta", clear
merge m:1 time_d using "$pathDataIntermediate/dailyFF", nogenerate keep(match)keepusing(rf mktrf smb hml)
replace ret = ret - rf
drop rf 

// SIGNAL CONSTRUCTION
sort permno time_d 

* create time_avail_m that is just the year-month of each year-day
gen time_avail_m = mofd(time_d)
format time_avail_m %tm

* get FF3 residuals within each month
bys permno time_avail_m: asreg ret mktrf smb hml, fit

* collapse into second and third moments
gcollapse (sd) RealizedVol = ret ///
	(sd) IdioVol3F = _residuals (skewness) ReturnSkew3F = _residuals, ///
	by(permno time_avail_m)



label var RealizedVol "Realized (Total) Vol (Daily)"
label var IdioVol3F "Idiosyncratic Risk (3 factor)"
label var ReturnSkew3F "Skewness of daily idiosyncratic returns (3F model)"


// SAVE 
do "$pathCode/savepredictor" RealizedVol
do "$pathCode/savepredictor" IdioVol3F
do "$pathCode/savepredictor" ReturnSkew3F
