* Prepare anomalies from multiple files

* 1. Business segment returns of conglomerates
* 2. Stock return around earnings announcements
* 3. Broker-Dealer leverage beta based on quarterly returns
*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* 1. Business segment returns of conglomerates
import delimited "$pathProject/DataRaw/CompustatAnnual.csv", clear  // Need sales data
* Require some reasonable amount of information
drop if at ==. | ni ==.
keep gvkey sale fyear
bys gvkey fyear: keep if _n == 1
rename sale saleACS
drop if saleACS <0 | mi(saleACS)
save tempCS, replace

* 
use "$pathProject/DataClean/m_CRSP", clear
keep permno time_avail_m ret
save tempCRSP, replace

*
import delimited "$pathProject/DataRaw/CompustatSegmentData.csv", clear varnames(1)
keep if stype == "OPSEG" | stype == "BUSSEG"

gen time_d = date(datadate, "YMD")
format time_d %td
drop if sales < 0 | mi(sales)
tostring sics1, replace
gen sic2D = substr(sics1, 1,2)
collapse (sum) sales, by(gvkey sic2D time_d)

gen fyear = yofd(time_d)
merge m:1 gvkey fyear using tempCS, keep(match) nogenerate

egen temptotalSales = total(sales), by(gvkey fyear)
gen tempCSSegmentShare = sales/saleACS

bys gvkey time_d: gen tempNInd = _N
tab tempNInd

gen Conglomerate = 0 if tempNInd == 1 & tempCSSegmentShare > .8
replace Conglomerate = 1 if tempNInd > 1 & tempCSSegmentShare > .8
drop if mi(Conglomerate)
tab Conglomerate
save tempConglomerate, replace

* Prepare industry returns of stand-alones
keep if Conglomerate == 0
// Add identifiers for merging with stock returns
joinby gvkey using "$pathProject/DataClean/CCMLinkingTable", update

* Use only if data date is within the validity period of the link
gen temp = (timeLinkStart_d <= time_d  & time_d <= timeLinkEnd_d)
tab temp
keep if temp == 1
drop temp

* Merge stock returns
keep lpermno sic2D fyear
duplicates drop
rename lpermno permno
rename sic2D sic2DCSS
*bysort permno time_avail_m: keep if _n == 1  // deletes 64 observations
joinby permno using tempCRSP, unmatched(none)

gen year = yofd(dofm(time_avail_m))
keep if fyear == year

collapse (mean) ret, by(sic2DCSS time_avail_m)
drop if sic2DCSS == "."

save tempReturns, replace

* Now, match industry returns of stand-alones to conglomerates
use tempConglomerate, clear
keep if Conglomerate == 1

keep gvkey time_d sic2D sales fyear
rename sic2D sic2DCSS
drop if sic2DCSS == "."
joinby sic2DCSS using tempReturns, unmatched(none)

gen year = yofd(dofm(time_avail_m))
keep if fyear == year

* Now take weighted return
egen tempTotal = total(sales), by(time_avail_m gvkey)
gen tempweight = sales/tempTotal

*ALL WEIGHTS ALMOST 1. WHERE ARE THE CONGLOMERATES?
collapse (mean) ret [iweight = tempweight], by(gvkey time_avail_m)
rename ret retConglomerate
save "$pathProject/DataClean/ConglomerateReturns", replace


*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* 2. Returns around earnings announcements

* Prepare crosswalk CRSP-CS
use "$pathProject/DataClean/CCMLinkingTable", clear
keep gvkey lpermno timeLink*
rename lpermno permno
save tempCW, replace

* Earnings announcement dates from Compustat Quarterly
import delimited "$pathProject/DataRaw/CompustatQuarterly.csv", clear
keep gvkey rdq
gen time_ann_d = date(rdq, "YMD")
format time_ann_d %td
keep gvkey time_ann_d
drop if mi(time_ann_d)
duplicates drop

save tempAnnDats, replace

*
import delimited "$pathProject/DataRaw/d_CRSP.csv", clear
gen time_d = date(date, "YMD")
format time_d %td
drop date vol shrout prc cfacshr

