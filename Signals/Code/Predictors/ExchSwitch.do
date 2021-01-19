* --------------
// DATA LOAD
use gvkey permno time_avail_m exchcd using "$pathDataIntermediate/SignalMasterTable", clear
xtset permno time_avail_m
// SIGNAL CONSTRUCTION
gen ExchSwitch = ( ( exchcd == 1 & (l1.exchcd == 2 | l2.exchcd == 2 | l3.exchcd == 2 | ///
    l4.exchcd == 2 | l5.exchcd == 2 | l6.exchcd == 2 | l7.exchcd == 2 | ///
    l8.exchcd == 2 | l9.exchcd == 2 | l10.exchcd == 2 | l11.exchcd == 2 | l12.exchcd == 2 | ///
    l1.exchcd == 3 | l2.exchcd == 3 | l3.exchcd == 3 | ///
    l4.exchcd == 3 | l5.exchcd == 3 | l6.exchcd == 3 | l7.exchcd == 3 | ///
    l8.exchcd == 3 | l9.exchcd == 3 | l10.exchcd == 3 | l11.exchcd == 3 | l12.exchcd == 3)) | ///
    ( exchcd == 2 & (l1.exchcd == 3 | l2.exchcd == 3 | l3.exchcd == 3 | ///
    l4.exchcd == 3 | l5.exchcd == 3 | l6.exchcd == 3 | l7.exchcd == 3 | ///
    l8.exchcd == 3 | l9.exchcd == 3 | l10.exchcd == 3 | l11.exchcd == 3 | l12.exchcd == 3) ))

label var ExchSwitch "Exchange Switch"
// SAVE
do "$pathCode/savepredictor" ExchSwitch