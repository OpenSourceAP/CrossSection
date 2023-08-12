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

* add some auxiliary vars and clean up
gen NYSE = exchcd == 1
xtset permno time_avail_m
gen bh1m  = f.ret  // Future buy and hold return

keep gvkey permno ticker time_avail_m ret bh1m mve_c prc NYSE exchcd shrcd sicCS sicCRSP 


* note: these additional linking tables only have two vars each (permno, alternate id)

* Add IBES ticker (if available)
cap confirm file "$pathProject/Signals/Data/Intermediate/IBESCRSPLinkingTable.dta"

if _rc == 0 {
    merge m:1 permno using "$pathProject/Signals/Data/Intermediate/IBESCRSPLinkingTable", keep(master match) nogenerate
} 
  else {
    di("Not adding IBES-CRSP link. Some signals cannot be generated.")
}

* Add OptionMetrics secid (if available)
cap confirm file "$pathProject/Signals/Data/Intermediate/OPTIONMETRICSCRSPLinkingTable.dta"

if _rc == 0 {
    merge m:1 permno using "$pathProject/Signals/Data/Intermediate/OPTIONMETRICSCRSPLinkingTable", keep(master match) nogenerate
} 
  else {
    di("Not adding Option Metrics-CRSP link. Some signals cannot be generated.")
}

// reinforce sort
xtset permno time_avail_m

// SAVE
compress

save "$pathProject/Signals/Data/Intermediate/SignalMasterTable", replace
