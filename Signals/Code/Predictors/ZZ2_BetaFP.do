* BetaFP
* -------

* debug mode
local DEBUG_MODE_PRE1950 1

// DATA LOAD
use permno time_d ret using "$pathDataIntermediate/dailyCRSP.dta", clear

* debug mode
if `DEBUG_MODE_PRE1950' == 1 {
    keep if time_d < td(01jan1950)
}

merge m:1 time_d using "$pathDataIntermediate/dailyFF", nogenerate keep(match) keepusing(rf mktrf)
replace ret = ret - rf
drop rf 


// SIGNAL CONSTRUCTION

gen LogRet = log(1+ret)
gen LogMkt = log(1+mktrf)

bys permno (time_d): gen time_temp = _n
xtset permno time_temp

* Standard deviations of log returns
asrol LogRet, window(time_temp 252) min(120) by(permno) stat(sd) gen(sd252_LogRet)
asrol LogMkt, window(time_temp 252) min(120) by(permno) stat(sd) gen(sd252_LogMkt)

* R2 of this regression is squared correlation coefficient
gen tempRi = l2.LogRet + l1.LogRet + LogRet
gen tempRm = l2.LogMkt + l1.LogMkt + LogMkt

* - CHECKPOINT 1: Check tempRi and tempRm for bad observations
di "CHECKPOINT 1: tempRi and tempRm values for bad permnos"
list permno time_d tempRi tempRm LogRet LogMkt if inlist(permno, 14269, 13389, 11797, 11252, 20271) & time_d >= td(01nov1941) & time_d <= td(31mar1942), sepby(permno)

asreg tempRi tempRm, window(time_temp 1260) min(750) by(permno) 

* - CHECKPOINT 2: Check R2 and standard deviations for bad observations
di "CHECKPOINT 2: R2 and standard deviations for bad permnos"
list permno time_d _R2 sd252_LogRet sd252_LogMkt if inlist(permno, 14269, 13389, 11797, 11252, 20271) & time_d >= td(01nov1941) & time_d <= td(31mar1942), sepby(permno)

gen BetaFP = sqrt(_R2)*(sd252_LogRet/sd252_LogMkt)

* - CHECKPOINT 3: Check final BetaFP calculation for bad observations
di "CHECKPOINT 3: Final BetaFP values for bad permnos"
list permno time_d BetaFP _R2 sd252_LogRet sd252_LogMkt if inlist(permno, 14269, 13389, 11797, 11252, 20271) & time_d >= td(01nov1941) & time_d <= td(31mar1942), sepby(permno)

drop _* Log* temp*

gen time_avail_m = mofd(time_d)
format time_avail_m %tm

sort permno time_avail_m time_d
gcollapse (lastnm) BetaFP, by(permno time_avail_m)

* - CHECKPOINT 4: Check monthly aggregated BetaFP values for bad observations
di "CHECKPOINT 4: Monthly aggregated BetaFP values for bad permnos"
list permno time_avail_m BetaFP if inlist(permno, 14269, 13389, 11797, 11252, 20271) & time_avail_m >= tm(1941m12) & time_avail_m <= tm(1942m4), sepby(permno)

label var BetaFP "Frazzini-Pedersen beta"

// SAVE 
do "$pathCode/savepredictor" BetaFP