* --------------
// DATA LOAD
use permno time_avail_m vol shrout prc using "$pathDataIntermediate/monthlyCRSP", clear
// SIGNAL CONSTRUCTION
gen tempturn = vol/shrout
bys permno: asrol tempturn, gen(std_turn) stat(sd) window(time_avail_m 36) min(24)
gen mve_c = (shrout * abs(prc)) 
egen tempqsize = fastxtile(mve_c), by(time_avail_m) n(5) 
replace std_turn = . if tempqsize >= 4 // OP Tab3B: tiny 10 bps spread in size quints 4 and 5
label var std_turn "Turnover volatility"
// SAVE
do "$pathCode/savepredictor" std_turn