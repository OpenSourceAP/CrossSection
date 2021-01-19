* --------------
// DATA LOAD
use permno time_avail_m exchcd mve_c using "$pathDataIntermediate/SignalMasterTable", clear
merge 1:1 permno time_avail_m using "$pathDataIntermediate/TR_13F", keep(master match) nogenerate keepusing(dbreadth)
// SIGNAL CONSTRUCTION
gen DelBreadth = dbreadth
preserve

keep if exchcd == 1

bys time_avail_m: egen temp = pctile(mve_c), p(20)

keep time_avail_m temp

duplicates drop

save "$pathtemp/temp", replace
restore
merge m:1 time_avail_m using "$pathtemp/temp", nogenerate
replace DelBreadth = . if mve_c < temp
drop temp
label var DelBreadth "Institutional Ownership"
// SAVE
do "$pathCode/savepredictor" DelBreadth