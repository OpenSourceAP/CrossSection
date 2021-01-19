** BidAskSpread
* -------------

// DATA LOAD
use "$pathDataIntermediate/BAspreadsCorwin.dta", clear

// SIGNAL CONSTRUCTION

* Construction is done in SAS code (Corwin_Schultz_Edit.sas)

label var BidAskSpread "Bid-ask spread"

// SAVE
do "$pathCode/savepredictor" BidAskSpread