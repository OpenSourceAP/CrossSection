* --------------
* Our signal balances users desire to have flexible data and 
* fidelity to OP's original test.

// PREP DISTRIBUTIONS DATA
use "$pathDataIntermediate/CRSPdistributions", clear

* cash div only
keep if cd2 == 2 | cd2 == 3

* collapse by exdt: this date tends to come first
gen time_avail_m = mofd(exdt)
format time_avail_m %tm
drop if time_avail_m == . | divamt == .

* sum dividends
gcollapse (sum) divamt, by(permno time_avail_m)

save "$pathtemp/tempdivamt", replace

// DATA LOAD
use permno time_avail_m exchcd shrcd using "$pathDataIntermediate/SignalMasterTable", clear
merge 1:1 permno time_avail_m using "$pathtemp/tempdivamt", keep(master match) nogenerate keepusing(divamt) 

// SIGNAL CONSTRUCTION
replace divamt = 0 if divamt == .
bys permno: asrol divamt, window(time_avail_m 24) stat(sum) gen(divsum)

xtset permno time_avail_m
//gen temp = divamt > 0 & l1.divsum == 0 & (exchcd == 1 | exchcd == 2) // OP does nyse/amex only, but we are more flexible
gen temp = divamt > 0 & l1.divsum == 0 

* keep for 6 months
bys permno: asrol temp, window(time_avail_m 6) stat(sum) gen(initsum)
gen DivInit = initsum == 1

// SAVE
label var DivInit "Dividend Initiation"
do "$pathCode/savepredictor" DivInit

