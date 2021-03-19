* CustomerMomentum
* --------------

// THIS SIGNAL IS CONSTRUCTED IN R4_CustomerMomentum.R !! 

** Run R4_CustomerMomentum.R before executing the rest of this file** (see 01_DownloadData.do)

// DATA LOAD
use "$pathDataIntermediate/customerMom", clear

// SIGNAL CONSTRUCTION
rename custmom CustomerMomentum
label var CustomerMomentum "Customer momentum"

// SAVE
do "$pathCode/savepredictor" CustomerMomentum