* SignalMasterTable
* Holds monthly list of firms with identifiers and some meta information
* --------------

// DATA LOAD

* Start with monthly CRSP
u permno ticker exchcd shrcd time_avail_m mve_c prc ret sicCRSP using "$pathProject/Signals/Data/Intermediate/monthlyCRSP", clear

* Screen on Stock market information: common stocks and major exchanges 
keep if (shrcd == 10 | shrcd == 11 | shrcd == 12) & (exchcd == 1 | exchcd == 2 | exchcd == 3)

merge 1:1 permno time_avail_m using "$pathProject/Signals/Data/Intermediate/m_aCompustat", keepusing(gvkey sic) keep(master match) nogenerate  
rename sic sicCS

* Add IBES ticker
merge m:1 permno using "$pathProject/Signals/Data/Intermediate/IBESCRSPLinkingTable", keep(master match) nogenerate

* Finish master table
gen NYSE = exchcd == 1
xtset permno time_avail_m
gen bh1m  = f.ret  // Future buy and hold return

// SAVE 
keep gvkey permno ticker time_avail_m ret bh1m mve_c prc NYSE exchcd shrcd sicCS sicCRSP tickerIBES
compress

save "$pathProject/Signals/Data/Intermediate/SignalMasterTable", replace
