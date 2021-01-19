// 2021 01 ac:
// this monthly version is a placebo.  OP is very specific about timing

* --------------
// DATA LOAD
use permno time_avail_m ceq ib txdi dv sale ni dp using "$pathDataIntermediate/m_aCompustat", clear
merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(using match) nogenerate keepusing(tickerIBES) 
merge m:1 tickerIBES time_avail_m using "$pathDataIntermediate/IBES_EPSLongRun", keep(master match) nogenerate keepusing(fgr5yr)

// SIGNAL CONSTRUCTION
xtset permno time_avail_m
gen fgr5yrLag = fgr5yr
replace fgr5yrLag = . if ceq == . | ib == . | txdi == . | dv == . | sale == . | ni == . | dp == .
label var fgr5yrLag "Long-term EPS forecast"

// SAVE
do "$pathCode/saveplacebo" fgr5yrLag
