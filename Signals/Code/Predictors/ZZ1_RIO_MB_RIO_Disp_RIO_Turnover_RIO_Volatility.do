* -------------- 
* RIO * signals
* Needs to be run after IdioRisk, so we run it last.  IdioRisk takes about 20 min
* 
* --------------

// Prep IBES data
use "$pathDataIntermediate/IBES_EPS_Unadj", replace
keep if fpi == "1" 
save "$pathtemp/tempIBES", replace

// DATA LOAD
use permno tickerIBES time_avail_m exchcd mve_c using "$pathDataIntermediate/SignalMasterTable", clear
merge 1:1 permno time_avail_m using "$pathDataIntermediate/TR_13F", keep(master match) nogenerate keepusing(instown_perc)
merge 1:1 permno time_avail_m using "$pathDataIntermediate/m_aCompustat", keep(master match) nogenerate keepusing(at ceq txditc)
merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keep(master match) nogenerate keepusing(vol shrout ret)
merge m:1 tickerIBES time_avail_m using "$pathtemp/tempIBES", keep(master match) nogenerate keepusing (stdev)

* filter below 20th pct NYSE me 
* do before indep sort
bys time_avail_m: astile sizecat = mve_c, qc(exchcd==1 | exchcd == 2) nq(5)
drop if sizecat == 1
drop sizecat

* Residual Institutional Ownership sort
gen temp = instown_perc/100
replace temp = 0 if mi(temp)
replace temp = .9999 if temp > .9999
replace temp = .0001 if temp < .0001
gen RIO = log(temp/(1-temp)) + 23.66 - 2.89*log(mve_c) + .08*(log(mve_c))^2

xtset permno time_avail_m
gen RIOlag = l6.RIO
egen cat_RIO = fastxtile(RIOlag), n(5) by(time_avail_m)


* Forecast dispersion, market-to-book, turnover, volatiltity sorts
replace txditc = 0 if mi(txditc)
gen MB = mve_c/(ceq + txditc)
replace MB = . if (ceq + txditc) < 0

gen Disp = stdev/at if stdev > 0
gen Turnover = vol/shrout
bys permno: asrol ret, gen(Volatility) stat(sd) window(time_avail_m 12) min(6)

foreach v of varlist MB Disp Volatility Turnover {
	egen cat_`v'  = fastxtile(`v'), n(5) by(time_avail_m)
	gen RIO_`v' = cat_RIO if cat_`v' == 5
}

* patch for Dispersion
replace RIO_Disp = cat_RIO if cat_Disp >= 4 & cat_Disp != .

label var RIO_MB "Inst Own and MB"
label var RIO_Disp "Inst Own and Forecast Dispersion"
label var RIO_Turnover "Inst Own and Turnover"
label var RIO_Volatility "Inst Own and Volatility"

// SAVE 
do "$pathCode/savepredictor" RIO_MB
do "$pathCode/savepredictor" RIO_Disp
do "$pathCode/savepredictor" RIO_Turnover
do "$pathCode/savepredictor" RIO_Volatility

