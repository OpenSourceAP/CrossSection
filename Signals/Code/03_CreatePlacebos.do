
* ------------------------------------------------------------------------------
cap log close
log using "$pathLogs/03_CreatePlacebos.log", replace

* ------------------------------------------------------------------------------
* Log file for signal creation
clear
gen SignalFile = ""
gen double SignalTime = .
gen lastRun = ""
gen ReturnCode = .
save "$pathLogs/03_CreatePlacebosFlags", replace

* ------------------------------------------------------------------------------
* Look-up signal scripts 
filelist, pat("*.do") nor directory("$pathCodePlacebos")
gen filenameLower = strlower(filename)
sort filenameLower
save "$pathLogs/tempFilenamesPlacebo", replace

* ------------------------------------------------------------------------------
* Loop over all signal scripts

local obs = _N
forvalues i=1/`obs' {
	*forvalues i=1/10 {
    
	use "$pathLogs/tempFilenamesPlacebo" in `i', clear
    local file = filename
	
    di "`file'"

    timer clear 1
    timer on 1 

	capture noisily do "$pathCodePlacebos/`file'"
	
	timer off 1
	
	clear
	set obs 1
	timer list
	gen SignalFile = "`file'"
	gen SignalTime = r(t1)
	gen lastRun = "$S_DATE $S_TIME"
	gen ReturnCode = _rc
	
	append using "$pathLogs/03_CreatePlacebosFlags"
	save "$pathLogs/03_CreatePlacebosFlags", replace
	export delimited using "$pathLogs/03_CreatePlacebosFlags.csv", replace 
	
}

di("The following signal scripts did not complete successfully")
li if ReturnCode !=0

*********************************
erase "$pathLogs/tempFilenamesPlacebo.dta"

log close 
