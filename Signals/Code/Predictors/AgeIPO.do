* AgeIPO
* --------------

// DATA LOAD
use permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear

merge m:1 permno using "$pathDataIntermediate/IPODates", keep(master match) nogenerate 

// SIGNAL CONSTRUCTION
gen tempipo = (time_avail_m - IPOdate <= 36) & (time_avail_m - IPOdate >= 3)
replace tempipo = . if IPOdate == .

gen AgeIPO = year(dofm(time_avail_m)) - FoundingYear
replace AgeIPO = . if tempipo == 0 // only sort recent IPO firms

egen tempTotal = total(tempipo), by(time_avail_m)  // Number of IPO = 1 firms per month
replace AgeIPO = . if tempTotal < 20*5

label var AgeIPO "IPO and Age"

// SAVE
do "$pathCode/savepredictor" AgeIPO