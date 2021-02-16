* --------------
// DATA LOAD
use permno gvkey time_avail_m shrcd mve_c using "$pathDataIntermediate/SignalMasterTable", clear
drop if mi(gvkey)
gen year = yofd(dofm(time_avail_m))
merge m:1 gvkey year using "$pathDataIntermediate/CompustatPensions", keep(match) nogenerate
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_aCompustat", keep(master match) nogenerate keepusing(at)

// SIGNAL CONSTRUCTION
gen FVPA = pbnaa if year >=1980 & year <=1986
replace FVPA = pplao + pplau if year >=1987 & year <= 1997
replace FVPA = pplao if year >= 1998
gen PBO = pbnvv if year >= 1980 & year <=1986
replace PBO = pbpro + pbpru if year >= 1987 & year <=1997
replace PBO = pbpro if year >=1998
gen FR = (FVPA - PBO)/mve_c
replace FR = . if shrcd > 11
label var FR "Pension Funding Status"

gen FRbook = (FVPA - PBO)/at
replace FRbook = . if shrcd > 11
label var FRbook "Pension Funding Status (scaled by book assets)"

// SAVE
do "$pathCode/savepredictor" FR
do "$pathCode/saveplacebo" FRbook
