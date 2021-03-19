* BMq
* --------------

// DATA LOAD
use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
keep if !mi(gvkey)

merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_QCompustat", keepusing(ceqq) nogenerate keep(match)

// SIGNAL CONSTRUCTION
gen BMq 		=	log(ceqq/mve_c)

label var BMq "Book-to-market quarterly"

// SAVE
do "$pathCode/saveplacebo" BMq