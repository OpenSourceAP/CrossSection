* --------------
// DATA LOAD
use permno time_avail_m ticker prc shrcd using "$pathDataIntermediate/SignalMasterTable", clear
merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keep(master match) nogenerate keepusing(vol)
* Add ticker-based data (many to one match due to permno-ticker not being unique in crsp)
preserve

keep if mi(ticker)

save "$pathtemp/temp", replace
restore
drop if mi(ticker)
merge m:1 ticker time_avail_m using "$pathDataIntermediate/OptionMetrics", keep(master match) nogenerate keepusing(optvolume)
append using "$pathtemp/temp"
// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen OptionVolume1 = optvolume/vol
replace OptionVolume1 = . if abs(prc) < 1 | shrcd > 11 | mi(l1.optvolume) | mi(l1.vol)
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