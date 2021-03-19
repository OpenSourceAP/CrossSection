* BetaBDLeverage
* --------------

// DATA LOAD
use permno time_avail_m ret using "$pathDataIntermediate/SignalMasterTable", clear

// SIGNAL CONSTRUCTION
replace ret = 0 if mi(ret)

* Collapse to quarterly returns
gen year = year(dofm(time_avail_m))
gen qtr = quarter(dofm(time_avail_m))

replace ret = 0 if mi(ret)

bys permno year qtr (time_avail_m): gen RetQ = (1+ret)*(1+ret[_n+1])*(1+ret[_n+2]) - 1 if _n == 1
keep if !mi(RetQ)

keep permno year qtr RetQ

* Merge BD leverage and T-bill rate
merge m:1 year qtr using "$pathDataIntermediate/brokerLev", keep(master match) nogenerate
merge m:1 year qtr using "$pathDataIntermediate/TBill3M", keep(master match) nogenerate

* Prepare and run regression
replace RetQ = RetQ - TbillRate3M

gen tempTime = yq(year, qtr)
format tempTime %tq

xtset permno tempTime
asreg RetQ levfac, window(tempTime 40) min(20) by(permno) 

* Lag by one quarter to make sure that beta is available
gen BetaBDLeverage = l._b_levfac

keep permno year qtr BetaBDLeverage

label var BetaBDLeverage "Broker-Dealer Leverage Beta"

* Spread out to monthly dataset
save "$pathtemp/temp", replace
use permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear
gen qtr = quarter(dofm(time_avail_m))
gen year = year(dofm(time_avail_m))
merge m:1 permno year qtr using "$pathtemp/temp", keep(master match) nogenerate

* remove firms with less than 20 quarters of return dataset
sort permno time_avail_m
bys permno: gen age = _n
replace BetaBDLeverage = . if age <= 20/4*12

// SAVE
do "$pathCode/saveplacebo" BetaBDLeverage
