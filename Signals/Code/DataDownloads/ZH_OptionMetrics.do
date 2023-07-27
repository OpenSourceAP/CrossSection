* R 1. OptionMetrics data ------------------------------------------------------

* Run R1_OptionMetrics.R first!

* For Bali-Hovakimiam (2009) data
import delimited "$pathDataPrep/bali_hovak_cp.csv", clear varnames(1)
gen time_d = date(date,"YMD")
drop date
drop if mi(secid)
gen time_avail_m = mofd(time_d)
format time_avail_m %tm

drop time_d

compress
order secid time_avail_m
save "$pathDataIntermediate/BH_cp", replace


import delimited "$pathDataPrep/bali_hovak_ri.csv", clear varnames(1)
gen time_d = date(date,"YMD")
drop date
drop if mi(secid)
gen time_avail_m = mofd(time_d)
format time_avail_m %tm

drop time_d

compress
order secid time_avail_m
save "$pathDataIntermediate/BH_ri", replace



* For all other option metrics data (skew, slope, up_volume)
import delimited "$pathDataPrep/OptionMetrics.csv", clear varnames(1)
drop if mi(ticker)
gen time_d = date(time_avail_m,"YMD")
drop time_avail_m
gen time_avail_m = mofd(time_d)
format time_avail_m %tm

compress
bys secid time_a (optvolume): keep if _n == _N // if more than one observation per month, keep one with highest volume


* Merge bali_hovak and option metrics data
merge m:m secid time_avail_m using "/cm/chen/openap/release_2023/CrossSection-master/Signals/Data/Intermediate/BH.dta"

drop time_d cusip _merge
order secid time_a

save "$pathDataIntermediate/OptionMetrics", replace

