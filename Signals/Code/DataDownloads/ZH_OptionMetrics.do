* OptionMetrics data ------------------------------------------------------

* Run PrepScripts/master.sh first!

* first option volume
import delimited "$pathDataPrep/OptionMetricsVolume.csv", clear varnames(1)
gen time_d = date(time_avail_m,"YMD")
drop time_avail_m
gen time_avail_m = mofd(time_d)
format time_avail_m %tm
drop time_d

compress
save "$pathDataIntermediate/OptionMetricsVolume", replace


* then vol surface
import delimited "$pathDataPrep/OptionMetricsVolSurf.csv", clear varnames(1)
gen time_d = date(time_avail_m,"YMD")
drop time_avail_m
gen time_avail_m = mofd(time_d)
format time_avail_m %tm
drop time_d

order secid days delta cp_flag time_avail_m
save "$pathDataIntermediate/OptionMetricsVolSurf", replace

* then Xing Zhang Zhao 2010 
import delimited "$pathDataPrep/OptionMetricsXZZ.csv", clear varnames(1)
gen time_d = date(time_avail_m,"YMD")
drop time_avail_m
gen time_avail_m = mofd(time_d)
format time_avail_m %tm
drop time_d

compress
order secid time_avail_m
save "$pathDataIntermediate/OptionMetricsXZZ", replace

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
