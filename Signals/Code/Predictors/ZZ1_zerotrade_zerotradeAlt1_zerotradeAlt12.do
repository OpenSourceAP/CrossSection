* --------
// DATA LOAD
use "$pathDataIntermediate/dailyCRSP.dta", clear

// SIGNAL CONSTRUCTION
gen time_avail_m = mofd(time_d)
format time_avail_m %tm

gen countzero = 1 if vol == 0
gen turn = vol/shrout /* daily turnover is the ratio of the number of shares traded
on a day to the number of shares outstanding at the end of the day (Liu (2006, p. 635)) */

gen days = 0 /* help variable because of some weirdness of collapse */
gcollapse (sum) countzero turn (count) ndays = days, by(permno time_avail_m) /*x-month turnover is turnover over the prior x months, calculated as the sum of daily
turnover over the prior x months (Liu (2006, p. 635))*/

xtset permno time_avail_m

// 40n1 Number of days with 0 trades (1 month version)
gen temp_zerotrade = (countzero + ((1/turn)/480000))*(21/ndays)
gen zerotrade1M = l.temp_zerotrade
label var zerotradeAlt1 "Days with zero trades (1 month version)"

// 40 Number of days with 0 trades (6 month version)
gen Turn6 = turn + l1.turn + l2.turn + l3.turn + l4.turn + l5.turn
gen countzero6 = countzero + l1.countzero + l2.countzero + l3.countzero + l4.countzero + l5.countzero
gen ndays6 = ndays + l1.ndays + l2.ndays + l3.ndays + l4.ndays + l5.ndays

gen temp_zerotrade6 = (countzero6 + ((1/Turn6)/11000))*(21*6/ndays6)  /* I use a deflator of 11,000 in constructing LM6 and LM12, and a deflator of 480,000 for LM1 (Liu (2006, fn 4, p. 635)) */

gen zerotrade6M = l.temp_zerotrade6
label var zerotrade "Days with zero trades (6 month version)"

// 40n12 Number of days with 0 trades (12 month version)
gen Turn12 = turn + l1.turn + l2.turn + l3.turn + l4.turn + l5.turn + l6.turn + l7.turn + l8.turn + l9.turn + l10.turn + l11.turn
gen countzero12 = countzero + l1.countzero + l2.countzero + l3.countzero + l4.countzero + l5.countzero + l6.countzero + l7.countzero + l8.countzero + l9.countzero + l10.countzero + l11.countzero
gen ndays12 = ndays + l1.ndays + l2.ndays + l3.ndays + l4.ndays + l5.ndays + l6.ndays + l7.ndays + l8.ndays + l9.ndays + l10.ndays + l11.ndays

gen temp_zerotrade12 = (countzero12 + ((1/Turn12)/11000))*(21*12/ndays12)  /* I use a deflator of 11,000 in constructing LM6 and LM12, and a deflator of 480,000 for LM1 (Liu (2006, fn 4, p. 635)) */

gen zerotrade12M = l.temp_zerotrade12
label var zerotradeAlt12 "Days with zero trades (12 month version)"

// SAVE 
do "$pathCode/savepredictor" zerotrade1M
do "$pathCode/savepredictor" zerotrade6M
do "$pathCode/savepredictor" zerotrade12M
