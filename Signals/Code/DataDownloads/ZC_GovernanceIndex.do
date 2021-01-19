* 28. Governance index ---------------------------------------------------------
local webloc "https://spinup-000d1a-wp-offload-media.s3.amazonaws.com/faculty/wp-content/uploads/sites/7/2019/06/Governance.xlsx"

capture {
	import excel "`webloc'", ///
    sheet("governance index") cellrange(A24:F14024) clear firstrow
}
if _rc!= 0 {
	shell wget `webloc' -O $pathDataIntermediate/deleteme.xlsx
	import excel "$pathDataIntermediate/deleteme.xlsx", ///
    sheet("governance index") cellrange(A24:F14024) clear firstrow
}

replace ticker = strtrim(ticker)
bys ticker year: keep if _n == 1
replace year = 1999 if year == 2000

gen month = .
replace month = 9 if year == 1990
replace month = 7 if year == 1993
replace month = 7 if year == 1995
replace month = 2 if year == 1998
replace month = 11 if year == 1999
replace month = 1 if year >= 2002

gen time_avail_m = ym(year, month)
format time_avail_m %tm

* Interpolate missing dates, extend one year beyond end of data
bysort ticker (time_avail_m): gen byte last = _n == _N 
expand 2 if last 
bysort ticker (time_avail_m): replace time_avail_m = ym(2007,1) if _n == _N
keep ticker time_avail_m G

egen tempID = group(ticker)
xtset tempID time_avail_m
tsfill

foreach v of varlist ticker G {
	bys tempID (time_avail_m): replace `v' = `v'[_n-1] if _n > 1 & mi(`v')
}

drop tempID
compress
save "$pathDataIntermediate/GovIndex", replace
