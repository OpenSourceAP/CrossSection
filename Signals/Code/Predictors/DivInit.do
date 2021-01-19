* --------------
// DATA LOAD
use permno time_avail_m shrcd using "$pathDataIntermediate/SignalMasterTable", clear
merge 1:1 permno time_avail_m using "$pathDataIntermediate/mCRSPdistributions", keep(master match) nogenerate keepusing(divamt) 
// SIGNAL CONSTRUCTION
gen temp = divamt
replace temp = 0 if divamt ==.
gen PayedDividend = temp > 0
* Make columns with dividends over last 24 months
foreach n of numlist 1(1)25 {

gen Divtemp`n' = l`n'.temp

replace Divtemp`n' = 0 if mi(Divtemp`n')
}
egen tempNo = rowtotal(Divtemp*)
gen NoDiv24 = (tempNo == 0)
gen tempDivInit = (NoDiv24 == 1 & PayedDividend == 1)
gen DivInit = (tempDivInit == 1 | l.tempDivInit == 1 | l2.tempDivInit == 1 ///
    | l3.tempDivInit == 1 | l4.tempDivInit == 1 | l5.tempDivInit == 1 ///
    | l6.tempDivInit == 1 | l7.tempDivInit == 1 | l8.tempDivInit == 1 ///
    | l9.tempDivInit == 1 | l10.tempDivInit == 1 | l11.tempDivInit == 1)
    
replace DivInit = . if shrcd > 11 
label var DivInit "Dividend Initiation"
// SAVE
do "$pathCode/savepredictor" DivInit