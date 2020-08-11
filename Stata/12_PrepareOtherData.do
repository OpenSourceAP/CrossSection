** Import Other Data files
cd $pathdata

* 1. Governance Index
* 3. CPI 
* 3a. GNP price deflator
* 4. Compustat Pensions
* 5. CRSP Acquisition file
* 6. Corwin's bid-ask spreads
* 7. Jay Ritter's IPO dates
* 7a. Jay Ritter's updated IPO file
* 8. Daily Fama French Factors
* 9. Monthly Fama French Factors
* 10. Monthly market returns (equal and value weighted)
* 11. Original sin stock classifications
* 12. Compustat Segment data
* 13. Short interest
* 14. 13F data (most pre-processing is done in 1c_Download13FAndProcess.R)
* 15. OptionMetrics data (most pre-processing is done in 1b_DownloadOptionsAndProcess.R)
* 16. Liquidity factor
* 17. Probability of Informed Trading
* 18. Customer momentum (generated in R, here read in to Stata only)
* 19. Daily market returns
* 20. Trading cost from TAQ data (file by Andrew, runs in SAS on WRDS server)
* 21. Q-Factor data (daily)
* 22. VIX
* 23. Customer-Supplier momentum

* ---------------------------------------------------------------------------

* 1. Governance Index
import delimited "$pathProject/DataRaw/GovIndex.csv", clear varnames(1) delim(",")
gen temp = date(time_avail_m, "YMD")
drop time_avail_m
gen time_avail_m = mofd(temp)
format time_avail_m %tm
rename g G
rename g_binary G_Binary
drop temp
save "$pathProject/DataClean/GovIndex", replace

* 3. CPI
import delimited "$pathProject/DataRaw/CPI.csv", clear varnames(1) delim(",")
gen time_d = date(date, "YMD")
gen time_avail_m = mofd(time_d)
format time_avail_m %tm
drop time_d date
replace time_avail_m = time_avail_m + 3  // Assume that CPI is available with a 3 month lag
rename value cpi
replace cpi = cpi/100
save "$pathProject/DataClean/CPI", replace

* 3a. GNP price deflator
import delimited "$pathProject/DataRaw/GNPCTPI.csv", clear varnames(1) delim(",")
gen time_d = date(date, "YMD")
gen temp_time_m = mofd(time_d)
* Expand to monthly
expand 3
bys temp: gen time_avail_m = temp + _n - 1
format time_avail_m %tm
drop time_d date temp
replace time_avail_m = time_avail_m + 3  // Assume that CPI is available with a 3 month lag
gen gnpdefl = value/100
keep time gnpdefl

save "$pathProject/DataClean/GNPdefl", replace

* 4. Compustat Pensions
import delimited "$pathProject/DataRaw/CompustatPensions.csv", clear varnames(1)
gen time_d = date(datadate, "YMD")
format time_d %td
gen year = year(time_d)
replace year = year + 1  // Assume data available with a lag
bysort gvkey year: keep if _n == 1

drop datadate time*
mdesc  // Missing data for about 80% of firm-years in all but two variables

compress
save "$pathProject/DataClean/CompustatPensions", replace

* 5. CRSP Acquisition File
import delimited "$pathProject/DataRaw/mCRSPDistributionInfo.csv",clear
keep if acperm >999 & acperm <.
gen time_d = date(exdt, "YMD")
drop if missing(time_d)
format time_d %td
gen time_avail_m = mofd(time_d)
format time_avail_m %tm
drop time_d exdt 

* According to 
* http://www.crsp.com/products/documentation/distribution-codes
* distcd identifies true spinoffs using keep if distcd >= 3762 & distcd <= 3764
* But MP don't use it, and it results in a large share of months with no 
* spinoffs.

* turn into list of permnos which were created in spinoffs
gen SpinoffCo = 1
drop permno
rename acperm permno
keep permno SpinoffCo

* remove spinoffs which had multi-stock parents
duplicates drop
compress
save "$pathProject/DataClean/m_CRSPAcquisitions", replace

/*
import delimited DataRaw/mCRSPDistributionInfo.csv,clear
keep if acperm >999 & acperm <.
tostring exdt, replace
gen time_d = date(exdt, "YMD")
format time_d %td
gen time_avail_m = mofd(time_d)
format time_avail_m %tm
drop time_d exdt distcd acperm
gen Acquired = 1
bysort permno time_avail_m: keep if _n == 1

compress
save DataClean/m_CRSPAcquisitions, replace
*/

