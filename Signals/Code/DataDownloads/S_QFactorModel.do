* 19. Q Factor Model ------------------------------------------------------------

local webloc http://global-q.org/uploads/1/2/2/6/122679606/q5_factors_daily_2019.csv
capture {
	import delimited `webloc', clear varnames(1)
}
if _rc!= 0 {
	shell wget `webloc' -O $pathDataIntermediate/deleteme.csv
	import delimited "$pathDataIntermediate/deleteme.csv", clear varnames(1)
	shell rm $pathDataIntermediate/deleteme.csv -f
}

drop r_eg

rename r_* r_*_qfac
tostring date, replace
gen time_d = date(date, "YMD")
format time_d %td
drop date

foreach v of varlist r_* {
	replace `v' = `v'/100
}

save "$pathDataIntermediate/d_qfactor", replace
