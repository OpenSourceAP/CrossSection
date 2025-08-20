* --------------
// DATA LOAD
use gvkey permno time_avail_m fyear datadate xrd sale using "$pathDataIntermediate/a_aCompustat", clear

* CHECKPOINT 1
di "=== CHECKPOINT 1: Initial data load ==="
list gvkey permno time_avail_m fyear datadate xrd sale if permno == 79283 & time_avail_m >= tm(2002m1) & time_avail_m <= tm(2003m12), abbreviate(20)
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

* CHECKPOINT 2
di "=== CHECKPOINT 2: After creating tempY and tempX ==="
list gvkey permno fyear tempXRD tempSale tempY tempX if permno == 79283 & time_avail_m >= tm(2002m1) & time_avail_m <= tm(2003m12), abbreviate(20)
gen tempNonZero = .           // paper requires that "half of R&D observations"
                              // are non-zero". 
gen tempXLag = .
foreach n of numlist 1/5 {

replace tempXLag = l`n'.tempX
    asreg tempY tempXLag, window(fyear 8) min(6) by(gvkey)

rename _b_tempXLag gammaAbility`n'

* CHECKPOINT 3
di "=== CHECKPOINT 3: After asreg for lag `n' ==="
list gvkey permno fyear tempXLag gammaAbility`n' if permno == 79283 & time_avail_m >= tm(2002m1) & time_avail_m <= tm(2003m12), abbreviate(20)

drop _*


replace tempNonZero = tempXLag >0 & !mi(tempXLag) 
    asrol tempNonZero, window(fyear 8) min(6) by(gvkey) stat(mean) gen(tempMean)

* CHECKPOINT 4
di "=== CHECKPOINT 4: After tempMean filtering for lag `n' ==="
list gvkey permno fyear tempNonZero tempMean gammaAbility`n' if permno == 79283 & time_avail_m >= tm(2002m1) & time_avail_m <= tm(2003m12), abbreviate(20)

replace gammaAbility`n' = . if tempMean < .5 & !mi(tempMean)

drop tempMean
}
drop temp*
egen RDAbility = rowmean(gammaAbil*)

* CHECKPOINT 5
di "=== CHECKPOINT 5: After rowmean of gammaAbil ==="
list gvkey permno fyear gammaAbility* RDAbility if permno == 79283 & time_avail_m >= tm(2002m1) & time_avail_m <= tm(2003m12), abbreviate(20)

gen tempRD = xrd/sale
replace tempRD = . if xrd <= 0
egen tempRDQuant = fastxtile(tempRD), n(3) by(time_avail_m)

* CHECKPOINT 6
di "=== CHECKPOINT 6: After fastxtile ==="
list gvkey permno fyear tempRD tempRDQuant RDAbility if permno == 79283 & time_avail_m >= tm(2002m1) & time_avail_m <= tm(2003m12), abbreviate(20)
replace RDAbility = . if tempRDQuant != 3
replace RDAbility = . if xrd <=0

* CHECKPOINT 7
di "=== CHECKPOINT 7: After final filtering ==="
list gvkey permno fyear RDAbility if permno == 79283 & time_avail_m >= tm(2002m1) & time_avail_m <= tm(2003m12) & !mi(RDAbility), abbreviate(20)

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

* CHECKPOINT 8
di "=== CHECKPOINT 8: Final monthly expansion ==="
list permno time_avail_m RDAbility if permno == 79283 & time_avail_m >= tm(2002m1) & time_avail_m <= tm(2003m12) & !mi(RDAbility), abbreviate(20)
// SAVE
do "$pathCode/savepredictor" RDAbility