* 6. Corwin's bid-ask spreads
import delimited "$pathProject/DataRaw/corwin_schultz_spread.csv", clear varnames(1)
tostring month, replace
gen y = substr(month, 1,4)
gen m = substr(month, 5,2)
destring y m, replace
gen time_avail_m = ym(y, m)
format time_avail_m %tm
drop y m month

bysort permno time: keep if _n ==1  // Drop obs with missing permno and keep only one if more than one csid
drop if mi(permno)

compress
save "$pathProject/DataClean/BAspreadsCorwin", replace

* 7. Jay Ritter's IPO dates (File does not read easily into Stata)
/*import excel DataRaw/IPODatesJayRitter.xlsx, sheet("Table 1") clear
egen double temp = rowmin(B C D E F G)
tostring temp, replace
gen IPOdate_d = date(temp, "YMD")
format IPOdate_d %td
gen time_avail_m = mofd(IPOdate_d)
format time %tm

order IP*
gen cusipJR = H + I

tostring K, replace
gen permnoJR = J if K == "."
replace permnoJR = K if J == ""

rename N FoundingYear
rename O tickerJR

keep time_avail_m permno cusip ticker FoundingYear
destring permno, replace
drop if permno ==.

bysort permno time: keep if _n == 1 

compress
save DataClean/IPODates, replace
*/

* 7a. Jay Ritter's updated IPO file
import delimited "$pathProject/DataRaw/IPODates.csv", clear varnames(1)
rename founding FoundingYear
rename crspperm permno
tostring offerdate, replace
gen temp = date(offerdate, "YMD")
gen IPOdate = mofd(temp)
format IPOdate %tm

keep permno FoundingYear IPOdate
drop if mi(permno) | permno == 999 | permno <= 0
bys permno: keep if _n == 1
replace FoundingYear = . if FoundingYear < 0

save "$pathProject/DataClean/IPODatesV2", replace


* 8. Daily Fama French Factors
insheet using "$pathProject/DataRaw/dFamaFrench.csv", clear
gen time_d = date(date,"YMD")
format time_d %td
gen time_w = wofd(time_d)
format time_w %tw
drop date

compress
save "$pathProject/DataClean/dFF", replace

* 9. Monthly Fama French Factors
insheet using "$pathProject/DataRaw/mFamaFrench.csv", clear
gen time_d = date(date,"YMD")
format time_d %td
gen time_m = mofd(time_d)
format time_m %tm
drop date time_d
rename time_m time_avail_m

compress
save "$pathProject/DataClean/mFF", replace

* 10. Monthly market returns
insheet using "$pathProject/DataRaw/mMarket.csv", clear
gen time_d = date(date,"YMD")
format time_d %td
gen time_avail_m = mofd(time_d)
format time_avail_m %tm
drop date time_d

