*! version 1.0.3, Ben Jann, 26jan2005
program define relrank, byable(onecall) sort
	version 8.2
	syntax varname(numeric) [if] [in] [fw aw] , Reference(str) Generate(name) [ cdf(varname) ]
	marksample touse
	confirm new var `generate'
	gettoken refvar refif: reference
	if _by() local by "by `_byvars':"
	if "`cdf'"=="" {
		`by' cumul `refvar' `refif' [`weight'`exp'] , generate(`generate') equal
	}
	else {
		capt assert inrange(`cdf',0,1) | ( `cdf'>=. & `refvar'>=. ) `refif'
		if _rc {
			di as error "`cdf' not in [0,1] or has missing values"
			exit 459
		}
		qui gen `: type `cdf'' `generate' = `cdf' `refif'
		qui replace `generate' = . if `refvar'>=.
	}
	quietly {
		nobreak {
			expand 2 if `generate'<. & `touse'
			tempvar id x
			sort `_sortindex'
			by `_sortindex': gen byte `id' = _n
			replace `touse' = 0 if `id'==2
			replace `generate' = . if `touse'
			gen `: type `varlist'' `x' = `varlist' if `touse'
			replace `x' = `refvar' if `generate'<. & !`touse'
			sort `_byvars' `x' `touse'
			`by' replace `generate' = 0 if _n==1 & `touse'
			`by' replace `generate' = `generate'[_n-1] if _n>1 & `touse'
			replace `generate' = . if !`touse'
			drop if `id'==2
		}
	}
end
