* --------------
// THIS SIGNAL IS CONSTRUCTED IN R3_InputOutputMomentum.R !! 
** Run R3_InputOutputMomentum.R before executing the rest of this file** (see 01_DownloadData.do)
// DATA LOAD
use permno gvkey time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
drop if gvkey ==.
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/InputOutputMomentumProcessed", keep(master match) nogenerate

// SIGNAL CONSTRUCTION
replace iomom_supp = floor(iomom_supp)
gen temp = 1 if iomom_supp >= 8 & !mi(iomom_supp)
replace temp = 0 if iomom_supp <= 1
replace iomom_supp = temp
label var iomom_supp "IO supplier momentum"

// SAVE
do "$pathCode/savepredictor" iomom_supp
