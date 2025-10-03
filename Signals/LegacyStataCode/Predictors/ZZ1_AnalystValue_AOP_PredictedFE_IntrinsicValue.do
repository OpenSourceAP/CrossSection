* AnalystValue, AOP, PredictedFE
* IntrinsicValue is created in this code but is not saved since it
* wasn't shown to predict returns in the OP
* Our AnalystValue is a simplification of OP, which means all of the others 
* are even further from OP

* v0.1.2: we thought we had it working, but the sign of AOP 
* was wrong
* --------------

// Prep IBES FROE1
use "$pathDataIntermediate/IBES_EPS_Unadj", replace
keep if fpi == "1" & month(statpers) == 5 // only May p 290
keep if fpedats != . & fpedats > statpers + 30 // keep only forecasts past June
replace time_avail_m = time_avail_m + 1 // OP is conservative, this matches with Compustat following FF
rename meanest feps1
keep tickerIBES time_avail_m feps1
save "$pathtemp/tempFROE", replace

// Prep IBES FROE2
use "$pathDataIntermediate/IBES_EPS_Unadj", replace
keep if fpi == "2" & month(statpers) == 5 // only May p 290
replace time_avail_m = time_avail_m + 1 // OP is conservative, this matches with Compustat following FF
rename meanest feps2
keep tickerIBES time_avail_m feps2
save "$pathtemp/tempFROE2", replace

// Prep IBES LTG
use "$pathDataIntermediate/IBES_EPS_Unadj", replace
keep if fpi == "0" 
rename meanest LTG
keep tickerIBES time_avail_m LTG
save "$pathtemp/tempLTG", replace


// DATA LOAD
use permno tickerIBES time_avail_m prc using "$pathDataIntermediate/SignalMasterTable", clear
merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keep(master match) nogenerate keepusing(shrout) 
merge 1:1 permno time_avail_m using "$pathDataIntermediate/m_aCompustat", keep(master match) nogenerate keepusing(ceq ib ibcom ni sale datadate dvc at)
gen SG = sale/l60.sale
keep if month(dofm(time_avail_m)) == 6
merge m:1 tickerIBES time_avail_m using "$pathtemp/tempFROE", keep(match) nogenerate 
merge m:1 tickerIBES time_avail_m using "$pathtemp/tempFROE2", keep(master match) nogenerate 
merge m:1 tickerIBES time_avail_m using "$pathtemp/tempLTG", keep(master match) nogenerate 

	
* common screens and variables
xtset permno time_avail_m

gen ceq_ave = (ceq + l12.ceq)/2
bys permno (time_avail_m): replace ceq_ave = ceq if _n <= 1 // seems important
gen mve_c = (shrout * abs(prc))
gen BM = ceq/mve_c
gen k = dvc/ibcom // p 288 says ib, but Table 1 says ibcom
replace k = dvc/(0.06*at) if ibcom < 0
gen ROE = ibcom/ceq_ave // p 290 or Table 1

// p 317 (Appendix)
gen FROE1 = feps1*shrout/ceq_ave
gen ceq1 = ceq*(1+FROE1*(1-k))
gen ceq1h = ceq*(1+ROE*(1-k))

gen FROE2 = feps2*shrout/((ceq1 + ceq)/2)
gen ceq2 = ceq1*(1+FROE1*(1-k))
gen ceq2h = ceq1h*(1+ROE*(1-k))

gen FROE3 = feps2*(1+LTG/100)*shrout/((ceq1+ceq2)/2)
replace FROE3 = FROE2 if LTG == .
gen ceq3 = ceq2*(1+FROE2*(1-k))

// screens 
drop if ceq < 0 | ceq == . // page 291
drop if abs(ROE) > 1 | abs(FROE1) > 1 | k > 1 // page 291
keep if month(datadate) >= 6 // p 290
drop if feps2 == . | feps1 == . // p 290.  i find this is important for AOP, somehow?

// SIGNAL CONSTRUCTION (annual)
* footnote on p 294 describes r.  I find value of r if constant r does not matter
gen r = 0.12	

	* uncomment below if you want to do a hacked version of the FF3 expected return
	* but I find this generally works worse than constant r
	* egen catBM = fastxtile(BM), by(time_avail_m) n(5)
	* gen r = 0.12 + (catBM-3)/2*0.00  // value premium is about 6 pct per year

	
* p 290: formulas  p 294: 3-stage for AnalystValue and 2-stage for IntrinsicValue
gen AnalystValue = (ceq1 + (FROE1-r)/(1+r)*ceq1 + (FROE2-r)/(1+r)^2*ceq2 + (FROE3-r)/(1+r)^2/r*ceq3)/mve_c
gen IntrinsicValue = (ceq1h + (ROE-r)/(1+r)*ceq1h + (ROE-r)/(1+r)/r*ceq2h)/mve_c
gen AOP = (AnalystValue - IntrinsicValue)/abs(IntrinsicValue)

// Predicted FE
xtset permno time_avail_m

* sign of FErr is confusing
* Tab 5 says actual - forecasted, but that's counterintuitive
* and doesn't match the summary stats or signs in Tab 5
* e.g. Tab 5 shows high optimism => high FErr
gen FErr = l12.FROE1 - ROE // almost works!
winsor2 FErr, replace cuts(1 99) trim by(time_avail_m)
	
* convert to ranks
sort time_avail_m
foreach v of varlist SG BM AOP LTG{
	by time_avail_m: relrank `v', gen(rank`v') ref(`v')
}

* lag for forecasting and run reg
xtset permno time_avail_m
foreach v of varlist SG AOP BM LTG{
	gen lag`v' = l12.rank`v'
}
asreg FErr lag*, by(time_avail_m) 

* compute fitted with up-to-date ranks
gen PredictedFE = _b_cons + _b_lagSG*rankSG + _b_lagBM*rankBM + _b_lagAOP*rankAOP + _b_lagLTG*rankLTG

* hand from OP
* even using these hand collected coefficients, t=1.5
*gen PredictedFE = 0.035*rankSG + 0.001*rankBM + 0.051*rankAOP + 0.05*rankLTG

// EXPAND TO MONTHLY
* signal relevant for one year
gen temp = 12
expand temp
drop temp
gen tempTime = time_avail_m
bysort permno tempTime: replace time_avail_m = time_avail_m + _n - 1 
drop tempTime

label var AnalystValue "Analyst Value"
label var AOP "Analyst Optimism"
label var PredictedFE "Predicted Forecast Error"
label var IntrinsicValue "Intrinsic Value"

// SAVE 
do "$pathCode/savepredictor" AnalystValue
do "$pathCode/savepredictor" AOP
do "$pathCode/savepredictor" PredictedFE
do "$pathCode/saveplacebo" IntrinsicValue
