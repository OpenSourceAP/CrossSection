* --------------
* Our signal balances users desire to have flexible data and 
* fidelity to OP's original test.
// DATA LOAD
use permno time_avail_m exchcd shrcd using "$pathDataIntermediate/SignalMasterTable", clear
merge 1:1 permno time_avail_m using "$pathDataIntermediate/mCRSPdistributions", keep(master match) nogenerate keepusing(divamt) 

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

