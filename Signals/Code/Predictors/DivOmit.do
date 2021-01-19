* --------------
// DATA LOAD
use permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
merge 1:1 permno time_avail_m using "$pathDataIntermediate/mCRSPdistributions", keep(master match) nogenerate keepusing(divamt) 
// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen temp = divamt
replace temp = 0 if divamt ==.
gen tempND = ( temp ==0 & l.temp ==0 & l2.temp ==0)
gen temp3  = (l3.temp >0 & l6.temp>0 & l9.temp >0 & l12.temp > 0 & l15.temp > 0 & l18.temp >0)
gen tempOmit = (tempND == 1 & temp3 == 1)
gen DivOmit = (tempOmit == 1 | l1.tempOmit == 1 | l2.tempOmit == 1 | l3.tempOmit ==1 ///
    | l4.tempOmit == 1 | l5.tempOmit == 1 | l6.tempOmit == 1 | l7.tempOmit == 1 ///
    | l8.tempOmit == 1 | l9.tempOmit == 1 | l10.tempOmit ==1 | l11.tempOmit == 1)

label var DivOmit "Dividend Omission"
// SAVE
do "$pathCode/savepredictor" DivOmit