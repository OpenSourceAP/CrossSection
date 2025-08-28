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

asreg tempRi tempRm, window(time_temp 1260) min(750) by(permno) 

gen BetaFP = sqrt(_R2)*(sd252_LogRet/sd252_LogMkt)

drop _* Log* temp*

gen time_avail_m = mofd(time_d)
format time_avail_m %tm

sort permno time_avail_m time_d
gcollapse (lastnm) BetaFP, by(permno time_avail_m)

label var BetaFP "Frazzini-Pedersen beta"

// SAVE 
do "$pathCode/savepredictor" BetaFP