* BidAskTAQ
* --------------

// THIS SIGNAL IS CONSTRUCTED USING THE SAS CODE IN THE ZIP FOLDER !! (SEE REPO)

// DATA LOAD
use "$pathDataIntermediate/tcost_TAQ", clear

// SIGNAL CONSTRUCTION
rename tcost BidAskTAQ
label var BidAskTAQ "Bid-ask spread (TAQ data)"

// SAVE
do "$pathCode/saveplacebo" BidAskTAQ