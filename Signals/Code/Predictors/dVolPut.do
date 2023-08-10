* -------------
* An Ang Bali Cakici 2014 Table II B


// Clean OptionMetrics data 
use "$pathDataIntermediate/OptionMetricsVolSurf", clear

* screen (page 2283)
keep if days == 30 & abs(delta) == 50 

* create signal (page 2285)
keep if cp_flag == "P"
xtset secid time_avail_m
gen dVolPut = impl_vol- l1.impl_vol

keep secid time_avail_m dVolPut
save "$pathtemp/temp", replace

// Merge onto master table
use permno time_avail_m secid using "$pathDataIntermediate/SignalMasterTable", clear
merge m:1 secid time_avail_m using "$pathtemp/temp", keep(master match) nogenerate

keep if dVolPut != .

label var dVolPut "Change in Put Implied Vol"

// SAVE
do "$pathCode/savepredictor" dVolPut
