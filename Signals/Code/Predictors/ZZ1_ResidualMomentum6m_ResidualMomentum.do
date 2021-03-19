* --------------
// DATA LOAD
use permno time_avail_m ret using "$pathDataIntermediate/monthlyCRSP", clear
merge m:1 time_avail_m using "$pathDataIntermediate/monthlyFF", nogenerate keep(match) keepusing(rf mktrf hml smb)

// SIGNAL CONSTRUCTION
gen retrf = ret - rf
bys permno (time_avail_m): gen time_temp = _n
xtset permno time_temp
asreg retrf mktrf hml smb, window(time_temp 36) min(36) by(permno) fitted
gen temp = l1._residuals  // To skip most recent month in what follows

* 6 month version
asrol temp, window(time_temp 6) min(6) by(permno) stat(mean sd)
gen ResidualMomentum6m = mean6_temp/sd6_temp

* 12 month version
asrol temp, window(time_temp 11) min(11) by(permno) stat(mean sd)
gen ResidualMomentum = mean11_temp/sd11_temp
label var ResidualMomentum6m "6 month residual momentum"
label var ResidualMomentum "Momentum based on FF3 residuals"

// SAVE 
do "$pathCode/saveplacebo" ResidualMomentum6m
do "$pathCode/savepredictor" ResidualMomentum
