* 26. Ritter's IPO dates ---------------------------------------

*local webloc "https://site.warrington.ufl.edu/ritter/files/2019/05/age19752019.xlsx" * pre 2021 01 location
*local webloc "https://site.warrington.ufl.edu/ritter/files/age7520.xlsx" // 2021 01-2021 02 location
local webloc "https://site.warrington.ufl.edu/ritter/files/IPO-age.xlsx"  // 2022-02-09 location


capture {
	import excel `webloc', clear firstrow
}
if _rc!= 0 {
	shell wget "`webloc'" -O $pathDataIntermediate/deleteme.xlsx
	import excel "$pathDataIntermediate/deleteme.xlsx", clear firstrow
}

rename Founding FoundingYear
*rename Offerdate OfferDate	// variable OfferDate changed to Offerdate
rename offerdate OfferDate	// variable OfferDate changed to offerdate in 2024 version

*rename CRSPpermanentID permno
rename CRSPperm permno  // var name change in 2024 version
destring permno, replace

tostring OfferDate, gen(temp)
gen temp2 = date(temp, "YMD")
gen IPOdate = mofd(temp2)
format IPOdate %tm

keep permno FoundingYear IPOdate
drop if mi(permno) | permno == 999 | permno <= 0
bys permno: keep if _n == 1
replace FoundingYear = . if FoundingYear < 0

save "$pathDataIntermediate/IPODates", replace
