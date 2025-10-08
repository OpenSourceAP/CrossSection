* --------------
// DATA LOAD
use permno time_avail_m fopt oancf ib at dltt act lct txt xint sale ceq using "$pathDataIntermediate/m_aCompustat", clear
merge 1:1 permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", keep(match) nogenerate keepusing(mve_c) 
merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keep(match) nogenerate keepusing(shrout) 
// SIGNAL CONSTRUCTION
replace fopt = oancf if fopt == .
gen p1 = 0
replace p1 = 1 if ib > 0
gen p2 = 0
replace p2 = 1 if fopt > 0
gen p3 = 0
replace p3 = 1 if (ib/at - l12.ib/l12.at)>0
gen p4 = 0
replace p4 =1 if fopt > ib
gen p5 = 0
replace p5 = 1 if dltt/at - l12.dltt/l12.at < 0
gen p6 = 0
replace p6 = 1 if act/lct - l12.act/l12.lct > 0
gen p7 = 0
gen tempebit = ib + txt + xint
replace p7 = 1 if tempebit/sale - tempebit/l12.sale > 0
gen p8 = 0
replace p8 = 1 if sale/at - l12.sale/l12.at>0
gen p9 = 0
replace p9 = 1 if shrout <= l12.shrout
gen PS = p1 + p2 + p3 + p4 + p5 + p6 + p7 + p8 + p9
replace PS = . if fopt == . | ib == . | at == . | dltt == . | sale == . | act == . ///
	| tempebit == . | shrout == .	
	
gen BM = log(ceq/mve_c)
egen temp = fastxtile(BM), by(time_avail_m) n(5)  // Find highest BM quintile
replace PS =. if temp != 5

label var PS "Piotroski F-score"
// SAVE
do "$pathCode/savepredictor" PS