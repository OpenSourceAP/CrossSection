* SAS 3. CRSP-OPTION METRICS linking files -----------------------------------------------
import delimited "$pathDataPrep/oclink.csv", clear varnames(1)
bysort permno (score): keep if _n == 1  // If link to more than one permno, keep the best match

* rename ticker tickerIBES
keep if score <= 6  // score is 0 to 6.  6 seems to work best for Bali Hovak
rename score om_score
keep secid permno om_score
save "$pathDataIntermediate/OPTIONMETRICSCRSPLinkingTable", replace
