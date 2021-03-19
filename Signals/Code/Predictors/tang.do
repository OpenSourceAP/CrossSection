* --------------
// DATA LOAD
use permno time_avail_m che rect invt ppegt at sic using "$pathDataIntermediate/m_aCompustat", clear
bysort permno time_avail_m: keep if _n == 1  // deletes a few observations
// SIGNAL CONSTRUCTION
destring sic, replace
drop if sic < 2000 | sic > 3999  // Manufacturing firms only
egen tempFC = fastxtile(at), n(10) by(time_avail_m)
gen FC = 1 if tempFC <=3  // Lower three deciles are defined as financially constrained
replace FC = 0 if tempFC >=8 & !mi(tempFC)
gen tang = (che + .715*rect + .547*invt + .535*ppegt)/at 
label var tang "Tangibility"
// SAVE
do "$pathCode/savepredictor" tang