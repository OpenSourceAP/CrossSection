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
gen G_Binary = .
replace G_Binary = 1 if G <=5
replace G_Binary = 0 if G >=14 & !mi(G)
label var G_Binary "Governance Index"
// SAVE
do "$pathCode/savepredictor" G_Binary