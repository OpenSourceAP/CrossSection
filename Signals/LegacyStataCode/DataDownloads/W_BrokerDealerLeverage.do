* 23. Broker-Dealer financial assets and liabilities----------------------------
import fred BOGZ1FL664090005Q, clear
rename BOGZ1FL664090005Q assets
drop datestr
save "$pathtemp/temp", replace

import fred BOGZ1FL664190005Q, clear
rename BOGZ1FL664190005Q liab
drop datestr
merge 1:1 daten using "$pathtemp/temp", nogenerate
save "$pathtemp/temp", replace

import fred BOGZ1FL665080003Q, clear
rename BOGZ1FL665080003Q equity
drop datestr
merge 1:1 daten using "$pathtemp/temp", nogenerate

gen qtr = quarter(daten)
gen year = yofd(daten)
gen lev = assets/equity 

drop if year < 1968

gen levfacnsa = log(lev) - log(lev[_n-1])

* Compute seasonal adjustment (rolling mean of quarter values)
bys qtr (year): gen tempMean = sum(levfacnsa)/_n
bys qtr (year): replace tempMean = sum(levfacnsa)/(_n-1) if qtr == 1

replace tempMean = 0 if year == 1968

by qtr: gen levfac = levfacnsa - tempMean[_n-1]
by qtr: replace levfac = levfacnsa if _n==1
replace levfac = levfacnsa if qtr ==1 & year == 1969

keep year qtr levfac
sort year qtr

compress
save "$pathDataIntermediate/brokerLev", replace

erase "$pathtemp/temp.dta"
