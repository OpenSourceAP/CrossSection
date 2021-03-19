* saves signal in a standardized way
* 2020 12 23

display "saving `1'"

preserve

	// clean up
	drop if `1' == .

	// save dta, optional
	if $save_dta {
		keep permno time_avail_m `1'
		order permno time_avail_m `1'
		compress
		save "$pathDataPredictors/`1'", replace
	}

	// save csv, main output, need to change date from stata format
	if $save_csv{
		gen yyyymm = year(dofm(time_avail_m))*100 + month(dofm(time_avail_m))
		keep permno yyyymm `1'
		order permno yyyymm `1'
		export delimited "$pathDataPredictors/`1'.csv", replace  
	}	

restore

// clean up temp dta
local list : dir "$pathtemp" files "temp*.dta"
foreach f of local list {
	erase "$pathtemp/`f'"
}
