* Chen-Velikov effective spreads ----------------------------------------
* replaced Corwin Schultz spreads 2022 02

* it's tricky to download large files from gdrive.  best to use a package
* but on the fed linux system, i use this workaround (thouliha's answer)
* https://stackoverflow.com/questions/25010369/wget-curl-large-file-from-google-drive

* Raw gdrive link from Chen's webpage
* https://drive.google.com/file/d/1emGygbWj6Y-X1e6MUwuSIGUG4lUWwOAI/view?usp=sharing

* === DOWNLOAD LOW FREQUENCY SPREADS ===
if "`c(os)'" == "Unix"{
	* set up folder to download to
	shell cd "$pathDataIntermediate"; mkdir "deleteme"
	shell cd "$pathDataIntermediate/deleteme"; rm * -f

	* download awkwardly to avoid redirect for large files
	shell cd "$pathDataIntermediate/deleteme"; wget --no-check-certificate "https://docs.google.com/uc?export=download&id=1emGygbWj6Y-X1e6MUwuSIGUG4lUWwOAI" -r -A 'uc*' -e robots=off -nd
	shell cd "$pathDataIntermediate/deleteme"; find . -name "*" -type 'f' -size -160k -delete

	* unzip to pathDataIntermediate, clean up
	shell cd "$pathDataIntermediate/deleteme"; unzip * -d ../
	shell cd "$pathDataIntermediate/deleteme"; rm * -f	
	
} 
else {
	
	* tbc
}

import delimited "$pathDataIntermediate/low_frequency_average_tcosts.csv", clear varnames(1)

* === FILL WITH 


* old code below 	 ====================
* local webloc "https://drive.google.com/uc?export=download&id=1U0xQw9CwKJAVZYHbur8p_jj24vLtVwBu"

capture {
	import excel "`webloc'", clear firstrow
}
if _rc!= 0 {
	shell wget "`webloc'" -O $pathDataIntermediate/deleteme.zip
	unzipfile "$pathDataIntermediate/deleteme.zip"
}



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
