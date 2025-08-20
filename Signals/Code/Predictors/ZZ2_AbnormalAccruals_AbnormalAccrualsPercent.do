* AbnormalAccruals, AbnormalAccrualsPercent
* --------------


// DATA LOAD
use gvkey permno time_avail_m fyear datadate at oancf fopt act che lct dlc ib sale ppegt ni sic  using "$pathDataIntermediate/a_aCompustat", clear
merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(master match) keepusing(exchcd)

// SIGNAL CONSTRUCTION
xtset gvkey fyear

// Compute abnormal accruals for Xie (2001)
gen tempCFO = oancf
replace tempCFO = fopt - (act - l.act) + (che - l.che) + (lct - l.lct) - (dlc - l.dlc) if mi(tempCFO)
gen tempAccruals = (ib - tempCFO) / l.at
gen tempInvTA = 1/l.at
gen tempDelRev = (sale - l.sale)/l.at
gen tempPPE = ppegt/l.at

* - CHECKPOINT 1: Check key variables after initial computation
display "=== CHECKPOINT 1: After initial variable computation ==="
list gvkey permno fyear datadate tempCFO tempAccruals tempInvTA tempDelRev tempPPE if (permno == 84005 & fyear == 2000) | (permno == 85712 & fyear == 2000) | (permno == 77649 & fyear == 1997), sep(0)

sort fyear
winsor2 temp*, replace cuts(0.1 99.9) trim by(fyear)  // p 360 (approx)

* - CHECKPOINT 2: Check variables after winsorization
display "=== CHECKPOINT 2: After winsorization ==="
list gvkey permno fyear datadate tempCFO tempAccruals tempInvTA tempDelRev tempPPE if (permno == 84005 & fyear == 2000) | (permno == 85712 & fyear == 2000) | (permno == 77649 & fyear == 1997), sep(0)

// * Run regressions for each year and industry
destring sic, replace
gen sic2 = floor(sic/100)
bys fyear sic2: asreg tempAccruals tempInvTA tempDelRev tempPPE , fitted

* - CHECKPOINT 3: Check regression results and _Nobs before dropping
display "=== CHECKPOINT 3: After regression, before dropping _Nobs < 6 ==="
list gvkey permno fyear sic2 _Nobs _fitted _residuals if (permno == 84005 & fyear == 2000) | (permno == 85712 & fyear == 2000) | (permno == 77649 & fyear == 1997), sep(0)

drop if _Nobs < 6 // p 360
drop if exchcd == 3 & fyear < 1982


rename _residuals AbnormalAccruals
drop _* temp* 

* drop a few duplicates
sort permno fyear
by permno fyear: keep if _n == 1

label var AbnormalAccruals "Abnormal Accruals"

* - CHECKPOINT 4: Check final AbnormalAccruals before monthly expansion
display "=== CHECKPOINT 4: Final AbnormalAccruals values ==="
list gvkey permno fyear datadate AbnormalAccruals if (permno == 84005 & fyear == 2000) | (permno == 85712 & fyear == 2000) | (permno == 77649 & fyear == 1997), sep(0)

* Abnormal Accruals Percent
xtset permno fyear
gen AbnormalAccrualsPercent = AbnormalAccruals*l.at/abs(ni)
label var AbnormalAccrualsPercent "Abnormal Accruals (Percent)"

* Expand to monthly
gen temp = 12
expand temp
drop temp

gen tempTime = time_avail_m
bysort gvkey tempTime: replace time_avail_m = time_avail_m + _n - 1 

drop tempTime
bysort gvkey time_avail_m (datadate): keep if _n == _N 
bysort permno time_avail_m (datadate): keep if _n == _N 

* - CHECKPOINT 5: Check final monthly observations for problematic permnos
display "=== CHECKPOINT 5: Final monthly data for problematic observations ==="
list permno time_avail_m AbnormalAccruals if (permno == 84005 & inrange(time_avail_m, tm(2001m1), tm(2001m12))) | (permno == 85712 & inrange(time_avail_m, tm(2001m1), tm(2001m12))) | (permno == 77649 & inrange(time_avail_m, tm(1997m6), tm(1998m6))), sep(0)

// SAVE 
do "$pathCode/savepredictor" AbnormalAccruals
do "$pathCode/saveplacebo" AbnormalAccrualsPercent


