* --------------
// THIS SIGNAL IS CONSTRUCTED IN R3_InputOutputMomentum.R !! 
** Run R3_InputOutputMomentum.R before executing the rest of this file** (see 01_DownloadData.do)
// DATA LOAD
use permno gvkey time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
drop if gvkey ==.
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/InputOutputMomentumProcessed", keep(master match) nogenerate

// SIGNAL CONSTRUCTION
replace iomom_cust = floor(iomom_cust)
gen temp = 1 if iomom_cust >= 8 & !mi(iomom_cust)
replace temp = 0 if iomom_cust <= 1
replace iomom_cust = temp
label var iomom_cust "IO customer momentum"

// SAVE
do "$pathCode/savepredictor" iomom_cust
