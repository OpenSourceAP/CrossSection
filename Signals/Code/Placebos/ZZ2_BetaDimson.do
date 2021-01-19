* BetaDimson
* -----------

// DATA LOAD
use permno time_d ret using "$pathDataIntermediate/dailyCRSP.dta", clear

merge m:1 time_d using "$pathDataIntermediate/dailyFF", nogenerate keep(match) keepusing(rf mktrf)
replace ret = ret - rf
drop rf 

// SIGNAL CONSTRUCTION
bys permno (time_d): gen time_temp = _n
xtset permno time_temp

gen tempMktLead = f.mktrf
gen tempMktLag  = l.mktrf

asreg ret tempMktLead mktrf tempMktLag, window(time_temp 20) min(15) by(permno)

gen BetaDimson = _b_tempMktLead + _b_mktrf + _b_tempMktLag

gen time_avail_m = mofd(time_d)
format time_avail_m %tm

sort permno time_avail_m time_d
gcollapse (lastnm) BetaDimson, by(permno time_avail_m)

label var BetaDimson "Dimson beta"

// SAVE
do "$pathCode/saveplacebo" BetaDimson