* Match announcement dates
// Add identifiers for merging
joinby permno using tempCW

* Use only if data date is within the validity period of the link
gen temp = (timeLinkStart_d <= time_d  & time_d <= timeLinkEnd_d)
tab temp
keep if temp == 1
drop temp timeLink*

rename time_d time_ann_d
merge m:1 gvkey time_ann_d using tempAnnDats
gen anndat = (_merge == 3)
drop if _merge ==2
drop _merge gvkey

* Merge market return
rename time_ann_d time_d
merge m:1 time_d using "$pathProject/DataClean/dFF", nogenerate keep(match) keepusing(mktrf rf)

* Compute returns around earnings announcement
gen AnnouncementReturn = ret - (mktrf + rf)
bys permno (time_d): gen time_temp = _n  // To deal with weekends
xtset permno time_temp

gen time_ann_d = time_temp if anndat == 1 
replace time_ann_d = time_temp + 1 if f1.anndat == 1
replace time_ann_d = time_temp + 2 if f2.anndat == 1
replace time_ann_d = time_temp - 1 if l1.anndat == 1

gen AnnTime = time_d if anndat == 1 
drop if mi(time_ann_d)

gcollapse (sum) AnnouncementReturn (firstnm) AnnTime, by(permno time_ann_d) 
gen time_avail_m = mofd(AnnTime)
format time_avail_m %tm

* Fill in months with no earnings announcements with most recent announcement return at most six months ago
keep permno time_avail_m AnnouncementReturn
drop if mi(time_avail_m)
bys permno time_a: keep if _n == _N
compress

xtset permno time_avail
tsfill
sort permno time_avail_m
gen temp = AnnouncementReturn  // Necesssary because Stata fills sequentially

by permno: replace AnnouncementReturn = temp[_n-1] if mi(AnnouncementReturn)
by permno: replace AnnouncementReturn = temp[_n-2] if mi(AnnouncementReturn)
by permno: replace AnnouncementReturn = temp[_n-3] if mi(AnnouncementReturn)
by permno: replace AnnouncementReturn = temp[_n-4] if mi(AnnouncementReturn)
by permno: replace AnnouncementReturn = temp[_n-5] if mi(AnnouncementReturn)
by permno: replace AnnouncementReturn = temp[_n-6] if mi(AnnouncementReturn)

drop if mi(AnnouncementReturn)
drop temp

* SAVE
save "$pathProject/DataClean/AnnouncementReturns", replace

*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* 3. Broker-Dealer leverage beta based on quarterly returns

use "$pathProject/DataClean/m_CRSP", clear

* Collapse to quarterly returns
gen year = year(dofm(time_avail_m))
gen qtr = quarter(dofm(time_avail_m))

replace ret = 0 if mi(ret)

bys permno year qtr (time_avail_m): gen RetQ = (1+ret)*(1+ret[_n+1])*(1+ret[_n+2]) - 1 if _n == 1
keep if !mi(RetQ)

keep permno year qtr RetQ

* Prepare FRED data and merge to returns
preserve
	import delimited "$pathProject/DataRaw/TBill3M.csv", varnames(1) clear
	save temp, replace
	
	import delimited "$pathProject/DataRaw/brokerLev.csv", varnames(1) clear
	save temp2, replace
restore

merge m:1 year qtr using temp, keep(master match) nogenerate
merge m:1 year qtr using temp2, keep(master match) nogenerate

* Prepare and run regression
replace RetQ = RetQ - tbillrate3m

gen tempTime = yq(year, qtr)
format tempTime %tq
xtset permno tempTime

asreg RetQ levfac, window(tempTime 40) min(20) by(permno) 

* Lag by one quarter to make sure that beta is available
gen BetaBDLeverage = l._b_levfac

keep permno year qtr BetaBDLeverage

save "$pathProject/DataClean/BDLeverageBeta", replace


*******************************************************************************
erase temp.dta
erase temp2.dta
erase tempIBES.dta
erase tempConglomerate.dta
erase tempCRSP.dta
