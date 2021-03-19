* SAS 2. 13F data --------------------------------------------------------------

* Run tr13f_download.sas first!

import delimited "$pathDataPrep/tr_13f.csv", clear varnames(1)
drop if mi(permno)
destring instown_perc maxinstown_perc numinstown, replace force

gen time_d = date(rdate,"DMY")
gen time_avail_m = mofd(time_d) // + 1  // WHAT'S THE REPORTING LAG FOR THESE DATA? WHAT WAS IT IN THE 80S?
format time_avail_m %tm
drop rdate time_d

* Fill in missing months
xtset permno time_avail_m
tsfill
sort permno time_avail_m
foreach v of varlist numinstown instown_perc dbreadth maxinstown_perc numinstown numinstblock {
	replace `v' = `v'[_n-1] if permno == permno[_n-1] & mi(`v') 
}

compress
save "$pathDataIntermediate/TR_13F", replace
