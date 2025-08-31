* --------------
// DATA LOAD
use gvkey permno time_avail_m fyear datadate xrd sale using "$pathDataIntermediate/a_aCompustat", clear
// SIGNAL CONSTRUCTION
xtset gvkey fyear
* Compute Ability measure of Cohen, Dieter and Malloy (2013)
gen tempXRD = xrd
replace tempXRD = . if tempXRD <0
gen tempSale = sale
replace tempSale = . if tempSale < 0
xtset gvkey fyear
gen tempY = log(tempSale/l.tempSale)
gen tempX = log(1 + tempXRD/tempSale)
gen tempNonZero = .           // paper requires that "half of R&D observations"
                              // are non-zero". 
gen tempXLag = .
foreach n of numlist 1/5 {

replace tempXLag = l`n'.tempX
    asreg tempY tempXLag, window(fyear 8) min(6) by(gvkey)

rename _b_tempXLag gammaAbility`n'

drop _*


replace tempNonZero = tempXLag >0 & !mi(tempXLag) 
    asrol tempNonZero, window(fyear 8) min(6) by(gvkey) stat(mean) gen(tempMean)

replace gammaAbility`n' = . if tempMean < .5 & !mi(tempMean)

drop tempMean
}
drop temp*
egen RDAbility = rowmean(gammaAbil*)
gen tempRD = xrd/sale
replace tempRD = . if xrd <= 0
egen tempRDQuant = fastxtile(tempRD), n(3) by(time_avail_m)
replace RDAbility = . if tempRDQuant != 3
replace RDAbility = . if xrd <=0
cap drop temp*
label var RDAbility "R&D ability"
* Expand to monthly
gen temp = 12
expand temp
drop temp
gen tempTime = time_avail_m
bysort gvkey tempTime: replace time_avail_m = time_avail_m + _n - 1 
drop tempTime
bysort gvkey time_avail_m (datadate): keep if _n == _N 
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
// SAVE
do "$pathCode/savepredictor" RDAbility