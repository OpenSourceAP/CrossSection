* R 1. OptionMetrics data ------------------------------------------------------

* Run R1_OptionMetrics.R first!

import delimited "$pathDataPrep/OptionMetrics.csv", clear varnames(1)
drop if mi(ticker)
gen time_d = date(time_avail_m,"YMD")
drop time_avail_m
gen time_avail_m = mofd(time_d)
format time_avail_m %tm

compress
bys ticker time_a (optvolume): keep if _n == _N // if more than one observation per month, keep one with highest volume

drop secid time_d cusip
order ticker time_a
save "$pathDataIntermediate/OptionMetrics", replace
