* SAS 4. Bid-ask TAQ data ------------------------------------------------------

* See zip code in our repo to see how to construct the csv file, run on the WRDS server, then run code below!

import delimited using "$pathDataPrep/tcosts_CV_20191203.csv", clear
tostring month, replace
gen y = substr(month, 1, 4)
gen m = substr(month, 5, 2)
destring y m, replace
gen time_avail_m = ym(y, m)
format time_avail_m %tm

keep permno time_avail_m tcost 
compress
save "$pathDataIntermediate/tcost_TAQ", replace
