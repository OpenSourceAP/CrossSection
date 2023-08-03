* --------------
// THIS SIGNAL IS CONSTRUCTED IN R3_InputOutputMomentum.R !! 
** Run R3_InputOutputMomentum.R before executing the rest of this file** (see 01_DownloadData.do)
// DATA LOAD
use permno gvkey time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
drop if gvkey ==.
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/InputOutputMomentumProcessed", keep(master match) nogenerate

// SIGNAL CONSTRUCTION
gen iomom_supp = retmatchsupplier
keep if iomom_supp != .
label var iomom_supp "IO supplier momentum"

// SAVE
do "$pathCode/savepredictor" iomom_supp
