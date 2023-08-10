* -------------
* An Ang Bali Cakici 2014 Table II C
* I guess the paper actually has dPCVolSpread, but that doesn't 
* sound as nice to my ear, and doesn't sync with our CPVolSpread
* name for the other Bali Hovak predictor

// Clean OptionMetrics data 
use "$pathDataIntermediate/OptionMetricsVolSurf", clear

* screen (page 2283)
keep if days == 30 & abs(delta) == 50 

* create signal (page 2290)
keep secid time_avail_m cp_flag impl_vol
reshape wide impl_vol, i(secid time_avail_m) j(cp_flag) string

xtset secid time_avail_m
gen dVolCall = impl_volC- l1.impl_volC
gen dVolPut  = impl_volP - l1.impl_volP
gen dCPVolSpread = dVolPut - dVolCall 

keep secid time_avail_m dCPVolSpread
save "$pathtemp/temp", replace

// Merge onto master table
use permno time_avail_m secid using "$pathDataIntermediate/SignalMasterTable", clear
merge m:1 secid time_avail_m using "$pathtemp/temp", keep(master match) nogenerate

keep if dCPVolSpread != .

label var dCPVolSpread "Change in Call-Put Vol Spread"

// SAVE
do "$pathCode/savepredictor" dCPVolSpread
