* Activism1, Activism2
* --------------

// DATA LOAD
use permno time_avail_m ticker exchcd mve_c using "$pathDataIntermediate/SignalMasterTable", clear

merge 1:1 permno time_avail_m using "$pathDataIntermediate/TR_13F", keep(master match) nogenerate keepusing(maxinstown_perc)

merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keep(master match) nogenerate keepusing(shrcls)

* Add ticker-based data (many to one match due to permno-ticker not being unique in crsp)
preserve
	keep if mi(ticker)
	save "$pathtemp/temp", replace
restore

drop if mi(ticker)

merge m:1 ticker time_avail_m using "$pathDataIntermediate/GovIndex", keep(master match) nogenerate

append using "$pathtemp/temp"

// SIGNAL CONSTRUCTION

* Shareholder activism proxy 1
gen tempBLOCK = maxinstown_perc if maxinstown_perc > 5
replace tempBLOCK = 0 if tempBLOCK == .
egen tempBLOCKQuant = fastxtile(tempBLOCK), n(4) by(time_avail_m)

gen tempEXT = 24 - G
replace tempEXT = . if G == . 
replace tempEXT = . if tempBLOCKQuant <= 3
replace tempEXT = . if !mi(shrcls) // Exclude dual class shares

gen Activism1 = tempEXT
label var Activism1 "Shareholder activism I: External Gov among Large Blockheld"

drop temp*

* Shareholder activism proxy 2
gen tempBLOCK = maxinstown_perc if maxinstown_perc > 5
replace tempBLOCK = 0 if tempBLOCK == .

replace tempBLOCK = . if G == .
replace tempBLOCK = . if !mi(shrcls) // Exclude dual class shares

replace tempBLOCK = . if 24 - G < 19

gen Activism2 = tempBLOCK
label var Activism2 "Shareholder activism II: Blockholdings among High Ext Gov"


// SAVE
do "$pathCode/savepredictor" Activism1
do "$pathCode/savepredictor" Activism2