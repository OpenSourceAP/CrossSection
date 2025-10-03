** Download file
** Downloads and saves raw data from WRDS and other sources
* settings

/*
A. Three files have to be run in SAS and one in R for everything below to work!
    - Corwin_Schultz_Edit.sas
	- tr13f_download.sas
	- WRDS_DL_IBES.sas
	- R1_OptionMetrics.R

--------------------------------------------------------------------------------

B. To generate BidAskSpreadTAQ, you will need to run the files in the zip archive
   provided in the repo first!.
   
--------------------------------------------------------------------------------
  
Most of the code will work even you cannot run these files! But you will not be able
to generate IBES, 13F or OptionMetrics based signals (and no bid-ask spreads).	

--------------------------------------------------------------------------------

C. The code below processes and saves Stata versions of the following sources:

A. CCM Linking Table
B. Compustat Annual
C. Compustat Quarterly
D. Compustat Pensions
E. Compustat Segments 
F. Compustat Customer segments
G. Compustat Short interest
H. CRSP Distributions
I. CRSP monthly
J. CRSP daily
K. CRSP Acquisitions
L. IBES EPS
M. IBES Recommendations
N. IBES unadjusted actuals file
O. Daily Fama-French factors
P. Monthly Fama-French factors
Q. Monthly equal- and value-weighted market returns
R. Monthly liquidity factor
S. Q Factor Model
T. VIX data
U. GNP Deflator
V. 3-month T-bill rate
W. Broker-Dealer financial assets and liabilities
X. Credit ratings
Y. Original sin stock classifications
ZA. Ritter's IPO dates
ZB. Probability of informed trading
ZC. Governance index

--------------------------------------------------------------------------------
For the next ones, you need to run the SAS codes first:

ZD SAS 1. Corwin-Schultz bid-ask spreads
ZE SAS 2. 13F data
ZF SAS 3. CRSP-IBES linking files
ZG SAS 4. Bid-ask TAQ data

-------------------------------------------------------------------------------
For OptionMetrics, you will need to run the R code first (the remaining ones R2-R4 should call R from within Stata)

ZH R 1. OptionMetrics data
ZI R 2. Patent citation data
ZJ R 3. Input-Output Momentum
ZK R 4. Customer Segments

*/

* ------------------------------------------------------------------------------
* Check whether SAS-generated data exist
cap confirm file "$pathDataPrep/iclink.csv"

if _rc != 0 {
	di("IBES-CRSP link not available. Some signals cannot be generated")
}

* ------------------------------------------------------------------------------
* Log files 

* stata output log
cap log close
log using "$pathLogs/01_DownloadData.log", replace

* file for error flags
clear
gen DataFile = ""
gen double DataTime = .
gen ReturnCode = .
save "$pathLogs/01_DownloadDataFlags", replace

* ------------------------------------------------------------------------------
* Look-up scripts in DataDownload folder
filelist, pat("*.do") nor directory("$pathCodeDownloads")
sort filename
save "$pathtemp/tempFilenames", replace

* ------------------------------------------------------------------------------
* Loop over all download scripts

local obs = _N

forvalues i=1/`obs' {	
    
	use "$pathtemp/tempFilenames" in `i', clear
    local file = filename
	
    di "`file'"

    timer clear 1
    timer on 1 

	capture noisily do "$pathCodeDownloads/`file'"
	
	timer off 1
	
	clear
	set obs 1
	timer list
	gen DataFile = "`file'"
	gen DataTime = r(t1)
	gen ReturnCode = _rc
	
	append using "$pathLogs/01_DownloadDataFlags"
	save "$pathLogs/01_DownloadDataFlags", replace
	export delimited using "$pathLogs/01_DownloadDataFlags.csv", replace 
	
}

gen Message = "Processing successful" if ReturnCode == 0
replace Message = "Processing error" if mi(Message)

save "$pathLogs/01_DownloadDataFlags", replace  // Check this file for errors!!

di("The following download scripts did not complete succcessfully")
li if ReturnCode !=0

**********
erase "$pathtemp/tempFilenames.dta"
log close

