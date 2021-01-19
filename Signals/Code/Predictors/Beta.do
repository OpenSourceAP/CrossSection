* Beta, 
* BetaSquared was weak in OP
* --------------

// DATA LOAD
use permno time_avail_m ret using "$pathDataIntermediate/monthlyCRSP", clear
merge m:1 time_avail_m using "$pathDataIntermediate/monthlyFF", nogenerate keep(match) keepusing(rf)
merge m:1 time_avail_m using "$pathDataIntermediate/monthlyMarket",  nogenerate keep(match) keepusing(ewretd)

// SIGNAL CONSTRUCTION
gen retrf = ret - rf
gen ewmktrf = ewretd - rf

bys permno (time_avail_m): gen time_temp = _n
xtset permno time_temp

asreg retrf ewmktrf, window(time_temp 60) min(20) by(permno)
rename _b_ewmktrf Beta
label var Beta "CAPM Beta"

// SAVE
do "$pathCode/savepredictor" Beta