// 2021 01 ac:
// Changed timing to be closer to OP: december only, lag 6 months, then fill
// Very sensitive to details, even in the lagging method, but can be replicated pretty much
* --------------
// Prep IBES data
use "$pathDataIntermediate/IBES_EPS_Unadj", replace
keep if fpi == "0" 
rename meanest fgr5yr
save "$pathtemp/temp", replace

// DATA LOAD
use permno time_avail_m ceq ib txdi dv sale ni dp using "$pathDataIntermediate/m_aCompustat", clear
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(match) nogenerate keepusing(tickerIBES) 
merge m:1 tickerIBES time_avail_m using "$pathtemp/temp", keep(match) nogenerate keepusing(fgr5yr)

drop if ceq == . | ib == . | txdi == . | dv == . | sale == . | ni == . | dp == . | fgr5yr == .
drop ceq dp dv ib ni sale txdi 

// SIGNAL CONSTRUCTION
* lag 6 months, then keep June / Dec obs
xtset permno time_avail_m
gen fgr5yrLag = l6.fgr5yr
keep if month(dofm(time_avail_m)) == 6  

// expand to monthly
gen temp = 12
expand temp
drop temp
gen tempTime = time_avail_m
bysort permno tempTime: replace time_avail_m = time_avail_m + _n - 1 
drop tempTime

label var fgr5yrLag "Long-term EPS forecast Lagged"

// SAVE
do "$pathCode/savepredictor" fgr5yrLag
