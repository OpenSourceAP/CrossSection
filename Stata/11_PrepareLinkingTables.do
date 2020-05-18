*** Prepare Compustat-CRSP linkingtable ***

* CRSP-IBES link
import delimited "$pathdata/DataRawAndrew/iclink.csv", clear varnames(1)
keep if score <= 2  // WHICH LINKS DO WE WANT TO KEEP?
bysort permno (score): keep if _n == 1  // If link to more than one permno, keep the best match
rename ticker tickerIBES
keep tickerIBES permno
save "$pathProject/DataClean/IBESCRSPLinkingTable", replace

* CRSP-Compustat (annual)
import delimited "$pathProject/DataRaw/CCMLinkingTable.csv", clear

gen timeLinkStart_d = date(linkdt, "YMD")
gen timeLinkEnd_d   = date(linkenddt, "YMD")
format timeLink* %td

drop linkdt linkenddt

compress
save "$pathProject/DataClean/CCMLinkingTable", replace
