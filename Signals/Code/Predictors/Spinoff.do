* --------------
// DATA LOAD
use permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
merge m:1 permno using "$pathDataIntermediate/m_CRSPAcquisitions", keep(master match) nogenerate 

// SIGNAL CONSTRUCTION
bys permno (time_avail_m): gen FirmAgeNoScreen = _n
gen Spinoff = 1 if SpinoffCo == 1 & FirmAgeNoScreen <= 24
replace Spinoff = 0 if Spinoff ==.
label var Spinoff "Spinoff"

// SAVE
do "$pathCode/savepredictor" Spinoff
