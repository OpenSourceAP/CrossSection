* 25. Original sin stock classifications ---------------------------------------

* This is an Excel file made from the pdf list here: http://www.columbia.edu/~hh2679/sinstocks.pdf
local webloc "https://drive.google.com/uc?export=download&id=1U0xQw9CwKJAVZYHbur8p_jj24vLtVwBu"

capture {
	import excel "`webloc'", clear firstrow
}
if _rc!= 0 {
	shell wget "`webloc'" -O $pathDataIntermediate/deleteme.xlsx
	import excel "$pathDataIntermediate/deleteme.xlsx", clear firstrow
}

	
replace begy = E if mi(begy)
replace endy = G if mi(endy)
keep permno begy endy

save "$pathDataIntermediate/SinStocksHong", replace

