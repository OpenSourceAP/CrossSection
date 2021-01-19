* SAS 1. Corwin-Schultz bid-ask spread  ----------------------------------------

* Run Corwin_Schultz_Edit.sas first!

import delimited "$pathDataPrep/corwin_schultz_spread.csv", clear varnames(1)
tostring month, replace
gen y = substr(month, 1,4)
gen m = substr(month, 5,2)
destring y m, replace
gen time_avail_m = ym(y, m)
format time_avail_m %tm
drop y m month

drop if mi(permno)
rename hlspread BidAskSpread  // MP divides by price but hlspread already divides by price (in both Corwin's xlsx and sas code)

compress
save "$pathDataIntermediate/BAspreadsCorwin", replace
