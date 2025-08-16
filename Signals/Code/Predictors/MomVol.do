* --------------
// DATA LOAD
use permno time_avail_m ret using "$pathDataIntermediate/SignalMasterTable", clear
merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keepusing(vol) nogenerate keep(match)

// SIGNAL CONSTRUCTION
replace vol = . if vol <0
replace ret = 0 if mi(ret)

* old
// gen Mom6m = ( (1+l.ret)*(1+l2.ret)*(1+l3.ret)*(1+l4.ret)*(1+l5.ret)) - 1
// bys permno (time_avail_m): asrol vol, gen(temp) window(time_avail_m 6) min(5) stat(mean)
// egen tempVol = fastxtile(temp), by(time_avail_m) n(3)
// gen MomVol = Mom6m if tempVol == 3

* new
// indep sort
gen Mom6m = ( (1+l.ret)*(1+l2.ret)*(1+l3.ret)*(1+l4.ret)*(1+l5.ret)) - 1
* CHECKPOINT 1: Debug momentum calculation for problematic observations
list permno time_avail_m ret l.ret l2.ret l3.ret l4.ret l5.ret Mom6m if permno == 10006 & time_avail_m == tm(1943m1)
egen catMom = fastxtile(Mom6m), by(time_avail_m) n(10)
* CHECKPOINT 2: Debug momentum quantiles
list permno time_avail_m Mom6m catMom if permno == 10006 & time_avail_m == tm(1943m1)
summarize Mom6m if time_avail_m == tm(1943m1), detail
_pctile Mom6m if time_avail_m == tm(1943m1), n(10)
display "Momentum decile cutoffs for " %tm time_avail_m ": " r(r1) " " r(r2) " " r(r3) " " r(r4) " " r(r5) " " r(r6) " " r(r7) " " r(r8) " " r(r9)


bys permno (time_avail_m): asrol vol, gen(temp) window(time_avail_m 6) min(5) stat(mean)
* CHECKPOINT 3: Debug volume rolling calculation
list permno time_avail_m vol temp if permno == 10006 & time_avail_m == tm(1943m1)
egen catVol = fastxtile(temp), by(time_avail_m) n(3)
* CHECKPOINT 4: Debug volume quantiles  
list permno time_avail_m temp catVol if permno == 10006 & time_avail_m == tm(1943m1)
summarize temp if time_avail_m == tm(1943m1), detail
_pctile temp if time_avail_m == tm(1943m1), n(3)
display "Volume tercile cutoffs for " %tm time_avail_m ": " r(r1) " " r(r2)
tabulate catVol if time_avail_m == tm(1943m1)

gen MomVol = catMom if catVol == 3 // keep high vol at only
* CHECKPOINT 5: Debug final signal assignment
list permno time_avail_m catMom catVol MomVol if permno == 10006 & time_avail_m == tm(1943m1)
count if catVol == 3 & time_avail_m == tm(1943m1)
count if !missing(MomVol) & time_avail_m == tm(1943m1)

// filter
bys permno (time_avail_m): replace MomVol = . if _n < 24
* CHECKPOINT 6: Debug time filter  
list permno time_avail_m MomVol if permno == 10006 & time_avail_m == tm(1943m1)
drop temp*
label var MomVol "Momentum among high volume stocks"

// SAVE
do "$pathCode/savepredictor" MomVol
