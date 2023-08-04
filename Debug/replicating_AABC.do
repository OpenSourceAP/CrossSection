* --------------
* Import stuff


// Clean OptionMetrics data 
use "$pathDataIntermediate/OptionMetricsVolSurf", clear


keep if days == 30 & abs(delta) == 50
keep if year(dofm(time_avail_m)) >= 1996 & year(dofm(time_avail_m)) <= 2011

*keep if year(dofm(time_avail_m)) > 2011

rename impl_vol vol
keep secid time_avail_m cp_flag vol
reshape wide vol, i(secid time_avail_m) j(cp_flag) string

// Table 1
* we have about 500 more stocks but pretty close overall
gen year = year(dofm(time_avail_m))
preserve
	collapse (count) n = volP (mean) vol*, by(year)
	replace n = n/12
	list
restore	

* generate first differences (eq 2)
xtset secid time_avail_m
gen dvolC = volC - l1.volC
gen dvolP = volP - l1.volP
gen dP_minus_dC = dvolP - dvolC

save "$pathtemp/temp", replace


// DATA LOAD
use permno time_avail_m secid bh1m shrcd sicCRSP using "$pathDataIntermediate/SignalMasterTable", clear
gen retlead = 100*bh1m

* then add optionm data
merge m:1 secid time_avail_m using "$pathtemp/temp", keep(master match) nogenerate

// Table II A
* port 10 looks kinda bad, but otherwise sort is decent

preserve
	
	egen port = fastxtile(dvolC), by (time_avail_m) n(10)
	drop if port == .

	collapse (mean) retlead, by(time_avail_m port)
	reshape wide retlead, i(time_avail_m) j(port)
	gen retleadLS = retlead10 - retlead1
	summarize 
	regress retleadLS
restore



// Table II B
* So, OP actually also lacks monotonicity, so perhaps this is reasonably close
preserve	
	egen port = fastxtile(dvolP), by (time_avail_m) n(10)
	drop if port == .

	collapse (mean) retlead, by(time_avail_m port)
	reshape wide retlead, i(time_avail_m) j(port)
	gen retleadLS = retlead10 - retlead1
	summarize 
	regress retleadLS
restore


// Table II C
* gorgeous
preserve	
	egen port = fastxtile(dP_minus_dC), by (time_avail_m) n(10)
	drop if port == .

	collapse (mean) retlead, by(time_avail_m port)
	reshape wide retlead, i(time_avail_m) j(port)
	gen retleadLS = retlead10 - retlead1
	summarize 
	regress retleadLS
restore

