* --------------
// DATA LOAD
use permno time_avail_m exchcd using "$pathDataIntermediate/SignalMasterTable", clear
merge 1:1 permno time_avail_m using "$pathDataIntermediate/mCRSPdistributions", keep(master match) nogenerate keepusing(divamt) 

// SIGNAL CONSTRUCTION
sort permno time_avail_m
xtset permno time_avail_m

// OP selects "companies that had existed on the NYSE or AMEX for more than one year and paid regular period div"
// but we're more flexible
gen div = divamt
replace div = 0 if divamt ==. 
//gen divind = div > 0 & (exchcd == 1 | exchcd == 2)
gen divind = div > 0 

* quarterly
order permno time_avail_m divind
bys permno: asrol divind, window(time_avail_m 3) stat(sum)
gen temppaid = sum3_divind == 1
bys permno: asrol temppaid, window(time_avail_m 18) stat(mean)
gen temppayer = mean18_temppaid == 1
gen omit_3 = sum3_divind == 0 & l1.sum3_divind > 0 & l3.temppayer == 1 

drop temp* sum* mean*

* semi-annual
order permno time_avail_m divind
bys permno: asrol divind, window(time_avail_m 6) stat(sum)
gen temppaid = sum6_divind == 1
bys permno: asrol temppaid, window(time_avail_m 18) stat(mean)
gen temppayer = mean18_temppaid == 1
gen omit_6 = sum6_divind == 0 & l1.sum6_divind > 0 & l6.temppayer == 1 

drop temp* sum* mean*

* annual
order permno time_avail_m divind
bys permno: asrol divind, window(time_avail_m 12) stat(sum)
gen temppaid = sum12_divind == 1
bys permno: asrol temppaid, window(time_avail_m 24) stat(mean)
gen temppayer = mean24_temppaid == 1
gen omit_12 = sum12_divind == 0 & l1.sum12_divind > 0 & l12.temppayer == 1 

drop temp* sum* mean*

gen omitnow = omit_3 == 1 | omit_6 == 1 | omit_12 == 1
bys permno: asrol omitnow, window(time_avail_m 6) stat(sum) gen(temp)
gen DivOmit = temp == 1


label var DivOmit "Dividend Omission"

// SAVE
do "$pathCode/savepredictor" DivOmit


