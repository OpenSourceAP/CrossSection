* --------------
// DATA LOAD
use permno time_avail_m ret using "$pathDataIntermediate/monthlyCRSP", clear
merge m:1 time_avail_m using "$pathDataIntermediate/monthlyFF", nogenerate keep(match) keepusing(rf mktrf hml smb)

// SIGNAL CONSTRUCTION
gen retrf = ret - rf
* CHECKPOINT 1: After data merge and excess return calculation
list permno time_avail_m ret rf retrf mktrf hml smb if permno == 43880 & time_avail_m == tm(1993m1) in 1/10
bys permno (time_avail_m): gen time_temp = _n
xtset permno time_temp
* CHECKPOINT 2: After creating time_temp position index
list permno time_avail_m time_temp retrf if permno == 43880 & time_avail_m == tm(1993m1) in 1/10
count if permno == 43880
asreg retrf mktrf hml smb, window(time_temp 36) min(36) by(permno) fitted
* CHECKPOINT 3: After rolling FF3 regression
list permno time_avail_m time_temp _residuals _fitted retrf mktrf if permno == 43880 & time_avail_m == tm(1993m1) in 1/5
summarize _residuals if permno == 43880 & time_avail_m == tm(1993m1)
count if _residuals != . & permno == 43880
gen temp = l1._residuals  // To skip most recent month in what follows
* CHECKPOINT 4: After lagged residuals calculation
list permno time_avail_m time_temp _residuals temp if permno == 43880 & time_avail_m == tm(1993m1) in 1/5
list permno time_avail_m time_temp _residuals temp if permno == 43880 in -10/-1
count if temp != . & permno == 43880

* 6 month version
asrol temp, window(time_temp 6) min(6) by(permno) stat(mean) gen(mean6_temp)
asrol temp, window(time_temp 6) min(6) by(permno) stat(sd) gen(sd6_temp)

gen ResidualMomentum6m = mean6_temp/sd6_temp
* CHECKPOINT 5: After 6-month rolling statistics
list permno time_avail_m temp mean6_temp sd6_temp ResidualMomentum6m if permno == 43880 & time_avail_m == tm(1993m1)
summarize mean6_temp sd6_temp ResidualMomentum6m if permno == 43880 & time_avail_m == tm(1993m1)

* 12 month version
asrol temp, window(time_temp 11) min(11) by(permno) stat(mean) gen(mean11_temp)
asrol temp, window(time_temp 11) min(11) by(permno) stat(sd) gen(sd11_temp)
gen ResidualMomentum = mean11_temp/sd11_temp
* CHECKPOINT 6: After 11-month rolling statistics and final calculation
list permno time_avail_m temp mean11_temp sd11_temp ResidualMomentum if permno == 43880 & time_avail_m == tm(1993m1)
summarize mean11_temp sd11_temp ResidualMomentum if permno == 43880 & time_avail_m == tm(1993m1)
list permno time_avail_m ResidualMomentum6m ResidualMomentum if permno == 43880 & time_avail_m == tm(1993m1)

label var ResidualMomentum6m "6 month residual momentum"
label var ResidualMomentum "Momentum based on FF3 residuals"

// SAVE 
do "$pathCode/saveplacebo" ResidualMomentum6m
do "$pathCode/savepredictor" ResidualMomentum
