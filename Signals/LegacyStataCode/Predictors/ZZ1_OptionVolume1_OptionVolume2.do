* --------------
* Johnson and So 2012 JFE
// DATA LOAD
use permno time_avail_m secid prc shrcd using "$pathDataIntermediate/SignalMasterTable", clear

* add stock volume
merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keep(master match) nogenerate keepusing(vol)

preserve

keep if mi(secid)

save "$pathtemp/temp", replace
restore
drop if mi(secid)

* add option volume

merge m:1 secid time_avail_m using "$pathDataIntermediate/OptionMetricsVolume", keep(master match) nogenerate keepusing(optvolume)
append using "$pathtemp/temp"

// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen OptionVolume1 = optvolume/vol
replace OptionVolume1 = . if mi(l1.optvolume) | mi(l1.vol)
foreach n of numlist 1/6 {

gen tempVol`n' = l`n'.OptionVolume1

}
egen tempMean = rowmean(tempVol*)
gen OptionVolume2 = OptionVolume1/tempMean
label var OptionVolume1 "Option Volume"
label var OptionVolume2 "Option Volume (abnormal)"

// SAVE 
do "$pathCode/savepredictor" OptionVolume1
do "$pathCode/savepredictor" OptionVolume2
