
* ------------------------------------------------------------------------------
cap log close
log using "$pathLogs/02_CreatePredictors.log", replace

* ------------------------------------------------------------------------------
* Log file for signal creation
clear
gen SignalFile = ""
gen double SignalTime = .
gen lastRun = ""
gen ReturnCode = .
save "$pathLogs/02_CreatePredictorsFlags", replace

* ------------------------------------------------------------------------------
* Create Signal Master Table with some meta data
do "$pathCode/SignalMasterTable.do"

* ------------------------------------------------------------------------------
* Look-up signal scripts 
filelist, pat("*.do") nor directory("$pathCodePredictors")
gen filenameLower = strlower(filename)
sort filenameLower
save "$pathLogs/tempFilenames", replace

* ------------------------------------------------------------------------------
* Loop over all signal scripts

local obs = _N
forvalues i=1/`obs' {
	*forvalues i=1/10 {
    
	use "$pathLogs/tempFilenames" in `i', clear
    local file = filename
	
    di "`file'"

    timer clear 1
    timer on 1 

	capture noisily do "$pathCodePredictors/`file'"
	
	timer off 1
	
	clear
	set obs 1
	timer list
	gen SignalFile = "`file'"
	gen SignalTime = r(t1)
	gen lastRun = "$S_DATE $S_TIME"
	gen ReturnCode = _rc
	
	append using "$pathLogs/02_CreatePredictorsFlags"
	save "$pathLogs/02_CreatePredictorsFlags", replace
	export delimited using "$pathLogs/02_CreatePredictorsFlags.csv", replace 
	
}

di("The following signal scripts did not complete successfully")
li if ReturnCode !=0

*******************************************
erase "$pathLogs/tempFilenames.dta"

log close 
