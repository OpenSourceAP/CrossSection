* --------------
// DATA LOAD
use permno time_avail_m ticker using "$pathDataIntermediate/SignalMasterTable", clear
* Add ticker-based data (many to one match due to permno-ticker not being unique in crsp)
preserve

keep if mi(ticker)

save "$pathtemp/temp", replace
restore
drop if mi(ticker)
merge m:1 ticker time_avail_m using "$pathDataIntermediate/BH", keep(master match) nogenerate
append using "$pathtemp/temp"
// SIGNAL CONSTRUCTION
gen CPVolSpread = bh_call - bh_put
drop if CPVolSpread == .

label var CPVolSpread "Bali-Hovak (2009) panel B"
// SAVE
do "$pathCode/savepredictor" CPVolSpread
