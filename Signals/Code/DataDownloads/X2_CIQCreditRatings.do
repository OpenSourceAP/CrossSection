* CIQ Credit ratings ------------------------------------------------------------

/* Notes on 2024 08 patch -Andrew
The Compustat credit ratings data ends in 2017. As pointed out by Peng Li, there is
new data here:
https://wrds-www.wharton.upenn.edu/documents/1849/WRDS_Credit_Rating_Data_Overview.pdf

it's unclear to me how to best assign ratings to firms, but the method below
yields the following number of gvkeys per year-month

       year |      Freq.     Percent        Cum.
       2016 |      2,888        2.86       80.65
       2017 |      2,883        2.85       83.51
       2018 |      2,669        2.64       86.15
       2019 |      2,517        2.49       88.64
       2020 |      2,814        2.79       91.43
       2021 |      2,614        2.59       94.01
       2022 |      2,100        2.08       96.09
       2023 |      2,163        2.14       98.23
       2024 |      1,784        1.77      100.00

*/

// --- Download

* First entity ratings
#delimit ;
	local sql_statement
	SELECT DISTINCT b.gvkey, b.ticker, a.ratingdate, a.ratingtime, a.ratingactionword, a.currentratingsymbol, b.entity_id
    FROM ciq.wrds_erating a
    LEFT JOIN ciq.ratings_ids b
    ON a.entity_id = b.entity_id
    WHERE b.gvkey IS NOT NULL
    AND a.ratingdate >= '1970-01-01';
#delimit cr
odbc load, exec("`sql_statement'") dsn($wrdsConnection) clear

* fill in missings for instrument and security id
gen str6 instrument_id = ""
gen str6 security_id = ""

save "$pathtemp/ciq_entity", replace

* Second instrument ratings
#delimit ;
	local sql_statement
	SELECT DISTINCT b.gvkey, b.ticker, a.ratingdate, a.ratingtime, a.ratingactionword, a.currentratingsymbol, b.instrument_id
    FROM ciq.wrds_irating a
    LEFT JOIN ciq.ratings_ids b
    ON a.instrument_id = b.instrument_id
    WHERE b.gvkey IS NOT NULL
	AND a.ratingdate >= '1970-01-01';
#delimit cr
odbc load, exec("`sql_statement'") dsn($wrdsConnection) clear

* fill in missings 
gen str6 entity_id = ""
gen str6 security_id = ""

save "$pathtemp/ciq_instr", replace

* Last security ratings
#delimit ;
	local sql_statement
	SELECT DISTINCT b.gvkey, b.ticker, a.ratingdate, a.ratingtime, a.ratingactionword, a.currentratingsymbol, b.security_id
    FROM ciq.wrds_srating a
    LEFT JOIN ciq.ratings_ids b
    ON a.security_id = b.security_id
    WHERE b.gvkey IS NOT NULL
	AND a.ratingdate >= '1970-01-01';
#delimit cr
odbc load, exec("`sql_statement'") dsn($wrdsConnection) clear

* fill in missings 
gen str6 entity_id = ""
gen str6 instrument_id = ""

save "$pathtemp/ciq_sec", replace

// --- Append 
use "$pathtemp/ciq_entity", clear
append using "$pathtemp/ciq_instr"
append using "$pathtemp/ciq_sec"

// --- Make distinct gvkey-ratingdate-ratingtime
* drop not rated action (why is this here)
drop if ratingaction == "Not Rated"

* rank the sources
gen source = 1 if !missing(entity_id)
replace source = 2 if !missing(instrument_id)
replace source = 3 if !missing(security_id)

* for each time, keep the best source
sort gvkey ratingdate ratingtime source
by gvkey ratingdate, sort: gen dupcount = _n
keep if dupcount == 1
drop dupcount 

// ---- Make distinct gvkey-time_avail_m

* add year-month 
gen time_avail_m = mofd(ratingdate)
format time_avail_m %tm

* remove dups by keeping last rating time each year-month (unclear if this is ideal)
gsort gvkey time_avail_m -ratingdate -ratingtime
by gvkey time_avail_m, sort: gen dupcount = _n
keep if dupcount == 1
drop dupcount 

// --- Save file
destring gvkey, replace
compress
save "$pathDataIntermediate/m_CIQ_creditratings.dta", replace
