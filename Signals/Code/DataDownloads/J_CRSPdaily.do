* 10. CRSP daily ----------------------------------------------------------------
// clean up temp dta
local cdir "`c(pwd)'"
cd $pathtemp
local list : dir . files "tempcrspd*.dta"
foreach f of local list {
	display "erasing `f'"
	erase "`f'"
}
cd `cdir'

// Download, loop over years and ave to disk to avoid crashing program 
// (in case of memory limits)
forvalues y=1926/2200{
	display "`y'"
	#delimit ;
	local sql_statement
		SELECT a.permno, a.date, a.ret, a.vol, a.shrout, a.prc, a.cfacshr, a.cfacpr
		FROM crsp.dsf as a
		WHERE date >= '`y'-01-01' and date <= '`y'-12-31'
		;
	#delimit cr	
	odbc load, exec("`sql_statement'") dsn($wrdsConnection) clear	
	
	if _N >= 1 {
		save "$pathtemp/tempcrspd`y'"
	}
	
	sleep 1000 // to try to avoid login errors
}

// Append first stuff used for betas and liquiidty
local cdir "`c(pwd)'"
cd $pathtemp
local files : dir "" files "tempcrsp*.dta"
display `files'
clear
foreach file in `files' {
	display "appending `file'"
	append using `file', keep(permno date ret vol prc cfacpr shrout)
}
cd `cdir'

// Save file
rename date time_d 
compress
save "$pathDataIntermediate/dailyCRSP.dta", replace

	
// Append stuff used for High 52, Zero trade
local cdir "`c(pwd)'"
cd $pathtemp
local files : dir "" files "tempcrsp*.dta"
display `files'
clear
foreach file in `files' {
	display "appending `file'"
	append using `file', keep(permno date prc cfacpr shrout)
}
cd `cdir'

// Save file
rename date time_d 
compress
save "$pathDataIntermediate/dailyCRSPprc.dta", replace


	
// clean up temp dta
local cdir "`c(pwd)'"
cd $pathtemp
local list : dir . files "tempcrspd*.dta"
foreach f of local list {
	display "erasing `f'"
	erase "`f'"
}
cd `cdir'
	
	
