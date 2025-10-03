* --------------
// DATA LOAD
use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(foptyq oancfyq ibq atq dlttq actq lctq txtq xintq saleq ceqq) nogenerate keep(match)
merge 1:1 permno time_avail_m using "$pathDataIntermediate/monthlyCRSP", keep(match) nogenerate keepusing(shrout) 
// SIGNAL CONSTRUCTION
replace foptyq = oancfyq if foptyq == .
gen p1 = 0
replace p1 = 1 if ibq > 0 | !mi(ibq)
gen p2 = 0
replace p2 = 1 if (oancfyq > 0  & !mi(oancfyq)) | (mi(oancfyq) & !mi(foptyq) & foptyq > 0)
gen p3 = 0
replace p3 = 1 if (ibq/atq - l12.ibq/l12.atq)>0
gen p4 = 0
replace p4 = 1 if oancfyq > ibq
gen p5 = 0
replace p5 = 1 if dlttq/atq - l12.dlttq/l12.atq < 0
gen p6 = 0
replace p6 = 1 if actq/lctq - l12.actq/l12.lctq > 0
gen p7 = 0
gen tempebit = ibq + txtq + xintq
replace p7 = 1 if tempebit/saleq - tempebit/l12.saleq > 0
gen p8 = 0
replace p8 = 1 if saleq/atq - l12.saleq/l12.atq>0
gen p9 = 0
replace p9 = 1 if shrout <= l12.shrout  // this can be the same as in annual version
  
gen PS_q = p1 + p2 + p3 + p4 + p5 + p6 + p7 + p8 + p9
drop p1 p2 p3 p4 p5 p6 p7 p8 p9
replace PS_q = . if foptyq == . | ibq == . | atq == . | dlttq == . | saleq == . | actq == . ///
	| tempebit == . | shrout == .
	
gen BM = log(ceqq/mve_c)
egen temp = fastxtile(BM), by(time_avail_m) n(5)  // Find highest BM quintile
replace PS_q =. if temp != 5

label var PS_q "Piotroski F-score (quarterly)"
// SAVE
do "$pathCode/saveplacebo" PS_q