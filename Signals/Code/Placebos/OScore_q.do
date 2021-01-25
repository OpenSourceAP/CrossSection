* --------------
// DATA LOAD
use permno gvkey time_avail_m sicCRSP prc using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(foptyq atq ltq actq lctq ibq oancfyq) nogenerate keep(match)
merge m:1 time_avail_m using "$pathDataIntermediate/GNPdefl", keep(match) nogenerate 
// SIGNAL CONSTRUCTION
xtset permno time_avail_m
replace foptyq = oancfyq if foptyq == .
gen OScore_q = -1.32 - .407*log(atq/gnpdefl) + 6.03*(ltq/atq) - 1.43*( (actq - lctq)/atq) + ///
    .076*(lctq/actq) - 1.72*(ltq>atq) - 2.37*(ibq/atq) - 1.83*(foptyq/ltq) + .285*(ibq + l12.ibq <0) - ///
    .521*( (ibq - l12.ibq)/(abs(ibq) + abs(l12.ibq)) )
    
destring sic, replace
replace OScore_q = . if (sicCRSP > 3999 & sicCRSP < 5000) | sicCRSP > 5999 

* form LS following Tab 5
egen tempsort = fastxtile(OScore), by(time_avail_m) n(10)
replace OScore = .
replace OScore = 1 if tempsort == 10
replace OScore = 0 if tempsort <= 7  & tempsort >= 1

label var OScore_q "O-Score (quarterly)"
// SAVE
do "$pathCode/saveplacebo" OScore_q
