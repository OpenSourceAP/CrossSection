* --------------
// DATA LOAD
use gvkey permno time_avail_m ret using "$pathDataIntermediate/SignalMasterTable", clear
drop if gvkey ==.
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_SP_creditratings", keep(master match) nogenerate
// SIGNAL CONSTRUCTION
xtset permno time_avail_m
replace ret = 0 if mi(ret)
gen Mom6m = ( (1+l.ret)*(1+l2.ret)*(1+l3.ret)*(1+l4.ret)*(1+l5.ret)) - 1
gen Mom6mJunk = Mom6m if credrat <= 14
label var Mom6mJunk "Junk stock momentum"
// SAVE
do "$pathCode/savepredictor" Mom6mJunk