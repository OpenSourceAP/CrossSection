* AnalystValue, AOP, PredictedFE
* IntrinsicValue is created in this code but is not saved since it
* wasn't shown to predict returns in the OP
* --------------

// DATA LOAD
use permno tickerIBES time_avail_m prc using "$pathDataIntermediate/SignalMasterTable", clear

merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keep(master match) nogenerate keepusing(shrout) 

merge 1:1 permno time_avail_m using "$pathDataIntermediate/m_aCompustat", keep(master match) nogenerate keepusing(ceq ib sale)

merge m:1 tickerIBES time_avail_m using "$pathDataIntermediate/IBES_EPS", keep(master match) nogenerate keepusing(meanest) 

// SIGNAL CONSTRUCTION
xtset permno time_avail_m

* Analyst value
gen mve_c = (shrout * abs(prc))
gen FROE = (meanest*shrout)/ceq
replace FROE = . if abs(FROE) > 1  // Frankel and Lee, page 291

gen tempBM = ceq/mve_c
gen tempBMAve = (tempBM + l12.tempBM)/2
bys permno (time_avail_m): replace tempBMAve = tempBM if _n <= 12

gen AnalystValue = (1 + (FROE - .1)/1.1 + (FROE - .1)/(.1*1.1))*tempBMAve
replace AnalystValue = . if ceq < 0 | abs(prc) < 1 | abs(ib/ceq) > 1 // Frankel and Lee, page 291
drop temp* FROE
label var AnalystValue "Analyst Value"

// 238 Intrinsic value
gen FROE = ib/ceq
replace FROE = . if abs(FROE) > 1  // Frankel and Lee, page 291
 
gen tempBM = ceq/mve_c
xtset permno time_avail_m 

gen tempBMAve = (tempBM + l12.tempBM)/2
bys permno: replace tempBMAve = tempBM if _n <= 12
 
gen IntrinsicValue = (1 + (FROE - .1)/1.1 + (FROE - .1)/(.1*1.1))*tempBMAve
replace IntrinsicValue = . if ceq < 0 | abs(prc) < 1  // Frankel and Lee, page 291
drop temp* FROE
label var IntrinsicValue "Intrinsic Value"

// 239 Analyst Optimism
gen AOP = (AnalystValue - IntrinsicValue)/abs(IntrinsicValue)
label var AOP "Analyst Optimism"

// 240 Predicted earnings forecast error
gen BM 		=	log(ceq/mve_c)

bys time_avail_m: relrank sale, gen(tempRKSale) ref(sale)
by time_avail_m: relrank BM, gen(tempRKBM) ref(BM)
by time_avail_m: relrank AOP, gen(tempRKAOP) ref(AOP)
 
gen FROE = (meanest*shrout)/ceq
by time_avail_m: relrank FROE, gen(tempRKFROE) ref(FROE)
 
gen tempError = ib/ceq - FROE
 
gen PredictedFE = .

xtset permno time_avail_m
gen tempLag36RKSale = l36.tempRKSale
gen tempLag36RKBM   = l36.tempRKBM
gen tempLag36RKAOP  = l36.tempRKAOP
gen tempLag36RKFROE  = l36.tempRKFROE

levelsof time_avail_m 
foreach t of numlist `r(levels)' {
    
    cap drop tempY
    cap reg tempError tempLag36RKSale tempLag36RKBM tempLag36RKAOP tempLag36RKFROE if time_avail_m == `t'
    cap predict tempY if time_avail_m == `t'
    cap replace PredictedFE = tempY if time_avail_m == `t'
}

label var PredictedFE "Predicted Forecast Error"

// SAVE 
do "$pathCode/savepredictor" AnalystValue
do "$pathCode/savepredictor" IntrinsicValue
do "$pathCode/savepredictor" PredictedFE
do "$pathCode/savepredictor" AOP