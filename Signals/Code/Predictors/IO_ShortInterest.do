* --------------
// DATA LOAD
use permno gvkey time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
merge 1:1 permno time_avail_m using "$pathDataIntermediate/TR_13F", keep(master match) nogenerate keepusing(instown_perc)
merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keep(master match) nogenerate keepusing(shrout)
preserve

keep if mi(gvkey)

save "$pathtemp/temp", replace  // Temporarily store obs with missing gvkeys in another file
restore
drop if mi(gvkey)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/monthlyShortInterest", keep(master match) nogenerate keepusing(shortint)
* Append obs without gvkey again
append using "$pathtemp/temp"
// SIGNAL CONSTRUCTION
gen tempshortratio = shortint/shrout
replace tempshortratio = 0 if tempshortratio == .
sort time_avail_m
by time_avail_m: egen temps99 = pctile(shortint/shrout), p(99)
gen     temp = instown_perc
replace temp = 0 if mi(temp)
replace temp = . if tempshortratio < temps99
gen IO_ShortInterest = temp
cap drop temp*
label var IO_ShortInterest "Inst Onwership for high short interest"
// SAVE
do "$pathCode/savepredictor" IO_ShortInterest