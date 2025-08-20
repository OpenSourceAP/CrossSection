* --------------
// DATA LOAD
use permno time_avail_m ret using "$pathDataIntermediate/monthlyCRSP", clear
merge m:1 time_avail_m using "$pathDataIntermediate/monthlyFF", nogenerate keep(match) keepusing(rf mktrf hml smb)

// SIGNAL CONSTRUCTION
gen retrf = ret - rf
bys permno (time_avail_m): gen time_temp = _n
xtset permno time_temp

* - CHECKPOINT 1: Check retrf calculation for problematic observations
list permno time_avail_m ret rf retrf if (permno == 43880 & (time_avail_m >= tm(1993m1) & time_avail_m <= tm(1993m6))) | (permno == 79490 & (time_avail_m >= tm(2007m12) & time_avail_m <= tm(2008m3))) | (permno == 85570 & (time_avail_m >= tm(2007m12) & time_avail_m <= tm(2008m3))) | (permno == 13725 & (time_avail_m >= tm(1935m1) & time_avail_m <= tm(1935m12))), sepby(permno)

asreg retrf mktrf hml smb, window(time_temp 36) min(36) by(permno) fitted

* - CHECKPOINT 2: Check FF3 regression results for problematic observations  
list permno time_avail_m time_temp _fitted _residuals if (permno == 43880 & (time_avail_m >= tm(1993m1) & time_avail_m <= tm(1993m6))) | (permno == 79490 & (time_avail_m >= tm(2007m12) & time_avail_m <= tm(2008m3))) | (permno == 85570 & (time_avail_m >= tm(2007m12) & time_avail_m <= tm(2008m3))) | (permno == 13725 & (time_avail_m >= tm(1935m1) & time_avail_m <= tm(1935m12))), sepby(permno)

gen temp = l1._residuals  // To skip most recent month in what follows

* - CHECKPOINT 3: Check lagged residuals
list permno time_avail_m time_temp _residuals temp if (permno == 43880 & (time_avail_m >= tm(1993m1) & time_avail_m <= tm(1993m6))) | (permno == 79490 & (time_avail_m >= tm(2007m12) & time_avail_m <= tm(2008m3))) | (permno == 85570 & (time_avail_m >= tm(2007m12) & time_avail_m <= tm(2008m3))) | (permno == 13725 & (time_avail_m >= tm(1935m1) & time_avail_m <= tm(1935m12))), sepby(permno)

* 6 month version
asrol temp, window(time_temp 6) min(6) by(permno) stat(mean) gen(mean6_temp)
asrol temp, window(time_temp 6) min(6) by(permno) stat(sd) gen(sd6_temp)

gen ResidualMomentum6m = mean6_temp/sd6_temp

* - CHECKPOINT 4: Check 6-month rolling statistics
list permno time_avail_m time_temp temp mean6_temp sd6_temp ResidualMomentum6m if (permno == 43880 & (time_avail_m >= tm(1993m1) & time_avail_m <= tm(1993m6))) | (permno == 79490 & (time_avail_m >= tm(2007m12) & time_avail_m <= tm(2008m3))) | (permno == 85570 & (time_avail_m >= tm(2007m12) & time_avail_m <= tm(2008m3))) | (permno == 13725 & (time_avail_m >= tm(1935m1) & time_avail_m <= tm(1935m12))), sepby(permno)

* 12 month version
asrol temp, window(time_temp 11) min(11) by(permno) stat(mean) gen(mean11_temp)
asrol temp, window(time_temp 11) min(11) by(permno) stat(sd) gen(sd11_temp)
gen ResidualMomentum = mean11_temp/sd11_temp

* - CHECKPOINT 5: Check 11-month rolling statistics and final ResidualMomentum
list permno time_avail_m time_temp temp mean11_temp sd11_temp ResidualMomentum if (permno == 43880 & (time_avail_m >= tm(1993m1) & time_avail_m <= tm(1993m6))) | (permno == 79490 & (time_avail_m >= tm(2007m12) & time_avail_m <= tm(2008m3))) | (permno == 85570 & (time_avail_m >= tm(2007m12) & time_avail_m <= tm(2008m3))) | (permno == 13725 & (time_avail_m >= tm(1935m1) & time_avail_m <= tm(1935m12))), sepby(permno)

label var ResidualMomentum6m "6 month residual momentum"
label var ResidualMomentum "Momentum based on FF3 residuals"

// SAVE 
do "$pathCode/saveplacebo" ResidualMomentum6m
do "$pathCode/savepredictor" ResidualMomentum
