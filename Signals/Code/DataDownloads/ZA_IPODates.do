* 26. Ritter's IPO dates ---------------------------------------
local webloc "https://site.warrington.ufl.edu/ritter/files/2019/05/age19752019.xlsx"
capture {
	import excel `webloc', clear firstrow
}
if _rc!= 0 {
	shell wget `webloc' -O $pathDataIntermediate/deleteme.xlsx
	import excel "$pathDataIntermediate/deleteme.xlsx", clear firstrow
}


rename Founding FoundingYear
rename CRSPperm permno
destring permno, replace

tostring Offerdate, replace
gen temp = date(Offerdate, "YMD")
gen IPOdate = mofd(temp)
format IPOdate %tm

keep permno FoundingYear IPOdate
drop if mi(permno) | permno == 999 | permno <= 0
bys permno: keep if _n == 1
replace FoundingYear = . if FoundingYear < 0

save "$pathDataIntermediate/IPODates", replace
