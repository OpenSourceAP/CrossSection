* -------------
// DATA LOAD
use permno time_d ret using "$pathDataIntermediate/dailyCRSP.dta", clear
merge m:1 time_d using "$pathDataIntermediate/dailyFF", nogenerate keep(match) keepusing(rf mktrf)
replace ret = ret - rf

* CHECKPOINT 1: After data merge and excess return calculation
list permno time_d ret mktrf if permno == 10346 & time_d >= td(01jul1995) & time_d <= td(31aug1995) in 1/10
count if permno == 10346 & time_d >= td(01jul1995) & time_d <= td(31aug1995)

drop rf 
// SIGNAL CONSTRUCTION
* IdioVol as in HXZ citing Ali et al (2003)
bys permno (time_d): gen time_temp = _n
xtset permno time_temp

* CHECKPOINT 2: After creating time position index
list permno time_d time_temp ret if permno == 10346 & time_d >= td(01jul1995) & time_d <= td(31aug1995) in 1/10
count if permno == 10346
asreg ret mktrf, window(time_temp 252) min(100) by(permno) rmse

* CHECKPOINT 3: After rolling regression
list permno time_d time_temp _rmse ret mktrf if permno == 10346 & time_d >= td(01jul1995) & time_d <= td(31aug1995) in 1/5
summarize _rmse if permno == 10346 & time_d >= td(01jul1995) & time_d <= td(31aug1995)
count if _rmse != . & permno == 10346

rename _rmse IdioVolAHT
gen time_avail_m = mofd(time_d)
format time_avail_m %tm
sort permno time_avail_m time_d
gcollapse (lastnm) IdioVolAHT, by(permno time_avail_m)

* CHECKPOINT 4: Before final output
list permno time_avail_m IdioVolAHT if permno == 10346 & time_avail_m == tm(1995m8)
summarize IdioVolAHT if permno == 10346 & time_avail_m == tm(1995m8)
count if IdioVolAHT != . & permno == 10346

label var IdioVolAHT "Idiosyncratic Risk (AHT)"

// SAVE 
do "$pathCode/savepredictor" IdioVolAHT