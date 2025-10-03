* SAS 4. Bid-ask TAQ data ------------------------------------------------------

* created via Signals/Code/Prep/master.sh as of 2022 02
* uses Chen-Velikov JFQA Forthcoming code
* also includes ISSM spreads


import delimited using "$pathDataPrep/hf_monthly.csv", clear
tostring yearm, replace
gen y = substr(yearm, 1, 4)
gen m = substr(yearm, 5, 2)
destring y m, replace
gen time_avail_m = ym(y, m)
format time_avail_m %tm

gen hf_spread = espread_pct_mean

keep permno time_avail_m hf_spread
compress
save "$pathDataIntermediate/hf_spread", replace
