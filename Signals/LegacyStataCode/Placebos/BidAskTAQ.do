* BidAskTAQ
* --------------

* as of 2022 02 this is technically BidAskTAQandISSM, but we're too lazy
* to relabel

// DATA LOAD
use "$pathDataIntermediate/hf_spread", clear

// SIGNAL CONSTRUCTION
rename hf_spread BidAskTAQ
label var BidAskTAQ "Bid-ask spread (TAQ + ISSM data)"

// SAVE
do "$pathCode/saveplacebo" BidAskTAQ
