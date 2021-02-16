* --------
// DATA LOAD
use "$pathDataIntermediate/dailyCRSP.dta", clear

// SIGNAL CONSTRUCTION
gen time_avail_m = mofd(time_d)
format time_avail_m %tm
gen countzero = 1 if vol == 0
gen turn = vol/shrout
gen days = 0 /* help variable because of some weirdness of collapse */
gcollapse (sum) countzero turn (count) ndays = days, by(permno time_avail_m)
gen temp_zerotrade = (countzero + ((1/turn)/480000))*(21/ndays)
xtset permno time_avail_m
// 40n1 Number of days with 0 trades (1 month version)
gen zerotradeAlt1 = l.temp_zerotrade
label var zerotradeAlt1 "Days with zero trades (1 month version)"
// 40 Number of days with 0 trades (6 month version)
gen zerotrade = (temp_zerotrade + l.temp_zerotrade + l2.temp_zerotrade + l3.temp_zerotrade + ///
    l4.temp_zerotrade + l5.temp_zerotrade)/6

label var zerotrade "Days with zero trades (6 month version)"

// 40n12 Number of days with 0 trades (12 month version)
gen zerotradeAlt12 = (zerotradeAlt1 + l.zerotradeAlt1 + l2.zerotradeAlt1 + l3.zerotradeAlt1 + ///
    l4.zerotradeAlt1 + l5.zerotradeAlt1 + l6.zerotradeAlt1 + l7.zerotradeAlt1 + l8.zerotradeAlt1 + ///
    l9.zerotradeAlt1 + l10.zerotradeAlt1 + l11.zerotradeAlt1)/12
label var zerotradeAlt12 "Days with zero trades (12 month version)"

// SAVE 
do "$pathCode/savepredictor" zerotrade
do "$pathCode/savepredictor" zerotradeAlt1
do "$pathCode/savepredictor" zerotradeAlt12
