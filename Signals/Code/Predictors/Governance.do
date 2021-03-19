* --------------
// DATA LOAD
use permno time_avail_m ticker exchcd mve_c using "$pathDataIntermediate/SignalMasterTable", clear
* Add ticker-based data (many to one match due to permno-ticker not being unique in crsp)
preserve

keep if mi(ticker)

save "$pathtemp/temp", replace
restore
drop if mi(ticker)
merge m:1 ticker time_avail_m using "$pathDataIntermediate/GovIndex", keep(master match) nogenerate
append using "$pathtemp/temp"

// SIGNAL CONSTRUCTION
gen Governance = G
replace Governance = 5 if G <=5
replace Governance = 14 if G >=14 & !mi(G)
label var Governance "Governance Index"

// SAVE
do "$pathCode/savepredictor" Governance
