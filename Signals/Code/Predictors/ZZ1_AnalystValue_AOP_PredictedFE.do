* AnalystValue, AOP, PredictedFE
* IntrinsicValue is created in this code but is not saved since it
* wasn't shown to predict returns in the OP
* Our AnalystValue is a simplification of OP, which means all of the others 
* are even further from OP
* --------------
// Prep IBES data
use "$pathDataIntermediate/IBES_EPS_Unadj", replace
keep if fpi == "1" & month(statpers) == 5
keep if fpedats != . & fpedats > statpers + 30 // keep only forecasts past June
replace time_avail_m = time_avail_m + 1 // OP is conservative, this matches with Compustat following FF

save "$pathtemp/temp", replace

// DATA LOAD
use permno tickerIBES time_avail_m prc using "$pathDataIntermediate/SignalMasterTable", clear
merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keep(master match) nogenerate keepusing(shrout) 
merge 1:1 permno time_avail_m using "$pathDataIntermediate/m_aCompustat", keep(master match) nogenerate keepusing(ceq ib sale datadate)
merge m:1 tickerIBES time_avail_m using "$pathtemp/temp", keep(match) nogenerate keepusing(meanest) 

* common screens and variables
sort permno time_avail_m
xtset permno time_avail_m

gen mve_c = (shrout * abs(prc))
gen FROE = (meanest*shrout)/ceq
gen FROEi = ib/ceq

gen ceq_ave = (ceq + l12.ceq)/2
bys permno (time_avail_m): replace ceq_ave = ceq if _n <= 1

drop if ceq < 0 | ceq == . // Frankel and Lee, page 291
drop if abs(FROEi) > 1 | abs(FROE) > 1 // Frankel and Lee, page 291
keep if month(datadate) >= 6


// SIGNAL CONSTRUCTION (annual)
gen AnalystValue = (1 + (FROE - .1)/1.1 + (FROE - .1)/(.1*1.1))*ceq_ave/mve_c
gen IntrinsicValue = (1 + (FROEi - .1)/1.1 + (FROEi - .1)/(.1*1.1))*ceq_ave/mve_c
gen AOP = (AnalystValue - IntrinsicValue)/abs(IntrinsicValue)



// 240 Predicted earnings forecast error
gen BM 		=	log(ceq/mve_c)

bys time_avail_m: relrank sale, gen(tempRKSale) ref(sale)
by time_avail_m: relrank BM, gen(tempRKBM) ref(BM)
by time_avail_m: relrank AOP, gen(tempRKAOP) ref(AOP)
by time_avail_m: relrank FROE, gen(tempRKFROE) ref(FROE)
 



gen PredictedFE = .

sort permno time_avail_m
xtset permno time_avail_m
gen tempError = l12.FROE  - ib/ceq  
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


// SAVE 
do "$pathCode/savepredictor" AnalystValue
do "$pathCode/savepredictor" AOP
do "$pathCode/savepredictor" PredictedFE

