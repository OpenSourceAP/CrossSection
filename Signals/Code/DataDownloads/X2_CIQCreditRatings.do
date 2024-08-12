* 24. Credit ratings ------------------------------------------------------------

/* Notes on 2024 08 patch -Andrew
The Compustat credit ratings data ends in 2017. As pointed out by Peng Li, there is
new data here:
https://wrds-www.wharton.upenn.edu/documents/1849/WRDS_Credit_Rating_Data_Overview.pdf

It seems the simplest way to deal with this is to start using CIQ credit ratings starting in 2016.

https://github.com/OpenSourceAP/CrossSection/issues/135

*/

// --- Download files first for reasonable speed (WRDS runs out of ram?)

// Download only (unique) firm identifiers
#delimit ;
	local sql_statement
	SELECT b.entity_id, b.gvkey
	FROM ciq.ratings_ids as b
	WHERE entity_id IS NOT NULL and gvkey IS NOT NULL
	GROUP BY entity_id, gvkey;
	
#delimit cr
odbc load, exec("`sql_statement'") dsn($wrdsConnection) clear

save "$pathtemp/temp_ciq_ids", replace

// Download ratings 
* data goes back to 1923, but is sparse until 1991
* downloading 1970-present makes it easy to check
#delimit ;
	local sql_statement
	SELECT a.entity_id, a.ratingdate, a.ratingactionword, a.currentratingsymbol, a.priorratingsymbol
	FROM ciq.wrds_erating AS a	
	WHERE a.ratingdate >= '1970-01-01';
#delimit cr
odbc load, exec("`sql_statement'") dsn($wrdsConnection) clear

save "$pathtemp/temp_ciq_rating", replace

// Clean and Merge
use "$pathtemp/temp_ciq_rating", clear
merge m:1 entity_id using "$pathtemp/temp_ciq_ids", keep(master match) nogenerate
sort gvkey ratingdate

// Save file
destring gvkey, replace
compress
save "$pathDataIntermediate/m_CIQ_creditratings.dta", replace
