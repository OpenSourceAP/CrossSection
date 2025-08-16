* --------------
// DATA LOAD
use permno time_avail_m txfo txfed ib txt txdi using "$pathDataIntermediate/m_aCompustat", clear
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
// SIGNAL CONSTRUCTION
gen year = yofd(dofm(time_avail_m))
* Define highest tax rate by year
gen tr = .48
replace tr = .46 if year >= 1979 & year <= 1986
replace tr = .4 if year ==1987
replace tr = .34 if year >= 1988 & year <=1992
replace tr = .35 if year >=1993

* CHECKPOINT 1
list permno time_avail_m year tr txfo txfed txt txdi ib if permno == 26542 & year >= 1989 & year <= 1990, abbrev(10)

gen Tax = ((txfo+txfed)/tr)/ib
replace Tax = ((txt-txdi)/tr)/ib if txfo ==. | txfed ==.
replace Tax = 1 if (txfo + txfed > 0 | txt > txdi) & ib <=0

* CHECKPOINT 2
list permno time_avail_m Tax if permno == 26542 & year >= 1989 & year <= 1990, abbrev(10)
label var Tax "Taxable income to income"
// SAVE
do "$pathCode/savepredictor" Tax