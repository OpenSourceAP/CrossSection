* OptionMetrics data ------------------------------------------------------

* Run PrepScripts/master.sh first!

* For skew, slope, op_volume
import delimited "$pathDataPrep/OptionMetrics.csv", clear varnames(1)
gen time_d = date(time_avail_m,"YMD")
drop time_avail_m
gen time_avail_m = mofd(time_d)
format time_avail_m %tm

compress
bys secid time_avail_m (optvolume): keep if _n == _N // if more than one observation per month, keep one with highest volume

drop time_d cusip
order secid time_avail_m
save "$pathDataIntermediate/OptionMetrics", replace


* For Bali-Hovakimiam (2009) implied vol  (near the money)
import delimited "$pathDataPrep/bali_hovak_imp_vol.csv", clear varnames(1)
gen time_d = date(date,"YMD")
drop date
gen time_avail_m = mofd(time_d)
format time_avail_m %tm
drop time_d

drop if mi(secid)

compress
order secid time_avail_m
save "$pathDataIntermediate/OptionMetricsBH", replace
