* 13. IBES Recommendations -----------------------------------------------------

// Prepare query
#delimit ;
local sql_statement
    SELECT a.ticker, a.estimid, a.ereccd, a.etext, a.ireccd, a.itext, a.emaskcd, 
           a.amaskcd, a.anndats
    FROM ibes.recddet as a
	WHERE a.usfirm = '1';
#delimit cr

odbc load, exec("`sql_statement'") dsn(wrds-stata) clear

gen time_avail_m = mofd(anndats)
format time_avail %tm

* Prepare Change in Recommendation variable
destring ireccd, replace
bys ticker amaskcd (anndats): gen ChangeInRecommendation = 1 if ireccd == 1 & ireccd[_n-1] !=1 
bys ticker amaskcd (anndats): replace ChangeInRecommendation = -1 if ireccd != ireccd[_n-1] & ireccd !=1
replace Change = 0 if mi(Change)

gcollapse (mean) Change ireccd, by(ticker time_avail_m)

* Prepare for match with other files
rename ticker tickerIBES
rename irec MeanRecomm
compress

save "$pathDataIntermediate/IBES_Recommendations", replace
