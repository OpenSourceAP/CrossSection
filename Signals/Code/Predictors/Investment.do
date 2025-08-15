* --------------
// DATA LOAD
use gvkey permno time_avail_m capx revt using "$pathDataIntermediate/m_aCompustat", clear

* CHECKPOINT 1: Initial data load
count
di "Initial observations: " _N
list permno time_avail_m capx revt if inlist(permno, 10006, 10051, 11406, 12473) & time_avail_m == tm(2007m4)

// SIGNAL CONSTRUCTION
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations

* CHECKPOINT 2: After removing duplicates  
count
di "After duplicate removal: " _N
list permno time_avail_m capx revt if inlist(permno, 10006, 10051, 11406, 12473) & time_avail_m == tm(2007m4)
xtset permno time_avail_m
gen Investment = capx/revt 

* CHECKPOINT 3: After creating Investment ratio
count if !missing(Investment)
di "Non-missing Investment after creation: " _result(1)
list permno time_avail_m Investment capx revt if inlist(permno, 10006, 10051, 11406, 12473) & time_avail_m == tm(2007m4)

bys permno: asrol Investment, gen(tempMean) window(time_avail_m 36) min(24) stat(mean)

* CHECKPOINT 4: After rolling mean calculation
count if !missing(tempMean)
di "Non-missing tempMean after asrol: " _result(1)
list permno time_avail_m Investment tempMean if inlist(permno, 10006, 10051, 11406, 12473) & time_avail_m == tm(2007m4)

replace Investment = Investment/tempMean

* CHECKPOINT 5: After normalizing by rolling mean
count if !missing(Investment)
di "Non-missing Investment after normalization: " _result(1)
list permno time_avail_m Investment tempMean if inlist(permno, 10006, 10051, 11406, 12473) & time_avail_m == tm(2007m4)

replace Investment = . if revt<10  // Replace with missing if revenue less than 10 million (units are millions)

* CHECKPOINT 6: After revenue filter
count if !missing(Investment)
di "Non-missing Investment after revenue filter: " _result(1)
list permno time_avail_m Investment revt if inlist(permno, 10006, 10051, 11406, 12473) & time_avail_m == tm(2007m4)
drop temp*
label var Investment "Investment"
// SAVE
do "$pathCode/savepredictor" Investment