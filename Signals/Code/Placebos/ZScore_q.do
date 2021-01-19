* --------------
// DATA LOAD
use permno gvkey time_avail_m sicCRSP mve_c using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(actq lctq atq req atq niq xintq txtq ltq revtq) nogenerate keep(match)
// SIGNAL CONSTRUCTION
gen ZScore_q = 1.2*(actq - lctq)/atq + 1.4*(req/atq) + 3.3*(niq + xintq + txtq)/atq + ///
    .6*(mve_c/ltq) + revtq/atq
destring sic, replace
replace ZScore_q = . if (sicCRSP >3999 & sicCRSP < 4999) | sicCRSP > 5999
* returns are non-monotonic (see Panel A of original), so we want to exclude
* the lowest quintile of ZScores
egen tempsort = fastxtile(ZScore_q), by(time_avail_m) n(5)
replace ZScore_q = . if tempsort == 1
label var ZScore_q "Altman Z-Score (quarterly)"
// SAVE
do "$pathCode/saveplacebo" ZScore_q