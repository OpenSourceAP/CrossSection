* 27. Probability of informed trading ------------------------------------------

* These data are originally from here: https://sites.google.com/site/hvidkjaer/data
* import delimited using "https://drive.google.com/uc?export=download&id=15RU_gxWS0rZ8Jyq7MFAno3cLKbB1_P0T", delimiter(whitespace, collapse) clear

local webloc "https://drive.google.com/uc?export=download&id=15RU_gxWS0rZ8Jyq7MFAno3cLKbB1_P0T"
capture {
	import delimited "`webloc'", clear varnames(1) delimiter(whitespace, collapse)
}

if _rc!= 0 {
	shell wget "`webloc'" -O $pathDataIntermediate/deleteme.dat
	import delimited "$pathDataIntermediate/deleteme.dat", delimiter(whitespace, collapse) clear
	shell rm $pathDataIntermediate/deleteme.csv -f
}

rename permn permno
replace year = year +1  // To trade on information from previous year

compress
save "$pathDataIntermediate/aInformedTrading", replace
