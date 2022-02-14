* 27. Probability of informed trading ------------------------------------------

local webloc "https://sites.google.com/site/hvidkjaer/data/data-files/pin1983-2001.zip"
capture {
	copy "`webloc'" temp.zip
    unzipfile temp.zip
	import delimited pin1983-2001.dat, clear varnames(1) delimiter(whitespace, collapse)
	erase temp.zip
}

if _rc!= 0 {
	shell wget "`webloc'" -O $pathDataIntermediate/deleteme.zip
    unzipfile $pathDataIntermediate/deleteme.zip
	import delimited "$pathDataIntermediate/pin1983-2001.dat", delimiter(whitespace, collapse) clear
	shell rm $pathDataIntermediate/deleteme.zip -f
}

rename permn permno
replace year = year +1  // To trade on information from previous year

compress
save "$pathDataIntermediate/aInformedTrading", replace
