* -------------
* An Ang Bali Cakici 2014 Table II A


// Clean OptionMetrics data 
use "$pathDataIntermediate/OptionMetricsVolSurf", clear

* screen (page 2283)
keep if days == 30 & abs(delta) == 50 

* create signal (page 2285)
keep if cp_flag == "C"
xtset secid time_avail_m
gen dVolCall = impl_vol- l1.impl_vol

keep secid time_avail_m dVolCall
save "$pathtemp/temp", replace

// Merge onto master table
use permno time_avail_m secid using "$pathDataIntermediate/SignalMasterTable", clear
merge m:1 secid time_avail_m using "$pathtemp/temp", keep(master match) nogenerate

keep if dVolCall != .

label var dVolCall "Change in Call Implied Vol"

// SAVE
do "$pathCode/savepredictor" dVolCall
