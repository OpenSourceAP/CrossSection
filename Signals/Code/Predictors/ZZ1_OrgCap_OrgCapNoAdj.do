// 2021 AC
// OP actually is value weighted, we previously had EW
// also updated: dec and sic restriction, missing xsga => 0,  drop OrgCapNoAdj == 0
// also updated: price index deflation (using GNP defl), this helps too
// Keeping only december fyr ends is absolutely critical for some reason
// Is the unadjusted version even predictive? 
//	I don't see it in OP.  Page 18 top discusses the industry adjustment
// 	HXZ find that it is in the full sample, with deciles
//	it seems that in our data, deciles is required to make this predictive, 
//	and it works a lot better in the full sample (post 2008)
// OP gets tstat of 2.85 for OrgCap, we get 2.3 ish, 
// 	perhaps because we skip the cpi
// OrgCapNoAdj is not predictive for us, t-stat = 1.20 insamp, but works better postpub
//	and also in deciles


* --------------
// DATA LOAD
use permno time_avail_m sicCRSP shrcd exchcd using "$pathDataIntermediate/SignalMasterTable", clear
merge 1:1 permno time_avail_m using "$pathDataIntermediate/m_aCompustat", nogenerate keepusing(xsga at datadate sic) keep(master match)
merge m:1 time_avail_m using "$pathDataIntermediate/GNPdefl", keep(match) nogenerate
destring sic, replace
keep if month(datadate) == 12 & (sic < 6000 | sic >= 7000) ///
	& sic != . //OP p 18, the dec fyr end is critical for some reason

	
// SIGNAL CONSTRUCTION
xtset permno time_avail_m
bys permno (time_avail_m): gen tempAge = _n 
replace xsga = 0 if xsga == . // OP (p 17) 
replace xsga = xsga/gnpdefl // supposed to use cpi, but gnpdefl is used in Oscore

* CHECKPOINT 1: Check data for problem observations before OrgCapNoAdj calculation
list permno time_avail_m tempAge xsga gnpdefl at if (permno == 13812 & time_avail_m == tm(2024m6)) | ///
                                                     (permno == 14925 & time_avail_m == tm(2024m6)) | ///
                                                     (permno == 24087 & time_avail_m == tm(2024m6)) | ///
                                                     (permno == 89698 & time_avail_m == tm(2024m6))

gen OrgCapNoAdj     = 4*xsga if tempAge <= 12 
replace OrgCapNoAdj = .85*l12.OrgCapNoAdj + xsga if tempAge > 12
replace OrgCapNoAdj = OrgCapNoAdj/at

* CHECKPOINT 2: Check OrgCapNoAdj calculation for problem observations
list permno time_avail_m OrgCapNoAdj l12.OrgCapNoAdj if (permno == 13812 & time_avail_m == tm(2024m6)) | ///
                                                         (permno == 14925 & time_avail_m == tm(2024m6)) | ///
                                                         (permno == 24087 & time_avail_m == tm(2024m6)) | ///
                                                         (permno == 89698 & time_avail_m == tm(2024m6))

replace OrgCapNoAdj = . if OrgCapNoAdj == 0 // OP p 18: works better without this
label var OrgCapNoAdj "Organizational capital without industry adjustment"

*Adjusted version
winsor2 OrgCapNoAdj, suffix("temp") cuts(1 99) by(time_avail_m)

* CHECKPOINT 3: Check winsorized values for problem observations
list permno time_avail_m OrgCapNoAdj OrgCapNoAdjtemp if (permno == 13812 & time_avail_m == tm(2024m6)) | ///
                                                         (permno == 14925 & time_avail_m == tm(2024m6)) | ///
                                                         (permno == 24087 & time_avail_m == tm(2024m6)) | ///
                                                         (permno == 89698 & time_avail_m == tm(2024m6))

sicff sicCRSP, generate(tempFF17) industry(17)
drop if mi(tempFF17)

* CHECKPOINT 4: Check FF17 industry classification for problem observations  
list permno time_avail_m sicCRSP tempFF17 if (permno == 13812 & time_avail_m == tm(2024m6)) | ///
                                             (permno == 14925 & time_avail_m == tm(2024m6)) | ///
                                             (permno == 24087 & time_avail_m == tm(2024m6)) | ///
                                             (permno == 89698 & time_avail_m == tm(2024m6))

egen tempMean = mean(OrgCapNoAdjtemp), by(tempFF17 time_avail_m)
egen tempSD   = sd(OrgCapNoAdjtemp), by(tempFF17 time_avail_m)

* CHECKPOINT 5: Check industry mean and SD for problem observations
list permno time_avail_m tempFF17 tempMean tempSD if (permno == 13812 & time_avail_m == tm(2024m6)) | ///
                                                      (permno == 14925 & time_avail_m == tm(2024m6)) | ///
                                                      (permno == 24087 & time_avail_m == tm(2024m6)) | ///
                                                      (permno == 89698 & time_avail_m == tm(2024m6))

gen OrgCap = (OrgCapNoAdjtemp - tempMean)/tempSD

* CHECKPOINT 6: Check final OrgCap values for problem observations
list permno time_avail_m OrgCap if (permno == 13812 & time_avail_m == tm(2024m6)) | ///
                                   (permno == 14925 & time_avail_m == tm(2024m6)) | ///
                                   (permno == 24087 & time_avail_m == tm(2024m6)) | ///
                                   (permno == 89698 & time_avail_m == tm(2024m6))

label var OrgCap "Organizational capital"

// SAVE
do "$pathCode/saveplacebo" OrgCapNoAdj
do "$pathCode/savepredictor" OrgCap
