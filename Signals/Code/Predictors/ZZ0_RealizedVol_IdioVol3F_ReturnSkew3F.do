* -------------------------
* Realized Vol is used in one other predictor so this is run before other ZZ stuff
// DATA LOAD
use permno time_d ret using "$pathDataIntermediate/dailyCRSP.dta", clear

merge m:1 time_d using "$pathDataIntermediate/dailyFF", nogenerate keep(match)keepusing(rf mktrf smb hml)
replace ret = ret - rf
drop rf

* CHECKPOINT 1: After data merge and return adjustment
list permno time_d ret mktrf smb hml if permno == 11651 & time_d >= td(01sep1987) & time_d <= td(30sep1987) in 1/10 

// SIGNAL CONSTRUCTION
sort permno time_d 

* create time_avail_m that is just the year-month of each year-day
gen time_avail_m = mofd(time_d)
format time_avail_m %tm

* CHECKPOINT 2: After creating time_avail_m
list permno time_d time_avail_m ret mktrf smb hml if permno == 11651 & time_avail_m == tm(1987m9) in 1/10

* get FF3 residuals within each month
bys permno time_avail_m: asreg ret mktrf smb hml, fit

* CHECKPOINT 3: After FF3 regression
list permno time_avail_m _Nobs _residuals ret mktrf smb hml if permno == 11651 & time_avail_m == tm(1987m9) in 1/10
summarize _Nobs _residuals if permno == 11651 & time_avail_m == tm(1987m9)

keep if _Nobs >= 15 // Bali-Hovak 2009 footnote 9. AHXZ seem to require > 17

* CHECKPOINT 4: After filtering by _Nobs >= 15
count if permno == 11651 & time_avail_m == tm(1987m9)
list permno time_avail_m _Nobs _residuals ret if permno == 11651 & time_avail_m == tm(1987m9) in 1/10

* CHECKPOINT 5: Before gcollapse aggregation
summarize ret _residuals if permno == 11651 & time_avail_m == tm(1987m9)
display "Number of observations for calculation: " _N
egen temp_sd_ret = sd(ret) if permno == 11651 & time_avail_m == tm(1987m9)
egen temp_sd_resid = sd(_residuals) if permno == 11651 & time_avail_m == tm(1987m9)
egen temp_skew_resid = skew(_residuals) if permno == 11651 & time_avail_m == tm(1987m9)
list temp_sd_ret temp_sd_resid temp_skew_resid if permno == 11651 & time_avail_m == tm(1987m9) in 1/1
drop temp_*

* collapse into second and third moments
gcollapse (sd) RealizedVol = ret ///
	(sd) IdioVol3F = _residuals (skewness) ReturnSkew3F = _residuals, ///
	by(permno time_avail_m)

* CHECKPOINT 6: After gcollapse aggregation
list permno time_avail_m RealizedVol IdioVol3F ReturnSkew3F if permno == 11651 & time_avail_m == tm(1987m9)
summarize RealizedVol IdioVol3F ReturnSkew3F if permno == 11651 & time_avail_m == tm(1987m9)


label var RealizedVol "Realized (Total) Vol (Daily)"
label var IdioVol3F "Idiosyncratic Risk (3 factor)"
label var ReturnSkew3F "Skewness of daily idiosyncratic returns (3F model)"


// SAVE 
do "$pathCode/savepredictor" RealizedVol
do "$pathCode/savepredictor" IdioVol3F
do "$pathCode/savepredictor" ReturnSkew3F