* Index market capitalization relative to July 1962 (for Acharya and Pedersen illiquidity measures)
sum usdval if time_avail_m == ym(1962,7)
replace usdval = usdval/`r(mean)'
rename usdval MarketCapitalization

compress
save "$pathProject/DataClean/mMarket", replace

* 11. Original sin stock classifications
import excel "$pathProject/DataRaw/SinStocksHong.xlsx", clear firstrow
replace begy = E if mi(begy)
replace endy = G if mi(endy)
keep permno begy endy
save "$pathProject/DataClean/SinStocksHong", replace

* 12. Compustat Segment data
import delimited "$pathProject/DataRaw/CompustatSegmentData.csv", clear varnames(1)
rename sics1 sic
gen sinInd = 0
replace sinInd = 1 if (sic >= 2100 & sic <= 2199) | (sic >=2080 & sic <= 2085) ///
	| ((naics == 7132) | (naics == 71312) | (naics == 713210) | ///
	(naics == 71329) | (naics == 713290) | (naics == 72112) | (naics == 721120))

bys gvkey: egen temp = max(sinInd)
keep if temp == 1

keep gvkey
duplicates drop  // THE CRITICAL ASSUMPTION HERE IS (AS IN THE ORIGINAL PAPER) THAT THE SIN INDICATOR PASSES TO THE ENTIRE HISTORY AND FUTURE OF A FIRM
save "$pathProject/DataClean/sinStocksAlgo", replace

* 13. Short interest from Compustat
import delimited "$pathProject/DataRaw/CompustatShortInterest.csv", clear varnames(1)
gen time_d = date(datadate, "YMD")
format time_d %td
gen time_avail_m = mofd(time_d)
format time_avail_m %tm

collapse (firstnm) shortint shortintadj, by(gvkey time_avail_m)  // Data reported bi-weekly and made available with a four day lag (according to
							   // Rapach et al. (2016). As they do, we use the mid-month observation to make sure 
							   // Data would be available in real time

save "$pathProject/DataClean/m_ShortInterest", replace

* 14. 13F data
import delimited "$pathProject/DataRaw/TR_13F.csv", clear varnames(1)
drop if mi(permno)
destring instown_perc maxinstown_perc numinstown, replace force

gen time_d = date(rdate,"DMY")
gen time_avail_m = mofd(time_d) // + 1  // WHAT'S THE REPORTING LAG FOR THESE DATA? WHAT WAS IT IN THE 80S?
format time_avail_m %tm
drop rdate time_d

* Fill in missing months
xtset permno time_avail_m
tsfill
sort permno time_avail_m
foreach v of varlist numinstown instown_perc dbreadth maxinstown_perc numinstown numinstblock {
	replace `v' = `v'[_n-1] if permno == permno[_n-1] & mi(`v') 
}

compress
save "$pathProject/DataClean/TR_13F", replace

* 15. OptionMetrics data
import delimited "$pathProject/DataRaw/OptionMetrics.csv", clear varnames(1)
drop if mi(ticker)
gen time_d = date(time_avail_m,"YMD")
drop time_avail_m
gen time_avail_m = mofd(time_d)
format time_avail_m %tm

compress
bys ticker time_a: keep if _n == 1

drop secid time_d cusip
order ticker time_a
save "$pathProject/DataClean/OptionMetrics", replace

* 16. Liquidity Factor
import delimited using "$pathProject/DataRaw/mLiquidityFactor.csv", clear
gen time_d = date(date,"YMD")
format time_d %td
gen time_m = mofd(time_d)
format time_m %tm
drop date time_d
rename time_m time_avail_m

compress
save "$pathProject/DataClean/mLiquidity", replace

* 17. Probability of Informed Trading
import delimited using "$pathProject/DataRaw/pin1983-2001.dat", delimiter(whitespace, collapse) clear
rename permn permno
replace year = year +1  // To trade on information from previous year
compress
save "$pathProject/DataClean/aInformedTrading", replace

* 18. Customer momentum
import delimited using "$pathProject/DataRaw/customerMom.csv", clear
gen temp = date(time_avail_m, "YMD")
drop time_avail_m
gen time_avail_m  = mofd(temp)
format time_avail_m %tm
drop temp
compress
save "$pathProject/DataClean/customerMom", replace


* 19. Daily market returns
insheet using "$pathProject/DataRaw/dMarket.csv", clear
gen time_d = date(date,"YMD")
format time_d %td
drop date

compress
save "$pathProject/DataClean/dMarket", replace

* 20. Trading cost
import delimited using "$pathProject/DataClean/tcosts_CV_20191203.csv", clear
tostring month, replace
gen y = substr(month, 1, 4)
gen m = substr(month, 5, 2)
destring y m, replace
gen time_avail_m = ym(y, m)
format time_avail_m %tm

keep permno time_avail_m tcost 
compress
save "$pathProject/DataClean/tcost_TAQ", replace

* 21. Q-factor data (daily)
import delimited "$pathProject/DataRaw/D_qfactor.csv", clear
rename r_* r_*_qfac
tostring date, replace
gen time_d = date(date, "YMD")
format time_d %td
drop date

foreach v of varlist r_* {
	replace `v' = `v'/100
}

save "$pathProject/DataClean/d_qfactor", replace

* 22. VIX
import delimited using "$pathProject/DataRaw/VIX.csv", clear varnames(1) delim(",")
rename value vix
gen time_d = date(date, "YMD")
format time_d %td
drop date
gen time_temp = _n
tsset time_temp
gen dVIX = vix - l.vix
drop time_temp

compress
save "$pathProject/DataClean/d_vix", replace

* 23. Customer-Supplier momentum
import delimited using "$pathProject/DataRaw/InputOutputMomentum.csv", clear
gen time_avail_m = ym(year_avail, month_avail)
format time_avail_m %tm

collapse (mean) iomom*, by(gvkey time_avail_m)  // A few observations are duplicates

save "$pathProject/DataClean/InputOutputMomentum", replace
