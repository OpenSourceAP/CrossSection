* 13. IBES Recommendations -----------------------------------------------------
* https://www.tilburguniversity.edu/sites/default/files/download/IBESonWRDS_2.pdf
* ANNDATS, ANNTIMS: Date and Time when the estimate/ recommendation was releasedby an analyst
* ACTDATS, ACTTIMS: Date and Time when the estimate/ recommendation was enteredinto the database
* https://wrds-web.wharton.upenn.edu/wrds/ds/ibes/recddet/index.cfm?navId=232
// ? I/B/E/S Text ? As many estimators have different ratings, Thomson Reuters maintains a standard
// set of recommendations, each with an assigned numeric value:
// 1. Strong Buy
// 2. Buy
// 3. Hold
// 4. Underperform
// 5. Sell 
* This data only begins in 1993, while the OPs use Zack's going back to 1985

// Prepare query
#delimit ;
local sql_statement
    SELECT a.ticker, a.estimid, a.ereccd, a.etext, a.ireccd, a.itext, a.emaskcd, 
           a.amaskcd, a.anndats, actdats
    FROM ibes.recddet as a
	WHERE a.usfirm = '1';
#delimit cr

odbc load, exec("`sql_statement'") dsn(wrds-stata) clear

destring ireccd, replace
gen time_avail_m = mofd(anndats)
format time_avail %tm

* Prepare Change in Recommendation variable
bys ticker amaskcd (anndats): gen ChangeInRecommendation = 1 if ireccd == 1 & ireccd[_n-1] !=1 
bys ticker amaskcd (anndats): replace ChangeInRecommendation = -1 if ireccd != ireccd[_n-1] & ireccd !=1
replace Change = 0 if mi(Change)

* sort my ticker analyst day, keep last within in month
*	and then average within ticker
* 	not clear how long to keep recommendations around for
*	OP says it keeps analysts
* 	"who have oustanding recommendations for the firm on that day"
keep ticker amaskcd anndats time_avail_m ireccd Change

sort ticker amaskcd anndats
gcollapse (lastnm) Change ireccd, by(ticker amaskcd time_avail_m) // drops only 3/80
gcollapse (mean) Change ireccd, by(ticker time_avail_m)  // drops about 1/2

* Prepare for match with other files
rename ticker tickerIBES
rename irec MeanRecomm
compress

save "$pathDataIntermediate/IBES_Recommendations", replace
