* --------------
// DATA LOAD
* Prepare crosswalk
use gvkey permno timeLink* using "$pathDataIntermediate/CCMLinkingTable", clear
destring gvkey, replace
save "$pathtemp/tempCW", replace
* Prepare returns
use "$pathDataIntermediate/monthlyCRSP", clear
keep permno time_avail_m ret
save "$pathtemp/tempCRSP", replace
* Annual sales from CS
use gvkey permno sale fyear using "$pathDataIntermediate/a_aCompustat", clear
rename sale saleACS
drop if saleACS <0 | mi(saleACS)
save "$pathtemp/tempCS", replace
* Conglomerates from CS segment data
u gvkey datadate stype sics1 sales using "$pathDataIntermediate/CompustatSegments", clear
keep if stype == "OPSEG" | stype == "BUSSEG"
drop if sales < 0 | mi(sales)
tostring sics1, replace
gen sic2D = substr(sics1, 1,2)
gcollapse (sum) sales, by(gvkey sic2D datadate)
gen fyear = yofd(datadate)
merge m:1 gvkey fyear using "$pathtemp/tempCS", keep(match) nogenerate
egen temptotalSales = total(sales), by(gvkey fyear)
gen tempCSSegmentShare = sales/saleACS
bys gvkey datadate: gen tempNInd = _N
tab tempNInd
gen Conglomerate = 0 if tempNInd == 1 & tempCSSegmentShare > .8
replace Conglomerate = 1 if tempNInd > 1 & tempCSSegmentShare > .8
drop if mi(Conglomerate)
tab Conglomerate
save tempConglomerate, replace
* Industry returns from stand-alones
keep if Conglomerate == 0
// Add identifiers for merging with stock returns
joinby gvkey using "$pathtemp/tempCW", update
* Use only if data date is within the validity period of the link
gen temp = (timeLinkStart_d <= datadate  & datadate <= timeLinkEnd_d)
tab temp
keep if temp == 1
drop temp
* Merge stock returns
keep permno sic2D fyear
duplicates drop
rename sic2D sic2DCSS
joinby permno using "$pathtemp/tempCRSP", unmatched(none)
gen year = yofd(dofm(time_avail_m))
keep if fyear == year
gcollapse (mean) ret, by(sic2DCSS time_avail_m)
drop if sic2DCSS == "."
save "$pathtemp/tempReturns", replace
// SIGNAL CONSTRUCTION
* Now, match industry returns of stand-alones to conglomerates
use tempConglomerate, clear
keep if Conglomerate == 1
keep permno sic2D sales fyear
rename sic2D sic2DCSS
drop if sic2DCSS == "."
joinby sic2DCSS using "$pathtemp/tempReturns", unmatched(none)
gen year = yofd(dofm(time_avail_m))
keep if fyear == year
* Now take weighted return
egen tempTotal = total(sales), by(permno time_avail_m)
gen tempweight = sales/tempTotal
*ALL WEIGHTS ALMOST 1. WHERE ARE THE CONGLOMERATES?
gcollapse (mean) ret [iweight = tempweight], by(permno time_avail_m)
rename ret retConglomerate
label var retConglomerate "Conglomerate return"

// SAVE
do "$pathCode/savepredictor" retConglomerate