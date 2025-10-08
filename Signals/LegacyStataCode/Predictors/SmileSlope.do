* --------------
* Yan 2011 JFE

// Data Prep
use "$pathDataIntermediate/OptionMetricsVolSurf", clear

* bottom right page 221
keep if days == 30 & abs(delta) == 50

* make signal
keep secid time_avail_m cp_flag impl_vol 
reshape wide impl_vol, i(secid time_avail_m) j(cp_flag) string
gen SmileSlope = impl_volP - impl_volC

save "$pathtemp/temp", replace

// Merge onto master table
use permno time_avail_m secid using "$pathDataIntermediate/SignalMasterTable", clear
merge m:1 secid time_avail_m using "$pathtemp/temp", keep(master match) nogenerate

keep if SmileSlope != .

label var SmileSlope "Average Jump Size"

// SAVE
do "$pathCode/savepredictor" SmileSlope
