* --------------
// DATA LOAD
use gvkey permno time_avail_m fyear datadate ceq ib sale prcc_f csho using "$pathDataIntermediate/a_aCompustat", clear
// SIGNAL CONSTRUCTION
xtset gvkey fyear
* Compute ROE, book equity growth, and cash distributions to equity
gen tempRoE = ib/l.ceq //ROE
gen temp_g_eq = sale/l.sale - 1 //Growth in equity
gen tempCD = l.ceq*(tempRoE - temp_g_eq) //Cash distribution to equity
*Inputs used from the paper
//Autocorrelation coefficient for return on equity = 0.57
//Cost of equity capital = 0.12
//Autocorrelation coefficient for growth in sales/book value = 0.24
//Long-run growth rate in sales/book value = 0.06
* Project the variables forward
gen tempRoE1 = .57 * tempRoE + .12 * (1-.57)
gen temp_g_eq1 = .24 * temp_g_eq + .06 * (1-.24)
gen tempBV1= ceq * (1+temp_g_eq1)
gen tempCD1 = ceq - tempBV1 + ceq * tempRoE1

foreach t of numlist 2/10{

local j = `t'-1

gen tempRoE`t' = .57 * tempRoE`j' + .12 * (1-.57)

gen temp_g_eq`t' = .24 * temp_g_eq`j' + .06 * (1-.24)

gen tempBV`t'= tempBV`j' * (1+temp_g_eq`t')

gen tempCD`t'= tempBV`j' - tempBV`t' + tempBV`j' * tempRoE`t' 
}
gen MD_Part1 = 1*tempCD1/(1+.12) + 2*tempCD2/(1+.12)^2 + 3*tempCD3/(1+.12)^3 ///
    + 4*tempCD4/(1+.12)^4 + 5*tempCD5/(1+.12)^5 + 6*tempCD6/(1+.12)^6 ///
    + 7*tempCD7/(1+.12)^7 + 8*tempCD8/(1+.12)^8 + 9*tempCD9/(1+.12)^9 ///
    + 10*tempCD10/(1+.12)^10

gen PV_Part1 = tempCD1/(1+.12) + tempCD2/(1+.12)^2 + tempCD3/(1+.12)^3 ///
    + tempCD4/(1+.12)^4 + tempCD5/(1+.12)^5 + tempCD6/(1+.12)^6 ///
    + tempCD7/(1+.12)^7 + tempCD8/(1+.12)^8 + tempCD9/(1+.12)^9 ///
    + tempCD10/(1+.12)^10
*Compute equity duration
gen tempME = prcc_f*csho
gen tempED = PV_Part1/tempME * MD_Part1 + (10 + (1+.12)/.12)*(1-PV_Part1/tempME)
* gen EquityDuration = l.tempED // Lag the equity duration
gen EquityDuration = tempED // no lag - ac 2020 11 12
* Exclusions: Exclude firms that have a negative book equity at some point
egen tempBE = min(ceq), by(gvkey)
replace EquityDuration = . if tempBE < 0
drop temp*
label var EquityDuration "Equity Duration"
* Expand to monthly
gen temp = 12
expand temp
drop temp
gen tempTime = time_avail_m
bysort gvkey tempTime: replace time_avail_m = time_avail_m + _n - 1 
drop tempTime
bysort gvkey time_avail_m (datadate): keep if _n == _N 
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
// SAVE
do "$pathCode/savepredictor" EquityDuration