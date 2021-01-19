* betaRR, betaCC, betaRC, betaCR, betaNet
* --------------

// DATA LOAD

* Compute illiquidity from daily CRSP data
use permno time_d ret vol prc using  "$pathDataIntermediate/dailyCRSP", clear

gen time_avail_m = mofd(time_d)
format time_avail_m %tm

gen double ill  = (abs(ret)/(abs(prc)*vol)) * 10^6 // Scaling as in Acharya and Pedersen (2005)
gcollapse (mean) ill, by(permno time_avail_m)

save "$pathtemp/tempILL", replace

* Load monthly data
use permno time_avail_m ret prc exchcd shrout using "$pathDataIntermediate/monthlyCRSP", clear
merge 1:1 permno time_avail_m using "$pathtemp/tempILL", keep(master match) keepusing(ill) nogenerate
merge m:1 time_avail_m using "$pathDataIntermediate/monthlyMarket",  nogenerate keep(match) keepusing(vwretd usdval)

// SIGNAL CONSTRUCTION

* Index market capitalization relative to July 1962
sum usdval if time_avail_m == ym(1962,7)
replace usdval = usdval/`r(mean)'
rename usdval MarketCapitalization

xtset permno time_avail_m
gen double c_i = min(.25 +.3*ill*MarketCapitalization, 30)  // Amounts to winsorization of 10% of data

* Compute market illiquidity innovation and market return innovation
preserve

    // Filters in Acharya and Pedersen (2005)
    keep if abs(prc) > 5 & abs(prc) < 1000  
	keep if exchcd == 1 | exchcd == 2

	gen temp = shrout*abs(prc)  // Market cap of stock i
	gen double temp2 = min(ill, (30-.25)/(.3*MarketCapitalization))  // Unnormalized liquidity
	replace temp2 = . if mi(ill)
	gcollapse (mean) MarketIlliquidity = temp2 rM = vwretd MarketCapitalization [aweight = temp], by(time_avail_m)

	tsset time_avail_m
	gen double temp = .25 + MarketIlliquidity*l.MarketCapitalization
	gen double templ1 = .25 + l.MarketIlliquidity*l.MarketCapitalization
	gen double templ2 = .25 + l2.MarketIlliquidity*l.MarketCapitalization

	asreg temp templ1 templ2, window(time 60) min(48) fitted
	rename _residuals eps_c_M
	rename _b_cons APa0
	rename _b_templ1 APa1
	rename _b_templ2 APa2  // Acharya and Pedersen use coefficients from market model to compute stock (portfolio) illiquidity innovations
	drop _*

	gen tempRlag1 = l.rM
	gen tempRlag2 = l2.rM
	asreg rM tempRlag1 tempRlag2, window(time 60) min(48) fitted
	rename _residuals eps_r_M

	keep time_avail_m eps* AP*
	save "$pathtemp/tempPlacebo", replace

restore

merge m:1 time_avail_m using "$pathtemp/tempPlacebo", keep(master match) nogenerate
xtset permno time_avail_m

* Compute stock-level innovation in illiquidity (using coefficients from market model, see WP of Acharya and Pedersen)
gen double tempIll = min(ill, (30-.25)/(.3*MarketCapitalization))
gen double temp = .25 + tempIll*l.MarketCapitalization
gen double templ1 = .25 + l.tempIll*l.MarketCapitalization
gen double templ2 = .25 + l2.tempIll*l.MarketCapitalization
	
gen eps_c_i = temp - (APa0 + APa1*templ1 + APa2*templ2)

* Compute betas (requires some work because covariances are not implemented in asrol)
asrol ret eps_r_M eps_c_i eps_c_M, window(time_avail_m 60) min(24) stat(mean) by(permno)
gen tempEpsDiff = eps_r_M - eps_c_M
asrol tempEpsDiff, window(time 60) min(24) stat(sd) by(permno)  // To make steps easier to follow, could have done this above in preserve/restore step
replace sd60_tempEpsDiff = sd60_tempEpsDiff^2

gen tempRR = (ret - mean60_ret)*(eps_r_M - mean60_eps_r_M)
gen tempCC = (eps_c_i - mean60_eps_c_i)*(eps_c_M - mean60_eps_c_M)
gen tempRC = (ret - mean60_ret)*(eps_c_M - mean60_eps_c_M)
gen tempCR = (eps_c_i - mean60_eps_c_i)*(eps_r_M - mean60_eps_r_M)

asrol tempRR tempCC tempRC tempCR, window(time 60) min(24) stat(mean) by(permno)

gen betaRR = mean60_tempRR/sd60_tempEpsDiff
gen betaCC = mean60_tempCC/sd60_tempEpsDiff
gen betaRC = mean60_tempRC/sd60_tempEpsDiff
gen betaCR = mean60_tempCR/sd60_tempEpsDiff
gen betaNet = betaRR + betaCC - betaRC - betaCR

foreach v of varlist betaRR betaCC betaRC betaCR betaNet {

replace `v' = . if  abs(prc) > 1000
}

label var betaRR "Liquidity beta (return-return)"
label var betaCC "Liquidity beta (ill-ill)"
label var betaRC "Liquidity beta (return-ill)"
label var betaCR "Liquidity beta (ill-return)"
label var betaNet "Liquidity beta (Net)"


// SAVE
do "$pathCode/saveplacebo" betaRR
do "$pathCode/saveplacebo" betaCC
do "$pathCode/saveplacebo" betaRC
do "$pathCode/saveplacebo" betaCR
do "$pathCode/saveplacebo" betaNet